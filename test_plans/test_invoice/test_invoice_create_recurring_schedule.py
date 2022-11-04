
import uuid
from playwright.sync_api import Page, expect
from fixtures.login import create_account, login 
from helpers.customer import create_customer 
from time import sleep
import pytest
import variables
 

@pytest.mark.regression
def test_invoice_create_recurring_schedule(page:Page, login,api_request_context):

        # Pre-condition

        customer_name = str(uuid.uuid4())
        create_customer(customer_name, api_request_context)
        template_name = str(uuid.uuid4())
        invoice_name = str(uuid.uuid4())

        page.click('a[role="button"]:has-text("More")') 
        page.click('ul[role="menu"] >> text=Admin')
        page.click('text=Recurring Invoices')

        # The backend jobs are not already done setting up the accounts by the time we get 
        # to this point, so we have to pause and reload.  Even this may not consistently

        sleep(10)
        page.reload()

        check_positive_test_case(page, template_name, invoice_name)

        page.click('a[role="button"]:has-text("More")') 
        page.click('ul[role="menu"] >> text=Admin')
        page.click('text=Recurring Invoices')

        check_negative_test_case(page, template_name, invoice_name)
        
def check_negative_test_case(page, template_name, invoice_name):
        
        # Check that the schedule does not get created when no data is set
               
        page.click('text=New Schedule')
        page.click('text=Select an Option') 
        page.click('//*[@id="schedule_customer_chosen"]/div/ul/li')
        page.click('text=Proceed') 
        page.click('text=Create Schedule')

        # Check that the error messages are visible

        page.locator('text=Frequency Must be a valid selection') != None
        page.locator('text=Frequency can\'t be blank') != None
        page.locator('text=Next run can\'t be blank') != None
        page.locator('text=Name can\'t be blank') != None

        # This can be extended later for more negative test cases


def check_positive_test_case(page, template_name, invoice_name):
        
        # Create the new schedule
               
        page.click('text=New Schedule')
        page.click('text=Select an Option') 
        page.click('//*[@id="schedule_customer_chosen"]/div/ul/li')
        page.click('text=Proceed') 
        page.fill('input[name="schedule[name]"]',template_name)
        page.select_option('select[name="schedule[frequency]"]','Monthly')
        page.click('input[name="schedule[next_run_label]"]')
        page.click('#ui-datepicker-div >> text=29')
        page.click('text=Last day of the calendar month') 
        page.click('input[name="schedule[generated_invoice_name]"]')
        page.fill('input[name="schedule[generated_invoice_name]"]', invoice_name)
        page.check('text=Allow generation of blank invoices >> input[name="schedule[allow_blank_invoices]"]') 
        page.check('text=Email customer the PDF >> input[name="schedule[email_customer]"]') 
        page.check('text=Mail Physical Invoice (costs money) >> input[name="schedule[snail_mail]"]') 
        page.check('text=Add any pending Ticket charges >> input[type="checkbox"]')
        page.check('text=Keep prices in sync with products if they change >> input[name="schedule[keep_pricing_current]"]') 
        page.check('text=Pause this recurring Invoice >> input[name="schedule[paused]"]') 
        page.click('text=All (Default)') 
        page.click('label:has-text("In Progress")')
        page.click('text=Create Schedule') 

        # Check for the set fields

        expect(page.locator('input[name="schedule[name]"]')).to_have_value(template_name)
        expect(page.locator('input[name="schedule[generated_invoice_name]"]')).to_have_value(invoice_name)
        expect(page.locator('text=Allow generation of blank invoices >> input[name="schedule[allow_blank_invoices]"]')).to_be_checked()
        expect(page.locator('text=Email customer the PDF >> input[name="schedule[email_customer]"]')).to_be_checked()
        expect(page.locator('text=Mail Physical Invoice (costs money) >> input[name="schedule[snail_mail]"]')).to_be_checked()
        expect(page.locator('text=Add any pending Ticket charges >> input[type="checkbox"]')).to_be_checked()
        expect(page.locator('text=Keep prices in sync with products if they change >> input[name="schedule[keep_pricing_current]"]')).to_be_checked()
        expect(page.locator('text=Pause this recurring Invoice >> input[name="schedule[paused]"]')).to_be_checked()
        expect(page.locator('text=Last day of the calendar month')).to_be_checked()
        page.locator('button[title=In Progress]') != None
        page.locator("text= Great, now add some line items and you are all set!") != None
 


 












    
