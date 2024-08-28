##############################################################################
# COPYRIGHT Ericsson 2019
#
# The copyright to the computer program(s) herein is the property of
# Ericsson Inc. The programs may be used and/or copied only with written
# permission from Ericsson Inc. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################

# pylint: disable=R1705,W1201

"""Module for common functions for Kubernetes."""

import time
import yaml
from kubernetes import client
from kubernetes.client.rest import ApiException
import helpers.common.common as common
import helpers.common.constants as constants
import kubernetes_resources.common.constants as kubernetes_constants
from configuration.logging import LOG


def wait_for_pod_status_ready(core_v1, pod_name, namespace,
                              timeout=constants.KUBERNETES_POD_STATUS_CHANGE_TIMEOUT):
    """
    Wait for pod status to be ready.

    :param core_v1: Kubernetes client for CoreV1Api
    :param pod_name: Pod name
    :param namespace: Namespace
    :param timeout: Timeout in seconds
    :return: True if pod status becomes "ready: True", else False
    """
    LOG.info("Waiting for pod %s to be ready", pod_name)
    timeout = time.time() + timeout
    ready = False
    while not ready:
        response = core_v1.read_namespaced_pod(pod_name, namespace=namespace)
        LOG.debug(response)

        status = response.status
        LOG.info("STATUS : %s", str(status.container_statuses))
        if status.container_statuses is not None:
            ready = response.status.container_statuses[0].ready

        if time.time() > timeout:
            LOG.error("timed out waiting for '%s' to be ready", pod_name)
            return False
        time.sleep(constants.KUBERNETES_POD_STATUS_CHECK_SLEEP_TIME)

    return True


def wait_for_pod_status_waiting_none(core_v1, pod_name, namespace,
                                     timeout=constants.KUBERNETES_POD_STATUS_CHANGE_TIMEOUT):
    """
    Wait for pod status to be waiting none.

    :param core_v1: Kubernetes client for CoreV1Api
    :param pod_name: Pod name
    :param namespace: Namespace
    :param timeout: Timeout in seconds
    :return: True if pod status becomes "waiting: None", else False
    """
    LOG.info("Waiting for pod %s to be waiting : None", pod_name)
    timeout = time.time() + timeout
    waiting = False
    while waiting is not None:
        response = core_v1.read_namespaced_pod(pod_name, namespace=namespace)
        LOG.debug(response)

        status = response.status
        LOG.info("STATUS : %s", str(status.container_statuses))
        if status.container_statuses is not None:
            waiting = status.container_statuses[0].state.waiting

        if time.time() > timeout:
            LOG.error("timed out waiting for '%s' to be waiting none", pod_name)
            return False
        time.sleep(constants.KUBERNETES_POD_STATUS_CHECK_SLEEP_TIME)

    return True


def list_and_verify_pods_status_in_namespace(
        core_v1, namespace, pod_status_to_check=kubernetes_constants.KUBERNETES_POD_STATUS_RUNNING):
    """
    List all pods in given namespace and verify with given status

    :param core_v1: Kubernetes CoveV1 API object
    :param namespace: Namespace
    :param pod_status_to_check: Pod status to check
    :return: True/False based on Pods status check
    """
    response = core_v1.list_namespaced_pod(namespace)
    return verify_pods_status(response, pod_status_to_check)


def verify_pods_status(pods_dict,
                       pod_status_to_check=kubernetes_constants.KUBERNETES_POD_STATUS_RUNNING):
    """
    Verify pods status with given input

    :param pods_dict: Pods dictionary
    :param pod_status_to_check:  Pod status to check [default = RUNNING]
    :return: True if all pods' status match with given status to check
    """
    result = True
    LOG.info("Name - Status")
    for item in pods_dict.items:
        pod_name = item.metadata.name
        phase = item.status.phase
        LOG.info("%s - %s", pod_name, phase)
        if phase != pod_status_to_check:
            LOG.error("Pod %s is not in %s state", pod_name, pod_status_to_check)
            result = False

    return result


def update_kubernetes_resource_file(file_name, namespace):
    """
    Read Kubernetes resource file (in json format) into dict and replace 'namespace' in it.

    :param file_name: Kubernetes file name
    :param namespace: namespace
    :return: updated resource file as dict
    """
    body = None
    try:
        input_file = open(file_name, 'r')

        body = yaml.load(input_file)
        body['metadata']['namespace'] = namespace

        input_file.close()

        LOG.info("Updated file content :\n%s", str(body))
    except IOError as error:
        LOG.error("Couldn't read the input file %s %s", file_name, str(error))

    return body


def log_kubernetes_api_exception(error, response):
    """
    Log Kubernetes API exception.

    :param error: Exception
    :param response: API response
    """
    LOG.error("Exception occurred : %s\n", str(error))
    LOG.error("API response : %s\n", str(response))


def create_deployment_object(name, image_name, port):
    """
    Create a deployment object with container,image, replicas deployment

    :param name: name of the deploy
    :param image_name: the name of the image
    :param port: number of the port
    :return: the object for the deployment
    """
    container = client.V1Container(
        name=name,
        image=image_name,
        ports=[client.V1ContainerPort(container_port=port)])

    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "" + name + ""}),
        spec=client.V1PodSpec(containers=[container]))

    spec = client.ExtensionsV1beta1DeploymentSpec(
        replicas=1,
        template=template)

    deployment = client.ExtensionsV1beta1Deployment(
        api_version="extensions/v1beta1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=name),
        spec=spec)

    return deployment


def create_deployment(api_instance, deployment, namespace):
    """
    Create a deployment in Kubernetes

    :param api_instance: is Kubnernetes client API instance
    :param namespace: is Kubnernetes namespace to work
    :param deployment: is the name of the deployment object
    :return: True if able to create the deployment and False if not
    """
    try:
        api_response = api_instance.create_namespaced_deployment(
            body=deployment, namespace=namespace)
        LOG.info("Response %s ", api_response)
        return True
    except ApiException as error:
        LOG.error("error %s ", str(error))
        return False


def delete_deployment(api_instance, name, namespace):
    """
    Delete a deployment in Kubernetes

    :param api_instance: is Kubnernetes client API instance
    :param name: is the name of the deployment object
    :param namespace: The name of the Namespace
    :return: True if able to delete the deployment and False if not
    """
    try:
        api_response = api_instance.delete_namespaced_deployment(
            name=name, namespace=namespace,
            body=client.V1DeleteOptions(propagation_policy='Foreground', grace_period_seconds=2))
        LOG.info("Response %s ", api_response)
        return True
    except ApiException as error:
        LOG.info("Error %s ", str(error))
        return False


def update_deployment_replicas(name, replicas, namespace):
    """
    Update the number of replicas in Kubernetes

    :param name: the name of the deployment
    :param replicas: the number of replicas
    :param namespace: The name of the Namespace
    :return: True if able to update the deployment and False if not
    """
    try:
        command = "kubectl scale --replicas=" + str(replicas) + " " \
                  + "deployment/" + name + " -n " + namespace

        response = common.execute_cli_locally(
            command,
            constants.KUBERNETES_POD_STATUS_CHANGE_TIMEOUT)

        if response is False:
            return False

        return True

    except ApiException as error:
        LOG.info("Error  %s ", str(error))
        return False
