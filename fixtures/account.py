from email.mime import base
import pytest
from fixtures.constants import *
from contextvars import Context
from time import sleep
import pytest
import uuid
from playwright.sync_api import Page
import requests
import re
from playwright.sync_api import sync_playwright
from helpers.api_token import generate_api_token
import variables


@pytest.fixture
def create_account(page):
 
    if OVERRIDE_ACCOUNT_CREATED == True :

        variables.subdomain = OVERRIDE_ACCOUNT_SUBDOMAIN
        variables.base_url = f'https://{variables.subdomain}.{BASE_DOMAIN}'
        variables.account_email = OVERRIDE_ACCOUNT_EMAIL
        return


    # Please make sure anything added here is also added to the OVERRIDE section above, if applicable.
    # Please make sure to test OVERRIDE as well after adding anything here.
    variables.subdomain = str(uuid.uuid4())
    variables.base_url = f'https://{variables.subdomain}.{BASE_DOMAIN}'
    variables.account_email = variables.subdomain + '@' + TEST_EMAIL_DOMAIN
    variables.admin_name = str(uuid.uuid4())

    page.goto(f'https://demo.{BASE_DOMAIN}/syncro_startup/free_trial_rmm_software')
    variables.business_name = str(uuid.uuid4())
    variables.admin_name = str(uuid.uuid4())
    page.fill('#account_admin_full_name', variables.admin_name)
    page.fill('#account_admin_user_email', variables.account_email)
    page.fill('#account_name', variables.business_name)
    page.fill('#account_number_techs', '4')
    page.select_option('#account_number_endpoints', label='<100')

    page.fill('#account_admin_password', DEFAULT_PASSWORD)
    page.fill(
        '#account_admin_password_confirmation', DEFAULT_PASSWORD)

    page.fill('#account_lead_source', str(uuid.uuid4()))

    page.fill('#account_subdomain', variables.subdomain)

    page.check('#read_tos')

    page.click('.submit-signup')

    page.fill('#account_info_street', str(uuid.uuid4()))
    page.fill('#account_info_city', str(uuid.uuid4()))
    page.fill('#account_info_state', 'CA')
    page.fill('#account_info_state', 'CA')
    page.select_option('#account_info_country', label='United States')
    page.select_option('#account_info_locale_code', label='USA')
    page.select_option('#account_info_time_zone',
                            label='(GMT-08:00) Pacific Time (US & Canada)')
    page.fill('#account_info_tax_rate', '2.9')
    page.fill('#account_info_phone', '555-212-1955')
    page.fill('#account_info_website',
                    'https://www.'+str(uuid.uuid4()) + '.com')

    page.click('.btn-success')
    page.click('.email-dropdown')
    variables.token = generate_api_token(page)
    sleep(5)
    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/users/sign_out')




# @pytest.fixture
# def account_create(page : Page):
#     if fixtures.OVERRIDE_ACCOUNT_CREATED == True :
#         variables.subdomain = fixtures.OVERRIDE_ACCOUNT_variables.subdomain
#         variables.account_email = fixtures.OVERRIDE_variables.account_email
#         return

#     if not hasattr(pytest,'variables.account_email'):

#         variables.subdomain = str(uuid.uuid4())
#         variables.account_email = variables.subdomain + '@' + fixtures.TEST_EMAIL_DOMAIN

#         verification_email = str(uuid.uuid4()) + '@endtest-mail.io'
#         locator = page.frame_locator(".pardot_form")
#         variables.subdomain = str(uuid.uuid4())


#         page.goto('https://syncromsp.com/daniel-form-handler-test-010722')
#         page.fill('input[name="post_password"]', 'trial-test')
#         page.click('button[name=et_divi_submit_button]')
#         #sleep(5)
#         page.wait_for_load_state('domcontentloaded')
#         locator.locator('[placeholder="Enter Admin First Name *"]').fill(str(uuid.uuid4()))
#         locator.locator('[placeholder="Enter Admin Last Name *"]').fill(str(uuid.uuid4()))
#         locator.locator('[placeholder="Enter Business Name *"]').fill(str(uuid.uuid4()))
#         locator.locator('#insertedPhoneField').fill('4256569832')
#         locator.locator('[placeholder="Enter Email Address *"]').fill(verification_email)
#         locator.locator('input[type="checkbox"]').check()
#         locator.locator('text=Start My Free Trial').click()


#         url = f'http://endtest.io/mailbox?email={verification_email}&format=json'
#         data = ''
#         max = 5
#         while len(data) < 10 and max >= 0:
#                 x = requests.get(url)
#                 data = x.text
#                 sleep(3)
#                 max = max -1
#         data = data.replace(f'\\"','"')
#         data = data.replace(f'\\/','/')
#         data = data.replace(f'\\r\\r\\n','')
#         result = re.findall('(https://.+?)\"', data)

#         page.goto(result[2])
#         page.wait_for_load_state('load')
#         page.fill('#account_variables.subdomain', variables.subdomain)
#         page.click('#account_password')
#         page.fill('#account_password', fixtures.DEFAULT_PASSWORD)
#         page.fill('#account_password_confirmation', fixtures.DEFAULT_PASSWORD)
#         page.locator('text=Business Country *Country >> svg').click()
#         page.locator('#react-select-2-option-234').click()
#         page.locator('#account_number_of_techs >> text=Number of Techs').click()
#         page.locator('#react-select-4-option-1').click()
#         page.locator('text=Start My Trial').click()
#         page.wait_for_load_state('load')
#         page.click('.email-dropdown')
#         page.click('[data-method="delete"]')



