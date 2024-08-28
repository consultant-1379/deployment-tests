##############################################################################
# COPYRIGHT Ericsson 2019
#
# The copyright to the computer program(s) herein is the property of
# Ericsson Inc. The programs may be used and/or copied only with written
# permission from Ericsson Inc. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################

"""Module to manage client and session connections to AWS resources."""

import boto3
from botocore.exceptions import ClientError
from configuration.logging import LOG


class AWSClient:
    """Class for defining the basic structure to connect to AWS resources."""

    def __init__(self, resource_name):
        """Initialize the class informing the resource to connect."""
        self.resource_name = resource_name
        self.client_resource = None

    def client_connect(self):
        """
        Get a client connection to resource.

        :return: Service client.
        """
        try:
            self.client_resource = boto3.client(self.resource_name)
            return self.client_resource
        except ClientError as client_error:
            LOG.error("Connection to AWS %s failed", self.resource_name)
            LOG.error(client_error.response)

    def get_resource(self):
        """
        Get a resource service client based on resource name.

        :return: Resource service client fetched from aws.
        """
        try:
            resource = boto3.resource(self.resource_name)
            return resource
        except Exception as exception:
            LOG.error("Connection to AWS %s failed", self.resource_name)
            LOG.error(str(exception))

    @staticmethod
    def get_session(profile):
        """
        Start a session configuration on aws with a specific profile.

        :param profile: aws profile.
        :return: aws session.
        """
        try:
            session = boto3.Session(profile_name=profile)
            return session
        except ClientError as client_error:
            LOG.error(client_error.response)


class Ec2Client(AWSClient):
    """Class for connecting to EC2 instances and services."""

    def __init__(self, resource_name='ec2'):
        """Initialize the class with EC2 resource to connect."""
        super(Ec2Client, self).__init__(resource_name)
        self.resource_name = resource_name

    def client_connect_with_profile(self, profile):
        """
        Get a client connection to EC2 resource using a specific aws cli profile.

        :param profile: aws cli profile.
        :return: client connection for the informed profile.
        """
        try:
            session = AWSClient.get_session(profile)
            ec2 = session.client(self.resource_name)
            return ec2
        except ClientError as client_error:
            LOG.error("Connection to AWS %s failed", self.resource_name)
            LOG.error(client_error.response)


class S3Client(AWSClient):
    """Class for connecting to S3 buckets and services."""

    def __init__(self, resource_name='s3'):
        """Initialize the class with S3 resource to connect."""
        super(S3Client, self).__init__(resource_name)
        self.resource_name = resource_name
