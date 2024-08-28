*** Settings ***
Documentation   Test suite for EKS test cases
Default Tags    Kubernetes  EKS
Suite Teardown  Perform suite teardown
Library         ${CURDIR}/../kubernetes_resources/eks/eks_tests.py
Library         ${CURDIR}/../kubernetes_resources/eks/helm_tests.py

*** Variables ***

*** Keywords ***
Perform suite teardown
    [Documentation]     Delete Deployments for eks test
    ...                 Delete Helm app Neo4j Statefulset
    delete_eks_deployment
    helm_delete_neo4j_sts      ${namespace}

*** Test Cases ***
Kube-system pods verification
    [Documentation]  Verify all pods status = "Running" in "kube-system" namespace
    ${response} =   check_kube_system_pods
    should be true  ${response}

EKS verify deployment creation
    [Documentation]  Verify the EKS deployment creation
    ${response} =   create_eks_deployment
    should be true  ${response}

EKS verify deployment scale up
    [Documentation]  Verify the EKS deployment scaling increase
    ${response} =   scale_deployment_increase
    should be true  ${response}

EKS verify deployment checking nodes
    [Documentation]  Verify the EKS checking nodes
    ${response} =   check_eks_deployment_nodes
    should be true  ${response}

EKS verify deployment scale down
    [Documentation]  Verify the EKS deployment scaling decrease
    ${response} =   scale_deployment_decrease
    should be true  ${response}

Helm install verification with Neo4j Statefulset
    [Documentation]  Install Neo4j Statefulset using Helm charts
    ...              and verify deployment and pod status
    [Tags]          Helm    Statefulset     Neo4j
    ${response} =   helm_install_neo4j_sts      ${namespace}
    should be true  ${response}

Helm deployments verification
    [Documentation]  Verify all Helm deployments status = "DEPLOYED" in given namespace
    ${response} =   check_helm_list      ${namespace}
    should be true  ${response}

Neo4j pods logs verification
    [Documentation]  Verify below message in all Neo4j pods logs
    ...              "INFO  Remote interface available at "
    [Tags]          Helm    Statefulset     Neo4j
    ${response} =   verify_neo4j_pods_logs      ${namespace}
    should be true  ${response}

Neo4j pods recovery verification
    [Documentation]  Verify below using test.sh script
    ...              1. Neo4j role (LEADER/FOLLOWER) on all pods can be retrieved.
    ...              2. Delete a pod.
    ...              3. New pod is replaced automatically, and it's Neo4j role can be retrieved.
    [Tags]          Helm    Statefulset     Neo4j
    ${response} =   verify_neo4j_pod_recovery      ${namespace}
    should be true  ${response}
