from typing import Optional

from boto3.session import Session
from mypy_boto3_medialive import MediaLiveClient
from mypy_boto3_medialive.literals import InputTypeType
from typing_extensions import override

from sendlive.exceptions import SendLiveError
from sendlive.stream import BaseStream
from sendlive.logger import logger


class AWSStream(BaseStream):
    """Represents a single stream on AWS."""

    endpoint: Optional[str] = None

    def setup_endpoint(
        self,
        boto_session: Session,
        security_input_group_id: int,
        tags: Optional[dict[str, str]] = None,
        stream_type: InputTypeType = "RTMP_PUSH",
    ) -> str:
        """Set up and return a livestream endpoint for the stream."""
        if tags is None:
            tags = dict()
        medialive: MediaLiveClient = boto_session.client("medialive")
        medialive_input = medialive.create_input(
            Destinations=[{"StreamName": self.name}],
            InputSecurityGroups=[str(security_input_group_id)],
            Name=self.name,
            Type=stream_type,
            Tags=tags,
        )
        logger.info(f"MEDIALIVE RESPONSE:\n\n{medialive_input}\n\n")
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
            logger.error(medialive_input)
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
