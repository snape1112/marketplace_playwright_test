import pytest
import re
import uuid
from uuid import uuid4
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from playwright.sync_api import Page, expect
from helpers.api_token import generate_api_token
from datetime import date
from time import sleep
import variables

def create_ticket(customer_id, api_request_context, **kwargs):

    status = kwargs.get('status') or 'New'
    problem_type = kwargs.get('problem_type') or 'Remote Support'
    subject = kwargs.get('subject') or 'Printer not working'

    #API call to create an asset
    response = api_request_context.post(
        f'{variables.base_url}/api/v1/tickets',
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": variables.token,
        },
        data={
        "customer_id": customer_id,
        "subject": subject,
        "problem_type": problem_type,
        "status": status,
        "properties": {},
        "asset_ids": [

        ],
        "signature_name": "string",
        "signature_data": "string",
        "sla_id": 0,
        "contact_id": 0,
        "priority": "string",
        "outtake_form_data": "string",
        "outtake_form_date": "2022-05-11T19:07:37.531Z",
        "outtake_form_name": "string",
        "comments_attributes": [
            {
            "subject": subject,
            "body": "Please fix my printer",
            "hidden": False,
            "sms_body": "Please fix my printer",
            "do_not_email": True,
            "tech": "string"
            }
        ]
        }
    )
    assert response.ok
    json = response.json()
    ticket_id = json['ticket']['id']
    ticket_number = json['ticket']['number']


    add_comment_to_ticket(ticket_id, api_request_context, "Remote Support", "Please fix my printer")

    return ticket_id, ticket_number


def add_comment_to_ticket(ticket_id, api_request_context, subject, body):


    response = api_request_context.post(
        f'{variables.base_url}/api/v1/tickets/{ticket_id}/comment',
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": variables.token,
        },
        data={

            "subject": subject,
           # "tech": "string",
            "body": body,
            "hidden": False,
            "sms_body": "string",
            "do_not_email": True
        }

    )
    assert response.ok



# def create_ticket(page : Page, customer_name : str, **kwargs) -> str:
#     """
#     Creates a new ticket
#         Arguments:
#             page: a Page
#             customer_name: a string
#         Returns:
#             Creates the new ticket for the customer and returns the database id
#     """
#     page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets/start')
#     page.click('#ticket_customer_name')
#     page.type('#ticket_customer_name', customer_name)
#     page.click(f'text=/{customer_name}.*/')
#     page.click('text=Create Ticket')
#     page.fill('#ticket_subject', 'Printer not working')
#     page.select_option('#ticket_problem_type', 'Remote Support')
#     page.fill('#ticket_comments_attributes_0_body','Please fix my printer')
#     page.click('#ticket_notify_emails_tagsinput')
#     page.click('text=Create Ticket')
#     page.wait_for_selector('text="New"') != None
#     ticket_id_result = re.search(r".*tickets/(\d+)",  page.url)
#     ticket_id = ticket_id_result.group(1)
#     parsed_ticket_num = re.search(r'.*Ticket #(\d+)', page.content())
#     ticket_num = parsed_ticket_num.group(1)
#     #if status != "New":
#     if kwargs.get('status'):
#         sleep(2)
#         page.click('span[data-bip-attribute="status"]')
#         page.select_option('form.form_in_place select', kwargs['status'])
#     return ticket_id, ticket_num

# def create_tickets(page, customer_name, statuses):
#     for status in statuses:
#         create_ticket(page, customer_name, status)

def create_parts_status_entry(page: Page, ticket_id : str) -> str:
    """
    Creates a new parts entry tied to the provided ticket and is added to the 'Add/View Charges' line items on the ticket.
        Arguments:
            page: a Page
            ticket_id: a string
        Returns:
            ticket_num: The visible number of the ticket
            item_id: The ID of the part entry
    """
    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets/{ticket_id}')
    parsed_ticket_num = re.search(r'.*Ticket #(\d+)', page.content())
    ticket_num = parsed_ticket_num.group(1)
    page.click('text=Actions')
    page.click('text=Parts Status')
    assert page.locator('text="Part Order List"') != None
    page.click('text=New Item')
    page.click('#item_ticket_id_chosen')
    page.type('#item_ticket_id_chosen', ticket_num)
    page.keyboard.press("Enter")
    page.fill('#item_description', 'Random Part for Customer')
    page.fill('#item_parturl', 'https://google.com')
    #page.click('#item_quantity')
    page.fill('#item_quantity', '2')
    #page.click('#item_price')
    page.fill('#item_price', '10.00')
    #page.click('#item_price_retail')
    page.fill('#item_price_retail', '100.00')
    page.fill('#item_shipping', 'Shipping Field')
    page.fill('#item_trackingnum', '1Z2345678901234567890')
    page.fill('#item_notes', 'Notes relating to this part order should go here.')
    page.fill(f'#demo1', date.today().strftime("%d/%m/%Y"))
    page.click('text=Create Item')
    assert page.locator('text="Item was successfully created."') != None
    # Since the newly created item is first in the table, we can reliably grab the ID of the entry in the first row.
    rough_item_id = page.locator('//*[text()="ID"]/parent::tr/parent::thead/following-sibling::tbody/child::tr/child::td/child::a/child::span').first.inner_text()
    # [1:] grabs the value from 1 character from the left.  Orig Text: "&nbsp33" = '\xa033' so '\xa0' = &nbsp in HEX which counts as one character.
    item_id = rough_item_id[1:]
    return ticket_num, item_id


def create_workflow(page : Page, workflow_name : str) -> str:
    """
    Creates a new workflow
        Arguments:
            page: a Page
            workflow_name: a string
        Returns:
            Creates the new workflow and returns the database id
    """
    page.click('a[role="button"]:has-text("More")')
    page.click('ul[role="menu"] >> text=Admin')
    page.click('text=Workflows')
    page.click("text=New Workflow")
    page.fill('input[name="new_ticket_form[name]"]',workflow_name)
    page.fill('input[name="customer_details-firstname"]','Test First')
    page.locator('input[name="customer_details- firstname"]').nth(1).check()
    page.fill('input[name="customer_details-lastname"]','Test Last')
    page.click('input[name="ticket_details-subject"]')
    page.fill('input[name="ticket_details-subject"]','Test Ticket Subject')
    with page.expect_navigation():
        page.click("text=Save Workflow")
    parsed_workflow_id = re.search(r'(?<=new_ticket_forms\/)(\d+)/edit', page.url)
    return parsed_workflow_id.group(1)

def create_custom_field(page : Page, custom_field_name : str) -> str:
    """
    Creates a new custom field
        Arguments:
            page: a Page
            custom_field_name: a string
        Returns:
            Creates the new custom field
    """
    page.click('a[role="button"]:has-text("More")')
    page.click('ul[role="menu"] >> text=Admin')
    page.click('text=Ticket Custom Fields')
    page.click('text=New Custom Field Type')
    page.fill('[placeholder="e.g., Hardware, Recovery or Virus"]',custom_field_name)
    page.click("text=Create Custom Field")

def create_custom_field_field(page : Page, custom_field_name : str, custom_field_field_name : str, field_name_exists : bool):
    """
    Creates the new custom field field.  It will also create the custom field if the field_name_exists is set to False
        Arguments:
            page: a Page
            custom_field_name: a string
            custom_field_field_name: a string
            field_name_exists: a bool
    """
    if field_name_exists == False:
            create_custom_field(page, custom_field_name)

    page.click('a[role="button"]:has-text("More")')
    page.click('ul[role="menu"] >> text=Admin')
    page.click('text=Ticket Custom Fields')
    manage_page_anchor = page.locator(f'//*[text()="{custom_field_name}"]//parent::td//following-sibling::td/a').first
    manage_page_anchor.click()

    page.click('text=New Field')
    page.click('input[name="ticket_field[name]"]')
    page.fill('input[name="ticket_field[name]"]',custom_field_field_name)
    page.once('dialog', lambda dialog: dialog.dismiss())
    page.check('text=Required >> input[name="ticket_field[required]"]')
    with page.expect_navigation():
        page.click('text=Create Ticket field')

class Ticket:
    def __init__(self, **kwargs):
        self.status = kwargs.get('status') or 'New'
        self.customer_id = kwargs.get('customer_id')
        self.subject = kwargs.get('subject')
        self.problem_type = kwargs.get('problem_type')
        self.description = kwargs.get('description')
        self.ticket_id = None # I think id is reserved by Python
        self.number = None

    def create(self, api_request_context):
        # Remove duplicate code from ticket tests. Extract customer creation to the ticket class
        # If we don't need to set special parameters for customer(we don't need to change customer_name for example) in test,
        # we just call the create method for ticket object Ticket class, and we call create_customer method in a single place.
        # We don't need to duplicate customer creation in all tests

        if self.customer_id is None:
           customer_name = str(uuid.uuid4())
           self.customer_id, _= create_customer(customer_name, api_request_context)

        self.ticket_id, self.number = create_ticket(self.customer_id,
                                                    api_request_context,
                                                    status = self.status,
                                                    problem_type = self.problem_type,
                                                    subject = self.subject)

def wait_for_worker(page, selector, wait_for_presence = True):
    # The ticket is generated in a worker
    # It may take from 20 seconds to a minutes
    # Reload the page until we get our new ticket
    for i in range(0, 20):
        page.wait_for_timeout(5000)
        if wait_for_presence:
            if page.query_selector(selector):
                break
        else:
            if page.query_selector(selector) == None:
                break
        page.reload()
