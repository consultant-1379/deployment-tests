*** Settings ***
Documentation   Test suite to verity 3PP tools versions
Default Tags    TERRAFORM   KUBERNETES  HELM    ELASTICSEARCH
Library         ${CURDIR}/../three_pp_tools/three_pp_tools_tests.py

*** Variables ***
${TERRAFORM_VERSION}            0.11.11
${KUBERNETES_CLIENT_VERSION}    1.12.6
${KUBERNETES_SERVER_VERSION}    1.12.10
${HELM_CLIENT_VERSION}          2.13.1
${HELM_SERVER_VERSION}          2.13.1
${ELASTICSEARCH_VERSION}        6.5

*** Keywords ***

*** Test Cases ***
Verify Terraform version
    [Documentation]  Verify Terraform version
    ${response} =   get_terraform_version
    LOG  Expected version = ${TERRAFORM_VERSION}
    LOG  Installed version = ${response}
    should be equal as strings  ${response}     ${TERRAFORM_VERSION}

Verify Kubernetes version
    [Documentation]  Verify Kubernetes version
    ${client_version}  ${server_version} =   get_kubernetes_versions
    LOG  Kubernetes client : Expected version = ${KUBERNETES_CLIENT_VERSION}
    LOG  Kubernetes client : Installed version = ${client_version}
    LOG  Kubernetes server : Expected version = ${KUBERNETES_SERVER_VERSION}
    LOG  Kubernetes server : Installed version = ${server_version}
    should be equal as strings  ${client_version}     ${KUBERNETES_CLIENT_VERSION}
    should be equal as strings  ${server_version}     ${KUBERNETES_SERVER_VERSION}

Verify Helm version
    [Documentation]  Verify Helm version
    ${client_version}  ${server_version} =   get_helm_versions
    LOG  Helm client : Expected version = ${HELM_CLIENT_VERSION}
    LOG  Helm client : Installed version = ${client_version}
    LOG  Helm server : Expected version = ${HELM_SERVER_VERSION}
    LOG  Helm server : Installed version = ${server_version}
    should be equal as strings  ${client_version}     ${HELM_CLIENT_VERSION}
    should be equal as strings  ${server_version}     ${HELM_SERVER_VERSION}

Verify AWS Elasticsearch version
    [Documentation]  Verify AWS Elasticsearch version
    LOG     AWS Elasticsearch is not installed. Hence, bypass the test.
    Pass Execution If   "${enable_aws_elasticsearch}" == "false"   Bypass Elasticsearch test
    ${response} =   get_elasticsearch_version       ${tfvars}
    LOG  Expected version = ${ELASTICSEARCH_VERSION}
    LOG  Installed version = ${response}
    should be equal as strings  ${response}     ${ELASTICSEARCH_VERSION}

Log Terraform providers version
    [Documentation]     Log Terraform providers version
    log_terraform_providers_version
