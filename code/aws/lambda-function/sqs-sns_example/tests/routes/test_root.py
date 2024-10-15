# -*- coding: utf-8 -*-
""" Test Root service handler module for AWS Lambda function. """

import os
import json
import pytest

from lib.routes import root

fixtures_path = os.path.join(os.path.dirname(__file__), '..', 'fixtures')


@pytest.fixture
def sns_event_record():
    sns_event_record_path = os.path.join(fixtures_path, 'SNS_contract.json')
    with open(sns_event_record_path, 'r') as sns_event_record_json:
        return json.load(sns_event_record_json)


@pytest.fixture
def context():
    return {}


class TestHandler():
    def test_type_error_for_bad_params(self, context):
        try:
            root.handler('', context)
        except TypeError as e:
            pass
        else:
            self.fail('ExpectedException not raised')
