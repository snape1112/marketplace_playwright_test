import pytest
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.ticket import Ticket, wait_for_worker
from playwright.sync_api import expect
import variables

global_filestack_upload_finished = False
global_syncro_upload_finished = False

def wait_for_filestack_upload(request):
    global global_filestack_upload_finished
    if 'complete' in request.url:
        global_filestack_upload_finished = True

def wait_for_syncro_upload(dialog):
    global global_syncro_upload_finished
    dialog.accept()
    global_syncro_upload_finished = True


@pytest.mark.regression
def test_ticket_attachment(page, login, api_request_context):
    # Prerequisites
    ticket = Ticket()
    ticket.create(api_request_context)

    # Go to ticket page
    page.goto(f'{variables.base_url}/tickets/{ticket.ticket_id}')

    # Click 'Upload' button
    page.click('div.widget.borderless.overflowable a.filepicker.btn.btn-widget.btn-sm:has-text("Upload")')

    # Upload test_ticket_attachment.py file
    page.set_input_files('input#fsp-fileUpload', __file__)

    # Register async upload handler
    page.on("requestfinished", wait_for_filestack_upload)
    page.on("dialog", wait_for_syncro_upload)

    # We need to wait for the upload to Filestack to finish
    # Wait and check the global flag for finished upload
    for i in range(1, 20) :
        if global_filestack_upload_finished:
            break
        page.wait_for_timeout(2000)

    page.click('div.fsp-footer span[title="Upload"]')

    # We need to wait for the upload to Syncro to finish
    # Wait and check the global flag for finished upload
    for i in range(1, 30) :
        if global_syncro_upload_finished:
            break
        page.wait_for_timeout(2000)

    # We are processing the upload, refresh the page until we get our selector.
    # Wait until the dialog handler finish the page reloading in the other async thread
    # Without the wait_for_timeout here wait_for_worker context will be destroyed in the middle of query_selector
    page.wait_for_timeout(5000)
    wait_for_worker(page, 'a.attachment-title')

    # Verify that the file was uploaded
    expect(page.locator('div.widget:has-text("Attachment")')).to_contain_text('test_ticket_attachment.py')

    # Click Remove attachment
    page.click('div.btn-group a.btn.btn-xs.btn-sm.dropdown-toggle:has-text("•••")')
    page.click('ul.dropdown-menu a[data-method="delete"]:has-text("Remove")')

    # Verify that the file was removed
    expect(page.locator('div.widget:has-text("Attachment")')).not_to_contain_text('test_ticket_attachment.py')