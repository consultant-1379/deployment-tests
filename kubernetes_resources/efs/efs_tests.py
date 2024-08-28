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

"""Module for defining EFS tests."""

from kubernetes.client.rest import ApiException
from kubernetes import client, config
from configuration.logging import LOG
import kubernetes_resources.common.common as common
import kubernetes_resources.common.constants as common_constants
import kubernetes_resources.efs.constants as constants


def check_efs_storage_class():
    """
    Verify EFS Storageclass details.

    :return: True if storageclass details are verified OK, else False
    """
    response = None
    try:
        config.load_kube_config()
        storage_v1 = client.StorageV1Api()

        response = storage_v1.read_storage_class(constants.EFS_STORAGE_CLASS_NAME)

        LOG.info("Storage class : " + str(response))

        LOG.info("Verifying below details :")
        LOG.info("Name = " + constants.EFS_STORAGE_CLASS_NAME)
        LOG.info("Provisioner = " + constants.EFS_STORAGE_PROVISIONER)
        LOG.info("Reclaim policy = " + common_constants.KUBERNETES_RECLAIM_POLICY_DELETE)
        LOG.info("Volume binding mode = " +
                 common_constants.KUBERNETES_VOLUME_BINDING_MODE_IMMEDIATE)

        if response.metadata.name != constants.EFS_STORAGE_CLASS_NAME\
                or response.provisioner != constants.EFS_STORAGE_PROVISIONER\
                or response.reclaim_policy != common_constants.KUBERNETES_RECLAIM_POLICY_DELETE\
                or response.volume_binding_mode != \
                common_constants.KUBERNETES_VOLUME_BINDING_MODE_IMMEDIATE:
            return False

        return True

    except ApiException as error:
        common.log_kubernetes_api_exception(error, response)
        return False


def check_efs_pvc(namespace):
    """
    Verify EFS PVC details.

    :param namespace: Namespace
    :return: True if PVC details are verified OK, else False
    """
    response = None
    try:
        config.load_kube_config()
        core_v1 = client.CoreV1Api()

        response = core_v1.read_namespaced_persistent_volume_claim(constants.EFS_PVC_NAME,
                                                                   namespace)
        LOG.info("Persistent Volume Claim : " + str(response))

        LOG.info("Verifying below details :")
        LOG.info("Phase = " + common_constants.KUBERNETES_PVC_PHASE_BOUND)
        LOG.info(common_constants.KUBERNETES_VOLUME_STORAGE_CLASS + " = " +
                 constants.EFS_STORAGE_CLASS_NAME)
        LOG.info(common_constants.KUBERNETES_VOLUME_STORAGE_PROVISIONER + " = " +
                 constants.EFS_STORAGE_PROVISIONER)
        LOG.info(common_constants.KUBERNETES_PV_BIND_COMPLETED + " = " +
                 common_constants.KUBERNETES_OBJECT_STATUS_YES)
        LOG.info(common_constants.KUBERNETES_PV_BOUND_BY_CONTROLLER + " = " +
                 common_constants.KUBERNETES_OBJECT_STATUS_YES)

        annotations = response.metadata.annotations
        if annotations[common_constants.KUBERNETES_VOLUME_STORAGE_CLASS] \
                != constants.EFS_STORAGE_CLASS_NAME\
                or annotations[common_constants.KUBERNETES_VOLUME_STORAGE_PROVISIONER] != \
                constants.EFS_STORAGE_PROVISIONER\
                or annotations[common_constants.KUBERNETES_PV_BIND_COMPLETED] != \
                common_constants.KUBERNETES_OBJECT_STATUS_YES\
                or annotations[common_constants.KUBERNETES_PV_BOUND_BY_CONTROLLER] != \
                common_constants.KUBERNETES_OBJECT_STATUS_YES\
                or response.status.phase != common_constants.KUBERNETES_PVC_PHASE_BOUND:
            return False

        return True

    except ApiException as error:
        common.log_kubernetes_api_exception(error, response)
        return False


def test_efs_service(namespace):
    """
    Test EFS service with the test pod.

    :param namespace: Namespace
    :return: True if EFS test service was OK, else False
    """
    body = common.update_kubernetes_resource_file(constants.EFS_TEST_POD_FILENAME,
                                                  namespace)
    if body is None:
        return False

    response = None
    try:
        config.load_kube_config()
        core_v1 = client.CoreV1Api()

        response = core_v1.create_namespaced_pod(namespace, body)
        pod_name = constants.EFS_TEST_POD_NAME
        LOG.info("Namespace created OK")

        wait_result = common.wait_for_pod_status_waiting_none(core_v1, pod_name, namespace)
        if wait_result is not True:
            return False
        LOG.info("Pod waiting OK")

        response = core_v1.read_namespaced_pod_log(pod_name, namespace)
        LOG.info("Pod logs :\n" + response)

        if constants.EFS_TEST_POD_SUCCESS_LOG not in response:
            return False

        return True

    except ApiException as error:
        common.log_kubernetes_api_exception(error, response)
        return False


def delete_efs_test_pod(namespace):
    """
    Delete Test EFS service pod.

    :param namespace: Namespace
    """
    response = None
    try:
        config.load_kube_config()
        core_v1 = client.CoreV1Api()

        response = core_v1.delete_namespaced_pod(constants.EFS_TEST_POD_NAME, namespace)

    except ApiException as error:
        common.log_kubernetes_api_exception(error, response)
