##############################################################################
# COPYRIGHT Ericsson 2019
#
# The copyright to the computer program(s) herein is the property of
# Ericsson Inc. The programs may be used and/or copied only with written
# permission from Ericsson Inc. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################

"""Module for creating a log object."""

import logging

logging.basicConfig(filename="NMaaSLogging.log", format='%(asctime)s %(message)s', filemode='a')
LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)
