#!/usr/bin/env bash

curl -i URL?startDate=$(date -v '-1H' +%s)000&endDate=$(date +%s)000
