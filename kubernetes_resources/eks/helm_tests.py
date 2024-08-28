##############################################################################
# COPYRIGHT Ericsson 2019
#
# The copyright to the computer program(s) herein is the property of
# Ericsson Inc. The programs may be used and/or copied only with written
# permission from Ericsson Inc. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################

# pylint: disable=R0801,W1201

"""Module for defining Helm tests."""

import re
from kubernetes import client
from configuration.logging import LOG
import helpers.common.common as common
import helpers.common.constants as common_constants
import kubernetes_resources.common.common as kubernetes_common
import kubernetes_resources.eks.constants as eks_constants


def check_helm_list(namespace):
    """
    Check Helm deployments' status in the given namespace.

    :param namespace: Namespace
    :return: True if all Helm list status is DEPLOYED, else False
    """
    command = "helm list --namespace " + namespace
    stdout = common.execute_cli_locally(command, eks_constants.HELM_COMMAND_TIMEOUT,
                                        return_output_as_string=False)
    if stdout is False:
        return False

    try:
        result = True
        LOG.info("Regex to be parsed : %s", eks_constants.REGEX_FOR_HELM_DEPLOYMENTS)

        for line in stdout[1:]:
            line = line.decode(common_constants.BYTE_TO_STRING_DECODE_TYPE_UTF_8)
            LOG.info(line)
            regex_match = re.match(eks_constants.REGEX_FOR_HELM_DEPLOYMENTS, line)
            if not regex_match:
                result = False
                LOG.error("Regex pattern didn't match for the line : %s", line)
            else:
                m_dict = regex_match.groupdict()
                LOG.info("Regex outputs : %s", str(m_dict))
                if m_dict['status'] != eks_constants.HELM_STATUS_DEPLOYED:
                    result = False
                    LOG.error("Helm deployment %s's status is not %s",
                              m_dict['name'], eks_constants.HELM_STATUS_DEPLOYED)

        return result

    except Exception as error:
        return common.handle_common_exception(error,
                                              eks_constants.HELM_CLI_PARSING_EXCEPTION_MESSAGE)


def helm_install_neo4j_sts(namespace):
    """
    Install sample Helm app and verify deployment and pod status

    :param namespace: Namespace
    :return: True if Neo4j charts installed successfully, else False
    """
    command = "helm install " + eks_constants.HELM_NEO4J_CHART_DIR + " --namespace " + namespace + \
              " --name " + eks_constants.HELM_NEO4J_STS_TEST_DEPLOYMENT_NAME
    stdout = common.execute_cli_locally(command, eks_constants.HELM_COMMAND_TIMEOUT)
    if stdout is False:
        return False

    try:
        LOG.info("Regex to be parsed : %s", eks_constants.HELM_DEPLOYMENT_NAME_REGEX)
        LOG.info("Regex to be parsed : %s", eks_constants.HELM_DEPLOYMENT_STATUS_REGEX)

        regex_name_match = re.match(eks_constants.HELM_DEPLOYMENT_NAME_REGEX, stdout)
        regex_status_match = re.match(eks_constants.HELM_DEPLOYMENT_NAME_REGEX, stdout)
        if not (regex_name_match or regex_status_match):
            LOG.error("Regex pattern didn't match for the string : %s", stdout)
            return False

        core_v1 = client.CoreV1Api()

        result = True
        for pod_count in range(eks_constants.NEO4J_TEST_POD_COUNT):
            pod_name = eks_constants.NEO4J_STS_TEST_DEPLOYMENT_NAME + "-" + str(pod_count)
            wait_result = kubernetes_common.wait_for_pod_status_ready(core_v1, pod_name, namespace)
            if not wait_result:
                result = False

        return result

    except Exception as error:
        return common.handle_common_exception(error,
                                              eks_constants.HELM_CLI_PARSING_EXCEPTION_MESSAGE)


def verify_neo4j_pods_logs(namespace):
    """
    Verify Neo4j pods logs to match the string : "INFO  Remote interface available at"

    :param namespace: Namespace
    :return: True if all Neo4j pods have success message in log, else False
    """
    command = "kubectl logs -l " + eks_constants.NEO4J_TEST_POD_LABEL \
              + " -n " + namespace

    return common.execute_command_and_wait_for_regex_count_match(
        command, eks_constants.NEO4J_PODS_LOGS_REGEX, eks_constants.NEO4J_TEST_POD_COUNT)


def verify_neo4j_pod_recovery(namespace):
    """
    Verify Neo4j's role on all pods and verify recovery a deleted a pod

    :param namespace: Namespace
    :return: True if a deleted pod is recovered successfully, else False
    """
    command = "./" + eks_constants.HELM_STS_TEST_SCRIPT_PATH + " " + namespace + " " \
              + eks_constants.NEO4J_STS_TEST_DEPLOYMENT_NAME + " " + \
              str(eks_constants.NEO4J_TEST_POD_COUNT)

    return common.execute_command_and_match_regex_list(
        command, eks_constants.NEO4J_TEST_SCRIPT_SUCCESS_MESSAGES_LIST)


def helm_delete_neo4j_sts(namespace):
    """
    Delete sample Helm app

    :param namespace: Namespace
    """
    command = "helm delete " + eks_constants.HELM_NEO4J_STS_TEST_DEPLOYMENT_NAME + " --purge"

    common.execute_cli_locally(command, eks_constants.HELM_COMMAND_TIMEOUT)

    core_v1 = client.CoreV1Api()

    for count in range(eks_constants.NEO4J_TEST_POD_COUNT):
        pvc_name = eks_constants.NEO4J_TEST_PVC_NAME + "-" + str(count)
        core_v1.delete_namespaced_persistent_volume_claim(pvc_name, namespace)
