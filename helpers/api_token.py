import pytest
from fixtures.constants import *
import variables


def generate_api_token(page):
    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/api_tokens/new#new-api-token')
    checkboxes = page.locator('input[type=checkbox]')
    for i in range(0, checkboxes.count()):
        checkboxes.nth(i).check()
    page.click('input[type=submit]')
    token = page.locator('//*//*[@class="blurb-container-warning "]/following-sibling::pre').inner_text()
    return token