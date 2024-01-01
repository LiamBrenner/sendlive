from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, SecretStr


class ServiceProvider(Enum):
    """Enum for the different cloud providers."""

    AWS = "aws_medialive"
    GCP = "gcp"


class BaseCredential(BaseModel):
    """Base class for all credentials."""

    service_provider: ServiceProvider = Field(frozen=True)


class AWSCredentials(BaseCredential):
    """Credentials for AWS."""

    access_key: str
    secret_key: SecretStr
    region: str
    service_provider: ServiceProvider = ServiceProvider.AWS


class GCPCredentials(BaseCredential):
    """Credentials for GCP."""

    project_id: str
    service_account_json: dict[str, str]
    service_provider: ServiceProvider = ServiceProvider.GCP
    region: str


class ProviderOptions(BaseModel):
    """Base abstract class for cloud service provider options."""


class AWSOptions(ProviderOptions):
    """AWS configuration."""

    medialive_input_security_group_id: Optional[int]


class GCPOptions(ProviderOptions):
    """GCP configuration."""

    get_or_create_bucket: bool = True

    # if unset, first check using labels on gcp, then generate a name with faker
    bucket_name: Optional[str] = None


CREATED_BY_KEY = "Created By"
CREATED_BY_VALUE = "sendlive"

DEFAULT_TAGS: dict[str, str] = {CREATED_BY_KEY: CREATED_BY_VALUE}
