# -*- coding: utf-8 -*-
""" AWS Wrapper Test Module """

import unittest
import mock

import lib.aws_wrapper


class TestAwsWrapper(unittest.TestCase):

    def setUp(self):
        self.filename = 'filename_test'
        self.destination = 'destination_test'
        self.clip_metadata = {'test': 'test'}
        self.aw = lib.aws_wrapper.AwsWrapper()

    @mock.patch('lib.aws_wrapper.boto3')
    def test_download_clip_boto(self, boto3):
        self.aw.download_video(self.filename, self.destination)
        boto3.resource.assert_called_with('s3')

    @mock.patch('lib.aws_wrapper.boto3')
    def test_upload_clip_boto(self, boto3):
        self.aw.upload_asset(self.filename, self.destination)
        boto3.client.assert_called_with('s3')

    @mock.patch('lib.aws_wrapper.boto3')
    def test_send_sns_msg_boto(self, boto3):
        aw = lib.aws_wrapper.AwsWrapper()
        aw.send_sns_msg(self.clip_metadata)
        boto3.client.assert_called_with('sns')
