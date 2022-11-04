import pytest
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer_purchase import create_customer_purchase, set_customer_purchase_status, add_manual_item_to_customer_purchase
from helpers.customer import Customer
from playwright.sync_api import expect
import uuid
import variables

@pytest.mark.regression
def test_customer_purchase_refurb(page, login, api_request_context):

    # Preconditions: create 2 customers and 2 customer purchases for search
    customer = Customer(business_name = 'Jack' + str(uuid.uuid4())[1:10], last_name = 'Smith')
    customer.create(api_request_context)
    customer_purchase_id = create_customer_purchase(page, customer.business_name)

    # Set Customer Purchase Status
    set_customer_purchase_status(page, 'Paid')

    # Add Item to the Purchase (Manual New Inventory Item)
    add_manual_item_to_customer_purchase(page)

    # If you entered the product in the Manual New Inventory Item fields on the right
    # because it did not exist in your inventory, do the following.
    page.wait_for_timeout(2000)
    page.click('input:has-text("Add Product")')
    assert page.wait_for_selector('text="We created that product, click the link on the line item to view/modify it"')

    # Click Start Refurb
    # The Status will change to "Waiting on Refurb"
    page.click('a:has-text("Start Refurb")')

    # Enter the Issue—what needs to be fixed before selling it
    page.fill('input#refurb_issue', 'Laptop')

    #Click Send to Refurb
    page.click('text="Send to Refurb"')

    page.fill('input#refurb_line_item_name', 'Labor')
    page.fill('textarea#refurb_line_item_description', 'Clean Up')
    page.click('text="Use Item in Refurb"')

    # Click the big green Complete - Move to Stock button to add your new item to inventory
    page.on("dialog", lambda dialog: dialog.accept())
    page.click('text="Complete - Move to Stock"')

    page.click('td > a:has-text("Acer")') # Go to the product page
    # See the serial with the link to the customer purchase
    expect(page.locator(f'a[href="/customer_purchases/{customer_purchase_id}"]')).to_contain_text(str(customer_purchase_id))

    # Check that the customer purchase is completed
    page.goto(f'{variables.base_url}/customer_purchases/{customer_purchase_id}')
    expect(page.locator('span[data-bip-attribute="status"]')).to_contain_text('Completed')
