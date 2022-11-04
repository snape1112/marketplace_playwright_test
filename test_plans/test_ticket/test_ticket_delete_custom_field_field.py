import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.ticket import create_custom_field_field
import variables

@pytest.mark.regression
def test_ticket_delete_custom_field_field(page, login):

        # Create new field / field field

        custom_field_name = str(uuid.uuid4())
        custom_field_field_name = str(uuid.uuid4())
        create_custom_field_field(page, custom_field_name, custom_field_field_name, False)

        # Delete the new field

        manage_page_anchor = page.locator(f'//*[text()="{custom_field_field_name}"]//parent::tr/td[6]/a').first
        manage_page_anchor.click()

        # Validate that it was delete successfully and no longer appears in the table

        missing_element = page.locator('//*[text()="Name"]//parent::tr//parent::thead//following-sibling::tbody[not(tr)]')

        assert missing_element != None
 
