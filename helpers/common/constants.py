##############################################################################
# COPYRIGHT Ericsson 2019
#
# The copyright to the computer program(s) herein is the property of
# Ericsson Inc. The programs may be used and/or copied only with written
# permission from Ericsson Inc. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################

"""Common Constants"""

import os

TERRAFORM_TEMPLATES_DIR = os.path.join(os.path.expanduser("~"), 'terraform-templates')
ENM_COMPONENT_DIR = os.path.join("aws", "components", "enm")
TERRAFORM_ENM_COMPONENT_DIR = os.path.join(TERRAFORM_TEMPLATES_DIR, ENM_COMPONENT_DIR)

TERRAFORM_LOCAL_DIR = ".terraform"
TERRAFORM_PLUGINS_DIR = "plugins"
TERRAFORM_PLUGINS_LINUX_AMD_64_DIR = "linux_amd64"
TERRAFORM_ENM_COMPONENT_PLUGINS_DIR = os.path.join(TERRAFORM_ENM_COMPONENT_DIR,
                                                   TERRAFORM_LOCAL_DIR,
                                                   TERRAFORM_PLUGINS_DIR,
                                                   TERRAFORM_PLUGINS_LINUX_AMD_64_DIR)
TERRAFORM_PROVIDER_NAME_PREFIX = "terraform-provider-"

DEFAULT_DELIMITER = "-"
DEFAULT_APPLICATION_NAME = "enm"
DEFAULT_STAGE = "prod"

KUBERNETES_POD_STATUS_CHANGE_TIMEOUT = 300
KUBERNETES_POD_STATUS_CHECK_SLEEP_TIME = 5

REGEX_MATCH_COUNT_DEFAULT = 1

COMMAND_OUTPUT_REGEX_MATCH_TIMEOUT = 300
COMMAND_OUTPUT_REGEX_MATCH_SLEEP_TIME = 5

BYTE_TO_STRING_DECODE_TYPE_UTF_8 = "utf-8"

CLI_EXECUTION_TIMEOUT = 300

CLI_PARSING_EXCEPTION_MESSAGE = "Exception occurred while parsing CLI."
COMMON_EXCEPTION_MESSAGE = "Exception occurred while executing the command :"
