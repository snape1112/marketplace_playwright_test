from fixtures.login import create_account, login
from playwright.sync_api import Page
from contextvars import Context
from time import sleep
import pytest
import uuid
from fixtures.constants import *
from playwright.sync_api import Page
import requests
import re
import variables

@pytest.mark.regression

def test_account_create(page : Page):
        variables.subdomain = str(uuid.uuid4())
        variables.account_email = str(uuid.uuid4()) + '@' + TEST_EMAIL_DOMAIN
        account_name = str(uuid.uuid4())

        page.goto(f'https://admin.{BASE_DOMAIN}/syncro_startup/free_trial_rmm_software')

        page.fill('#account_admin_full_name', str(uuid.uuid4()))
        page.fill('#account_admin_user_email', variables.account_email)
        page.fill('#account_name', account_name) 
        page.fill('#account_number_techs', '4')
        page.select_option('#account_number_endpoints', label='<100')

        page.fill('#account_admin_password', DEFAULT_PASSWORD)
        page.fill(
            '#account_admin_password_confirmation', DEFAULT_PASSWORD)

        page.fill('#account_lead_source', str(uuid.uuid4()))

        page.fill('#account_variables.subdomain', variables.subdomain)

        page.check('#read_tos')
        page.locator('.submit-signup').first.click()

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
        page.fill('#account_info_website',f'https://www.{str(uuid.uuid4())}.com')

        # previously this was use to logout
        page.locator('.btn-success').first.click()

        sleep(20)
#         def test_account_create(page : Page):
#     verification_email = str(uuid.uuid4()) + '@endtest-mail.io'
#     locator = page.frame_locator(".pardot_form")
#     variables.subdomain = str(uuid.uuid4())


#     page.goto('https://syncromsp.com/daniel-form-handler-test-010722')
#     page.fill('input[name="post_password"]', 'trial-test')
#     page.click('button[name=et_divi_submit_button]')
#     sleep(5)
#     locator.locator('[placeholder="Enter Admin First Name *"]').fill(str(uuid.uuid4()))
#     locator.locator('[placeholder="Enter Admin Last Name *"]').fill(str(uuid.uuid4()))
#     locator.locator('[placeholder="Enter Business Name *"]').fill(str(uuid.uuid4()))
#     locator.locator('#insertedPhoneField').fill('4256569832')
#     locator.locator('[placeholder="Enter Email Address *"]').fill(verification_email)
#     locator.locator('input[type="checkbox"]').check()
#     locator.locator('text=Start My Free Trial').click()
    
  
#     url = f'http://endtest.io/mailbox?email={verification_email}&format=json'
#     data = ''
#     max = 5
#     while len(data) < 10 and max >= 0:
#             x = requests.get(url)
#             data = x.text
#             sleep(3)
#             max = max -1
#     data = data.replace(f'\\"','"')
#     data = data.replace(f'\\/','/')
#     data = data.replace(f'\\r\\r\\n','')
#     result = re.findall('(https://.+?)\"', data)

#     page.goto(result[2])
#     page.wait_for_load_state('load')
#     page.fill('#account_variables.subdomain', variables.subdomain)
#     page.click('#account_password')
#     page.fill('#account_password', DEFAULT_PASSWORD)
#     page.fill('#account_password_confirmation', DEFAULT_PASSWORD) 
#     page.locator('text=Business Country *Country >> svg').click()
#     page.locator('#react-select-2-option-234').click()
#     page.locator('#account_number_of_techs >> text=Number of Techs').click()
#     page.locator('#react-select-4-option-1').click()
#     assert page.locator('//*[contains (text(),"GMT")]').inner_text != None
#     assert page.locator('//*[text()="Managed Service Provider"]').inner_text != None
#     page.locator('text=Start My Trial').click()
#     page.wait_for_timeout(20000)

        #check_default_tabs(page)
        check_default_assets(page)
        check_default_scripts(page)
        #check_default_policies(page)
        check_default_documentation(page)
        check_default_products(page)

def check_default_tabs(page : Page):
 
    tab_url = f'https://{variables.subdomain}.{BASE_DOMAIN}/settings/tabs'
    page.goto(tab_url)

    assert page.is_checked('#settings_training_tab')
    assert page.is_checked('#settings_msp_dashboard_tab')
    assert page.is_checked('#settings_chat_tab')
    assert page.is_checked('#settings_customers_tab')
    assert page.is_checked('#settings_assets_tab')
    assert page.is_checked('#settings_scripts_tab')
    assert page.is_checked('#settings_alerts_tab')
    assert page.is_checked('#settings_tickets_tab')
    assert page.is_checked('#settings_invoices_tab')
    assert page.is_checked('#settings_kabuto_policies_tab')
    assert page.is_checked('#settings_contracts_tab')
    assert page.is_checked('#settings_reports_tab')
    assert page.is_checked('#settings_wiki_tab')
    assert page.is_checked('#settings_field_jobs_tab')
    assert page.is_checked('#settings_products_tab')
    assert page.is_checked('#settings_app_center_tab')
    assert page.is_checked('#settings_leads_tab')
    assert page.is_checked('#settings_estimates_tab')
    assert page.is_checked('#settings_marketr_tab')
 
def check_default_assets(page):
 
    assets = f'https://{variables.subdomain}.{BASE_DOMAIN}/customer_assets'
    page.goto(assets)
    page.wait_for_url(assets)
    page.wait_for_load_state('domcontentloaded')


    anchor = page.query_selector('text="Example Computer (fake)"')
    assert anchor != None

def check_default_scripts(page):
 
        page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/scripts')
        page.wait_for_load_state('domcontentloaded')
        assert page.query_selector('text=Syncro (Alerts) - Close An RMM Alert') != None
        assert page.query_selector('text=Syncro (Alerts) - Open An RMM Alert') != None
        assert page.query_selector('text=Syncro (Assets) - Log Custom Activity') != None
        assert page.query_selector('text=Syncro (Assets) - Write To An Asset Custom Field') != None
        assert page.query_selector('text=Syncro (Email) - Send An Email') != None
        assert page.query_selector('text=Syncro (Event Log) - Retrieve Recent Logs') != None
        assert page.query_selector('text=Syncro (Files) - Capture A Screenshot To File') != None
        assert page.query_selector('text=Syncro (Files) - Download And Run A File') != None
        assert page.query_selector('text=Syncro (Files) - Get User Profile Folder Size') != None
        assert page.query_selector('text=Syncro (Files) - Upload File To An Asset Record') != None
        assert page.query_selector('text=Syncro (Notifications) - Send A Broadcast Message') != None
        assert page.query_selector('text=Syncro (Registry) - Create A New Registry Key') != None
        assert page.query_selector('text=Syncro (Registry) - Create / Set A Registry Key Parameter') != None
        assert page.query_selector('text=Syncro (Scripting) - Generate An Error Code') != None
        assert page.query_selector('text=Syncro (Scripting) - Write To Script Output') != None
        assert page.query_selector('text=Syncro (Tickets) - Create A New Ticket') != None
        assert page.query_selector('text=Syncro (Tickets) - Fully Process Ticket With Billable Time') != None
        assert page.query_selector('text=Syncro (Windows) - Kill A Windows Process') != None
        assert page.query_selector('text=Syncro (Windows) - Restart A Windows Service') != None
        assert page.query_selector('text=Syncro (Windows) - Start A Windows Process') != None

 
def check_default_policies(page):
 
        page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/policies')
        page.wait_for_load_state('domcontentloaded')
        assert page.query_selector('text="[Example] Base Package"') != None
        assert page.query_selector('text="[Example] Monitoring + AV"') != None
        assert page.query_selector('text="[Example] Monitoring + AV PLUS"') != None
        assert page.query_selector('text="[Example] Monitoring Package"') != None

def check_default_documentation(page):
 
        page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/documentation/') 
        page.wait_for_load_state('domcontentloaded')
        assert page.query_selector('a[href="/documentation/welcome"]') != None

def check_default_products(page):
        
        page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/products')
        page.wait_for_load_state('domcontentloaded')
 
        assert page.query_selector('text=Contract Labor') != None
        assert page.query_selector('text="[Example] Base Package"') != None
        assert page.query_selector('text="[Example] Monitoring + AV"') != None
        assert page.query_selector('text="[Example] Monitoring + AV PLUS"') != None
        assert page.query_selector('text="[Example] Monitoring Package"') != None
        assert page.query_selector('text=Labor') != None
        assert page.query_selector('text=RushLabor') != None
        assert page.query_selector('text=TripCharge') != None