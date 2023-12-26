from typing_extensions import override

from sendlive.adapter import BaseAdapter
from sendlive.constants import GCPCredentials
from sendlive.providers.gcp.mixins import LiveStreamAPIMixin
from sendlive.providers.gcp.stream import GCPStream


class GCPAdapter(LiveStreamAPIMixin, BaseAdapter):
    """Adapter for GCP."""

    credentials: GCPCredentials

    @override
    def list_streams(self) -> list[str]:
        return list()

    @override
    def create_stream(self, name: str) -> GCPStream:
        return GCPStream(name=name)

    @override
    def setup_stream(self) -> None:
        return None
