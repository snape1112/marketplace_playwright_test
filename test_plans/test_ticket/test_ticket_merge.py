import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.ticket import create_ticket
from playwright.sync_api import expect
import variables

def test_ticket_merge_via_dropdown(page, login, api_request_context):
    # Merge ticket using "Destination Ticket" dropdown.

    # Prerequisites
    customer_name = str(uuid.uuid4()) 
    customer_id, _  = create_customer(customer_name, api_request_context)
    ticket_id_1, ticket_num_1 = create_ticket(customer_id, api_request_context)
    ticket_id_2, ticket_num_2 = create_ticket(customer_id, api_request_context)
    ticket_id_2_url = f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets/{ticket_id_2}'
    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets/{ticket_id_1}')
    assert page.locator(f'text={ticket_num_1}') != None
    
    # The merge part
    page.click('text=Actions')
    page.click('text=Merge')
    page.select_option('#merge_destination_ticket_id', value=f'{str(ticket_id_2)}')
    page.click('text="Merge Tickets"')

    # The verification part
    assert page.locator('text="Merge complete!!"') != None
    assert page.url == ticket_id_2_url
    assert page.locator('body').inner_html().find(str(ticket_num_1)) == -1
    assert page.locator('body').inner_html().find(str(ticket_num_2)) > -1
 

def test_ticket_merge_via_entry(page, login,api_request_context):
    # Merge ticket using "Destination ticket number" manual entry field.

    # Prerequisites
    customer_name = str(uuid.uuid4()) 
    customer_id, _  = create_customer(customer_name, api_request_context)
    ticket_id_1, ticket_num_1 = create_ticket(customer_id, api_request_context)
    ticket_id_2, ticket_num_2 = create_ticket(customer_id, api_request_context)
    ticket_id_2_url = f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets/{ticket_id_2}'
    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets/{ticket_id_1}')
    assert page.locator(f'text={ticket_num_1}') != None
    
    # The merge part
    page.click('text=Actions')
    page.click('text=Merge')
    page.click('a[class="ticket-by-number"]')
    page.fill('#merge_destination_ticket_number', str(ticket_num_2))
    page.click('text="Merge Tickets"')

    # The verification part
    assert page.locator('text="Merge complete!!"') != None
    assert page.url == ticket_id_2_url
    assert page.locator('body').inner_html().find(str(ticket_num_1)) == -1
    assert page.locator('body').inner_html().find(str(ticket_num_2)) > -1