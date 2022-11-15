import pytest
import uuid
from playwright.sync_api import Page, expect
import re
from time import sleep

@pytest.mark.regression
def test_checkout(page):
    # site_url = 'https://utility-marketplace-store.myshopify.com'
    site_url = 'https://dte-business-marketplace.myshopify.com/'

    page.goto(site_url)

    # input password
    # page.fill('#password', 'mifrap')
    page.fill('#password', 'DTE2022')
    page.click('text="Enter"')

    # go to list page

    # add to cart
    for i in range(8):
        page.click('a[class="site-nav--link"]:has-text("Lighting")')
        page.click(f".cat-product-container:nth-child({i * 2 + 3}) .grid-item:first-child")
        page.click('#addToCart-product-template')

    # go to checkout
    page.click('#checkoutButton')

    # input account number
    page.fill('#accountNumberInput', '548697832157')
    page.click('#verifyButton')

    # verify address
    page.select_option('#ee-account-verify-address--input', label='119 FOREST HILLS DRIVE, PITTSBURGH, PA, 15226')
    page.click('#verifyAddressButton')

    # input contact info and shipping address
    page.fill('#checkout_email', 'hello@email.com')
    page.fill('#checkout_shipping_address_first_name', 'A')
    page.fill('#checkout_shipping_address_last_name', 'B')
    page.fill('#checkout_shipping_address_address1', '1250 Ocean pkwy')
    page.fill('#checkout_shipping_address_address2', 'Apt. 20')
    page.fill('#checkout_shipping_address_city', 'Brooklyn')
    page.select_option('#checkout_shipping_address_province', label='New York')
    page.fill('#checkout_shipping_address_zip', '11235')
    page.click('text="Continue to shipping"')

    # select shipping method
    page.click('#checkout_shipping_rate_id_shopify-economy-0_00')
    page.click('text="Continue to payment"')

    # input credit card
    iframe_element = page.wait_for_selector(".card-fields-iframe")
    iframe = iframe_element.content_frame()
    sleep(3)
    iframe.fill('#number', '4242424242424242')
    sleep(3)    
    iframe.fill('#name', 'Bogus Gateway')
    sleep(3)
    iframe.fill('#expiry', '03/25')
    sleep(3)    
    iframe.fill('#verification_value', '333')
    page.click('#checkout_different_billing_address_false')
    page.click('text="Pay now"')

    # verify order number and thank you, address
    page.wait_for_selector(".os-order-number")
    expect(page.locator('.os-order-number')).to_contain_text('Order #')
    expect(page.locator('#main-header')).to_have_text('Thank you A!')
    expect(page.locator('.section__content__column--half:first-child .address')).to_contain_text('Brooklyn')
    expect(page.locator('.section__content__column--half:nth-child(2) .address')).to_contain_text('Brooklyn')
    page.click('text="Continue shopping"')

    expect(page).to_have_url(site_url)