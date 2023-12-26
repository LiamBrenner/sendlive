from typing import Any, Optional

from google.api_core.operation import Operation
from google.cloud.video.live_stream_v1 import Input as InputEndpoint
from google.cloud.video.live_stream_v1 import Channel
from google.cloud.video.live_stream_v1.services.livestream_service import (
    LivestreamServiceClient,
)
from google.protobuf.message import Message
from pydantic import BaseModel, PrivateAttr

from sendlive.constants import GCPCredentials, GCPOptions
from sendlive.exceptions import SendLiveError
from sendlive.logger import logger
from sendlive.mixins import TagMixin
from sendlive.providers.gcp.utils import build_gcp_channel_obj_from_defaults


class GCPBaseMixin(BaseModel, TagMixin):
    """Base mixin for GCP operations."""

    _gcp_session: LivestreamServiceClient = PrivateAttr()
    _gcp_credentials: GCPCredentials = PrivateAttr()
    provider_options: Optional[GCPOptions] = None

    def __init__(self, credentials: GCPCredentials, **data: dict[Any, Any]) -> None:
        """Set gcp session and credentials up."""
        super().__init__(credentials=credentials, **data)
        self._gcp_session = LivestreamServiceClient.from_service_account_info(
            info=credentials.service_account_json
        )
        self._gcp_credentials = credentials


class LiveStreamAPIMixin(GCPBaseMixin):
    """Mixin for GCP Live Streaming API operations."""

    gcp_input_endpoints: list[InputEndpoint] = []

    gcp_channels: list[Channel] = []

    def create_input_endpoint(self) -> InputEndpoint:
        """Create a GCP input endpoint.

        This operation appears to take a decent amount of time to complete.
        It may be advisable to use a library such as celery when invoking.
        """
        parent = f"projects/{self._gcp_credentials.project_id}/locations/{self._gcp_credentials.region}"
        input_endpoint = InputEndpoint(type_="RTMP_PUSH")
        operation: Operation = self._gcp_session.create_input(
            parent=parent,
            input=input_endpoint,
            input_id="test",
            metadata=self.get_operation_tags_as_sequence_tuple(),
        )
        response: Message = operation.result(900)  # type: ignore
        logger.info(f"\nGCP Create input endpoint res:{response}\n\n")

        if not isinstance(response, InputEndpoint):
            raise SendLiveError(
                f"Unexpected response from GCP - Create input endpoint response not of type InputEndpoint: {response}"
            )
        self.gcp_input_endpoints.extend([response])
        return response

    def create_channel(self, name: str, input_id: str, channel_id: str) -> Channel:
        """Create a GCP channel."""
        parent = f"projects/{self._gcp_credentials.project_id}/locations/{self._gcp_credentials.region}"
        input_str = f"{parent}/inputs/{input_id}"
        name = f"{parent}/channels/{channel_id}"
        channel: Channel = build_gcp_channel_obj_from_defaults(
            name, input_str, self.gcp_input_endpoints[0].uri
        )
        operation: Operation = self._gcp_session.create_channel(
            parent=parent, channel=channel, channel_id=channel_id
        )
        response: Message = operation.result(600)  # type: ignore
        logger.info(f"\nGCP Create channel res:{response}\n\n")

        if not isinstance(response, Channel):
            raise SendLiveError(
                f"Unexpected response from GCP - Create channel response not of type Channel: {response}"
            )
        return response
