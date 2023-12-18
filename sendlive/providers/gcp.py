from typing_extensions import override

from sendlive.adapter import BaseAdapter
from sendlive.stream import BaseStream


class GCPStream(BaseStream):
    """Represents a single stream on GCP."""

    @override
    def start(self) -> None:
        pass

    @override
    def stop(self) -> None:
        pass

    @override
    def is_alive(self) -> None:
        pass

    @override
    def get_url(self) -> None:
        pass

    @override
    def get_name(self) -> None:
        pass


class GCPAdapter(BaseAdapter):
    """Adapter for GCP."""

    @override
    def list_streams(self) -> list[str]:
        return list()

    @override
    def create_stream(self, name: str, url: str) -> BaseStream:
        return GCPStream(name="my_stream", url="rtmp://my_stream")
