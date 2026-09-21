from frontend.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class ConnectionPageElectricityMeter(BasePage):
    URL = 'http://host.docker.internal:5004/setting/connection'
    TYPE_INTERFACE = (By.ID, 'connectionTypeSelector')
    PORT = (By.ID, 'connectionPortSelector')
    HOST = (By.ID, 'connectionHostForTcpIpInput')
    PORT_IP = (By.ID, 'connectionPortForTcpIpInput')
    TYPE_AUTHORIZATION = (By.ID, 'clientTypeSelector')
    PASSWORD = (By.ID, 'meter-password')
    LOGICAL_ADDRESS_INPUT = (By.ID, 'meterLogicalAddress')
    PHYSICAL_ADDRESS_INPUT = (By.ID, 'serverAddressByDevPhysicalInput')
    SIZE_SELECTOR = (By.ID, 'serverAddressByDevSizeSelector')
    TIMEOUT_INPUT = (By.ID, 'additionallyTimeOutInput')
    RETRIES_INPUT = (By.ID, 'additionallyResendedDataInput')
    DELAY_INPUT = (By.ID, 'additionallyDelayInput')
    PDU_INPUT = (By.ID, 'maxPduSizeInput')
    KEEP_ALIVE_INPUT = (By.ID, 'keep-alive-period-input')
    BUTTON_DISCONNECT = (By.CSS_SELECTOR, '[class="btn rounded-0 border-0 btn-danger"]')
    BUTTON_CONNECTION = (By.ID, 'ConnectionButton')
    CURRENT_STATUS = (By.ID, 'NotificationComponent')
    BUTTON_READ_METER_DATA = (By.ID, 'passportReadButton')

    def load_page_url(self):
        self.visit_page(self.URL)
        return self

    def opto(self, port):
        self.dropdown(*self.TYPE_INTERFACE, value='Opto')
        self.dropdown(*self.PORT, value=port)
        return self

    def rs_485(self, port="COM3"):
        self.dropdown(*self.TYPE_INTERFACE, value='Rs485')
        self.dropdown(*self.PORT, value=port)
        return self

    def tcp_ip(self, host, port_ip):
        self.dropdown(*self.TYPE_INTERFACE, value='TcpIp')
        self.send_keys(*self.HOST, text=host)
        self.clear(*self.PORT_IP)
        self.send_keys(*self.PORT_IP, text=port_ip)
        return self

    def authorization_configuration(self, password='0000000100000001'):
        self.dropdown(*self.TYPE_AUTHORIZATION, value='ConfiguratorAccess')
        self.clear(*self.PASSWORD)
        self.send_keys(*self.PASSWORD, text=password)
        return self

    def authorization_read(self, password='00000001'):
        self.dropdown(*self.TYPE_AUTHORIZATION, value='ReaderAccess')
        self.clear(*self.PASSWORD)
        self.send_keys(*self.PASSWORD, text=password)
        return self

    def authorization_public(self):
        self.dropdown(*self.TYPE_AUTHORIZATION, value='PublicAccess')
        return self

    def server_address(self, log_address='1', physic_address='17', size_selector='4'):
        self.clear(*self.LOGICAL_ADDRESS_INPUT)
        self.send_keys(*self.LOGICAL_ADDRESS_INPUT, text=log_address)
        self.clear(*self.PHYSICAL_ADDRESS_INPUT)
        self.send_keys(*self.PHYSICAL_ADDRESS_INPUT, text=physic_address)
        self.dropdown(*self.SIZE_SELECTOR, value=size_selector)
        return self

    def additionally(self, timeout='5000', retries='3', delay='0', pdu='65635', keep_alive='5000'):
        self.clear(*self.TIMEOUT_INPUT)
        self.send_keys(*self.TIMEOUT_INPUT, text=timeout)
        self.clear(*self.RETRIES_INPUT)
        self.send_keys(*self.RETRIES_INPUT, text=retries)
        self.clear(*self.DELAY_INPUT)
        self.send_keys(*self.DELAY_INPUT, text=delay)
        self.clear_keys(*self.PDU_INPUT)
        self.send_keys(*self.PDU_INPUT, text=pdu)
        self.clear_keys(*self.KEEP_ALIVE_INPUT)
        self.send_keys(*self.KEEP_ALIVE_INPUT, text=keep_alive)
        return self

    @allure.step('Подключаемся к WebConfig')
    def connection(self):
        try:
            if self.get_color(*self.BUTTON_CONNECTION) == 'rgba(25, 135, 84, 1)':
                self.scroll(*self.BUTTON_CONNECTION)
                self.click(*self.BUTTON_CONNECTION)
                WebDriverWait(self.browser, 50).until(
                    EC.visibility_of_element_located(self.BUTTON_READ_METER_DATA))
            else:
                self.click(*self.BUTTON_CONNECTION)
                WebDriverWait(self.browser, 50).until(
                    lambda browser: self.get_text(*self.BUTTON_CONNECTION) == 'Подключиться')
                self.click(*self.BUTTON_CONNECTION)
                WebDriverWait(self.browser, 20).until(
                    EC.visibility_of_element_located(self.BUTTON_READ_METER_DATA))
        except Exception as e:
            self.error_action('Не смогли подключиться', element=e)
            raise
        return self

    @allure.step('Отключаемся от WebConfig')
    def disconnection(self):
        try:
            if self.visible(*self.BUTTON_DISCONNECT):
                self.scroll(*self.BUTTON_DISCONNECT)
                self.click(*self.BUTTON_DISCONNECT)
                WebDriverWait(self.browser, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, '[class="btn rounded-0 border-0 btn-success"]')))
        except Exception as e:
            self.error_action('Не смогли отключиться', element=e)
            raise

    @allure.step('Проверяем текущий статус')
    def checking_status(self, text):
        self.checking_text(*self.CURRENT_STATUS, expected_value=text)

    @allure.step('Ожидаем текущий статус')
    def wait_status(self, text):
        try:
            WebDriverWait(self.browser, 50).until(EC.text_to_be_present_in_element(self.CURRENT_STATUS, text))
        except Exception:
            self.error_action('Некорректная информационная ошибка в конфигураторе',
                              element=self.get_text(*self.CURRENT_STATUS))
            raise
