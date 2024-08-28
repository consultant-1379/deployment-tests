##############################################################################
# COPYRIGHT Ericsson 2019
#
# The copyright to the computer program(s) herein is the property of
# Ericsson Inc. The programs may be used and/or copied only with written
# permission from Ericsson Inc. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################

"""Module for defining 3PP tools tests."""

import helpers.common.common as common
import helpers.common.constants as common_constants
from configuration.logging import LOG


def get_terraform_version():
    """
    Get installed Terraform version.

    :return: Terraform version
    """
    command = "terraform version | cut -s -d ' ' -f2 | cut -s -d 'v' -f2 | grep -v \"ersion\""
    return common.execute_cli_locally(command)


def get_kubernetes_versions():
    """
    Get installed Kubernetes (server and client) versions.

    :return: Kubernetes versions
    """
    command = "kubectl version --short | cut -d ':' -f2 | cut -d 'v' -f2 | cut -d '-' -f1"
    stdout = common.execute_cli_locally(command, return_output_as_string=False)
    return stdout[0][:-1].decode(common_constants.BYTE_TO_STRING_DECODE_TYPE_UTF_8),\
        stdout[1][:-1].decode(common_constants.BYTE_TO_STRING_DECODE_TYPE_UTF_8)


def get_helm_versions():
    """
    Get installed Helm (server and client) versions.

    :return: Helm versions
    """
    command = "helm version --short | cut -d ':' -f2 | cut -d 'v' -f2 | cut -d '+' -f1"
    stdout = common.execute_cli_locally(command, return_output_as_string=False)
    return stdout[0][:-1].decode(common_constants.BYTE_TO_STRING_DECODE_TYPE_UTF_8),\
        stdout[1][:-1].decode(common_constants.BYTE_TO_STRING_DECODE_TYPE_UTF_8)


def get_elasticsearch_version(tfvars):
    """
    Get AWS Elasticsearch version.

    :return: Terraform version
    """
    command = "aws es describe-elasticsearch-domains --domain-names " + tfvars['cluster_name'] \
              + " --output json | jq -r '.DomainStatusList[0] .ElasticsearchVersion'"
    return common.execute_cli_locally(command)


def log_terraform_providers_version():
    """
    Log Terraform providers versions.

    """
    command = "ls -1 " + common_constants.TERRAFORM_ENM_COMPONENT_PLUGINS_DIR
    stdout = common.execute_cli_locally(command, return_output_as_string=False)
    if stdout is False:
        LOG.error("Error in listing Terraform providers")

    LOG.info("Provider - Version")
    for line in stdout:
        line = line.decode(common_constants.BYTE_TO_STRING_DECODE_TYPE_UTF_8)
        if common_constants.TERRAFORM_PROVIDER_NAME_PREFIX in line:
            provider_name = line[len(common_constants.TERRAFORM_PROVIDER_NAME_PREFIX):
                                 line.find("_v")]
            provider_version = line[(line.find("_v") + 2):line.rfind("_")]

            LOG.info("%s - %s", provider_name, provider_version)
