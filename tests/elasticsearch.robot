*** Settings ***
Documentation   Test suite for Elasticsearch test cases
Default Tags    Kubernetes  Elasticsearch
Suite Teardown  Perform suite teardown
Library         ${CURDIR}/../kubernetes_resources/elasticsearch/es_tests.py

*** Variables ***

*** Keywords ***
Perform suite teardown
    [Documentation]     Delete Elastic search health check job
    LOG     AWS Elasticsearch is not installed. Hence, bypass the test teardown.
    Pass Execution If   "${enable_aws_elasticsearch}" == "false"   Bypass Elasticsearch teardown
    delete_elasticsearch_health_check_job   ${namespace}

*** Test Cases ***
Elastic search health check
    [Documentation]  Verify Elasticsearch Cluster health using the job "es_test_job.yaml"
    ...              This job creates a temporary pod and performs curl operation to
    ...              http://elasticsearch/_cluster/health (where "elasticsearch" points to
    ...              the Elasticsearch cluster endpoint created on AWS).
    ...              From the pod's logs, we verify the curl response status = 200.
    ...              And from the response body, verify cluster name and status = "green".
    ...              Additionally, we verify ES index PUT, GET and DELETE operations.
    LOG     AWS Elasticsearch is not installed. Hence, bypass the test.
    Pass Execution If   "${enable_aws_elasticsearch}" == "false"   Bypass Elasticsearch test
    ${response} =   check_elasticsearch_service_health      ${tfvars}
    should be true  ${response}
