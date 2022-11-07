import pytest
import uuid
from playwright.sync_api import Page
import re
import variables
from time import sleep

@pytest.mark.regression
def test_checkout(page):
    page.goto('https://utility-marketplace-store.myshopify.com')

    # input password
    page.fill('#password', 'mifrap')
    page.click('text="Enter"')

    # go to list page

    # add to cart
    for i in range(1):
        page.click('a[class="site-nav--link"]:has-text("Lighting")')
        page.click(f".cat-product-container:nth-child({i * 2 + 3}) .product-grid-item:first-child")
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
    page.fill('#checkout_email_or_phone', 'hello@email.com')
    page.fill('#checkout_shipping_address_first_name', 'A')
    page.fill('#checkout_shipping_address_last_name', 'B')
    page.fill('#checkout_shipping_address_address1', '1250 Ocean pkwy')
    page.fill('#checkout_shipping_address_address2', 'Apt. 20')
    page.fill('#checkout_shipping_address_city', 'Brooklyn')
    page.select_option('#checkout_shipping_address_province', label='New York')
    page.fill('#checkout_shipping_address_zip', '11235')
    page.click('text="Continue to shipping"')

    # select shipping method
    page.click('#checkout_shipping_rate_id_shopify-economy-4_90')
    page.click('text="Continue to payment"')

    # input credit card
    iframe_element = page.wait_for_selector("#card-fields-number-p31q2xvxoo000000-scope-utility-marketplace-store.myshopify.com")
    iframe = iframe_element.content_frame()

    sleep(100000)