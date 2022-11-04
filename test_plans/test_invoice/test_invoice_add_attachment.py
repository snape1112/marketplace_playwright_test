
from venv import create
import pytest
import uuid
import pytest
from fixtures.constants import *
from playwright.sync_api import Page
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.invoice import create_new_invoice
import variables

def handle_dialog(dialog):
    print(dialog.message)
    dialog.dismiss()

@pytest.mark.regression
def test_invoice_add_attachment(page:Page, login, api_request_context):

    # Pre-condition

    customer_name = str(uuid.uuid4()) 
    create_customer(customer_name, api_request_context)
    create_new_invoice(page, customer_name)
    page.on("dialog", handle_dialog)

    # Upload file

    page.click('text=actions')
    page.click('text=add attachment')
    page.click(".fsp-source-list__icon.fsp-icon.fsp-icon--url")
    page.fill('[placeholder=\"Enter\\ a\\ URL\"]','https://syncromsp.com/')
    page.click('[id=\"__filestack-picker\"] button')
    page.click("text=Upload 1")

    # Validate a new entry was added

    assert page.locator('//*[text()="attachments"]/parent::span/parent::div/following-sibling::div//a') != None
 
    
