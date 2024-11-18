# -*- coding: utf-8 -*-
""" Cam Wrapper Test Module """

import mock
import unittest
import pytest

import lib.cam_wrapper
import lib.utils


class TestCamWrapper(unittest.TestCase):

    def setUp(self):
        self.session_start_ms = '1535223360000'
        self.session_end_ms = '1535224400000'
        self.cameraId = '1111111111111111'
        self.clipId = '1111111111111111'

        self.metadata_test_clip_key = '/{0}/{1}.mp4'.format(
            self.cameraId, self.clipId)
        self.metadata_test_tb_key = '/{0}/{1}'.format(
            self.cameraId, self.clipId) + '_{size}.jpg'
        self.cw = lib.cam_wrapper.CamWrapper(
            self.session_start_ms, self.session_end_ms,
            self.cameraId, self.clipId)

    @mock.patch('lib.utils.get_request')
    def test_get_alias(self, mocked_method):
        self.cw .get_alias()
        self.assertTrue(mocked_method.called)

    def test_metadata(self):
        self.assertEqual(
            self.cw .metadata['clip']['key'], self.metadata_test_clip_key)
        self.assertEqual(
            self.cw .metadata['thumbnail']['key'], self.metadata_test_tb_key)

    @mock.patch('lib.utils.get_request')
    def test_get_clip_names(self, mocked_method):
        alias = self.cw .get_clip_names()
        self.assertTrue(mocked_method.called)

    @mock.patch('lib.utils.put_request')
    def test_put_clip_metadata(self, mocked_method):
        alias = self.cw .put_clip_metadata()
        self.assertTrue(mocked_method.called)

    def test_update_clip_status(self):
        test_status = 'test'
        self.cw.update_clip_status(test_status)
        self.assertEqual(self.cw.metadata['status'], test_status)
