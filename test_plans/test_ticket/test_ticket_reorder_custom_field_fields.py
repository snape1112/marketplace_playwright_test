import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.ticket import create_custom_field,create_custom_field_field
import variables
 
@pytest.mark.regression
def test_ticket_reorder_custom_field_fields(page, login,api_request_context):
        customer_name = str(uuid.uuid4())
        create_customer(customer_name, api_request_context)

        # Add three custom fields that can be used to reorder

        custom_field_1_name = str(uuid.uuid4())
        create_custom_field(page, custom_field_1_name)

        custom_field_field_name_1 = str(uuid.uuid4())
        create_custom_field_field(page, custom_field_1_name, custom_field_field_name_1, True)

        custom_field_field_name_2 = str(uuid.uuid4())
        create_custom_field_field(page, custom_field_1_name, custom_field_field_name_2, True)

        custom_field_field_name_3 = str(uuid.uuid4())
        create_custom_field_field(page, custom_field_1_name, custom_field_field_name_3, True)

        # Grab the initial position of the two rows

        initial_field_1_id = page.locator(f'//*[text()="Name"]//parent::tr//parent::thead//following-sibling::tbody/tr[1]').get_attribute('id')
        initial_field_2_id = page.locator(f'//*[text()="Name"]//parent::tr//parent::thead//following-sibling::tbody/tr[2]').get_attribute('id')

        # Reverse the rows

        drag_handle_1 = page.locator(f'//*[text()="{custom_field_field_name_1}"]//parent::tr/td[7]/span/i')
        drag_handle_2 = page.locator(f'//*[text()="{custom_field_field_name_2}"]//parent::tr/td[7]/span/i')
        drag_handle_1.drag_to(drag_handle_2)

        # Grab the position of the rows after the reorder

        after_field_1_id = page.locator(f'//*[text()="Name"]//parent::tr//parent::thead//following-sibling::tbody/tr[1]').get_attribute('id')
        after_field_2_id = page.locator(f'//*[text()="Name"]//parent::tr//parent::thead//following-sibling::tbody/tr[2]').get_attribute('id')
       
        # Assert that the values do not match their initial values
        
        assert initial_field_1_id != after_field_1_id
        assert initial_field_2_id != after_field_2_id
