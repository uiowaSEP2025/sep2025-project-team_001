import base64
import json

import requests
from app.mobileViews import utils
from django.conf import settings


def test_get_fcm_credentials_decodes_and_constructs(monkeypatch):
    # Prepare a fake credentials dict
    creds_dict = {"project_id": "proj_123", "client_email": "test@example.com"}
    encoded = base64.b64encode(json.dumps(creds_dict).encode()).decode()
    monkeypatch.setattr(settings, 'FIREBASE_CREDENTIALS_JSON', encoded)

    # Capture the input dict passed to from_service_account_info
    captured = {}

    def fake_from_info(info, scopes):
        captured['info'] = info
        captured['scopes'] = scopes
        return 'fake_credentials'

    monkeypatch.setattr(utils.service_account.Credentials, 'from_service_account_info', fake_from_info)

    creds = utils.get_fcm_credentials()
    assert creds == 'fake_credentials'
    assert captured['info'] == creds_dict
    assert 'firebase.messaging' in captured['scopes'][0]


def test_send_fcm_httpv1_posts_correct_payload(monkeypatch):
    # Prepare fake credentials
    class DummyCreds:
        def __init__(self):
            self.token = 'tok_abc'
            self.project_id = 'proj_456'

        def refresh(self, transport):
            pass

    monkeypatch.setattr(utils, 'get_fcm_credentials', lambda: DummyCreds())

    # Monkeypatch requests.post
    calls = {}

    def fake_post(url, headers=None, json=None):
        calls['url'] = url
        calls['headers'] = headers
        calls['json'] = json

        class Resp:
            status_code = 202

            def json(self_inner):
                return {'result': 'ok'}

        return Resp()

    monkeypatch.setattr(requests, 'post', fake_post)

    resp = utils.send_fcm_httpv1('device123', 'Title', 'Body', data={'order_id': '42'})
    assert resp.status_code == 202
    assert resp.json() == {'result': 'ok'}

    # Check URL and headers
    assert calls['url'] == 'https://fcm.googleapis.com/v1/projects/proj_456/messages:send'
    assert 'Authorization' in calls['headers'] and 'Bearer tok_abc' in calls['headers']['Authorization']
    # Verify payload structure
    assert calls['json']['message']['token'] == 'device123'
    data_field = calls['json']['message']['data']
    assert data_field['type'] == 'ORDER_UPDATE'
    assert data_field['order_id'] == '42'
    assert data_field['title'] == 'Title'
    assert data_field['body'] == 'Body'


def test_send_notification_to_device_posts_notification(monkeypatch):
    class DummyCreds:
        def __init__(self):
            self.token = 'tok_xyz'
            self.project_id = 'proj_789'

        def refresh(self, transport):
            pass

    monkeypatch.setattr(utils, 'get_fcm_credentials', lambda: DummyCreds())

    calls = {}

    def fake_post(url, headers=None, json=None):
        calls['url'] = url
        calls['headers'] = headers
        calls['json'] = json

        class Resp:
            status_code = 200

            def json(self_inner):
                return {'delivered': True}

        return Resp()

    monkeypatch.setattr(requests, 'post', fake_post)

    resp = utils.send_notification_to_device('dev456', 'Notif', 'Hello', data={'key': 'val'})
    assert resp.status_code == 200
    assert resp.json() == {'delivered': True}

    assert calls['url'] == 'https://fcm.googleapis.com/v1/projects/proj_789/messages:send'
    payload = calls['json']['message']
    assert payload['token'] == 'dev456'
    assert 'notification' in payload and payload['notification']['title'] == 'Notif'
    assert payload['data'] == {'key': 'val'}
