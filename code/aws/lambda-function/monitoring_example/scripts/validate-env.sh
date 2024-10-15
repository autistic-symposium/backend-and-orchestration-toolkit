#!/usr/bin/env bash

set -o errexit  # always exit on error
set -o errtrace # trap errors in functions as well
set -o pipefail # don't ignore exit codes when piping output
set -o posix    # more strict failures in subshells

IFS=$'\n\t'

declare -a missing
for var in "$@"; do
  if [[ -z "${!var}" ]]; then
    echo "⚠️ ERROR: Missing required environment variable: ${var}" 1>&2
    missing+=("${var}")
  fi
done
if [[ -n "${missing[*]}" ]]; then
  exit 1
fi