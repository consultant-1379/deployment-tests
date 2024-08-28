*** Settings ***
Documentation   Test suite for EFS test cases
Default Tags    Kubernetes  EFS
Suite Teardown  Perform suite teardown
Library         ${CURDIR}/../kubernetes_resources/efs/efs_tests.py

*** Variables ***

*** Keywords ***
Perform suite teardown
    [Documentation]     Delete EFS test pod
    delete_efs_test_pod   ${namespace}

*** Test Cases ***
EFS Storageclass test
    [Documentation]  Verify EFS Storageclass "aws-efs" details
    ${response} =   check_efs_storage_class
    should be true  ${response}

EFS PVC check
    [Documentation]  Verify EFS PVC "efs" details
    ${response} =   check_efs_pvc      ${namespace}
    should be true  ${response}

EFS service check
    [Documentation]  Deploy test pod using efs_test_pod.yaml and verify output in the log
    ${response} =   test_efs_service      ${namespace}
    should be true  ${response}
