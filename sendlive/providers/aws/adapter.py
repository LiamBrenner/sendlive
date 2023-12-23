from typing import Optional

from mypy_boto3_medialive.type_defs import InputSecurityGroupTypeDef
from pydantic import ConfigDict
from typing_extensions import override

from sendlive.adapter import BaseAdapter
from sendlive.constants import AWSCredentials
from sendlive.exceptions import SendLiveError
from sendlive.providers.aws.mixins import MediaLiveMixin, MediaPackageV2Mixin
from sendlive.providers.aws.stream import AWSStream


class AWSAdapter(MediaLiveMixin, MediaPackageV2Mixin, BaseAdapter):
    """Adapter for AWS."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    credentials: AWSCredentials

    # @override
    # def setup_provider(self) -> None:
    #     self._boto_session = Session(
    #         aws_access_key_id=self.credentials.access_key,
    #         aws_secret_access_key=self.credentials.secret_key.get_secret_value(),
    #         region_name=self.credentials.region,
    #     )

    @override
    def setup_stream(self) -> None:
        return None

    @override
    def list_streams(self) -> list[str]:
        return list()

    @override
    def create_stream(
        self,
        name: str,
        input_security_group_id: Optional[int] = None,
        setup_endpoint: bool = True,
    ) -> AWSStream:
        if input_security_group_id is None:
            if (
                self.provider_options is None
                or self.provider_options.medialive_input_security_group_id is None
            ):
                input_security_group: InputSecurityGroupTypeDef = (
                    self.create_input_security_group()
                )
                input_security_group_id = int(input_security_group["Id"])
            else:
                input_security_group_id = (
                    self.provider_options.medialive_input_security_group_id
                )
        stream = AWSStream(name=name)
        if not self._boto_session:
            raise SendLiveError("Boto session not set up.")
        if setup_endpoint:
            stream.setup_endpoint(
                boto_session=self._boto_session,
                security_input_group_id=input_security_group_id,
            )
        return stream
