from typing import Any, Optional

from google.cloud.video import live_stream_v1
from google.cloud.video.live_stream_v1.services.livestream_service import (
    LivestreamServiceClient,
)
from pydantic import BaseModel, PrivateAttr, computed_field

from sendlive.constants import GCPCredentials, GCPOptions
from sendlive.exceptions import SendLiveError
from sendlive.logger import logger
from sendlive.mixins import TagMixin


class GCPBaseMixin(BaseModel, TagMixin):
    """Base mixin for GCP operations."""

    _gcp_session: LivestreamServiceClient = PrivateAttr()
    _gcp_credentials: GCPCredentials = PrivateAttr()
    provider_options: Optional[GCPOptions] = None

    def __init__(self, credentials: GCPCredentials, **data: dict[Any, Any]) -> None:
        super().__init__(**data)
        self._gcp_session = LivestreamServiceClient.from_service_account_info(
            info=credentials.service_account_json
        )
        self._gcp_credentials = credentials


class LiveStreamAPIMixin(GCPBaseMixin):
    """Mixin for GCP Live Streaming API operations."""

    gcp_input_endpoints: list[InputEndpoint] = []

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
