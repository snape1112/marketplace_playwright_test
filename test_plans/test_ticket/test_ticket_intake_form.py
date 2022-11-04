import pytest
import re
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.ticket import create_ticket, create_custom_field
from helpers.user import user_create
import variables

@pytest.mark.regression

def test_ticket_intake_form(page, login: login, api_request_context):
        # Enable Intake Form
        page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/settings/tickets')
        page.check('#settings_require_intake_form_with_ticket')
        assert page.is_checked('#settings_require_intake_form_with_ticket') == True
        page.click('input:has-text("Save")')
        assert page.wait_for_selector('text="Settings saved."') != None
        
        # Create a new user and return variables
        id, name, email, password = user_create(page)
        
        # Create a new Customer
        customer_name = str(uuid.uuid4())
        customer_id, _  = create_customer(customer_name, api_request_context)

        # Generic portion to create ticket (Cannot use helper for this)
        page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets/start')
        page.click('#ticket_customer_name')
        page.type('#ticket_customer_name', customer_name[:5], delay=150)
        page.click(f'text=/{customer_name[:5]}.*/')
        page.click('text=Create Ticket')
        page.fill('#ticket_subject', 'Printer not working')
        page.select_option('#ticket_problem_type', 'Remote Support')
        page.focus('#ticket_comments_attributes_0_body')
        page.fill('#ticket_comments_attributes_0_body','Please fix my printer')
        page.click('#ticket_notify_emails_tagsinput')
        page.click('text=Create Ticket')

        # Verify we are on the intake form
        assert page.locator('text="Ticket created, have them sign the intake form"') != None

        # Have to reload the page or it retains auth token from /tickets/start
        page.reload()

        # This will get the Ticket ID from the URL.  This is the db row number of the record.
        ticket_full_url = page.url
        parsed_ticket_id = re.search(r'(?<=tickets\/)(\d+)', ticket_full_url)
        ticket_id = parsed_ticket_id.group(0)

        # Change the Status
        auth_locator = page.locator('meta[name="csrf-token"]')
        token = auth_locator.get_attribute('content')
        assert token != None
        t_status = 'var formData = new FormData();'
        t_status += 'formData.append("_method", "put");'
        t_status += 'formData.append("ticket[status]", "In Progress");'
        t_status += f'formData.append("authenticity_token", "{token}");'
        t_status += 'var xhr = new XMLHttpRequest();'
        t_status += f'xhr.open("PUT", "https://{variables.subdomain}.{BASE_DOMAIN}/tickets/{ticket_id}", true);'
        t_status += 'xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");'
        t_status += 'xhr.send(new URLSearchParams(formData));'
        t_status_x = page.evaluate(t_status,)
        page.reload()
        
        # Change the assignee
        auth_locator = page.locator('meta[name="csrf-token"]')
        token = auth_locator.get_attribute('content')
        assert token != None
        assignee = 'var formData = new FormData();'
        assignee += 'formData.append("_method", "put");'
        assignee += f'formData.append("ticket[user_id]", "{id}");'
        assignee += f'formData.append("authenticity_token", "{token}");'
        assignee += 'var xhr = new XMLHttpRequest();'
        assignee += f'xhr.open("PUT", "https://{variables.subdomain}.{BASE_DOMAIN}/tickets/{ticket_id}", true);'
        assignee += 'xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");'
        assignee += 'xhr.send(new URLSearchParams(formData));'
        assignee_x = page.evaluate(assignee,)
        page.reload()
                
        # Change the Problem Type
        auth_locator = page.locator('meta[name="csrf-token"]')
        token = auth_locator.get_attribute('content')
        assert token != None
        problem_type = 'var formData = new FormData();'
        problem_type += 'formData.append("_method", "put");'
        problem_type += 'formData.append("ticket[problem_type]", "Other");'
        problem_type += f'formData.append("authenticity_token", "{token}");'
        problem_type += 'var xhr = new XMLHttpRequest();'
        problem_type += f'xhr.open("PUT", "https://{variables.subdomain}.{BASE_DOMAIN}/tickets/{ticket_id}", true);'
        problem_type += 'xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");'
        problem_type += 'xhr.send(new URLSearchParams(formData));'
        problem_type_x = page.evaluate(problem_type,)
        page.reload()
        
        # Accept the terms
        page.click('text=I accept the terms')
        assert page.locator('text=We saved the signature') != None
        assert page.locator(f'#best_in_place_ticket_{ticket_id}_status').first.inner_text() == 'In Progress' 
        assert page.locator(f'#best_in_place_ticket_{ticket_id}_user_id').first.inner_text() == name
        assert page.locator(f'#best_in_place_ticket_{ticket_id}_problem_type').first.inner_text() == 'Other'
        
        # Let's clean up after ourselves and disable intake forms
        page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/settings/tickets')
        page.uncheck('#settings_require_intake_form_with_ticket')
        assert page.is_checked('#settings_require_intake_form_with_ticket') is False
        page.click('input:has-text("Save")')
        assert page.wait_for_selector('text="Settings saved."') != None