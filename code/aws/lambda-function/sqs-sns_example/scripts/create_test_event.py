#!/usr/bin/env python2
#
# For integration tests, different SQS events are needed.
# This script generates events for alternate flows.
# Global variables are defined in main().

import time
import json
import argparse
import datetime
import calendar
import datetime


def time_to_epoch(timestamp, timestamp_format):
    """
        Given a timestamp string in seconds, return
        the epoch timestamp string, in milliseconds.
    """
    date = time.strptime(str(timestamp), timestamp_format)
    return str(calendar.timegm(date)) + '000'


def generate_delta_time(delta, timestamp_format, now, days):
    """
        Given a clip duration delta, and how many days back
        from today, return a begin and end timestamp for the event.
    """
    end = now - datetime.timedelta(days=days, minutes=0)
    begin = now - datetime.timedelta(days=days, minutes=delta)
    return begin.strftime(timestamp_format), end.strftime(timestamp_format)


def get_current_local_time(timestamp):
    """
        Return the current time in a datetime object, a
        human-readable string, and an epoch time integer.
    """
    now = datetime.datetime.now()
    human_now = now.strftime(timestamp)
    epoch_now = time_to_epoch(human_now, timestamp)
    return now, human_now, epoch_now


def create_event(begin, end, event_file, cam_id, epoch_now):
    """
        Create an event.json SQS message file for
        tests with the new timestamps and save it to the
        destination in event_file.
    """
    data = {'Records': [
        {
            "md5OfBody": "XXXXXXXXXXXXXXXXXXX",
            "receiptHandle": "XXXXXXXXXXXXXXXXXXX",
            "body": ("{'clipId': '1111111111111111',"
                     "'retryTimestamps': [],"
                     "'cameraId': '" + str(cam_id) + "',"
                     "'startTimestampInMs': '" + str(begin) + "',"
                     "'endTimestampInMs': '" + str(end) + "'}"),
            "eventSourceARN": "XXXXXXXXXXXXXXXXXXX",
            "eventSource": "aws:sqs",
            "awsRegion": "us-west-1",
            "messageId": "XXXXXXXXXXXXXXXXXXX",
            "attributes": {
                "ApproximateFirstReceiveTimestamp": "XXXXXXXXXXXXXXXXXXX",
                "SenderId": "XXXXXXXXXXXXXXXXXXX",
                "ApproximateReceiveCount": "1",
                "SentTimestamp": epoch_now
            },
            "messageAttributes": {}
        }
    ]
    }

    with open(event_file, 'w') as f:
        json.dump(data, f, separators=(',', ': '), sort_keys=True, indent=2)

    return data['Records'][0]['body']


def main():

    # Global variables.
    EVENT_FILE = 'event.json'
    TIMESTAMP_FORMAT = '%d-%m-%Y %H:%M:%S'
    DAYS_BEFORE_PENDING = 0
    DAYS_BEFORE_AVAILABLE = 0
    DAYS_BEFORE_NOT_AVAILABLE = 2
    DAYS_BEFORE_OUT_OF_RANGE = 8

    # Camera IDs used for tests, they should be checked whether
    # they are currently down or not. For instance:
    CAM_DOWN = '1111111111111111'
    CAM_UP = '1111111111111111'

    # This should not be more than 5 minutes (or the rewind clip generator
    # app won't accent the event).
    SESSION_DURATION_OK = 3
    SESSION_DURATION_CLIP_TO_LONG = 8

    # Get the time of event to be generated.
    parser = argparse.ArgumentParser(
        description='Clip duration you are looking for (in mins):')
    parser.add_argument('-a', '--clip_available',
                        action='store_true', help='Event for <15 min')
    parser.add_argument('-p', '--clip_pending',
                        action='store_true', help='Event cam down <15 min')
    parser.add_argument('-o', '--clip_out_of_range',
                        action='store_true', help='Event for >3 days')
    parser.add_argument('-n', '--clip_not_available',
                        action='store_true', help='Event cam down >3 days')
    parser.add_argument('-t', '--clip_too_long',
                        action='store_true', help='Clips > 5 min')
    args = parser.parse_args()

    # Define what type of event we want.
    if args.clip_pending:
        days_before = DAYS_BEFORE_PENDING
        cam_id = CAM_DOWN
        session_duration = SESSION_DURATION_OK

    elif args.clip_out_of_range:
        days_before = DAYS_BEFORE_OUT_OF_RANGE
        cam_id = CAM_UP
        session_duration = SESSION_DURATION_OK

    elif args.clip_not_available:
        days_before = DAYS_BEFORE_NOT_AVAILABLE
        cam_id = CAM_DOWN
        session_duration = SESSION_DURATION_OK

    elif args.clip_too_long:
        days_before = DAYS_BEFORE_AVAILABLE
        cam_id = CAM_UP
        session_duration = SESSION_DURATION_CLIP_TO_LONG

    else:
        # Defaults to CLIP_AVAILABLE event.
        days_before = DAYS_BEFORE_AVAILABLE
        cam_id = CAM_UP
        session_duration = SESSION_DURATION_OK

    # Get current time in human string and epoch int.
    now, human_now, epoch_now = get_current_local_time(TIMESTAMP_FORMAT)

    # Generates a random begin and end time within the last days.
    begin, end = generate_delta_time(
        session_duration, TIMESTAMP_FORMAT, now, days_before)

    # Convert these times to epoch timestamp and human time.
    end_epoch = time_to_epoch(end, TIMESTAMP_FORMAT)
    begin_epoch = time_to_epoch(begin, TIMESTAMP_FORMAT)

    if begin_epoch and end_epoch:

        # Creates the JSON file for the event.
        body = create_event(begin_epoch, end_epoch,
                            EVENT_FILE, cam_id, epoch_now)

        print('-----------------------------------------------------')
        print('Event test saved at {}'.format(EVENT_FILE))
        print('Camera id is {}'.format(cam_id))
        print('Timestamp for {0} days ago, delta time is {1} mins').format(
            days_before, session_duration)
        print('Begin: {0} -> End: {1}'.format(begin_epoch, end_epoch))
        print('Begin: {0} -> End: {1}'.format(begin, end))
        print('Time:  {}'.format(human_now))
        print('Body: ')
        print(body)
        print('-----------------------------------------------------')

    else:
        print('Could not create timestamps for {}'.format(duration))


if __name__ == '__main__':
    main()
