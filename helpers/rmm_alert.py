import pytest
import uuid
import re
import json
import requests
import types
from playwright.sync_api import Page
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.api_token import generate_api_token
from helpers.customer import create_customer
from helpers.ticket import create_ticket
from helpers.asset import create_asset
import variables

def create_rmm_alert(customer_id, asset_id, api_request_context):
    """
        Creates new RMM alert
        Arguments:
            customer_id
            asset_id
        Returns:
            Creates the new rmm_alert
    """
    # Api POST call to rmm alerts
    response = api_request_context.post(
        f'https://{variables.subdomain}.{BASE_DOMAIN}/api/v1/rmm_alerts',
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": variables.token,
        },
    data={
    "customer_id": customer_id,
    "asset_id": asset_id,
    "description": "New RMM Alert test description",
    "status": "string",
    "properties": {
    "subject": "New test asset subject",
    "body": "string",
    "hidden": 1,
    "sms_body": "string",
    "do_not_email": 1,
    "tech": "string"
    }
    }
    )
    # Asserting that response is 200 and returning id
    assert response.ok
    rmm_alert_id = response.json()['alert']['id']
    return rmm_alert_id
