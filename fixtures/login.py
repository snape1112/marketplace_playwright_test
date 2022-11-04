import pytest
from fixtures.constants import *
from fixtures.account import create_account
from playwright.sync_api import Page
from helpers.api_token import generate_api_token
import variables


@pytest.fixture
def login(page: Page, create_account):
    cookies = page.context.cookies(f'https://{variables.subdomain}.{BASE_DOMAIN}')
    if not cookies == None:
        page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/users/sign_in')
        page.fill('#user_email', variables.account_email)
        page.fill('#user_password', OVERRIDE_ACCOUNT_PASSWORD if OVERRIDE_ACCOUNT_CREATED == True else DEFAULT_PASSWORD )
        page.click('text="Sign in"')
        if OVERRIDE_ACCOUNT_CREATED == True:
            if OVERRIDE_ACCOUNT_API_KEY == True:
                # Use the stored value for the API Key and don't generate a new one
                variables.token = OVERRIDE_ACCOUNT_API_KEY_VALUE
            else:
                # Generate an API key for use with helpers
                variables.token = generate_api_token(page)
        
