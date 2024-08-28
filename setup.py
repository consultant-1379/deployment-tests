##############################################################################
# COPYRIGHT Ericsson 2019
#
# The copyright to the computer program(s) herein is the property of
# Ericsson Inc. The programs may be used and/or copied only with written
# permission from Ericsson Inc. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################

import io
from setuptools import setup, find_packages

with io.open('readme.md', 'rt', encoding='utf8') as f:
    readme = f.read()

requires = ['robotframework',
            'PyYAML',
            'requests',
            'urllib3==1.25',
            'flask_api',
            'boto3',
            'botocore',
            'kubernetes',
            'pylint']

setup(
    name='deployment-tests',
    version='0.1',
    packages=find_packages(),
    license='Proprietary',
    author='NEMESIS team',
    author_email='nemesis@ericsson.com',
    url='https://gerrit.ericsson.se/#/admin/projects/ENMaaS/enm-public-cloud/deployment-tests',
    long_description=readme,
    platforms=["unix", "linux", "osx", "cygwin", "win32"],
    install_requires=requires,
)
