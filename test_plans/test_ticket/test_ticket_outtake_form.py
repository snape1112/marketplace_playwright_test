import pytest
import re
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.ticket import create_ticket
from helpers.user import user_create
import variables

@pytest.mark.regression

def test_ticket_outtake_form(page, login: login, api_request_context):
        # Enable Outtake Form
        page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/settings/tickets')
        page.check('#settings_require_outtake_form_with_ticket')
        assert page.is_checked('#settings_require_outtake_form_with_ticket') is True
        page.click('input:has-text("Save")')
        assert page.wait_for_selector('text="Settings saved."') != None
        
        # Create a new user and return variables
        user_id, name, _, _ = user_create(page)
        
        # Create a new Customer and new ticket
        customer_name = str(uuid.uuid4())
        customer_id, _  = create_customer(customer_name, api_request_context)
        ticket_id, ticket_num = create_ticket(customer_id, api_request_context)
        page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets/{ticket_id}')
        # Open the Outtake form
        page.click('.btn.btn-default')
        page.click('text=Outtake Form')
        assert page.url == f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets/{ticket_id}/outtake_form'
        page.reload()

        # Change the Status
        auth_locator = page.locator('meta[name="csrf-token"]')
        token = auth_locator.get_attribute('content')
        assert token != None
        t_status = 'var formData = new FormData();'
        t_status += 'formData.append("_method", "put");'
        t_status += 'formData.append("ticket[status]", "Resolved");'
        t_status += f'formData.append("authenticity_token", "{token}");'
        t_status += 'var xhr = new XMLHttpRequest();'
        t_status += f'xhr.open("PUT", "https://{variables.subdomain}.{BASE_DOMAIN}/tickets/{ticket_id}", true);'
        t_status += 'xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");'
        # t_status += 'xhr.onload = function () {'
        # t_status += '   document.title = xhr.status; '
        # t_status += '}'
        t_status += 'xhr.send(new URLSearchParams(formData));'
        t_status_x = page.evaluate(t_status,)
        page.reload()
        
        # Change the assignee
        auth_locator = page.locator('meta[name="csrf-token"]')
        token = auth_locator.get_attribute('content')
        assert token != None
        assignee = 'var formData = new FormData();'
        assignee += 'formData.append("_method", "put");'
        assignee += f'formData.append("ticket[user_id]", "{user_id}");'
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
        problem_type += 'formData.append("ticket[problem_type]", "Network Project");'
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
        assert page.url == f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets/{ticket_id}'
        assert page.locator(f'#best_in_place_ticket_{ticket_id}_status').first.inner_text() == 'Resolved' 
        assert page.locator(f'#best_in_place_ticket_{ticket_id}_user_id').first.inner_text() == name
        assert page.locator(f'#best_in_place_ticket_{ticket_id}_problem_type').first.inner_text() == 'Network Project'
        
        # Let's clean up after ourselves and disable intake forms
        page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/settings/tickets')
        page.uncheck('#settings_require_intake_form_with_ticket')
        assert page.is_checked('#settings_require_intake_form_with_ticket') is False
        page.click('input:has-text("Save")')
        assert page.wait_for_selector('text="Settings saved."') != None