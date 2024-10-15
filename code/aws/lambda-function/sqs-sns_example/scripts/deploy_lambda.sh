#!/bin/bash -ex
# Script that deploy this app to the AWS lambda function, similarly to Jenkins.

USAGE=$(cat <<-END
Usage:
  deploy_lambda.sh <environment>
Examples:
  deploy_lambda.sh staging
END
)

if [[ "$1" = "-h" ]]; then
  echo "${USAGE}"
  exit
fi

if [[ -n "$1" ]]; then
  SERVER_GROUP=$1
else
  echo '[ERROR] You must specify  the env: production, sandbox, staging'
  echo
  echo "${USAGE}"
  exit 1
fi

BUILD_ENVIRONMENT=$1
APP_NAME=cameras-service-generate-clip
export AWS_DEFAULT_REGION="us-west-1"
export AWS_REGION="us-west-1"

if [[ "${BUILD_ENVIRONMENT}" == "sandbox" ]]; then
  S3_BUCKET=sl-artifacts-dev
else
  S3_BUCKET="sl-artifacts-${BUILD_ENVIRONMENT}"
fi

S3_PREFIX="lambda-functions/${APP_NAME}"
S3_BUNDLE_KEY="sl-${APP_NAME}.zip"
S3_TAGGED_BUNDLE_KEY="sl-${APP_NAME}-${BUILD_TAG}.zip"

make clean
make install
make lint
make build

aws \
    s3 cp "dist/${S3_BUNDLE_KEY}" "s3://${S3_BUCKET}/${S3_PREFIX}/${S3_BUNDLE_KEY}"

aws \
    s3 cp "s3://${S3_BUCKET}/${S3_PREFIX}/${S3_BUNDLE_KEY}" "s3://${S3_BUCKET}/${S3_PREFIX}/${S3_TAGGED_BUNDLE_KEY}"

aws \
    lambda update-function-code \
    --function-name "sl-${APP_NAME}-${BUILD_ENVIRONMENT}" \
    --s3-bucket "${S3_BUCKET}" \
    --s3-key "${S3_PREFIX}/${S3_TAGGED_BUNDLE_KEY}"

echo "build description:${APP_NAME}|${BUILD_ENVIRONMENT}|${BUILD_TAG}|"
