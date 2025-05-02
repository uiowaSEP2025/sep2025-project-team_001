import base64
import json

import requests
from django.conf import settings
from google.auth.transport.requests import Request
from google.oauth2 import service_account


def get_fcm_credentials():
    encoded = settings.FIREBASE_CREDENTIALS_JSON

    decoded = base64.b64decode(encoded).decode("utf-8")

    creds_dict = json.loads(decoded)
    return service_account.Credentials.from_service_account_info(
        creds_dict,
        scopes=['https://www.googleapis.com/auth/firebase.messaging']
    )


def send_fcm_httpv1(device_token, title, body, data=None):
    credentials = get_fcm_credentials()
    credentials.refresh(Request())

    access_token = credentials.token
    project_id = credentials.project_id

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json; UTF-8',
    }

    payload = {
        "message": {
            "token": device_token,
            "data": {
                "type": "ORDER_UPDATE",
                "order_id": data.get("order_id", ""),
                "title": title,
                "body": body
            }
        }
    }

    response = requests.post(
        f'https://fcm.googleapis.com/v1/projects/{project_id}/messages:send',
        headers=headers,
        json=payload
    )

    return response


def send_notification_to_device(device_token, title, body, data=None):
    credentials = get_fcm_credentials()
    credentials.refresh(Request())
    access_token = credentials.token
    project_id = credentials.project_id

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json; UTF-8',
    }

    payload = {
        "message": {
            "token": device_token,
            "notification": {
                "title": title,
                "body": body,
            },
            "data": data or {}
        }
    }

    response = requests.post(
        f'https://fcm.googleapis.com/v1/projects/{project_id}/messages:send',
        headers=headers,
        json=payload
    )
    return response
