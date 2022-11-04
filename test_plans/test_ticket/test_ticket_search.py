import pytest
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.ticket import Ticket
from playwright.sync_api import expect
import variables

@pytest.mark.regression
@pytest.mark.smoke
def test_ticket_search(page, login, api_request_context):

    # Preconditions: create customer and tickets

    ticket1 = Ticket(subject = 'Printer not working', problem_type = 'Contract Work', description = 'Please fix my printer')
    ticket1.create(api_request_context)

    ticket2 = Ticket(customer_id = ticket1.customer_id, status= "In Progress", subject = 'Subject2', problem_type = 'Remote Support', description = 'Description for ticket2')
    ticket2.create(api_request_context)

    ticket3 = Ticket(customer_id = ticket1.customer_id, status = "Customer Reply", subject = 'Subject3', problem_type = 'Network Project', description = 'Description for ticket3')
    ticket3.create(api_request_context)

    # Test 1, Ticket search by Subject
    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets')

    page.fill('div.input-group input#ticket_search_query_all_fields', ticket2.subject)
    page.click('div.input-group span.input-group-btn:has-text("Search")')

    locator = page.locator('div.widget-content')

    expect(locator).to_contain_text("Subject2")
    expect(locator).not_to_contain_text("Subject3")

    # Test 2,  Apply Filter with Ticket search by Status
    # Reload the tickes page
    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets')
    # Select status "New"
    page.click('div.form-group:has-text("Status is"):nth-child(3) button.dropdown-toggle')
    page.click('div.btn-group.open label:has-text("New")')

    # Click button 'Apply'
    page.click('input[value="Apply"]')

    # Verify after Apply filter we have the ticket with status 'New' and don't have tickets with 'In Progress' and 'Customer Reply' statuses on the page
    expect(page.locator('div.widget-content')).to_contain_text("New")
    expect(page.locator('div.widget-content')).not_to_contain_text("In Progress")
    expect(page.locator('div.widget-content')).not_to_contain_text("Customer Reply")

    # Test 3, Create new filter
    # Turn off previous filters
    page.click('a.btn.btn-default.btn-sm.dropdown-toggle')
    page.click('a.menu-default:has-text("All")')
    expect(page.locator('div.widget-content')).to_contain_text("Printer not working")
    expect(page.locator('div.widget-content')).to_contain_text("Subject2")
    expect(page.locator('div.widget-content')).to_contain_text("Subject3")

    # Create new search by clicking on 'Saved Search' button with 'filter' icon > then click 'Create New'
    page.click('a.btn.btn-default.btn-sm.dropdown-toggle')
    page.click('text=Create New')

    # Verify 'New Saved Ticket Search' text exist on the page
    assert page.locator('div.modal-header h3:has-text("New Saved Ticket Search")').inner_text() != None

    # Select fields in 'New Saved Ticket Search' form
    page.fill('input#ticket_search_name', 'Filter1')
    # Set ticket search as not default
    page.select_option('select#ticket_search_set_as_default', value = 'false')
    # Set ticket search as public
    page.select_option('select#ticket_search_public', label = 'Public')
    # Select Ticket Status
    page.click('div.ticket_search_query_status_is')
    page.click(f'div.ticket_search_query_status_is li:has-text("{ticket1.status}")')
    # Click anywhere to lose focus from multiselect
    page.click('h3:has-text("New Saved Ticket Search")')

    # Select Problem Type
    page.click('div.ticket_search_query_problem_type_is')
    page.click(f'div.ticket_search_query_problem_type_is li:has-text("{ticket1.problem_type}")')
    # Click anywhere to lose focus from multiselect
    page.click('h3:has-text("New Saved Ticket Search")')

    # Click 'Create Ticket Search' button
    page.click('input:has-text("Create Ticket Search")')

    # Verify that we have ticket with ticket_id in the search table and it has status 'New', issue type 'Contract Work'
    row_with_ticket1 = page.locator(f'div#bhv-ticketTable tr.bhv-ticketRow{ticket1.ticket_id}')
    expect(row_with_ticket1).to_contain_text("New")
    expect(row_with_ticket1).to_contain_text("Contract Work")

    # Verify we have Filter1 selected
    assert page.locator('div.btn-group a.dropdown-toggle:has-text("Filter1")').inner_text() != None

    # Test 4, Filter edit, set filter as default, set filter private, filter rename,
    # Go to page tickets, verify we have filter default as false
    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets')

    assert page.locator('a.btn.btn-default.btn-sm.dropdown-toggle:has-text("Saved Search")').inner_text() != None
    assert page.query_selector('a.btn.btn-default.btn-sm.dropdown-toggle:has-text("Filter1")') == None
    # Click on 'Saved Search' button
    page.click('a.btn.btn-default.btn-sm.dropdown-toggle')
    # Click 'Modify Filters'
    page.click('a.menu-default:has-text("Modify Filters")')

    # Verify table on the ticket searches page cantain search with Filter1 name  and this search is Public and Not Default
    expect(page.locator('div.widget-content')).to_contain_text("Filter1")
    expect(page.locator('div.widget-content')).to_contain_text("Public")
    expect(page.locator('div.widget-content')).to_contain_text("Make Default")
    # Click button Edit
    page.click('a.btn.btn-default:has-text("Edit")')

    # Verify 'Edit Saved Ticket Search' text exist on the page
    assert page.locator('div.modal-header h3:has-text("Edit Saved Ticket Search")').inner_text() != None

    # Modify filter name
    page.fill('input#ticket_search_name', 'Filter3')

    # Set ticket search as default
    page.select_option('select#ticket_search_set_as_default', value = 'true')

    # Set ticket search as Private
    page.select_option('select#ticket_search_public', label = 'Private')

    # Select Ticket Status
    page.click('div.form-group.ticket_search_query_status_is:has-text("Status is") button:has-text("New")')
    page.click(f'div.form-group.ticket_search_query_status_is:has-text("Status is") label:has-text("{ticket1.status}")')
    page.click(f'div.form-group.ticket_search_query_status_is:has-text("Status is") label:has-text("{ticket3.status}")')
    # Click anywhere to lose focus from multiselect
    page.click('h3:has-text("Edit Saved Ticket Search")')

    # Select Problem Type
    page.click('div.ticket_search_query_problem_type_is')
    page.click(f'div.ticket_search_query_problem_type_is label:has-text("{ticket1.problem_type}")')
    page.click(f'div.ticket_search_query_problem_type_is label:has-text("{ticket3.problem_type}")')
    # Click anywhere to lose focus from multiselect
    page.click('h3:has-text("Edit Saved Ticket Search")')

    # Click 'Update Ticket Search' button
    page.click('input:has-text("Update Ticket Search")')

    # Verify that we have ticket with ticket_id in the search table and it has status '', issue type ''
    row_with_ticket3 = page.locator(f'div#bhv-ticketTable tr.bhv-ticketRow{ticket3.ticket_id}')
    expect(row_with_ticket3).to_contain_text("Subject3")
    expect(row_with_ticket3).to_contain_text("Customer Reply")
    expect(row_with_ticket3).to_contain_text("Network Project")


    # Reload page
    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets')
    # Verify default filter is set
    assert page.locator('a.btn.btn-default.btn-sm.dropdown-toggle:has-text("Filter3")').inner_text() != None

    # Click on 'Filter3' button
    page.click('a.btn.btn-default.btn-sm.dropdown-toggle')
    # Click 'Modify Filters'
    page.click('a.menu-default:has-text("Modify Filters")')

    # Verify table on the ticket searches page contain search with  Filter3 name  and this search is Private and Default
    expect(page.locator('div.widget-content')).to_contain_text("Filter3")
    expect(page.locator('div.widget-content')).to_contain_text("Private")
    expect(page.locator('div.widget-content')).to_contain_text("Default - Remove Default")

    # Test 5 Delete Ticket search
    # Click on Delete button
    page.on("dialog", lambda dialog: dialog.accept())
    page.click('tr:has-text("Filter3") a.btn-danger')

    # Check that Ticket search Filter3 was deleted
    page.click('a.btn.btn-default.btn-sm.dropdown-toggle')
    expect(page.locator('div.btn-group.open ul.dropdown-menu:has-text("All")')).not_to_contain_text("Filter3")
    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets')

    # Test 6 Confirm Sort by 'Issue'
    # Click Saved Searches -> New Ticket Search
    page.click('a.btn.btn-default.btn-sm.dropdown-toggle')
    page.click('text=Create New')
    page.fill('input#ticket_search_name', 'Confirm Sort Filter')

    # Select Ticket Status
    page.click('div.ticket_search_query_status_is')
    page.click(f'div.ticket_search_query_status_is li:has-text("{ticket1.status}")')
    page.click(f'div.ticket_search_query_status_is li:has-text("{ticket2.status}")')
    page.click(f'div.ticket_search_query_status_is li:has-text("{ticket3.status}")')

    # Select Issue from Sort column
    page.select_option('select#ticket_search_sort_column', 'Issue')

    # Click 'Create Ticket Search' button
    page.click('input:has-text("Create Ticket Search")')

    # Check that image 'down' appears next to the text 'Issue' in the header in the tickets table,
    # so tickets are sorted by 'Issue' in the reverse alphabetical order
    assert page.locator('th:has-text("Issue") a.current.down') != None

    # Check that column Issue has records in the reverse alphabetical order in the tickets table
    expect(page.locator('div#bhv-ticketTable tbody tr:nth-child(1)')).to_contain_text('Remote Support')
    expect(page.locator('div#bhv-ticketTable tbody tr:nth-child(2)')).to_contain_text('Network Project')
    expect(page.locator('div#bhv-ticketTable tbody tr:nth-child(3)')).to_contain_text('Contract Work')

    # Turn off previous filters
    page.click('a.btn.btn-default.btn-sm.dropdown-toggle')
    page.click('a.menu-default:has-text("All")')

    # Check that column Issue records doesn't sorted by Issue and sorted by ticket number in the tickets table
    expect(page.locator('div#bhv-ticketTable tbody tr:nth-child(1)')).to_contain_text(str(ticket1.number))
    expect(page.locator('div#bhv-ticketTable tbody tr:nth-child(1)')).to_contain_text("Contract Work")

    expect(page.locator('div#bhv-ticketTable tbody tr:nth-child(2)')).to_contain_text(str(ticket2.number))
    expect(page.locator('div#bhv-ticketTable tbody tr:nth-child(2)')).to_contain_text("Remote Support")

    expect(page.locator('div#bhv-ticketTable tbody tr:nth-child(3)')).to_contain_text(str(ticket3.number))
    expect(page.locator('div#bhv-ticketTable tbody tr:nth-child(3)')).to_contain_text("Network Project")

    # Test 7 Set Primary Grouping test
    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets')

    expect(page.locator('div#bhv-ticketTable')).to_contain_text(str(ticket1.number))
    expect(page.locator('div#bhv-ticketTable')).to_contain_text(str(ticket2.number))
    expect(page.locator('div#bhv-ticketTable')).to_contain_text(str(ticket3.number))


    # Click the 'Grouping Options' icon
    page.click('div.btn-group.search-action-btns i.fas.fa-object-group.tooltipper')

    # Select primary grouping by Status
    page.select_option('select#primary_grouping', 'Status')
    # Click 'Apply'
    page.click('form.form-inline a#update-grouping:has-text("Apply")')

    # Verify the first filter group contains the status 'Customer Reply' and does not contain other statuses at the table header
    assert page.locator('div.widget-header h3:has-text("Customer Reply")').inner_text() != None
    expect(page.locator('div.widget-header h3:has-text("Customer Reply")')).not_to_contain_text("New")
    expect(page.locator('div.widget-header h3:has-text("Customer Reply")')).not_to_contain_text("In Progress")

    # Verify the first filter group contains the status 'Customer Reply' and does not contain other statuses in the table
    expect(page.locator('div#bhv-ticketTable div.widget.overflowable:nth-child(1)')).to_contain_text(str(ticket3.number))
    expect(page.locator('div#bhv-ticketTable div.widget.overflowable:nth-child(1)')).to_contain_text("Customer Reply")

    expect(page.locator('div#bhv-ticketTable div.widget.overflowable:nth-child(1)')).not_to_contain_text("New")
    expect(page.locator('div#bhv-ticketTable div.widget.overflowable:nth-child(1)')).not_to_contain_text("In Progress")

    # Verify the second filter group contains the status 'New' and does not contain another statuses at the table header
    assert page.locator('div.widget-header h3:has-text("New")').inner_text() != None
    expect(page.locator('div.widget-header h3:has-text("New")')).not_to_contain_text("Customer Reply")
    expect(page.locator('div.widget-header h3:has-text("New")')).not_to_contain_text("In Progress")

    # Verify the second filter group contains the status 'New' and does not contain other statuses in the table
    expect(page.locator('div#bhv-ticketTable div.widget.overflowable:nth-child(3)')).to_contain_text(str(ticket1.number))
    expect(page.locator('div#bhv-ticketTable div.widget.overflowable:nth-child(3)')).to_contain_text("New")

    expect(page.locator('div#bhv-ticketTable div.widget.overflowable:nth-child(3)')).not_to_contain_text("Customer Reply")
    expect(page.locator('div#bhv-ticketTable div.widget.overflowable:nth-child(3)')).not_to_contain_text("In Progress")

    # Verify the third filter group contains the status 'In Progress' and does not contain other statuses at the table header
    assert page.locator('div.widget-header h3:has-text("In Progress")').inner_text() != None
    expect(page.locator('div.widget-header h3:has-text("In Progress")')).not_to_contain_text("Customer Reply")
    expect(page.locator('div.widget-header h3:has-text("In Progress")')).not_to_contain_text("New")

    # Verify the third filter group contains the status 'New' and does not contain other statuses in the table
    expect(page.locator('div#bhv-ticketTable div.widget.overflowable:nth-child(5)')).to_contain_text(str(ticket2.number))

    expect(page.locator('div#bhv-ticketTable div.widget.overflowable:nth-child(5)')).not_to_contain_text("Customer Reply")
    expect(page.locator('div#bhv-ticketTable div.widget.overflowable:nth-child(5)')).not_to_contain_text("New")

    # Test 8 Set Secondary Grouping test
    page.select_option('select#secondary_grouping', 'Issue')
    # Click 'Apply'
    page.click('form.form-inline a#update-grouping:has-text("Apply")')

    # Verify the first filter group contains the status 'Customer Reply' and issue 'Network Project'
    assert page.locator('div.widget-header h3:has-text("Customer Reply: Network Project")').inner_text() != None
    # Verify the first filter group contains 'Customer Reply: Network Project' and does not contain other statuses in the table
    expect(page.locator('div#bhv-ticketTable div.widget.overflowable:nth-child(1)')).to_contain_text(str(ticket3.number))
    expect(page.locator('div#bhv-ticketTable div.widget.overflowable:nth-child(1)')).to_contain_text("Customer Reply")

    expect(page.locator('div#bhv-ticketTable div.widget.overflowable:nth-child(1)')).not_to_contain_text("New")
    expect(page.locator('div#bhv-ticketTable div.widget.overflowable:nth-child(1)')).not_to_contain_text("In Progress")

    # Turn off the 'Grouping' filter
    page.select_option('select#primary_grouping', 'None')
    # Click 'Apply'
    page.click('form.form-inline a#update-grouping:has-text("Apply")')

