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

    for supplier in ['ELED', 'Universe Electric']:
        for i in range(6):
            page.hover('a[class="site-nav--link"]:has-text("Suppliers")')
            page.click(f"a[class=\"site-nav--link\"]:has-text(\"{supplier}\")")
            try:
                page.click(f"#cat-product-next-maya-thing--link >> nth={i}", timeout=5000)
            except:
                break
            item = '.small--one-half:nth-child(1)'
            page.wait_for_selector(item + ' .product-title')
            item_name = page.query_selector(item + ' .product-title').inner_text()
            item_price = page.query_selector(item + ' .product-item--price .visually-hidden >> nth=1').inner_text()
            page.click(item)
            page.wait_for_selector('.product-title-container')
            expect(page.locator('.product-title-container .product-name')).to_contain_text(item_name)
            expect(page.locator('.product-price-container .product-price-amt .visually-hidden')).to_contain_text(item_price)
            print(item_name, item_price)
