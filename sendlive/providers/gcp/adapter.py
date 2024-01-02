from pydantic import ConfigDict
from typing_extensions import override

from sendlive.adapter import BaseAdapter
from sendlive.constants import GCPCredentials
from sendlive.providers.gcp.mixins import GCPLiveStreamAPIMixin
from sendlive.providers.gcp.stream import GCPStream


class GCPAdapter(GCPLiveStreamAPIMixin, BaseAdapter):
    """Adapter for GCP."""

    credentials: GCPCredentials
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @override
    def list_streams(self) -> list[str]:
        return []

    @override
    def create_stream(self, name: str) -> GCPStream:
        return GCPStream(name=name)

    @override
    def setup_stream(self) -> None:
        return None
