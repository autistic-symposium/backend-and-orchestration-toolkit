#!/usr/bin/env bash

set -o errexit  # always exit on error
set -o errtrace # trap errors in functions as well
set -o pipefail # don't ignore exit codes when piping output


IFS=$'\n\t'

cd "$(dirname "${BASH_SOURCE[0]}")/.."

source "$1"
make --makefile=./scripts/deploy.mk all
