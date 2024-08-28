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

"""Module for defining EKS tests."""

from kubernetes.client.rest import ApiException
from kubernetes import client, config
from configuration.logging import LOG
import kubernetes_resources.common.common as common
import kubernetes_resources.common.constants as kubernetes_constants
import kubernetes_resources.eks.constants as eks_constants


def check_eks_deployment_status_by_image_pull(api_instance, namespace, image):
    """
    Check the EKS deployment status in order to know if the image was pulled

    :param image: is the name of the image to pull
    :param namespace: is the name of the namespace  where the pod is
    :param api_instance: is Kubnernetes client API instance
    :return: True if the image was pulled and false if not
    """
    api_response = api_instance.list_namespaced_pod(namespace)
    for item in api_response.items:
        LOG.info("Response Item %s ", item)
        if item.status.container_statuses[0].image == image:
            return True
        return False


def check_pods_status_by_nodes(api_instance, namespace):
    """
    Check the pod status by nodes and verify if pods are in diferent nodes

    :param api_instance: is Kubnernetes client API instance
    :param namespace: the namespace for the pod_status_to_check
    :return: True if the pods are in diferent nodes and False if not.
    """
    api_response = api_instance.list_namespaced_pod(namespace)
    LOG.debug("Debug %s ", api_response)
    node_name = []
    items = api_response.items
    for item in items:
        LOG.debug("Debug %s ", item)
        if item in node_name:
            return False
        node_name.append(item.spec.node_name)
    return True


def check_kube_system_pods():
    """
    Check Kube-system pods' status.

    :return: True if all pods' status is RUNNING, else False
    """
    response = None
    try:
        config.load_kube_config()
        core_v1 = client.CoreV1Api()

        return common.list_and_verify_pods_status_in_namespace(
            core_v1, kubernetes_constants.KUBERNETES_NAMESPACE_KUBE_SYSTEM)

    except (ApiException, Exception) as error:
        common.log_kubernetes_api_exception(error, response)
        return False


def create_eks_deployment():
    """
    Create a EKS deployment with the deployment object

    :return: True if the deployment was created and False if not
    """
    try:
        config.load_kube_config()
        configuration = client.Configuration()
        extensions_v1beta1 = client.ExtensionsV1beta1Api(client.ApiClient(configuration))

        deployment_template = common.create_deployment_object(
            eks_constants.EKS_TEST_DEPLOYMENT_NAME,
            eks_constants.EKS_TEST_DEPLOYMENT_IMAGE_NAME,
            eks_constants.EKS_TEST_DEPLOYMENT_PORT)
        LOG.info("template %s ", deployment_template)

        deployment = common.create_deployment(
            extensions_v1beta1,
            deployment_template,
            eks_constants.EKS_TEST_DEPLOYMENT_NAMESPACE)
        LOG.info("Deployment %s ", deployment)

        return deployment
    except ApiException as error:
        LOG.error(" Error: %s\n", str(error))
        return False


def delete_eks_deployment():
    """
    Delete the EKS deployment

    :return: True if able to delete the deployment and False if not
    """
    try:
        config.load_kube_config()
        configuration = client.Configuration()
        extensions_v1beta1 = client.ExtensionsV1beta1Api(client.ApiClient(configuration))

        deployment_deletion = common.delete_deployment(
            extensions_v1beta1,
            eks_constants.EKS_TEST_DEPLOYMENT_NAME,
            eks_constants.EKS_TEST_DEPLOYMENT_NAMESPACE)
        LOG.info("deployment deletion %s ", deployment_deletion)

        deployment_ecr_deletion = common.delete_deployment(
            extensions_v1beta1,
            eks_constants.EKS_TEST_ECR_NAME,
            eks_constants.EKS_TEST_DEPLOYMENT_NAMESPACE)
        LOG.info("deployment deletion %s ", deployment_ecr_deletion)

        return True
    except ApiException as error:
        LOG.error(" Error: %s\n", str(error))
        return False


def check_eks_deployment_nodes():
    """
    Check the EKS test deployment for the test case

    :return: True if EKS_TEST deployment spread over the nodes and False if not
    """
    try:
        config.load_kube_config()
        core_v1 = client.CoreV1Api()
        check_pods_nodes = check_pods_status_by_nodes(
            core_v1,
            eks_constants.EKS_TEST_DEPLOYMENT_NAMESPACE)
        LOG.info("Check pods %s ", check_pods_nodes)
        return check_pods_nodes

    except ApiException as error:
        LOG.error(" Error: %s\n", str(error))
        return False


def scale_deployment_increase():
    """
    Scale the EKS test  deployment in 2 replicas

    :return: True if able to increase the number of replicas and  False if not
    """
    try:
        increase_deployment_replicas = common.update_deployment_replicas(
            eks_constants.EKS_TEST_DEPLOYMENT_NAME,
            eks_constants.EKS_TEST_DEPLOYMENT_UP_TO_REPLICAS,
            eks_constants.EKS_TEST_DEPLOYMENT_NAMESPACE)
        return increase_deployment_replicas

    except ApiException as error:
        LOG.error(" Error: %s\n", str(error))
        return False


def scale_deployment_decrease():
    """
    Decrease the EKS test deployment to 1 replica

    :return: True if able to decrease the number of replicas and False if not
    """
    try:
        decrease_deployment_replica = common.update_deployment_replicas(
            eks_constants.EKS_TEST_DEPLOYMENT_NAME,
            eks_constants.EKS_TEST_DEPLOYMENT_DOWN_TO_REPLICAS,
            eks_constants.EKS_TEST_DEPLOYMENT_NAMESPACE)
        return decrease_deployment_replica
    except ApiException as error:
        LOG.error(" Error: %s\n", str(error))
        return False


def deployment_with_ecr_image():
    """
    Deploy on EKS using the ECR images

    :return: True if able to create the deployment and False if not
    """
    try:
        config.load_kube_config()
        configuration = client.Configuration()
        extensions_v1beta1 = client.ExtensionsV1beta1Api(client.ApiClient(configuration))

        deployment_template = common.create_deployment_object(
            eks_constants.EKS_TEST_ECR_NAME,
            eks_constants.EKS_TEST_ECR_IMAGE,
            eks_constants.EKS_TEST_DEPLOYMENT_PORT)
        LOG.info("template %s ", deployment_template)

        deployment = common.create_deployment(
            extensions_v1beta1,
            deployment_template,
            eks_constants.EKS_TEST_DEPLOYMENT_NAMESPACE)
        LOG.info("Deployment %s ", deployment)

        return deployment
    except ApiException as error:
        LOG.error(" Error: %s\n", str(error))
        return False


def check_eks_ecr_pull():
    """
    Check if the deployment was able to pull the image

    :return: True if able to pull the EKS_ECR image and False if not
    """
    try:
        config.load_kube_config()
        configuration = client.Configuration()
        core_v1 = client.CoreV1Api(client.ApiClient(configuration))
        check_image_pull = check_eks_deployment_status_by_image_pull(
            core_v1,
            eks_constants.EKS_TEST_DEPLOYMENT_NAMESPACE,
            eks_constants.EKS_TEST_ECR_IMAGE)
        return check_image_pull
    except ApiException as error:
        LOG.error(" Error: %s\n", str(error))
        return False
