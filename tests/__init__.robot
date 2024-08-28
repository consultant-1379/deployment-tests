*** Settings ***
Documentation   Test suite for ENM terraform test cases
Suite Setup     Perform suite setup
Force Tags      ENM   Terraform
Library         ${CURDIR}/../configuration/terraform_inputs.py

*** Keywords ***
Perform suite setup
    [Documentation]  Read Terraform TFVars
    &{tfvars} =      read_terraform_tfvars
    set global variable      &{tfvars}
    set global variable      ${namespace}   ${tfvars.namespace}
    log many  &{tfvars}

    ${enable_aws_elasticsearch} =   Evaluate    $tfvars.get("enable_aws_elasticsearch", "true")
    set global variable      ${enable_aws_elasticsearch}     ${enable_aws_elasticsearch}
    log     Enable AWS Elasticsearch = ${enable_aws_elasticsearch}
