from typing import Optional

from boto3.session import Session
from mypy_boto3_medialive import MediaLiveClient
from mypy_boto3_medialive.type_defs import (
    CreateInputSecurityGroupResponseTypeDef,
    InputSecurityGroupTypeDef,
)
from pydantic import ConfigDict, PrivateAttr, computed_field
from typing_extensions import override

from sendlive.adapter import BaseAdapter
from sendlive.constants import AWSCredentials, AWSOptions
from sendlive.exceptions import SendLiveError
from sendlive.logger import logger
from sendlive.providers.aws.stream import AWSStream


class AWSAdapter(BaseAdapter):
    """Adapter for AWS."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    credentials: AWSCredentials

    provider_options: Optional[AWSOptions] = None

    _boto_session: Session = PrivateAttr()

    @computed_field
    @property
    def medialive(self) -> MediaLiveClient:
        """Return a MediaLive client."""
        return self._boto_session.client("medialive")

    @override
    def setup_provider(self) -> None:
        self._boto_session = Session(
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
                input_security_group = self.create_input_security_group()
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

    def create_input_security_group(self) -> InputSecurityGroupTypeDef:
        """Create a medialive input security group and return it."""
        if not self._boto_session:
            raise SendLiveError("Boto session not set up.")
        input_security_group: CreateInputSecurityGroupResponseTypeDef = (
            self.medialive.create_input_security_group(
                WhitelistRules=[{"Cidr": "0.0.0.0/0"}]
            )
        )
        if input_security_group["ResponseMetadata"]["HTTPStatusCode"] != 201:
            raise SendLiveError(
                f"Failed to create input security group, received non 201 created response: {input_security_group}"
            )
        new_input_security_group: InputSecurityGroupTypeDef = input_security_group[
            "SecurityGroup"
        ]
        if "Id" not in new_input_security_group:
            raise SendLiveError("Created input security group did not return an id.")
        logger.info(f"\n\nINPUT SEC GROUP RES:{input_security_group}\n\n")
        return new_input_security_group
