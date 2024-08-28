##############################################################################
# COPYRIGHT Ericsson 2019
#
# The copyright to the computer program(s) herein is the property of
# Ericsson Inc. The programs may be used and/or copied only with written
# permission from Ericsson Inc. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################

"""Constants for EFS tests."""

import os

EFS_TEST_POD_FILENAME = os.path.join("kubernetes_resources", "efs", "efs_test_pod.yaml")
EFS_TEST_POD_NAME = "efs-test-pod"
EFS_TEST_POD_SUCCESS_LOG = "EFS test pod success"
EFS_STORAGE_CLASS_NAME = "aws-efs"
EFS_PVC_NAME = "efs"
EFS_STORAGE_PROVISIONER = "example.com/aws-efs"
