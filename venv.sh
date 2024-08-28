#!/bin/bash
##############################################################################
# COPYRIGHT Ericsson 2019
#
# The copyright to the computer program(s) herein is the property of
# Ericsson Inc. The programs may be used and/or copied only with written
# permission from Ericsson Inc. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################

# Create and install required dependencies in one step.

venv_dir="venv"
python3 -m venv ${venv_dir}
WSDIR="$(pwd)/$venv_dir"

# Set-up virtualenv in the temporary directory
. "${WSDIR}/bin/activate"

# Install any required pip packages
pip3 install -e .

# Run a subshell with virtualenv already activated
bash --rcfile "${WSDIR}/bin/activate" -i
