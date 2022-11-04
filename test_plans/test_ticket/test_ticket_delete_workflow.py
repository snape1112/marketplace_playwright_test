import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login 
from helpers.ticket import create_workflow
from playwright.sync_api import Page, expect
import variables

@pytest.mark.regression
def test_ticket_delete_workflow(page, login):

    workflow_name = str(uuid.uuid4())
    create_workflow(page, workflow_name)
    page.click('a[role="button"]:has-text("More")') 
    page.click('ul[role="menu"] >> text=Admin')
    with page.expect_navigation():
        page.click('text=Workflows') 

    page.once("dialog", lambda dialog: dialog.accept())
    
    page.click(f'//*[text()="{workflow_name}"]/parent::a/parent::th/parent::tr/td[3]/div/div[3]/a')
    page.locator(f'//*[text()="{workflow_name}"]') == None
