import platform
import sys

import pytest

from flexget.api.app import base_message
from flexget.api.core.user import ObjectsContainer as OC
from flexget.utils import json


class TestUserAPI:
    config = 'tasks: {}'

    @pytest.mark.skipif(
        sys.version_info < (3, 9, 13) and platform.system() == 'Darwin',
        reason='After Python 3.9 support is dropped, this can be removed.',
    )
    def test_change_password(self, execute_task, api_client, schema_match):
        weak_password = {'password': 'weak'}
        medium_password = {'password': 'a.better.password'}
        strong_password = {'password': 'AVer123y$ron__g-=PaW[]rd'}

        rsp = api_client.json_put('/user/', data=json.dumps(weak_password))
        assert rsp.status_code == 400
        data = json.loads(rsp.get_data(as_text=True))

        errors = schema_match(base_message, data)
        assert not errors

        rsp = api_client.json_put('/user/', data=json.dumps(medium_password))
        assert rsp.status_code == 200
        data = json.loads(rsp.get_data(as_text=True))

        errors = schema_match(base_message, data)
        assert not errors

        rsp = api_client.json_put('/user/', data=json.dumps(strong_password))
        assert rsp.status_code == 200
        data = json.loads(rsp.get_data(as_text=True))

        errors = schema_match(base_message, data)
        assert not errors

    def test_change_token(self, execute_task, api_client, schema_match):
        rsp = api_client.json_put('user/token/')
        assert rsp.status_code == 200
        data = json.loads(rsp.get_data(as_text=True))

        errors = schema_match(OC.user_token_response, data)
        assert not errors
