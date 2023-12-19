import os

import boto3
import pytest
from moto import mock_medialive

from sendlive.constants import AWSCredentials


@pytest.fixture(scope="function")
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "ap-southeast-2"


@pytest.fixture(scope="function")
def sendlive_aws_credentials() -> AWSCredentials:
    sl_aws_credentials = AWSCredentials(access_key="testing", secret_key="testing")
    return sl_aws_credentials


@pytest.fixture(scope="function")
def medialive(aws_credentials):
    with mock_medialive():
        yield boto3.client("medialive", region_name="ap-southeast-2")


# def test_stream_setup(medialive, sendlive_aws_credentials):
#     from sendlive.providers.aws import AWSStream

#     s = AWSStream(url="my-url.com", name="my stream", endpoint="my-endpoint.com")
#     s.setup_endpoint()
