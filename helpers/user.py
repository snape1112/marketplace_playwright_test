import pytest
import uuid
import re
from fixtures.constants import *
from fixtures.login import login
from playwright.sync_api import expect
import variables

def user_create(page, admin = True):
    """
    Creates a new Global Admin User
        Arguments:
            page: a Page
        Returns:
            name: The name of the user "User_<rand>"
            email: The e-mail used for the user "user_<rand>-junk@syncromsp.com"
            password: The temp password created for the user
            id: The ID of the new user
    """
    randuuid = str(uuid.uuid4())
    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/administration/users')
    page.click('text=Add User')
    assert page.locator('text=New User') != None
    # Set a variable so we can reuse the name/e-mail
    name = ('User_'+randuuid)
    email = ('user_'+randuuid+'-junk@syncromsp.com')
    # Populate fields with specific info
    page.fill('#user_full_name', name)
    page.fill('#user_email', email)
    page.fill('#user_sms_notification_number', '555-555-5555')
    # Don't send temp pass (security reasons)
    page.uncheck('#user_send_tmp_password')
    assert page.is_checked('#user_send_tmp_password') == False
    # Copy the temp pass in case we need to use it
    page.click('text ="Show/Hide Temporary Password"')
    password = page.locator('#tmp_password').first.inner_text()
    #Enable Global Admin Rights
    if admin:
        page.check('#user_group')
        assert page.is_checked('#user_group') == True
    else:
        page.uncheck('#user_group')
        assert page.is_checked('#user_group') == False
        # Select Technicians Security Group
        page.click('div.user_groups div.btn-group')
        page.click('div.btn-group label.checkbox:has-text("Technicians")')
        # Click anywhere to lose focus from multiselect
        page.click('div:has-text("New User")')
    # Save the user
    page.click('text=Create User')
    # Get the ID of the user we just created
    page.click(f'text={name}')
    # This will get the User ID from the URL.  This is the db row number of the record.
    user_id_full_url = page.url
    parsed_user_id = re.search(r'(?<=user\/)(\d+)', user_id_full_url)
    id = parsed_user_id.group(0)

    #variables passed back that can be referenced
    return id, name, email, password

def login_as(page, email, password):
    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/users/sign_in')
    page.fill('#user_email', email)
    page.fill('#user_password', password)
    page.click('text="Sign in"')

def new_user_password_reset(page, old_password):
    new_password = old_password + '1_New_2'
    page.fill('#user_old_password', old_password)
    page.fill('#user_password', new_password)
    page.fill('#user_password_confirmation', new_password)
    page.click('#user_accepted_toc')
    page.click('input[value="Update Password"]')
    return new_password

def create_tech_and_login(page):
    _, tech_name, tech_email, tech_password = user_create(page, admin = False)

    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/users/sign_out')

    login_as(page, tech_email, tech_password)

    new_password = new_user_password_reset(page, tech_password)

    login_as(page, tech_email, new_password)
    # Verify that the tech user logged in
    expect(page.locator('ul.nav.user-menu')).to_contain_text(tech_name[0:10])