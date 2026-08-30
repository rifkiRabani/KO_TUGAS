from playwright.sync_api import sync_playwright, expect
import pytest
import allure
USERNAME = 'uno.testing3@gmail.com'
PW = '1234567890'
PRODUCT_PAGE = 'https://test.kelasotomesyen.com/products'

@allure.title('Valid login with valid credentials.')
@allure.description('this test case will validate user login with happy flow')
@allure.feature('Login')
@allure.testcase('https://test.kelasotomesyen.com/products/', name='TC-01-001')
@allure.suite('Login/')
@allure.severity(allure.severity_level.CRITICAL)

def test_valid_login(chrome):
        with allure.step('user attempt to fill email field'):
                chrome.get_by_test_id('login-email-input').fill(USERNAME)
        with allure.step('user attempt to fill password field'):
                chrome.get_by_test_id('login-password-input').fill(PW)
        with allure.step('user attempt to click submit button'):
                chrome.get_by_test_id('login-submit-button').click()
        with allure.step('user validate user is in product page'):
                expect(chrome).to_have_url(PRODUCT_PAGE)
                current_url = chrome.url
                assert current_url == PRODUCT_PAGE
                
@allure.title(' login with invalid credentials.')
@allure.description('this test case will validate user login with negative flow')
@allure.feature('Login')
@allure.testcase('https://test.kelasotomesyen.com/products/', name='TC-01-002')
@allure.suite('Login/')
@allure.severity(allure.severity_level.CRITICAL)

def test_invalid_pw(chrome):
        with allure.step('user attempt to fill email field'):
                chrome.get_by_test_id('login-email-input').fill(USERNAME)
        with allure.step('user attempt to fill password field'):
                chrome.get_by_test_id('login-password-input').fill('invalid_pw')
        with allure.step('user attempt click submit button'):
                chrome.get_by_test_id('login-submit-button').click()
        with allure.step('user attempt to validate login error'):
                expect(chrome.get_by_test_id('login-error')).to_be_visible()
                current_url = chrome.url
                assert current_url != PRODUCT_PAGE

@pytest.mark.parametrize(
        'test_id, email, password, field, expected',
        [pytest.param('TC-01-003', '!uno.testing3@gmail.com!', PW, 'login-email-input', "A part following '@' should not contain the symbol '!'.", id='3'),
         pytest.param('TC-01-004','uno.testing3', PW, 'login-email-input', "Please include an '@' in the email address. 'uno.testing3' is missing an '@'.", id='4'),
         pytest.param('TC-01-005','', PW, 'login-email-input', "Please fill out this field.", id='5'),
         pytest.param('TC-01-006','uno.testing3@gmail.com', '', 'login-password-input', "Please fill out this field.", id='6')]
)
@allure.suite('Login/')
def test_login_validation(chrome, test_id, email, password, field, expected):
        allure.dynamic.title(f'Login Validation - {field} - "{email}"/"{password}"')
        allure.dynamic.description(f'Validate error message for field "{field}" when input is invalid or empty')
        allure.dynamic.testcase(f'https://test.kelasotomesyen.com/products/', name=f'{test_id}')
        with allure.step(f'user attempt to fill email field with "{email}"'):
                chrome.get_by_test_id('login-email-input').fill(email)
        with allure.step(f'user attempt to fill password field with "{password}"'):
                chrome.get_by_test_id('login-password-input').fill(password)
        with allure.step(f'user attempt click submit button'):
                chrome.get_by_test_id('login-submit-button').click()
        with allure.step(f'user attempt to validate error message on "{field}"'):
                message = chrome.get_by_test_id(field).evaluate('element => element.validationMessage')
                assert message == expected
