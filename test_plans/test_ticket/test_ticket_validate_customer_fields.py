import email
import uuid
import pytest
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.ticket import create_ticket
from helpers.invoice import invoice_add_line_item
from helpers.customer import create_customer, Customer
import variables


@pytest.mark.regression

def test_ticket_validate_customer_fields(page, login, api_request_context):
    invoice_price = 300
    expected_balance = '${:.2f}'.format(invoice_price + 8.70)
    expected_credit = '${:.2f}'.format(0)
    expected_total = '${:.2f}'.format(invoice_price + 8.70)


    customer = Customer(business_name = str(uuid.uuid4()),
                        first_name = str(uuid.uuid4()),
                        last_name = str(uuid.uuid4()),
                        email = str(uuid.uuid4()) + '@syncromsp.com',
                        phone = "1425-654-5665",
                        address = "123 Main St",
                        city = "Columbus",
                        state = "OH")
    customer.create(api_request_context)

    #customer_id, _ = create_customer(customer_name, api_request_context)
    quick_view_selector = '#quick-view-customer-{}'.format(customer.customer_id)

    #Changing tax rate in admin
    page.goto(f'{variables.base_url}/administration')
    page.click('text=Tax Rates')
    page.click(f"//tr[@class='tax_rate']/td[4]/a[1]")
    page.fill(f"//input[@id='tax_rate_amount']", '2.9')
    page.on("dialog", lambda dialog: dialog.accept())
    page.click('//input[@type="submit"]')


    ticket_id, ticket_num = create_ticket(customer.customer_id, api_request_context)

    #Converting ticket to invoice and adding line item
    page.goto(f'{variables.base_url}/tickets')
    page.click(f'text={ticket_num}')
    page.click('text=Make Invoice')
    invoice_add_line_item(page)

    page.goto(f'{variables.base_url}/tickets')
    page.wait_for_selector(quick_view_selector)
    page.wait_for_timeout(3000)
    page.click(quick_view_selector)

    #Validating
    balance_selector = 'div:nth-child(1) > div.qv-overview-value'
    credit_selector = 'div:nth-child(2) > div.qv-overview-value'
    total_selector = 'div:nth-child(3) > div.qv-overview-value'

    page.wait_for_selector(balance_selector)

    balance_element = page.query_selector(balance_selector)
    credit_element = page.query_selector(credit_selector)
    total_element = page.query_selector(total_selector)
    customer_name_element = page.query_selector("//div[@class='qv-title']/a")
    email_element = page.query_selector("//a[starts-with(@href,'mailto:')]")
    phone_element = page.query_selector("//a[starts-with(@href,'tel:')]")
    address_element = page.query_selector("//a[starts-with(@href,'http://maps.google.com/maps')]")

    assert balance_element.inner_html() == expected_balance
    assert credit_element.inner_html() == expected_credit
    assert total_element.inner_html() == expected_total



    assert customer.business_name in customer_name_element.inner_html()
    assert email_element.inner_html() == customer.email
    assert phone_element.inner_html() == customer.phone
    assert customer.address in address_element.inner_html()
    assert customer.city in address_element.inner_html()
    assert customer.state in address_element.inner_html()
