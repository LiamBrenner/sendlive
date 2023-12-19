from enum import Enum

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
    service_account_json: SecretStr
    service_provider: ServiceProvider = ServiceProvider.GCP
