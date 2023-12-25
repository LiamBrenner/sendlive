from typing import Any, Optional

from google.cloud.video import live_stream_v1
from google.cloud.video.live_stream_v1.services.livestream_service import (
    LivestreamServiceClient,
)
from pydantic import BaseModel, PrivateAttr, computed_field

from sendlive.constants import GCPCredentials, GCPOptions
from sendlive.exceptions import SendLiveError
from sendlive.logger import logger
from google.api_core.operation import Operation
from google.protobuf.message import Message


class GCPBaseMixin(BaseModel):
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

    def create_input_endpoint(self) -> live_stream_v1.Input:
        """Create a GCP input endpoint."""
        parent = f"projects/{self._gcp_credentials.project_id}/locations/{self._gcp_credentials.region}"
        input_endpoint = live_stream_v1.Input(type_="RTMP_PUSH")
        operation: Operation = self._gcp_session.create_input(
            parent=parent, input=input_endpoint, input_id="test"
        )
        response: Message = operation.result(900)  # type: ignore
        print(f"Input: {response.name}")  # type: ignore

        return response  # type: ignore
