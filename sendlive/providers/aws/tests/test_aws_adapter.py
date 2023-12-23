import os
from collections.abc import Generator
from typing import Any

import boto3
import pytest
from moto import mock_medialive
from mypy_boto3_medialive import MediaLiveClient

from sendlive.constants import AWSCredentials
from sendlive.providers.aws.adapter import AWSAdapter
from sendlive.providers.aws.stream import AWSStream


@pytest.fixture(scope="function")
def aws_credentials() -> None:
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "ap-southeast-2"


@pytest.fixture(scope="function")
def sendlive_aws_credentials() -> AWSCredentials:
    sl_aws_credentials = AWSCredentials(
        access_key="testing", secret_key="testing", region="ap-southeast-2"
    )
    return sl_aws_credentials


@pytest.fixture(scope="function")
def medialive(aws_credentials: None) -> Generator[MediaLiveClient, Any, None]:
    with mock_medialive():
        yield boto3.client("medialive", region_name="ap-southeast-2")


def test_aws_adapter_has_bound_credentials(
    sendlive_aws_credentials: AWSCredentials,
) -> None:
    """Test adapter cls correctly binds credentials to the adapter instance."""
    aws_adapter = AWSAdapter(credentials=sendlive_aws_credentials)
    assert aws_adapter.credentials


@pytest.fixture(scope="function")
def sendlive_aws_adapter(sendlive_aws_credentials: AWSCredentials) -> AWSAdapter:
    return AWSAdapter(credentials=sendlive_aws_credentials)


def test_aws_adapter_provider_setup(
    sendlive_aws_adapter: AWSAdapter,
) -> None:
    """Test adapter can successfully attach a boto session to the instance."""
    sendlive_aws_adapter.setup_provider()
    assert sendlive_aws_adapter._boto_session


@pytest.fixture(scope="function")
def sendlive_aws_adapter_with_boto_session(
    sendlive_aws_adapter: AWSAdapter,
) -> AWSAdapter:
    sendlive_aws_adapter.setup_provider()
    return sendlive_aws_adapter


def test_aws_adapter_create_stream_with_endpoint_creation(
    sendlive_aws_adapter_with_boto_session: AWSAdapter, medialive: MediaLiveClient
) -> None:
    """Test adapter can successfully create a stream, and create and fetch an enpoint for it."""
    stream: AWSStream = sendlive_aws_adapter_with_boto_session.create_stream(
        name="my_stream"
    )
    assert stream
    assert stream.endpoint
