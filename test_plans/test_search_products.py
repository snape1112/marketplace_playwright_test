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

    # search
    product_name = 'LED shoebox area light'
    page.fill('input[type="search"]', product_name)
    page.click('.search-bar--submit')

    expect(page.locator('.search-result >> nth = 0')).to_contain_text(product_name, ignore_case=True)