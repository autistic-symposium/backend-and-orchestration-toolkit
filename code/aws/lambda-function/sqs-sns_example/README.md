# AWS Lambda Function to Trim Videos with FFMPEG 


An AWS Lambda Function to trim videos served from an API endpoint, within two given NTP UTC timestamps. 

The stack also uses SQS, SNS, and S3 resources.

----

# Table of Contents

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Introduction](#introduction)
- [Running Locally](#running-locally)
    - [Create a virtual environment](#create-a-virtual-environment)
    - [Configure the environment](#configure-the-environment)
      - [Changes when moving to another environment](#changes-when-moving-to-another-environment)
    - [Install the dependencies](#install-the-dependencies)
    - [Create Sample SQS events](#create-sample-sqs-events)
    - [Running the App locally](#running-the-app-locally)
- [AWS Deploynment](#aws-deploynment)
    - [Running the App as a Lambda Function](#running-the-app-as-a-lambda-function)
    - [Testing the flow in AWS](#testing-the-flow-in-aws)
    - [Debugging Errors](#debugging-errors)
- [Contributing](#contributing)
    - [Committing new code](#committing-new-code)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

----

# Introduction


As we see in this diagram, this application performs the following steps:

1. Receive a SQS event requesting a clip for a given time interval. An example of SQS event is the follow:

```json
        {
          "Records": [
            {
              "body": "{'clipId': '1111111111111', 'retryTimestamps': [], 'cameraId': '1111111111111', 'startTimestampInMs': 1537119363000, 'endTimestampInMs': 1537119423000}",
              "receiptHandle": "MessageReceiptHandle",
              "md5OfBody": "7b270e59b47ff90a553787216d55d91d",
              "eventSourceARN": "arn:aws:sqs:us-west-1:123456789012:MyQueue",
              "eventSource": "aws:sqs",
              "awsRegion": "us-west-1",
              "messageId": "19dd0b57-b21e-4ac1-bd88-01bbb068cb78",
              "attributes": {
                "ApproximateFirstReceiveTimestamp": "1523232000001",
                "SenderId": "123456789012",
                "ApproximateReceiveCount": "1",
                "SentTimestamp": "1523232000000"
              },
              "messageAttributes": {
                "SentTimestamp": "1523232000000"
              }
            }
          ]
        }
 ```


2. Call the camera API with the endpoint `/cameras/cameraID` to retrieve a camera alias for the given camera id.

3. Call the camera API with the endpoint `/cameras/recording/` to retrieve a list of cam rewind source files within the given time range. 

Which would generate this response:

```json
        [{
            "startDate":"2018-09-16T16:00:17.000Z",
            "endDate":"2018-09-16T16:10:17.000Z",
            "thumbLargeUrl":URL,
            "recordingUrl":URL,
            "thumbSmallUrl":URL,
            "alias":"test"
         }]
```

4. Retrieve the cam rewind source files from the origin S3 bucket (downloading them on disk).

5. Use ffmpeg to trim and merge clips into a single clip and to create several thumbnails.

6. If the clips are available, store them in the destination S3 bucket.

7. If the clips are not available, send a SQS message back to the queue, similar to the initial SQS, with a visibility timeout.

8. Call the camera API with endpoint `/cameras/clips` to update the information about the new clip and send a SNS message with the resulting metadata. An example of SNS message:

```json
       { 
          "clipId": "1111111111111",
          "cameraId": "1111111111111",
          "startTimestampInMs": 1534305591000,
          "endTimestampInMs": 1534305611000,
          "status": "CLIP_AVAILABLE",
          "bucket": "s3-test",
          "clip": {
            "url": URL,
            "key": "/test.mp4"
          },
          "thumbnail": {
            "url": "https://url_{size}.png",
            "key": "/1111111111111/1111111111111{size}.png",
            "sizes": [300, 640, 1500, 3000]
          }
        }
```



# Running Locally

To add new features to this application, follow these steps:

### Create a virtual environment

```bash
virtualenv venv
source venv/bin/activate
```

### Configure the environment

```bash
cp .env.sample_{env} .env
vim .env
```

Where these are the global variables in this file:

| Constant               | Definition                                                                             |
| :----------------------|:-------------------------------------------------------------------------------------- |
| CLIP_DOWNLOAD_DEST     | Where the clips are going to be downloaded in disk                                     |
| TIMESTAMP_FORMAT       | The timestamp we will be parsing from the clip name strings                            |
| OLD_FILE_FORMAT        | False if the clips to be downloaded have seconds encoded in their names (new format)   |
| SQS_RETRY_LIMIT        | The limit, in seconds, of retries for CLIP PENDING (default: 15 minutes)               |
| OUT_OF_RANGE_LIMIT     | The limit, in seconds, of how back in the past clips can be retrieved (default: 3 days)|
| CAM_SERVICES_URL       | The url where the camera services is available                                         |
| CLIP_URL               | The url where the clips are posted to, accordingly to the environment                  |
| RECORDINGS_URL         | The url where the source recordings are retrieved.                                     |
| THUMBNAIL_SIZES        | List of values for which clip thumbnails need to be created                            |
| VIDEO_MAX_LEN          | Maximum length allowed for a clip                                                      |
| S3_BUCKET_ORIGIN       | AWS S3 bucket where the rewinds are available                                          |
| S3_BUCKET_ORIGIN_DIR   | AWS S3 'folder' where the rewinds are available                                        |
| S3_BUCKET_DESTINATION  | AWS S3 bucket where the clips will be upload to.                                       |
| AWS_SNS_TOPIC          | AWS SNS topic arn                                                                      |
| AWS_SQS_QUEUE          | AWS SQS queue arn                                                                      |
| AWS_SQS_QUEUE_URL      | AWS SQS queue url                                                                      |
| SQS_TIMEOUT            | AWS SQS invisibility timeout in seconds                                                |



#### Changes when moving to another environment

Whenever you move among the environments (prod, sandbox, or staging), you need to change the following variables:


| Constant                | Possible value                                      |
| :---------------------- |:-------------------------------------------------   |
| CLIP_URL                |   https://camclips.{ENV}.test.com                   |
| S3_BUCKET_DESTINATION   |   cameras-service-clips-cdn-{ENV}                   |
| AWS_SNS_TOPIC           |   arn:aws:sns:test_{ENV}                            |
| AWS_SQS_QUEUE           |   arn:aws:sqs:test-sqs-{ENV}                        |
| AWS_SQS_QUEUE_URL       |   https://sqs.test-sqs-{ENV}                        |


### Install the dependencies

```bash
make install
```

### Create Sample SQS events

To create an `event.json` file to be tested in this application, run:

```bash
make event
```

Note that this command runs `./scripts/create_test_event.py` considering that the camera `test` is up. In case it is down, you should add a valid camera to the global variables section in that script.

You can create testing `event.json` to test alternate flows such as:

* **Clip pending** (i.e. when the requested clip is within 15 minutes to the SQS message timestamp but it was not created yet):

```bash
python scripts/create_test_event.py -p
```

* **Clip not available** (i.e. when the requested clip is later than 15 minutes but within 3 days to the SQS message timestamp):

```bash
python scripts/create_test_event.py -n
```

* **Clip out of range** (i.e. when the requested clip is later than 3 days to the SQS message timestamp):

```bash

python scripts/create_test_event.py -o
```


### Running the App locally

```bash
make invoke
```



-----

# AWS Deploynment

### Running the App as a Lambda Function

This creates a `.zip` package and deploys it to the lambda function:

```bash
make deploy
```

Check whether the package has the expected content:

```bash
unzip -l dist/cameras-service-generate-clip.zip
```

Note that this adds FFMPEG's dependencies manually and the Python dependencies are built within a Dockerfile.

### Testing the flow in AWS

You can test this application flow in sandbox and/or staging environment following theses steps:

1. In the [SQS dashboard](https://console.aws.amazon.com/sqs/home?region=us-west-1), select SQS queue and click `Queue action -> Send a Message`.
2. Type the value for `body`, similarly as the a message created in `event.json`. For instance:

```
{'clipId': '111111111111','retryTimestamps': [],'cameraId': '111111111111','startTimestampInMs': 1538412898000,'endTimestampInMs': 1538413498000}
```

1. This should trigger the lambda function and you should see the clips and thumbnails in the environment's S3 bucket in around 20-40 seconds.

### Debugging Errors

Errors will be logged in [CloudWatch](https://us-west-1.console.aws.amazon.com/cloudwatch/home?region=us-west-1#logs:). To make sense of logs in the CLI, you should install [saw](https://github.com/TylerBrock/saw).

For instance, to check error logs for staging in the last hour:

```bash
saw get /aws/lambda/clip-function -1h --filter error
```

----

# Contributing 

### Committing new code

Run unit tests with:

```bash
make test
```

When deploying scripts (or to report back to Github on PRs), we ensure that code follows style guidelines with:

```bash
make lint
```

To fix lint errors, use:

```bash
make fixlint
```

Update the documentation (README.md) with:

```bash
make doctoc
```
