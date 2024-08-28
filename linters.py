##############################################################################
# COPYRIGHT Ericsson 2019
#
# The copyright to the computer program(s) herein is the property of
# Ericsson Inc. The programs may be used and/or copied only with written
# permission from Ericsson Inc. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################

"""Module for checking pylint on code."""

from setuptools import find_packages
from pylint import epylint


for pack in find_packages():
    if pack.find('.') == -1:
        print("Checking linters on {} module.".format(pack))
        epylint.py_run(pack)
