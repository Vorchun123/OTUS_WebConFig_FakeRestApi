from selenium.common import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import inspect
import allure


class BasePage:
    def __init__(self, browser):
        self.meter_id = None
        self.browser = browser
        self.logger = browser.logger
        self.media = None
        self.client = None
        self.reader = None
        self.reply = None
        self.class_name = type(self).__name__

    def local_log(self, message):
        self.logger.info(f'{self.class_name}: {message}')

    def visit_page(self, url):
        self.local_log(f'Opening url: {url}')
        return self.browser.get(url)

    def get_meter_id(self):
        current_url = self.browser.current_url
        parse_url = current_url.split('/')
        self.meter_id = parse_url[3]
        return self.meter_id

    def get_current_function_name(self):
        return inspect.currentframe().f_back.f_code.co_name

    def error_action(self, error_text, locator=None, element=None):
        func_name = self.get_current_function_name()
        self.logger.error(f'{self.class_name} {error_text} {locator} {element} ')
        self.browser.save_screenshot(f'screenshot/{self.class_name}_{func_name}.png')
        screenshot = self.browser.get_screenshot_as_png()
        allure.attach(screenshot, f'{self.class_name}_{func_name}.png', allure.attachment_type.PNG)

    def find_element(self, *locator):
        self.local_log(f'Find element: {locator}')
        try:
            return self.browser.find_element(*locator)
        except Exception as e:
            self.error_action('Error find element:', locator, element=e)
            raise

    def find_elements(self, *locator):
        self.local_log(f'Find elements: {locator}')
        try:
            return self.browser.find_elements(*locator)
        except Exception as e:
            self.error_action('Error find elements:', locator, element=e)
            raise

    def click(self, *locator):
        self.local_log(f'Click to element: {locator}')
        self.find_element(*locator).click()

    def dropdown(self, *locator, value):
        self.local_log(f'Open element {value} in the drop-down menu {locator}')
        select = Select(self.find_element(*locator))
        select.select_by_value(value)

    def clear(self, *locator):
        self.local_log(f'Clear all in element {locator}')
        self.find_element(*locator).clear()

    def clear_keys(self, *locator):
        self.local_log(f'Clear all in element {locator}')
        self.find_element(*locator).send_keys(Keys.CONTROL + 'a')
        self.find_element(*locator).send_keys(Keys.DELETE)

    def send_keys(self, *locator, text):
        self.local_log(f'Input field: {locator}, input text: {text}')
        self.find_element(*locator).send_keys(text)

    def get_text(self, *locator):
        self.local_log(f'Get text: {locator}')
        return str(self.find_element(*locator).text)

    def get_color(self, *locator):
        self.local_log(f'Get color: {locator}')
        return self.find_element(*locator).value_of_css_property('background-color')

    def converting_str_in_float(self, *locator):
        text_value = self.get_text(*locator)
        self.local_log(f'Converting str_value - {text_value} in float')
        float_value = float(text_value.replace(',', '.'))
        return float_value

    def visible(self, *locator):
        self.local_log(f'Check that the {locator} is visible')
        return self.find_element(*locator).is_displayed()

    def scroll(self, *locator):
        self.local_log(f'Scroll to the {locator}')
        self.browser.execute_script("arguments[0].scrollIntoView(true);", self.find_element(*locator))

    def count_elements(self, *locator):
        self.local_log(f'Get count in {locator}')
        return len(self.browser.find_elements(*locator))

    def refresh(self):
        self.local_log(f'Refresh page')
        self.browser.refresh()

    def checking_text(self, *locator, expected_value):
        try:
            actual_value = self.get_text(*locator)
            self.logger.info(f'{self.class_name} Checking {locator} with {expected_value}')
            assert actual_value == expected_value, f'Expected value: {expected_value}, received value: {actual_value}'
        except Exception as e:
            self.error_action('Error getting text from element', locator, element=e)
            raise

    def generating_data_for_comparison_gurux(self, parameters, gurux_area, attribute_index):
        result = {}
        try:
            for obis_code, key in parameters.items():
                with allure.step(f'Читаем OBIS-код - {obis_code}'):
                    result[key] = self.read_data_gurux(gurux_area, obis_code, attribute_index)
        except NoSuchElementException:
            print(f"OBIS-код {obis_code} отсутствует")
            pass
        return result

    def generating_data_for_comparison_ui(self, parameters, for_what):
        result = {}
        try:
            for locator, key in parameters.items():
                with allure.step(f'Читаем OBIS-код - {locator}'):
                    if for_what == 'gurux':
                        result[key] = (self.converting_str_in_float(*locator)) * 1000
                    else:
                        result[key] = self.get_text(*locator)
        except NoSuchElementException:
            pass
        return result
