from typing import Optional

from boto3.session import Session
from pydantic import ConfigDict
from typing_extensions import override

from sendlive.adapter import BaseAdapter
from sendlive.constants import AWSCredentials
from sendlive.exceptions import SendLiveError
from sendlive.providers.aws.stream import AWSStream


class AWSAdapter(BaseAdapter):
    """Adapter for AWS."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    credentials: AWSCredentials
    boto_session: Optional[Session] = None

    @override
    def setup_provider(self) -> None:
        self.boto_session = Session(
            aws_access_key_id=self.credentials.access_key,
            aws_secret_access_key=self.credentials.secret_key.get_secret_value(),
            region_name=self.credentials.region,
        )

    @override
    def setup_stream(self) -> None:
        return None

    @override
    def list_streams(self) -> list[str]:
        return list()

    @override
    def create_stream(
        self, name: str, url: str, setup_endpoint: bool = True
    ) -> AWSStream:
        stream = AWSStream(name="my_stream", url="rtmp://my_stream")
        if not self.boto_session:
            raise SendLiveError("Boto session not set up.")
        if setup_endpoint:
            stream.setup_endpoint(boto_session=self.boto_session)
        return stream
