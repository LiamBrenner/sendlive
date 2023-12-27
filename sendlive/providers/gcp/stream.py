from typing_extensions import override

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
