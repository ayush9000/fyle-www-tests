import logging
from common.asserts import assert_thank_you_modal

logger = logging.getLogger(__name__)

def open_getdemo_form(browser):
    if browser.is_desktop():
        browser.click(xpath="//div[contains(@class, 'nav-item')]//a[contains(text(), 'Get a demo')]")
    else:
        browser.click(xpath="//div[contains(@class, 'sticky-cta-mobile')]/a")

def submit_getdemo_form(browser, email=None, firstname=None, lastname=None, phone=None, company_size=None, agree=None):
    if email:
        browser.input(xpath="//input[@name='email']", keys=email)
    if firstname:
        browser.input(xpath="//input[@name='firstname']", keys=firstname)
    if lastname:
        browser.input(xpath="//input[@name='lastname']", keys=lastname)
    if phone:
        browser.input(xpath="//input[@name='phone']", keys=phone)
    if company_size:
        browser.click(xpath="//input[@id='number_of_employees']")
        browser.click(xpath=f"//li[@value='{company_size}']")
    if agree:
        browser.click(xpath='//div[contains(@class, "custom-checkbox")]')
    browser.click(xpath='//button[text()=" Get a demo "]')

def assert_bad_email(browser):
    open_getdemo_form(browser)
    submit_getdemo_form(browser, email='foo')
    e = browser.find(xpath="//label[@for='demo-email'][@class='error']")
    assert e and e.is_displayed(), 'No error displayed for invalid email'

def assert_missing_firstname(browser):
    open_getdemo_form(browser)
    submit_getdemo_form(browser, email='megatron@fyle.in')
    e = browser.find(xpath="//label[@for='demo-first-name'][@class='error demo-first-name-error']")
    assert e and e.is_displayed(), 'No error displayed for missing firstname'

def assert_success(browser):
    open_getdemo_form(browser)
    submit_getdemo_form(browser, email='test@fyle.in', firstname='test', lastname='test', phone='123456789', company_size='Under 5', agree=True)
    e = browser.find(xpath="//h3[contains(text(), 'Thank')]")
    assert e and e.is_displayed(), 'Not displaying thank you message'
    ty_message = 'Sit back and relax. Our Sales team will get in touch with you within the next 24 hours to schedule a detailed demo.'
    assert_thank_you_modal(browser, ty_message, 'demoform')
