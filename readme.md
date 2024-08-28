# ENMaaS Cloud Deployment Tests

Insurance tests for any deployment of ENMaaS on cloud.

### Dependencies:

* [Robot Framework](https://github.com/robotframework/robotframework) -
Automation framework for acceptance testing, acceptance test driven development (ATDD)
and robotic process automation (RPA)
* [boto3](https://github.com/boto/boto3) - AWS SDK
* [botocore](https://github.com/boto/botocore) - Low-level, core functionality of boto3
* [Kubernetes](https://github.com/kubernetes-client/python) -
Python client for the kubernetes API

### Setup outside PyCharm IDE:

This project can be run with python and python3, although python3 is recommended.

* Execute the `venv.sh` script.
> In this case, venv.sh script should be executed only outside PyCharm to not conflict with the 
default venv used by the IDE.

```sh
$ sudo ./venv.sh
```

### Setup with PyCharm IDE:

After the project is open, a Virtual Environment should be created for the project (preferably 
inside the project directory).
> File -> Settings -> Project Interpreter -> Add -> New Environment\
> Location: [project_directory]/venv\
> Base interpreter: Python 3.6


* Install the dependencies:

```sh
$ pip3 install -e .
```


### AWS Credentials:
For that, awscli needs to be installed. Skip this if awscli is already installed.

```sh
$ sudo pip3 install awscli --upgrade
```

If no credentials were configured, do the following:

```sh
$ aws configure
```

Provide the input with a valid Access ID/Secret key pair.

### Executing the tests:

To run all tests:
```sh
$ PYTHONPATH=. robot tests
```

To run a specific test
```sh
$ PYTHONPATH=. robot tests/[robot_test_file]
```

* For Windows users, PYTHONPATH should be added to Environment variables,
with the references for Python installation directory, Python packages
directory and project directory.

The reports from the tests execution are created on project root.
If another directory needed to be pointed, the flag for output should be added:

```sh
$ PYTHONPATH=. robot --outputdir [output_directory] tests/[robot_test_file]
```

### Checking Pylint:

```sh
$ python linters.py
```

Or right-click on `linters.py` file and `Run 'linters'`
