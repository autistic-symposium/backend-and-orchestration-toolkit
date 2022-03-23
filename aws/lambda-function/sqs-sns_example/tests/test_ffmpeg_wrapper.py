# -*- coding: utf-8 -*-
""" Ffmpeg Wrapper Test Module """

import lib.ffmpeg_wrapper
import unittest


class TestFfmpegWrapper(unittest.TestCase):

    def setUp(self):
        self.epoch_video = 1.535884819e+12
        self.crop_start = '03:39.000'
        self.crop_end = '13:01.000'

        self.session_start_ms = '1535884600000'
        self.session_end_ms = '1535885600000'
        self.alias = 'test'
        self.clipId = '1111111111111111'
        self.clips = []
        self.fw = lib.ffmpeg_wrapper.FfmpegWrapper(
            self.alias, self.clips,
            self.session_start_ms,
            self.session_end_ms,
            self.clipId)

    def test_calculate_crop_time(self):
        crop_start, crop_end = self.fw.calculate_trim_time(self.epoch_video)
        print crop_start, crop_end, self.crop_end, self.crop_start
        self.assertEqual(crop_end, self.crop_end)
        self.assertEqual(crop_start, self.crop_start)
