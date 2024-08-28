*** Settings ***
Documentation  Test suite for aws resources.
Library  ../aws_resources/sample/sample_read.py
#Suite Setup      Pre requisites
#Make sure teardown when the suite is finished.
#Suite Teardown   Post Process

*** Variables ***
#Define variables at test suite level if only used once, otherwise define them on a higher level.
${TITLE}  Test cases for AWS Resources
${profile}  default

*** Keywords ***
#Use keywords so the test cases are easy to understand.
#Define a keyword on a higher level, if used in several suites.
Pre requisites
#add pre-requisites

Post Process
#add post process


*** Test Cases ***
#Test Cases should describe what they do
Fetch_S3_Buckets
         [Documentation]  List all s3 buckets in AWS account
         [Tags]  s3  aws
         connect_to_s3_fetch_all_buckets


List_Instances_by_Profile
         [Documentation]  List all EC2 instances in the AWS account
         [Tags]  ec2  aws
         describe_all_ec2_instances_for_profile  ${profile}


