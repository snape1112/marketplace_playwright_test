import pytest
import re
from uuid import uuid4
from fixtures.constants import *
from fixtures.login import create_account, login
from playwright.sync_api import expect
import variables

def validate_appointment(page, customer_name, appointment_type, reminders):
    create_appointment(page, customer_name, appointment_type, reminders)
    view_appointment(page, appointment_type, reminders)

def create_appointment(page, customer_name, appointment_type, reminders):
    page.click('div.widget.borderless.overflowable:has-text("Appointments") a:has-text("New")')
    page.fill('input#appointment_modal_appointment_summary', 'Appointment ' + customer_name)

    # Set Appointment type
    page.select_option('select#appointment_modal_appointment_appointment_type_id', label = appointment_type)

    # Set Appointment reminders schedule
    page.select_option('#appointment_modal_appointment_appointment_reminders_schedule_id', label = reminders)

    page.wait_for_timeout(2000)
    page.click('input[value="Create Appointment"]')

    assert page.wait_for_selector('text=We scheduled it')

    # Verify that Appointment was created
    expect(page.locator('a.typed-pretty-link.tooltipper')).to_contain_text('Appointment')
    expect(page.locator('a.typed-pretty-link.tooltipper')).to_contain_text(customer_name)

def view_appointment(page, appointment_type, reminders):
    # Click View Appointment Details
    page.click('div.btn-group a.btn.btn-xs.btn-sm.dropdown-toggle')
    page.click('a.menu-default:has-text("View Details")')

    # Verify 'Appointment type' and 'Appointment reminders schedule' in the Appointment view
    expect(page.locator('div.widget-content p:has-text("Appointment Type")')).to_contain_text(appointment_type)
    expect(page.locator('div.widget-content p:has-text("Appointment Reminders:")')).to_contain_text(reminders)
