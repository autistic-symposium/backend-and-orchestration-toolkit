#!/usr/bin/env bash

set -o errexit  # always exit on error
set -o errtrace # trap errors in functions as well
set -o pipefail # don't ignore exit codes when piping output
set -o posix    # more strict failures in subshells

IFS=$'\n\t'

##### RUNNING THE SCRIPT #####
# export FUNCTION = <name of the lambda function in aws, can be found by aws lambda list-functions"
# source .env
# ./scripts/invoke.sh {true|false} [count]

cd "$(dirname "${BASH_SOURCE[0]}")/.."
./scripts/validate-env.sh AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY
function=$(aws lambda list-functions | jq -r '.Functions[].FunctionName' | grep -E '^monitoring-lambda' | head -1)
payload="{\"forceError\": ${1:-false}}"
outpath="/tmp/monitoring-lambda.out"
count="${2:-1}"
for i in $(seq "${count}"); do
  aws lambda invoke \
    --function-name "${function}" \
    --invocation-type Event \
    --payload "${payload}" \
    "${outpath}"
done
