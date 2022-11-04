import pytest
import re
import uuid
from time import sleep
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.ticket import create_ticket
import variables

def check_dashboard_widgets(page):
   # Dashboard is dynamic
   # The page loads with the default data
   # After the load the page constantly polls the server for new data
   # without sleep Open Tickets widget would be on the page with value '0'
   sleep(5)
   # Check that 'Open Tickets' widget shows number 3 (we have 3 tickets).
   assert page.locator('div.stat:has-text("Open Tickets") span.value').inner_text() == '3'

   # Check that 'Breaching SLA Soon' widget exist and shows 0
   assert page.locator('div.stat:has-text("Breaching SLA Soon") span.value').inner_text() == '0'

   assert page.locator('div.stat:has-text("Breached SLA") span.value').inner_text() == '0'

   assert page.locator('div.stat:has-text("Tickets Resolved Last MTD/This MTD") span.value').inner_text() == '0/0'

   assert page.locator('div.stat:has-text("Current Hours to Diagnose") span.value').inner_text() == '0'

   # Check that widget with text 'Hours to Close Last MTD/This MTD' has value '0'
   assert page.locator('div.stat:has-text("Hours to Close Last MTD/This MTD") span.value').inner_text() == '0/0'


def test_ticket_create_open_dashboard(page, login: login, api_request_context):

   customer_name = str(uuid.uuid4())
   customer_id, _  = create_customer(customer_name, api_request_context)
   _, new_ticket_number = create_ticket(customer_id, api_request_context, status = 'New')
   _, in_progress_ticket_number = create_ticket(customer_id, api_request_context, status = 'In Progress')
   _, waiting_on_customer_ticket_number = create_ticket(customer_id, api_request_context, status = 'Waiting on Customer')

   # To access the ticket dashboard head over to your "Tickets" tab
   page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets')

   # Select the drop down that says "View"
   page.click('form#ticket_search_form a:has-text("View")')

   # Check that "Open Dashboard" link exist in the "View menu"
   # Don't click on open dasboard link, because it opens in new page.
   assert page.locator('a:has-text("Open Ticket Dashboard")') != None

   # Go to the page open ticket dashboard
   page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets/dashboard')

   check_dashboard_widgets(page)

   # Find a string from a card with the ticket number that we created before
   ticket_card1 = page.locator(f'div.cardr:has-text("{new_ticket_number}")').inner_text()
   ticket_card2 = page.locator(f'div.cardr:has-text("{waiting_on_customer_ticket_number}")').inner_text()
   ticket_card3 = page.locator(f'div.cardr:has-text("{in_progress_ticket_number}")').inner_text()

   # Check that card with ticket number has ticket number that we created before has status 'New'
   assert "New" in ticket_card1

   # Check that card with ticket number has status 'Waiting on Customer'
   assert "Waiting on" in ticket_card2

   # Check that card with ticket number has status 'In Progress'
   assert "In Progress" in ticket_card3

   page.click('a:has-text("Manage Dashboard Share Links")')

   # Button 'Create a new Dashboard Share Link' should exist
   page.click('a.bhv-createShareLink')

   # Check that new Share Link exist
   alert_body = page.locator('div.alert:has-text("New Share Link is: https://")')
   assert  alert_body != None
   share_link = re.search('http.*', alert_body.inner_text()).group()

   # Open Dashboard looks the same as Dashboard but they are server by different controllers
   page.goto(share_link)
   check_dashboard_widgets(page)