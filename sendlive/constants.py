from enum import Enum

from pydantic import BaseModel, Field, SecretStr

from sendlive.adapter import BaseAdapter
from sendlive.providers.aws import AWSAdapter
from sendlive.providers.gcp import GCPAdapter


class ServiceProvider(Enum):
    """Enum for the different cloud providers."""

    AWS = "aws_medialive"
    GCP = "gcp"


class BaseCredential(BaseModel):
    """Base class for all credentials."""

    service_provider: ServiceProvider = Field(frozen=True)
    adapter_cls: type[BaseAdapter]


class AWSCredentials(BaseCredential):
    """Credentials for AWS."""

    access_key: str
    secret_key: SecretStr
    region: str
    service_provider: ServiceProvider = ServiceProvider.AWS
    adapter_cls = AWSAdapter


class GCPCredentials(BaseCredential):
    """Credentials for GCP."""

    project_id: str
    service_account_json: SecretStr
    service_provider: ServiceProvider = ServiceProvider.GCP
    adapter_cls = GCPAdapter
