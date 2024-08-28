##############################################################################
# COPYRIGHT Ericsson 2019
#
# The copyright to the computer program(s) herein is the property of
# Ericsson Inc. The programs may be used and/or copied only with written
# permission from Ericsson Inc. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################

"""Constants for Elasticsearch tests."""

import os

ES_TEST_POD_FILENAME = os.path.join("kubernetes_resources", "elasticsearch", "es_test_pod.yaml")
ES_TEST_JOB_NAME = "elasticsearch-health-checker"
ES_CLUSTER_STATUS_GREEN = "green"
ES_TEST_JOB_LABEL_KEY = "job-name"

ES_TEST_POD_LOG_CHECK_CLUSTER_HEALTH_STRING = "check cluster health"
ES_TEST_POD_LOG_CREATE_AN_INDEX_STRING = "create an index"
ES_TEST_POD_LOG_GET_INDEX_STRING = "get index"
ES_TEST_POD_LOG_DELETE_INDEX_STRING = "delete index"

ES_POD_TEST_INDEX_DATA = "{'test': 'ENM'}"
ES_POD_TEST_INDEX_COUNT = 1
