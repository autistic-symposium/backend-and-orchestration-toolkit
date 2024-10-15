#!/usr/bin/env bash
# This script adds additional dependences that are need for the lambda function package.

set -x

PACKAGE_NAME=cameras-clip.zip

# If S3_BUCKET env var isn't set, default it
if [ -z "${S3_BUCKET}" ]; then
  S3_BUCKET=s3-test
fi

# Set dist env and create initial zip file
ORIGIN=$pwd
rm -rf dist && mkdir dist
lambda build --local-package . && mv dist/*.zip dist/$PACKAGE_NAME
cd dist/

## Fetch & add binary for FFMPEG
aws s3 cp "s3://${S3_BUCKET}/ffmpeg/ffmpeg-release-64bit-static.tar.xz" . && tar xf ffmpeg-release-64bit-static.tar.xz
zip -j -r9 $PACKAGE_NAME ffmpeg-*-64bit-static/ffmpeg
zip -j -r9 $PACKAGE_NAME ffmpeg-*-64bit-static/ffprobe

# Add this App's source code
cp -r ../lib .
zip -r9 $PACKAGE_NAME lib

# Add dependencies from pip
mkdir packages
cp ../scripts/Dockerfile.build Dockerfile
cp ../scripts/.dockerignore .dockerignore
cp ../requirements.txt .
docker build --tag pillow-build .
CTNHASH="$(docker create pillow-build)"
docker cp "${CTNHASH}":/opt/app/ .
cp -rf app/* packages/

# Package everything
cd packages
zip -ur9 ../$PACKAGE_NAME *
cd ..

# Clean up
#rm -rf ffmpeg-release-64bit-static.tar.xz ffmpeg-*-64bit-static/ packages/ lib/
docker rm ${CTNHASH}
cd $ORIGIN
