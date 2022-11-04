from time import sleep
import pytest
from fixtures.constants import *
from fixtures.login import create_account, login 
from playwright.sync_api import Page, expect
import variables

@pytest.mark.regression
def test_ticket_edit_workflow(page, login):

    workflow_name = 'Workflow test'
    first_name = 'Workflow test'
    last_name = 'First Name'
    business_name = 'Business Name'
    email = 'test@email.com'
    phone_number = '8585551234'
    mobile_phone_number = '8595551234'
    ticket_subject = 'New Ticket'

    create_base_workflow(page, workflow_name, first_name, last_name,
                                       business_name, email, phone_number, mobile_phone_number, ticket_subject)
    workflow_name = 'Workflow test1'
    first_name = 'Workflow test1'
    last_name = 'First Name1'
    business_name = 'Business Name1'
    email = 'test@email.com1'
    phone_number = '85855512341'
    mobile_phone_number = '85955512341'
    ticket_subject = 'New Ticket1'

    check_base_edit(page, workflow_name, first_name, last_name,
                                       business_name, email, phone_number, mobile_phone_number, ticket_subject)

    create_workflow_with_visibility_require(
        page, workflow_name, first_name, last_name, business_name, email, phone_number, mobile_phone_number, ticket_subject)
    create_workflow_with_visibility_show(page, workflow_name, first_name, last_name,
                                         business_name, email, phone_number, mobile_phone_number, ticket_subject)
    create_workflow_with_visibility_hide(page, workflow_name, first_name, last_name,
                                         business_name, email, phone_number, mobile_phone_number, ticket_subject)


def create_workflow_with_visibility_require(page, workflow_name, first_name, last_name, business_name, email, phone_number, mobile_phone_number, ticket_subject):
    page.locator('input[name="customer_details- firstname"]').nth(2).check()
    page.locator('input[name="customer_details- lastname"]').nth(2).check()
    page.locator(
        'input[name="customer_details- business_name"]').nth(2).check()
    page.locator('input[name="customer_details- email"]').nth(2).check()
    page.locator('input[name="customer_details- phone"]').nth(2).check()
    page.locator('input[name="customer_details- mobile"]').nth(2).check()
    page.locator('input[name="customer_details- address"]').nth(2).check()
    page.locator('input[name="customer_details- referred_by"]').nth(2).check()
    page.locator('input[name="customer_details- tax_rate_id"]').nth(2).check()
    page.locator('input[name="customer_details- get_sms"]').nth(2).check()
    page.locator('input[name="customer_details- opt_out"]').nth(2).check()
    page.locator('input[name="customer_details- no_email"]').nth(2).check()
    page.locator(
        'input[name="customer_details- send_portal_invitation"]').nth(2).check()

    page.locator('input[name="ticket_details- user_id"]').nth(2).check()
    page.locator('input[name="ticket_details- priority"]').nth(2).check()
    page.locator('input[name="ticket_details- due_date"]').nth(2).check()
    page.locator('input[name="ticket_details- notify_emails"]').nth(2).check()
    page.locator('input[name="ticket_details- category"]').nth(2).check()
    page.locator('input[name="ticket_details- location_id"]').nth(2).check()
    page.locator('input[name="ticket_details- address_id"]').nth(2).check()
    page.locator('input[name="ticket_details- contract_id"]').nth(2).check()
    page.locator('input[name="ticket_details- sla_id"]').nth(2).check()
    page.locator('input[name="ticket_details- do_not_email"]').nth(2).check()
    page.locator('input[name="ticket_details- isapproved"]').nth(2).check()
    page.locator('input[name="ticket_details- pre_diagnosed"]').nth(2).check()

    expect(page.locator(
        'input[name="customer_details- firstname"]').nth(2)).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- lastname"]').nth(2)).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- business_name"]').nth(2)).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- email"]').nth(2)).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- phone"]').nth(2)).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- mobile"]').nth(2)).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- address"]').nth(2)).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- referred_by"]').nth(2)).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- tax_rate_id"]').nth(2)).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- get_sms"]').nth(2)).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- opt_out"]').nth(2)).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- no_email"]').nth(2)).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- send_portal_invitation"]').nth(2)).to_be_checked()

    expect(page.locator(
        'input[name="ticket_details- user_id"]').nth(2)).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- priority"]').nth(2)).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- due_date"]').nth(2)).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- notify_emails"]').nth(2)).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- category"]').nth(2)).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- location_id"]').nth(2)).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- address_id"]').nth(2)).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- contract_id"]').nth(2)).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- sla_id"]').nth(2)).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- do_not_email"]').nth(2)).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- isapproved"]').nth(2)).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- pre_diagnosed"]').nth(2)).to_be_checked()

    page.click('text=Save Workflow')
    page.wait_for_load_state()


def create_workflow_with_visibility_show(page, workflow_name, first_name, last_name, business_name, email, phone_number, mobile_phone_number, ticket_subject):
    page.locator('input[name="customer_details- firstname"]').nth(1).check()
    page.locator('input[name="customer_details- lastname"]').nth(1).check()
    page.locator(
        'input[name="customer_details- business_name"]').nth(1).check()
    page.locator('input[name="customer_details- email"]').nth(1).check()
    page.locator('input[name="customer_details- phone"]').nth(1).check()
    page.locator('input[name="customer_details- mobile"]').nth(1).check()
    page.locator('input[name="customer_details- address"]').nth(1).check()
    page.locator('input[name="customer_details- referred_by"]').nth(1).check()
    page.locator('input[name="customer_details- tax_rate_id"]').nth(1).check()
    page.locator('input[name="customer_details- get_sms"]').nth(1).check()
    page.locator('input[name="customer_details- opt_out"]').nth(1).check()
    page.locator('input[name="customer_details- no_email"]').nth(1).check()
    page.locator(
        'input[name="customer_details- send_portal_invitation"]').nth(1).check()

    page.locator('input[name="ticket_details- user_id"]').nth(1).check()
    page.locator('input[name="ticket_details- priority"]').nth(1).check()
    page.locator('input[name="ticket_details- due_date"]').nth(1).check()
    page.locator('input[name="ticket_details- notify_emails"]').nth(1).check()
    page.locator('input[name="ticket_details- category"]').nth(1).check()
    page.locator('input[name="ticket_details- location_id"]').nth(1).check()
    page.locator('input[name="ticket_details- address_id"]').nth(1).check()
    page.locator('input[name="ticket_details- contract_id"]').nth(1).check()
    page.locator('input[name="ticket_details- sla_id"]').nth(1).check()
    page.locator('input[name="ticket_details- do_not_email"]').nth(1).check()
    page.locator('input[name="ticket_details- isapproved"]').nth(1).check()
    page.locator('input[name="ticket_details- pre_diagnosed"]').nth(1).check()

    expect(page.locator(
        'input[name="customer_details- firstname"]').nth(1)).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- lastname"]').nth(1)).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- business_name"]').nth(1)).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- email"]').nth(1)).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- phone"]').nth(1)).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- mobile"]').nth(1)).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- address"]').nth(1)).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- referred_by"]').nth(1)).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- tax_rate_id"]').nth(1)).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- get_sms"]').nth(1)).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- opt_out"]').nth(1)).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- no_email"]').nth(1)).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- send_portal_invitation"]').nth(1)).to_be_checked()

    expect(page.locator(
        'input[name="ticket_details- user_id"]').nth(1)).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- priority"]').nth(1)).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- due_date"]').nth(1)).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- notify_emails"]').nth(1)).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- category"]').nth(1)).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- location_id"]').nth(1)).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- address_id"]').nth(1)).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- contract_id"]').nth(1)).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- sla_id"]').nth(1)).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- do_not_email"]').nth(1)).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- isapproved"]').nth(1)).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- pre_diagnosed"]').nth(1)).to_be_checked()

    page.click('text=Save Workflow')
    page.wait_for_load_state()


def create_workflow_with_visibility_hide(page, workflow_name, first_name, last_name, business_name, email, phone_number, mobile_phone_number, ticket_subject):
    page.locator('input[name="customer_details- firstname"]').first.check()
    page.locator('input[name="customer_details- lastname"]').first.check()
    page.locator('input[name="customer_details- business_name"]').first.check()
    page.locator('input[name="customer_details- email"]').first.check()
    page.locator('input[name="customer_details- phone"]').first.check()
    page.locator('input[name="customer_details- mobile"]').first.check()
    page.locator('input[name="customer_details- address"]').first.check()
    page.locator('input[name="customer_details- referred_by"]').first.check()
    page.locator('input[name="customer_details- tax_rate_id"]').first.check()
    page.locator('input[name="customer_details- get_sms"]').first.check()
    page.locator('input[name="customer_details- opt_out"]').first.check()
    page.locator('input[name="customer_details- no_email"]').first.check()
    page.locator(
        'input[name="customer_details- send_portal_invitation"]').first.check()

    page.locator('input[name="ticket_details- user_id"]').first.check()
    page.locator('input[name="ticket_details- priority"]').first.check()
    page.locator('input[name="ticket_details- due_date"]').first.check()
    page.locator('input[name="ticket_details- notify_emails"]').first.check()
    page.locator('input[name="ticket_details- category"]').first.check()
    page.locator('input[name="ticket_details- location_id"]').first.check()
    page.locator('input[name="ticket_details- address_id"]').first.check()
    page.locator('input[name="ticket_details- contract_id"]').first.check()
    page.locator('input[name="ticket_details- sla_id"]').first.check()
    page.locator('input[name="ticket_details- do_not_email"]').first.check()
    page.locator('input[name="ticket_details- isapproved"]').first.check()
    page.locator('input[name="ticket_details- pre_diagnosed"]').first.check()

    expect(page.locator(
        'input[name="customer_details- firstname"]').first).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- lastname"]').first).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- business_name"]').first).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- email"]').first).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- phone"]').first).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- mobile"]').first).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- address"]').first).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- referred_by"]').first).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- tax_rate_id"]').first).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- get_sms"]').first).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- opt_out"]').first).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- no_email"]').first).to_be_checked()
    expect(page.locator(
        'input[name="customer_details- send_portal_invitation"]').first).to_be_checked()

    expect(page.locator(
        'input[name="ticket_details- user_id"]').first).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- priority"]').first).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- due_date"]').first).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- notify_emails"]').first).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- category"]').first).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- location_id"]').first).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- address_id"]').first).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- contract_id"]').first).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- sla_id"]').first).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- do_not_email"]').first).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- isapproved"]').first).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details- pre_diagnosed"]').first).to_be_checked()

    page.click('text=Save Workflow')
    page.wait_for_load_state()

def create_base_workflow(page, workflow_name, first_name, last_name, business_name, email, phone_number, mobile_phone_number, ticket_subject):
    page.goto(
        f'https://{variables.subdomain}.{BASE_DOMAIN}/new_ticket_forms')
    page.click('text=New Workflow')
    page.fill('input[name="new_ticket_form[name]"]', workflow_name)
    page.fill('input[name="customer_details-firstname"]', first_name)
    page.fill('input[name="customer_details-lastname"]', last_name)
    page.fill('input[name="customer_details-business_name"]', business_name)
    page.fill('input[name="customer_details-email"]', email)
    page.fill('input[name="customer_details-phone"]', phone_number)
    page.fill('input[name="customer_details-mobile"]', mobile_phone_number)
    page.check('text=SMS Enabled HideShowRequire >> input[type="checkbox"]')
    page.check(
        'text=Opt out of any marketing emails HideShowRequire >> input[type="checkbox"]')
    page.check(
        'text=No Email - of any kind HideShowRequire >> input[type="checkbox"]')
    page.check(
        'text=Send Portal Invite HideShowRequire >> input[type="checkbox"]')
    page.click('input[name="ticket_details-subject"]')
    page.fill('input[name="ticket_details-subject"]', ticket_subject)

    check_box = page.locator(
        'input[name="ticket_details-do_not_email"]').nth(1)
    check_box.check()

    check_box = page.locator('input[name="ticket_details-isapproved"]').nth(1)
    check_box.check()

    check_box = page.locator(
        'input[name="ticket_details-pre_diagnosed"]').nth(1)
    check_box.check()

    page.click('text=Save Workflow')
    page.wait_for_load_state()

    # Validate the fields
    expect(page.locator('input[name="new_ticket_form[name]"]')).to_have_value(
        workflow_name)
    expect(page.locator(
        'input[name="customer_details-firstname"]')).to_have_value(first_name)
    expect(page.locator(
        'input[name="customer_details-lastname"]')).to_have_value(last_name)
    expect(page.locator(
        'input[name="customer_details-business_name"]')).to_have_value(business_name)
    expect(page.locator(
        'input[name="customer_details-email"]')).to_have_value(email)
    expect(page.locator(
        'input[name="customer_details-phone"]')).to_have_value(phone_number)
    expect(page.locator(
        'input[name="customer_details-mobile"]')).to_have_value(mobile_phone_number)
    expect(page.locator(
        'input[name="ticket_details-subject"]')).to_have_value(ticket_subject)

    expect(page.locator(
        'text=SMS Enabled HideShowRequire >> input[type="checkbox"]')).to_be_checked()
    expect(page.locator(
        'text=Opt out of any marketing emails HideShowRequire >> input[type="checkbox"]')).to_be_checked()
    expect(page.locator(
        'text=No Email - of any kind HideShowRequire >> input[type="checkbox"]')).to_be_checked()
    expect(page.locator(
        'text=Send Portal Invite HideShowRequire >> input[type="checkbox"]')).to_be_checked()

    expect(page.locator(
        'input[name=ticket_details-do_not_email]').last).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details-isapproved"]').last).to_be_checked()
    expect(page.locator(
        'input[name="ticket_details-pre_diagnosed"]').last).to_be_checked()


def check_base_edit(page, workflow_name, first_name, last_name, business_name, email, phone_number, mobile_phone_number, ticket_subject):
    page.fill('input[name="new_ticket_form[name]"]', workflow_name)
    page.fill('input[name="customer_details-firstname"]', first_name)
    page.fill('input[name="customer_details-lastname"]', last_name)
    page.fill('input[name="customer_details-business_name"]', business_name)
    page.fill('input[name="customer_details-email"]', email)
    page.fill('input[name="customer_details-phone"]', phone_number)
    page.fill('input[name="customer_details-mobile"]', mobile_phone_number)
    page.click('text=SMS Enabled HideShowRequire >> input[type="checkbox"]')
    page.click(
        'text=Opt out of any marketing emails HideShowRequire >> input[type="checkbox"]')
    page.click(
        'text=No Email - of any kind HideShowRequire >> input[type="checkbox"]')
    page.click(
        'text=Send Portal Invite HideShowRequire >> input[type="checkbox"]')
    page.click('input[name="ticket_details-subject"]')
    page.fill('input[name="ticket_details-subject"]', ticket_subject)

    check_box = page.locator(
        'input[name="ticket_details-do_not_email"]').last
    check_box.click()

    check_box = page.locator('input[name="ticket_details-isapproved"]').last 
    check_box.click()

    check_box = page.locator(
        'input[name="ticket_details-pre_diagnosed"]').last
    check_box.click()

    page.click('text=Save Workflow')
    page.wait_for_load_state()

    # Validate the fields
    expect(page.locator('input[name="new_ticket_form[name]"]')).to_have_value(
        workflow_name)
    expect(page.locator(
        'input[name="customer_details-firstname"]')).to_have_value(first_name)
    expect(page.locator(
        'input[name="customer_details-lastname"]')).to_have_value(last_name)
    expect(page.locator(
        'input[name="customer_details-business_name"]')).to_have_value(business_name)
    expect(page.locator(
        'input[name="customer_details-email"]')).to_have_value(email)
    expect(page.locator(
        'input[name="customer_details-phone"]')).to_have_value(phone_number)
    expect(page.locator(
        'input[name="customer_details-mobile"]')).to_have_value(mobile_phone_number)
    expect(page.locator(
        'input[name="ticket_details-subject"]')).to_have_value(ticket_subject)

    expect(page.locator(
        'text=SMS Enabled HideShowRequire >> input[type="checkbox"]')).not_to_be_checked()
    expect(page.locator(
        'text=Opt out of any marketing emails HideShowRequire >> input[type="checkbox"]')).not_to_be_checked()
    expect(page.locator(
        'text=No Email - of any kind HideShowRequire >> input[type="checkbox"]')).not_to_be_checked()
    expect(page.locator(
        'text=Send Portal Invite HideShowRequire >> input[type="checkbox"]')).not_to_be_checked()

    expect(page.locator(
        'input[name=ticket_details-do_not_email]').last).not_to_be_checked()
    expect(page.locator(
        'input[name="ticket_details-isapproved"]').last).not_to_be_checked()
    expect(page.locator(
        'input[name="ticket_details-pre_diagnosed"]').last).not_to_be_checked()
