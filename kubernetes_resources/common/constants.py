##############################################################################
# COPYRIGHT Ericsson 2019
#
# The copyright to the computer program(s) herein is the property of
# Ericsson Inc. The programs may be used and/or copied only with written
# permission from Ericsson Inc. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################

# pylint: disable=R1705,W1201

"""Module for common constants for Kubernetes."""

KUBERNETES_NAMESPACE_KUBE_SYSTEM = "kube-system"
KUBERNETES_POD_STATUS_RUNNING = "Running"

KUBERNETES_CLI_PARSING_EXCEPTION_MESSAGE = "Exception occurred while parsing Kubernetes CLI."

KUBERNETES_VOLUME_STORAGE_CLASS = "volume.beta.kubernetes.io/storage-class"
KUBERNETES_VOLUME_STORAGE_PROVISIONER = "volume.beta.kubernetes.io/storage-provisioner"
KUBERNETES_PV_BIND_COMPLETED = "pv.kubernetes.io/bind-completed"
KUBERNETES_PV_BOUND_BY_CONTROLLER = "pv.kubernetes.io/bound-by-controller"
KUBERNETES_PVC_PHASE_BOUND = "Bound"
KUBERNETES_RECLAIM_POLICY_DELETE = "Delete"
KUBERNETES_VOLUME_BINDING_MODE_IMMEDIATE = "Immediate"
KUBERNETES_OBJECT_STATUS_YES = "yes"
