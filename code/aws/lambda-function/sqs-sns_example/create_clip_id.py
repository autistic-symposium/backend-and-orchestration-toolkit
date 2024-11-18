#!/usr/bin/env python2
#
# Create a clipId to be used in event.json

import requests
import subprocess
import json
import time


def put_request(url, data):
    """
        Send the PUT request to create the id, returning
        the clipId string.
    """

    r = requests.post(url, json=data)
    print('--------------------------------------------------------')
    print('Request to {}'.format(url))
    print('Data sent: {}'.format(data))
    print('Status code: {}'.format(r.status_code))

    if r.status_code == 200:
        print(r.json())
        return r.json()['clipId']

    else:
        return False


def create_timestamps():
    """
        Create a timestamp to send in the PUT request.
    """
    now = int(time.time()*1000)
    sent_ts = str(now)
    begin_ts = str(now - 600000)
    end_ts = str(now - 600000 + 180000)

    return sent_ts, begin_ts, end_ts


def create_data(cam_id, url, begin_ts, end_ts):
    """
        Create the data that need to be sent to the
        PUT request.
    """
    data = {
        "cameraId": cam_id,
        "startTimestampInMs": begin_ts,
        "endTimestampInMs": end_ts
    }

    return data


def main(url, cam_id):

    sent_ts, begin_ts, end_ts = create_timestamps()
    data = create_data(cam_id, url, begin_ts, end_ts)
    clip_id = put_request(url, data)

    print('clipId to be added to event.json: {}'.format(clip_id))
    print('send ts, start, end: {0}     {1}     {2}'.format(
        sent_ts, begin_ts, end_ts))

