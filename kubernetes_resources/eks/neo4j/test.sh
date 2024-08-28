#!/bin/bash

NAMESPACE=$1
STATEFULSET_NAME=$2
CORE_REPLICAS=$3

NEO4J_SECRETS_PASSWORD=$(kubectl get secret -n ${NAMESPACE} ${STATEFULSET_NAME}-secrets -o jsonpath='{.data.neo4j-password}' | base64 --decode)

echo "Testing we can get the cluster role of each server in statefulset ${STATEFULSET_NAME} in namespace: ${NAMESPACE}"

check_role() {
  name=$1
  end="$((SECONDS+120))"
  while true; do
    echo "checking cluster role: ${name}"
    kubectl exec ${name} -n ${NAMESPACE} -- bin/cypher-shell -u neo4j -p ${NEO4J_SECRETS_PASSWORD} "call dbms.cluster.role()" 2>/dev/null
    response_code=$?
    [[ "0" = "$response_code" ]] && break
    [[ "${SECONDS}" -ge "${end}" ]] && exit 1
    echo "waiting for connection to pod: ${name}"
    sleep 5
  done
}

for num in $(seq $CORE_REPLICAS); do
  id=$(expr $num - 1)
  name="${STATEFULSET_NAME}-$id"
  echo "checking role of $name"
  check_role $name
done

echo "All pods roles retrieved successfully!"
# kill a machine and make sure it comes back again
machine_to_kill="${STATEFULSET_NAME}-0"
echo "Testing recovery after failed/deleted pod"
echo "Deleting pod: ${machine_to_kill}"
kubectl delete pod ${machine_to_kill} -n ${NAMESPACE}
check_role ${machine_to_kill}
echo "Pod recovered successfully!"
