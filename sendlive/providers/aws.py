from typing import Optional

from boto3.session import Session
from mypy_boto3_medialive import MediaLiveClient
from mypy_boto3_medialive.literals import InputTypeType
from typing_extensions import override

from sendlive.adapter import BaseAdapter
from sendlive.constants import AWSCredentials
from sendlive.exceptions import SendLiveError
from sendlive.stream import BaseStream


class AWSStream(BaseStream):
    """Represents a single stream on AWS."""

    endpoint: Optional[str]

    def setup_endpoint(
        self,
        boto_session: Session,
        tags: dict[str, str],
        stream_type: InputTypeType = "RTMP_PUSH",
    ) -> str:
        """Set up and return a livestream endpoint for the stream."""
        medialive: MediaLiveClient = boto_session.client("medialive")
        # TODO security group setup/conf
        medialive_input = medialive.create_input(
            Destinations=[{"StreamName": self.name}],
            Name=self.name,
            Type=stream_type,
            Tags=tags,
        )
        response_metadata = medialive_input["ResponseMetadata"]
        if (
            response_metadata["HTTPStatusCode"] not in range(200, 300)
            or "Destinations" not in medialive_input["Input"]
        ):
            raise SendLiveError(
                f"Failed to create input for stream {self.name}: {response_metadata}"
            )
        destinations = medialive_input["Input"]["Destinations"]
        if len(destinations) != 1:
            raise SendLiveError(
                f"Failed to create input for stream {self.name}: expected 1 destination, got {len(destinations)}"
            )
        endpoint = destinations[0].get("Url")
        if not endpoint:
            raise SendLiveError(
                f"Failed to create input for stream {self.name}: no endpoint URL returned"
            )
        self.endpoint = endpoint
        return endpoint

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


class AWSAdapter(BaseAdapter):
    """Adapter for AWS."""

    credentials: AWSCredentials
    boto_session = Optional[Session]

    @override
    def setup_stream(self) -> None:
        self.boto_session = Session(
            aws_access_key_id=self.credentials.access_key,
            aws_secret_access_key=self.credentials.secret_key,
            region_name=self.credentials.region,
        )  # type: ignore

    @override
    def list_streams(self) -> list[str]:
        return list()

    @override
    def create_stream(self, name: str, url: str) -> BaseStream:
        return AWSStream(name="my_stream", url="rtmp://my_stream")
