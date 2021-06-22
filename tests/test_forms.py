from pylenium.driver import Pylenium
import pytest
from faker import Faker
import json

fake = Faker(['en-us'])

with open("./pylenium.json", "r") as caps:
    caps_loaded = json.load(caps)

attributes = caps_loaded['custom']
browser_targets = [attributes['capabilities']['desktop'][0]]


def form_text_entry_and_submit(py):
    url = attributes['urls'][0]

    py.visit(url)

    text_inputs = py.find('input[type="text"]')
    num_inputs = py.find('input[type="number"]')
    email_inputs = py.find('input[type="email"]')
    address_inputs = py.find('input[type="address"]')
    textareas = py.find('textarea')
    select_dropdowns = py.find('select')
    submit_button = py.get('#submit-holder-form-1').get('button')
    checkboxes = py.find('input[type="checkbox"]')
    radio_buttons = py.find('input[type="radio"]')
    checks_and_radios = checkboxes.append(radio_buttons)

    print(text_inputs,
          num_inputs,
          email_inputs,
          address_inputs,
          textareas,
          submit_button,
          checkboxes,
          radio_buttons,
          checks_and_radios)

    # date-picker
    # stripe
    # upload
    # state

    # todo: check against what is actually available in Twill
    # https://www.w3schools.com/html/html_form_input_types.asp

    for text in text_inputs:
        text.type(fake.lexify(text='??????????'))

    for address in address_inputs:
        address.type(fake.street_address())

    for num in num_inputs:
        num.type(fake.random_digit())

    for email in email_inputs:
        email.type(fake.company_email())

    for textarea in textareas:
        textarea.type(fake.paragraph(nb_sentences=5))

    for select in select_dropdowns:
        select.select_by_index(1)

    for check_and_radio in checks_and_radios:
        check_and_radio.check()

    submit_button.click()

@pytest.mark.parametrize('browser', browser_targets)
def test_forms(py: Pylenium, browser):
    py.config.driver.capabilities.update({"build": "forms automation"})
    py.config.driver.capabilities.update(browser)
    form_text_entry_and_submit(py)
