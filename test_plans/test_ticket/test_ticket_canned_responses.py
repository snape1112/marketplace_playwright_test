import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.ticket import create_ticket
from time import sleep
import variables

@pytest.mark.regression

def create_canned_responses(page, title, body):
        # Go to More > Admin > Tickets > Canned Responses
        page.click('span:has-text("More")')
        page.locator('ul[role="menu"] a:has-text("Admin")').click()
        page.click('text=Canned Responses')
        assert "Canned Responses" in page.locator('div.col-xs-12 span.customer-title').inner_text()

        # Add new Canned Response by clicking on the
        # green 'New Canned Response' button in the top right
        page.click('a.btn-sm:has-text("New Canned Response")')
        sleep(2)
        # To modify the 'Title' and 'Body' field click on it once to free it up for editing
        page.click('span[data-bip-attribute="title"]')
        page.fill('form.form_in_place input[name="title"]', title)
        # Click "Save"
        page.click('form.form_in_place input[value="Save"]')
        page.click('span[data-bip-attribute="body"]')
        page.fill('form.form_in_place textarea[name="body"]', body)
        # Click "Save"
        page.click('form.form_in_place input[value="Save"]')
        sleep(2)

def test_ticket_canned_responses(page, login, api_request_context):
        # Create a new Customer
        customer_name = str(uuid.uuid4())
        customer_id, _ = create_customer(customer_name, api_request_context)
        title1 = 'Will Reply 1'
        body1 = 'Hi! We will respond as soon as possible. Thanks!'

        title2 = 'Completed'
        body2 = 'Hey there - Your computer is all set.'
        # Create first canned response
        create_canned_responses(page, title1, body1)

        # Create second canned response
        create_canned_responses(page, title2, body2)

        #test1
        # You can access your Canned Responses from the New Ticket Creation screen
        # Create a new ticket
        page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets/start')
        page.click('#ticket_customer_name')
        page.type('#ticket_customer_name', customer_name)
        page.click(f'text=/{customer_name}.*/')
        page.click('text=Create Ticket')

        page.fill('#ticket_subject', 'Ticket with canned response')
        page.select_option('#ticket_problem_type', 'Remote Support')
        sleep(2)
        # Click the blue icon next to the "Complete Issue Description" field:
        page.click('a.btn-xs[href="#canny"]')

        # Verify that we get a pop-up box with "Insert Canned Response"
        assert page.locator('div.modal-header:has-text("Insert Canned Response")').inner_text() != None

        # Click insert button next to response to add it to the New Ticket Comment box
        page.click(f'text=Default {title1} {body1} Insert >> a')
        page.click('text=Create Ticket')

        # Verify that ticket  page has ticket description from the first Canned Response
        assert page.locator(f'p:has-text("{body1}")').inner_text() == 'Hi! We will respond as soon as possible. Thanks!'

        # Test2
        # You can access your Canned Responses right from a ticket
        # scroll down to the New Ticket Comment box to get to the "Canned Responses" button shown here:
        page.click('form#new_comment a[data-original-title="Canned Responses"]')

        # Click insert button next to response to add second canned response
        page.click(f'text=Default {title2} {body2} Insert >> a')

        # Click on 'Email' button to add new comment with canned response'
        page.click('form#new_comment a.bhv-submitComment')

        # Verify that page has ticket description from the second Canned Response
        assert page.locator(f'p:has-text("{body2}")').inner_text() == 'Hey there - Your computer is all set.'

