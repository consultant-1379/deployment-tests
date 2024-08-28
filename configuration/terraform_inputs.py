##############################################################################
# COPYRIGHT Ericsson 2019
#
# The copyright to the computer program(s) herein is the property of
# Ericsson Inc. The programs may be used and/or copied only with written
# permission from Ericsson Inc. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################

# pylint: disable=R1715,W1201

"""Module to get Terraform inputs."""

import os
import helpers.common.constants as constants
from configuration.logging import LOG


def read_terraform_tfvars():
    """
    Read the tfvars file from tf_working_dir and parse the variables as dictionary.

    :return: tfvars variables in a dictionary.
    """
    tfvars_filename = os.path.join(constants.TERRAFORM_ENM_COMPONENT_DIR, "terraform.tfvars")

    if not os.path.exists(tfvars_filename):
        return None

    tfvars_file = open(tfvars_filename, "r")
    tfvars_dict = {}

    for line in tfvars_file.readlines():
        if line.strip():
            key_value = line.strip().split("=", 1)
            key = key_value[0].strip()
            value = key_value[1].strip().strip('\"')

            tfvars_dict[key] = value

    tfvars_file.close()

    tfvars_dict['cluster_name'] = prepare_cluster_name(tfvars_dict)

    return tfvars_dict


def prepare_cluster_name(tfvars_dict):
    """
    Prepare cluster name from terraform tfvars parameters

    :param tfvars_dict: TFVars params dict
    :return: cluster_name in format <application_name>-<stage>-<customer_name>
    """

    delimiter = tfvars_dict['delimiter'] if 'delimiter' in tfvars_dict \
        else constants.DEFAULT_DELIMITER

    application_name = tfvars_dict['application_name'] if 'application_name' in tfvars_dict \
        else constants.DEFAULT_APPLICATION_NAME

    stage = tfvars_dict['stage'] if 'stage' in tfvars_dict \
        else constants.DEFAULT_STAGE

    cluster_name = "{0}{1}{2}{1}{3}".format(application_name, delimiter, stage, tfvars_dict['name'])
    cluster_name = cluster_name.lower()
    LOG.info("Cluster name : %s", cluster_name)

    return cluster_name
