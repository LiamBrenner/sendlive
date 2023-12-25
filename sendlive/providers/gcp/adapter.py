from typing_extensions import override

from sendlive.adapter import BaseAdapter
from sendlive.providers.gcp.mixins import LiveStreamAPIMixin
from sendlive.providers.gcp.stream import GCPStream


class GCPAdapter(LiveStreamAPIMixin, BaseAdapter):
    """Adapter for GCP."""

    @override
    def list_streams(self) -> list[str]:
        return list()

    @override
    def create_stream(self, name: str) -> GCPStream:
        return GCPStream(name="my_stream")
