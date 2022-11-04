import datetime
from datetime import timedelta
import enum
from time import sleep
import time
import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.ticket import create_ticket
from playwright.sync_api import expect
import variables

global_filestack_upload_finished = False
global_syncro_upload_finished = False

def wait_for_filestack_upload(request):
    global global_filestack_upload_finished
    if 'complete' in request.url:
        global_filestack_upload_finished = True

def wait_for_syncro_upload(dialog):
    global global_syncro_upload_finished
    dialog.accept()
    global_syncro_upload_finished = True

def test_ticket_validate_new_reminder(page, login, api_request_context):
    customer_name = str(uuid.uuid4())
    customer_id, email = create_customer(customer_name, api_request_context)

    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/customers/{customer_id}')
    page.wait_for_timeout(100)
    page.click('div[class="col-md-6 btn-bar title-btns by-right"] > div:first-child > a[class="btn btn-default btn-sm dropdown-toggle"]')
    page.click('div[class="col-md-6 btn-bar title-btns by-right"] > div:first-child a:has-text("Attachment")')

    time.sleep(1)

    # Upload test_ticket_attachment.py file
    page.set_input_files('input#fsp-fileUpload', __file__)

    # Register async upload handler
    page.on("requestfinished", wait_for_filestack_upload)
    page.on("dialog", wait_for_syncro_upload)

    # We need to wait for the upload to Filestack to finish
    # Wait and check the global flag for finished upload
    for i in range(1, 20) :
        if global_filestack_upload_finished:
            break
        page.wait_for_timeout(2000)

    page.click('div.fsp-footer span[title="Upload"]')

    # page.on('dialog', lambda dialog: dialog.accept())

    sleep(5)

    expect(page.locator('.attachment-title')).to_contain_text('test_customer_attachme...')
