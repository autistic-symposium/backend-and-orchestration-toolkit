# -*- coding: utf-8 -*-
""" Utils Test Module """

import os
import json
import pytest
import unittest

import mock
import requests
import requests_mock
import lib.utils


fixtures_path = os.path.join(os.path.dirname(__file__), 'fixtures')


@pytest.fixture
def get_fixture(fixture_json):
    get_sqs_event = os.path.join(fixtures_path, fixture_json)
    with open(get_sqs_event, 'r') as f:
        return json.load(f)


class TestClipGeneratorTrigger(unittest.TestCase):

    def setUp(self):
        self.domain = 'http://test.com'
        self.endpoint = 'filetest.mp4'
        self.file_url = 'http://test.com/filetest.mp4'
        self.clipname = 'camtest.20180815T140019.mp4'
        self.epoch_in_ms = 1535224400000
        self.timestamp = '20180825T191320'
        self.timestamp_format = '%Y%m%dT%H%M%S'
        self.msecs = 1807
        self.resp = {'test1': 'test2'}

    def test_url_join(self):
        self.assertEqual('http://test.com/filetest.mp4',
                         lib.utils.url_join(self.domain,
                                            self.endpoint), msg=None)

    def test_get_request(self):
        with requests_mock.Mocker() as m:
            m.get(self.file_url, json=self.resp)
            self.assertTrue(lib.utils.get_request(self.domain, self.endpoint))

    def test_get_basename_str(self):
        self.assertEqual('filetest.mp4', lib.utils.get_basename_str(
            self.file_url), msg=None)

    def test_get_timestamp_str(self):
        self.assertEqual('20180815T140019000',
                         lib.utils.get_timestamp_str(self.clipname), msg=None)

    def test_get_location_str(self):
        self.assertEqual('hbpiernscam', lib.utils.get_location_str(
            self.clipname), msg=None)

    def test_timestamp_to_epoch(self):
        self.assertEqual(self.epoch_in_ms, lib.utils.timestamp_to_epoch(
            self.timestamp, self.timestamp_format), msg=None)

    def test_epoch_to_timestamp(self):
        self.assertEqual(self.timestamp, lib.utils.epoch_to_timestamp(
            self.epoch_in_ms, self.timestamp_format), msg=None)

    def test_humanize_delta_time(self):
        self.assertEqual(
            '00:01.807', lib.utils.humanize_delta_time(self.msecs), msg=None)

    @mock.patch('lib.utils.os.remove')
    def test_remove_file(self, mocked_remove):
        lib.utils.remove_file(self.clipname)
        self.assertTrue(mocked_remove.called)

    @mock.patch('lib.utils.subprocess.check_output')
    def test_run_subprocess(self, mocked_subprocess):
        lib.utils.run_subprocess(['ls'], 'ok', 'err')
        self.assertTrue(mocked_subprocess.called)
