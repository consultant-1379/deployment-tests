##############################################################################
# COPYRIGHT Ericsson 2019
#
# The copyright to the computer program(s) herein is the property of
# Ericsson Inc. The programs may be used and/or copied only with written
# permission from Ericsson Inc. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################

# pylint: disable=R0801,W1201,R0911,R0914

"""Module for defining Elasticsearch tests."""

import time
import json
from flask_api import status
from kubernetes.client.rest import ApiException
from kubernetes import client, config
from configuration.logging import LOG
import kubernetes_resources.common.common as common
import kubernetes_resources.elasticsearch.constants as constants


def check_elasticsearch_service_health(tfvars):
    """
    Test Elasticsearch service with the test job.

    :param tfvars: TFvars
    :return: True if elasticsearch service connectivity is OK, else False
    """
    namespace = tfvars['namespace']
    cluster_name = tfvars['cluster_name']
    body = common.update_kubernetes_resource_file(constants.ES_TEST_POD_FILENAME,
                                                  namespace)
    if body is None:
        return False

    response = None
    try:
        config.load_kube_config()
        core_v1 = client.CoreV1Api()
        batch_v1 = client.BatchV1Api()

        response = batch_v1.create_namespaced_job(namespace, body)

        response = core_v1.list_namespaced_pod(namespace, label_selector=
                                               constants.ES_TEST_JOB_LABEL_KEY + "=" +
                                               constants.ES_TEST_JOB_NAME)
        pod_name = response.items[0].metadata.name
        wait_result = common.wait_for_pod_status_waiting_none(core_v1, pod_name, namespace)
        if wait_result is not True:
            return False

        # Wait before checking Elasticsearch APIs execution (that are logged) after the Pod is UP
        # This can be affected depending on Internet speed, since some packages are downloaded first
        # Since there is no defined way to track the pod logs, a manual sleep is kept.
        time.sleep(30)

        pod_log = core_v1.read_namespaced_pod_log(pod_name, namespace)
        LOG.info("Pod logs :\n%s", pod_log)

        if not check_elasticsearch_cluster_health_from_pod_log(pod_log, cluster_name) \
            or not check_elasticsearch_index_creation_from_pod_log(pod_log) \
            or not check_elasticsearch_index_get_from_pod_log(pod_log) \
                or not check_elasticsearch_index_delete_from_pod_log(pod_log):
            return False

        return True

    except ApiException as error:
        common.log_kubernetes_api_exception(error, response)
        return False


def check_elasticsearch_cluster_health_from_pod_log(pod_log, cluster_name):
    """
    Check elasticsearch cluster health from test pod log (based on API call)

    :param pod_log: Pod log in string format
    :param cluster_name: Elasticsearch Cluster name
    :return: True if cluster health is GREEN, else False
    """
    start_index = pod_log.find(constants.ES_TEST_POD_LOG_CHECK_CLUSTER_HEALTH_STRING) +\
        len(constants.ES_TEST_POD_LOG_CHECK_CLUSTER_HEALTH_STRING) + 1
    end_index = pod_log.find(constants.ES_TEST_POD_LOG_CREATE_AN_INDEX_STRING) - 1
    check_cluster_health_response = pod_log[start_index:end_index]
    LOG.info("Check cluster health response : %s", check_cluster_health_response)

    http_status = check_cluster_health_response[-3:]
    if str(status.HTTP_200_OK) not in http_status:
        return False

    check_cluster_health_response_json = \
        check_cluster_health_response[:len(check_cluster_health_response) - 3]
    LOG.info("Verify below details in the pod logs")
    LOG.info("HTTP response status = %d", status.HTTP_200_OK)
    LOG.info("Cluster name = %s", cluster_name)
    LOG.info("Cluster status = %s", constants.ES_CLUSTER_STATUS_GREEN)

    response_dict = json.loads(check_cluster_health_response_json)
    if cluster_name not in response_dict['cluster_name'] \
            or constants.ES_CLUSTER_STATUS_GREEN not in response_dict['status']:
        return False

    return True


def check_elasticsearch_index_creation_from_pod_log(pod_log):
    """
    Check Elasticsearch index creation from test pod log (based on API call)

    :param pod_log: Pod log in string format
    :return: True if HTTP STATUS = 200, else False
    """
    start_index = pod_log.find(constants.ES_TEST_POD_LOG_CREATE_AN_INDEX_STRING) + \
        len(constants.ES_TEST_POD_LOG_CREATE_AN_INDEX_STRING) + 1
    end_index = pod_log.find(constants.ES_TEST_POD_LOG_GET_INDEX_STRING) - 1
    create_an_index_response = pod_log[start_index:end_index]

    LOG.info("Create an index response : %s", create_an_index_response)
    LOG.info("Verify below details in the pod logs")
    LOG.info("HTTP response status = %d", status.HTTP_201_CREATED)

    http_status = create_an_index_response[-3:]
    LOG.debug(http_status)
    if str(status.HTTP_201_CREATED) not in http_status:
        return False

    return True


def check_elasticsearch_index_get_from_pod_log(pod_log):
    """
    Check Elasticsearch get index from pod log (based on API call)

    :param pod_log: Pod log in string format
    :return: True if get index check is OK, else False
    """
    start_index = pod_log.find(constants.ES_TEST_POD_LOG_GET_INDEX_STRING) + \
        len(constants.ES_TEST_POD_LOG_GET_INDEX_STRING) + 1
    end_index = pod_log.find(constants.ES_TEST_POD_LOG_DELETE_INDEX_STRING) - 1
    get_index_response = pod_log[start_index:end_index]

    LOG.info("Get index response : %s", get_index_response)
    http_status = get_index_response[-3:]
    LOG.debug(http_status)
    if str(status.HTTP_200_OK) not in http_status:
        return False

    get_index_response_json = get_index_response[:len(get_index_response) - 3]
    LOG.info("Verify below details in the pod logs")
    LOG.info("HTTP response status = %d", status.HTTP_200_OK)
    LOG.info("Total hits = %d", constants.ES_POD_TEST_INDEX_COUNT)
    LOG.info("Index data = %s", constants.ES_POD_TEST_INDEX_DATA)

    response_dict = json.loads(get_index_response_json)
    hits = response_dict['hits']
    hits_total = hits['total']
    hits_source = hits['hits'][0]['_source']
    LOG.debug("Dict : %s", str(response_dict))
    LOG.debug("Total : %d", hits_total)
    LOG.debug("Source : %s", str(hits_source))

    if hits_total != constants.ES_POD_TEST_INDEX_COUNT \
            or constants.ES_POD_TEST_INDEX_DATA not in str(hits_source):
        return False

    return True


def check_elasticsearch_index_delete_from_pod_log(pod_log):
    """
    Check Elasticsearch delete index from pod log (based on API call)

    :param pod_log: Pod log in string format
    :return: True if get index check is OK, else False
    """
    start_index = pod_log.find(constants.ES_TEST_POD_LOG_DELETE_INDEX_STRING) + \
        len(constants.ES_TEST_POD_LOG_DELETE_INDEX_STRING) + 1
    delete_index_response = pod_log[start_index:]

    LOG.info("Delete index response : %s", delete_index_response)
    LOG.info("Verify below details in the pod logs")
    LOG.info("HTTP response status = %d", status.HTTP_200_OK)

    http_status = delete_index_response[-3:]
    LOG.debug(http_status)
    if str(status.HTTP_200_OK) not in http_status:
        return False

    return True


def delete_elasticsearch_health_check_job(namespace):
    """
    Delete Elasticsearch service test pod.

    :param namespace: Namespace
    """
    response = None
    try:
        config.load_kube_config()
        batch_v1 = client.BatchV1Api()
        core_v1 = client.CoreV1Api()

        response = batch_v1.delete_namespaced_job(constants.ES_TEST_JOB_NAME, namespace)

        response = core_v1.list_namespaced_pod(namespace, label_selector=
                                               constants.ES_TEST_JOB_LABEL_KEY + "=" +
                                               constants.ES_TEST_JOB_NAME)
        for item in response.items:
            pod_name = item.metadata.name
            core_v1.delete_namespaced_pod(pod_name, namespace)

    except ApiException as error:
        common.log_kubernetes_api_exception(error, response)
