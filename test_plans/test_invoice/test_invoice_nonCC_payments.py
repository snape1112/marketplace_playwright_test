#this test contains nonCC payments and refunds. I added the functions to every payment type, and took them to the top function. 
from time import sleep
import pytest
import uuid
from fixtures.constants import *
from playwright.sync_api import Page
from fixtures.login import create_account, login
from playwright.sync_api import Page, expect
from helpers.invoice import create_new_invoice, create_invoice_with_line_item
from helpers.customer import create_customer as create_customer
import variables


@pytest.mark.regression

def test_invoice_payments_cash(page, login, api_request_context):
    customer_name = str(uuid.uuid4())
    create_customer(customer_name, api_request_context)
    create_invoice_with_line_item(page, customer_name)
    page.click('text=Take Payment')
    page.click('#payment_payment_method_id')
    page.type('#payment_payment_method_id','Cash', delay=150)

    #this is an assertion for the field to have some input
    expect(page.locator('#payment_payment_amount')).not_to_be_empty()
    expect(page.locator('#tenderedAmount')).not_to_be_empty()
    page.click('text=Take Payment')
    assert page.wait_for_selector('text=Payment successfully applied') != None
    page.click('text=Continue')
    page.wait_for_load_state('domcontentloaded')

    #this is refund 
    page.click('text=Actions')
    page.click('text=Refund')
    page.fill('//*[text()="Item"]/parent::tr/parent::thead/following-sibling::tbody/tr/td[4]/div/input', '1')
    page.click('text=Begin Refund')
    assert page.wait_for_selector('text=Ok, here is the refund transaction') != None
    page.click('text=Finalize Refund')
    assert page.wait_for_selector('text=Ok, here is the refund payment') != None
    page.click('text=Continue')

@pytest.mark.regression

def test_invoice_payments_check(page, login, api_request_context): 
    customer_name = str(uuid.uuid4())
    create_customer(customer_name, api_request_context)
    create_invoice_with_line_item(page, customer_name)
    page.click('text=Take Payment')
    page.click('#payment_payment_method_id')
    page.type('#payment_payment_method_id','Check', delay=150)
    expect(page.locator('#payment_payment_amount')).not_to_be_empty()
    page.click('text=Take Payment')
    assert page.wait_for_selector('text=Payment successfully applied') != None
    with page.expect_navigation():
        page.click('text=Continue') 
    page.wait_for_load_state('domcontentloaded')
    page.click('text=Actions')
    page.click('text=Refund')
    page.fill('//*[text()="Item"]/parent::tr/parent::thead/following-sibling::tbody/tr/td[4]/div/input', '1')
    page.click('text=Begin Refund')
    assert page.wait_for_selector('text=Ok, here is the refund transaction') !=None
    page.click('text=Finalize Refund')
    assert page.wait_for_selector('text=Ok, here is the refund payment') !=None
    page.click('.continue-button')


@pytest.mark.regression
  
def test_invoice_payments_quick(page, login, api_request_context): 
    customer_name = str(uuid.uuid4())
    create_customer(customer_name, api_request_context)
    create_invoice_with_line_item(page, customer_name)
    page.click('text=Take Payment')
    page.click('#payment_payment_method_id')
    page.type('#payment_payment_method_id','Quick', delay=150)
    expect(page.locator('#payment_payment_amount')).not_to_be_empty()
    page.click('text=Take Payment')
    assert page.wait_for_selector('text=Payment successfully applied') != None
    with page.expect_navigation():    
        page.click('text=Continue') 
    page.wait_for_load_state('domcontentloaded')
    page.click('text=Actions')
    with page.expect_navigation():
        page.click('text=Refund')
    page.fill('//*[text()="Item"]/parent::tr/parent::thead/following-sibling::tbody/tr/td[4]/div/input', '1')
    page.click('text=Begin Refund')
    assert page.wait_for_selector('text=Ok, here is the refund transaction') !=None
    page.click('text=Finalize Refund')
    assert page.wait_for_selector('text=Ok, here is the refund payment') !=None
    page.click('.continue-button')


@pytest.mark.regression

def test_invoice_payments_other(page, login, api_request_context): 
    customer_name = str(uuid.uuid4())
    create_customer(customer_name, api_request_context)
    create_invoice_with_line_item(page, customer_name)
    page.click('text=Take Payment')
    page.click('#payment_payment_method_id')
    page.type('#payment_payment_method_id','Other', delay=150)
    expect(page.locator('#payment_payment_amount')).not_to_be_empty()
    page.click('text=Take Payment')
    assert page.wait_for_selector('text=Payment successfully applied') != None
    with page.expect_navigation():
        page.click('text=Continue') 
    page.wait_for_load_state('domcontentloaded')
    page.click('text=Actions')
    with page.expect_navigation():
        page.click('text=Refund')
    page.fill('//*[text()="Item"]/parent::tr/parent::thead/following-sibling::tbody/tr/td[4]/div/input', '1')
    page.click('text=Begin Refund')
    assert page.wait_for_selector('text=Ok, here is the refund transaction') !=None
    page.click('text=Finalize Refund')
    assert page.wait_for_selector('text=Ok, here is the refund payment') !=None
    page.click('.continue-button')


@pytest.mark.regression

def test_invoice_payments_offlineCC(page, login, api_request_context): 
    customer_name = str(uuid.uuid4())
    create_customer(customer_name, api_request_context)
    create_invoice_with_line_item(page, customer_name)
    page.click('text=Take Payment')
    page.click('#payment_payment_method_id')
    page.type('#payment_payment_method_id','Offline CC', delay=150)
    expect(page.locator('#payment_payment_amount')).not_to_be_empty()
    page.click('text=Take Payment')
    assert page.wait_for_selector('text=Payment successfully applied') != None
    with page.expect_navigation():
        page.click('text=Continue')
    page.wait_for_load_state('domcontentloaded')
    page.click('text=Actions')
    page.click('text=Refund')
    page.fill('//*[text()="Item"]/parent::tr/parent::thead/following-sibling::tbody/tr/td[4]/div/input', '1')
    page.click('text=Begin Refund')
    assert page.wait_for_selector('text=Ok, here is the refund transaction') != None
    page.click('text=Finalize Refund')
    assert page.wait_for_selector('text=Ok, here is the refund payment') != None
    page.click('.continue-button')