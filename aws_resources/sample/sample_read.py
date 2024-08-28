##############################################################################
# COPYRIGHT Ericsson 2019
#
# The copyright to the computer program(s) herein is the property of
# Ericsson Inc. The programs may be used and/or copied only with written
# permission from Ericsson Inc. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################

"""Test sample to be executed by robot test."""

from helpers.aws.client import Ec2Client, S3Client
from configuration.logging import LOG


def connect_to_s3_fetch_all_buckets():
    """Function to connect to the AWS S3 and list all buckets."""
    conn = S3Client()
    client = conn.client_connect()
    if client:
        list_buckets_resp = client.list_buckets()
        LOG.info("Bucket List")
        for bucket in list_buckets_resp['Buckets']:
            LOG.info(bucket['Name'])
    else:
        LOG.error("Failed to fetch s3 bucket names")
        return False

    return True


def describe_all_ec2_instances_in_current_region():
    """Function to connect to EC2 service and describe all instances."""
    conn = Ec2Client()
    client = conn.client_connect()
    if client:
        describe_ec2_list = client.describe_instances()
        LOG.info(describe_ec2_list)
    else:
        LOG.error("Failed to fetch ec2 instances")
        return False

    return True


def describe_all_ec2_instances_for_profile(profile="default"):
    """Function to connect to EC2 service and describe all instances using specific aws profile."""
    conn = Ec2Client()
    client = conn.client_connect_with_profile(profile)
    if client:
        describe_ec2_list = client.describe_instances()
        LOG.info(describe_ec2_list)
    else:
        LOG.error("Failed to fetch ec2 instances")
        return False

    return True
