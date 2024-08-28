##############################################################################
# COPYRIGHT Ericsson 2019
#
# The copyright to the computer program(s) herein is the property of
# Ericsson Inc. The programs may be used and/or copied only with written
# permission from Ericsson Inc. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################

"""Constants for EKS tests."""

import os

REGEX_FOR_HELM_DEPLOYMENTS = \
    r"(?P<name>\S+)\s+(?P<revision>\d+)\s+\S{3}\s+\S{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\s+\d{4}\s+" \
    r"(?P<status>\S+)"
HELM_STATUS_DEPLOYED = "DEPLOYED"
HELM_COMMAND_TIMEOUT = 300
HELM_CLI_PARSING_EXCEPTION_MESSAGE = "Exception occurred while parsing Helm CLI."

EKS_TEST_DEPLOYMENT_FILENAME = os.path.join("kubernetes_resources", "eks",
                                            "eks_test_deployment.json")
EKS_TEST_DEPLOYMENT_NAME = "eks-test-deployment"
EKS_TEST_DEPLOYMENT_IMAGE_NAME = "152254703525.dkr.ecr.eu-west-1.amazonaws.com/" \
                                 "enm/deployment-tests/nginx:1.7.9"
EKS_TEST_DEPLOYMENT_PORT = 80
EKS_TEST_DEPLOYMENT_NAMESPACE = "default"
EKS_TEST_DEPLOYMENT_UP_TO_REPLICAS = 2
EKS_TEST_DEPLOYMENT_DOWN_TO_REPLICAS = 1
EKS_TEST_K8S_PODS_CHANGE_TIMEOUT = 3
EKS_TEST_ECR_IMAGE = "152254703525.dkr.ecr.eu-west-1.amazonaws.com/cm_provisioning:latest"
EKS_TEST_ECR_NAME = "cm-provisioning"
KUBERNETES_POD_STATUS_CHANGE_TIMEOUT = 10

HELM_NEO4J_CHART_DIR = os.path.join("kubernetes_resources", "eks", "neo4j")
HELM_NEO4J_STS_TEST_DEPLOYMENT_NAME = "neo4j-sts-test"
HELM_DEPLOYMENT_NAME_REGEX = r"NAME:\s+" + HELM_NEO4J_STS_TEST_DEPLOYMENT_NAME
HELM_DEPLOYMENT_STATUS_REGEX = r"STATUS:\s+" + HELM_STATUS_DEPLOYED

NEO4J_STS_TEST_DEPLOYMENT_NAME = "graphdb-neo4j"
NEO4J_TEST_PVC_NAME = "datadir-" + NEO4J_STS_TEST_DEPLOYMENT_NAME
NEO4J_TEST_POD_COUNT = 3
NEO4J_TEST_POD_LABEL = "app=neo4j,component=core"
NEO4J_PODS_LOGS_REGEX = r"INFO\s+Remote interface available at"
HELM_STS_TEST_SCRIPT_PATH = os.path.join("kubernetes_resources", "eks", "neo4j", "test.sh")
NEO4J_PODS_ROLE_RETRIEVED_SUCCESS_MESSAGE = r"All pods roles retrieved successfully!"
NEO4J_POD_DELETION_SUCCESS_MESSAGE = r"pod \"" + NEO4J_STS_TEST_DEPLOYMENT_NAME + r"-\d\" deleted"
NEO4J_POD_RECOVERED_SUCCESS_MESSAGE = r"Pod recovered successfully!"
NEO4J_TEST_SCRIPT_SUCCESS_MESSAGES_LIST = [NEO4J_PODS_ROLE_RETRIEVED_SUCCESS_MESSAGE,
                                           NEO4J_POD_DELETION_SUCCESS_MESSAGE,
                                           NEO4J_POD_RECOVERED_SUCCESS_MESSAGE]
