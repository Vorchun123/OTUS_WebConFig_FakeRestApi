from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from frontend.base_page import BasePage
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import allure
import pandas as pd
from pathlib import Path

CLIENT_ADDRESS = 48
SERVER_ADDRESS = 145
PASSWORD = '0000000100000001'


class NetworkParameters(BasePage):
    BUTTON_SIDEBAR_INDICATIONS = (By.ID, 'indications-link')
    BUTTON_SIDEBAR_NETWORK_PARAMETERS = (By.ID, 'indications-network-parameters-link')
    BUTTON_GET_DATA = (By.ID, 'getFromMeterButton')
    BUTTON_SAVE_DATA = (By.ID, 'saveReportButton')
    BLINK_ZONE = (By.ID, 'blink-zone')
    SERIAL_NUMBER = (By.ID, 'SerialNumber')
    PHASE_A_CURRENT = (By.ID, 'phaseACurrent, AValue')
    PHASE_A_VOLTAGE = (By.ID, 'phaseAVoltage, VValue')
    PHASE_A_ACTIVE_POWER = (By.ID, 'phaseAActive power, kW (P)Value')
    PHASE_A_REACTIVE_POWER = (By.ID, 'phaseAReactive power, kVar (Q)Value')
    PHASE_A_FULL_POWER = (By.ID, 'phaseAFull power, kVA (S)Value')
    PHASE_A_COEFFICIENT_POWER = (By.ID, 'phaseAPower coefficientValue')
    PHASE_A_TANGENT = (By.ID, 'phaseATanValue')
    PHASE_A_IN_PHASE_ANGLES = (By.ID, 'phaseAInpfase angles, °Value')
    PHASE_A_MAX_ACTIVE_POWER = (By.ID, 'phaseAMax active power, kWValue')
    FREQUENCY = (By.ID, 'anotherFrequency, HzValue')
    TEMPERATURE = (By.ID, 'anotherTemperature,  С°Value')
    NEUTRAL_CURRENT = (By.ID, 'anotherNeutral current, AValue')
    DIFFERENTIAL_CURRENT = (By.ID, 'anotherDifferential current, AValue')

    @allure.step('Переходим на страницу "Параметры сети"')
    def load_page_url(self):
        self.visit_page(f'http://localhost:5004/{self.get_meter_id()}/network_settings')

    def serial_meter_number(self):
        return self.get_text(*self.SERIAL_NUMBER)

    @allure.step('Переходим на страницу "Параметры сети" через боковую панель')
    def load_page_sidebar(self):
        self.click(*self.BUTTON_SIDEBAR_INDICATIONS)
        self.click(*self.BUTTON_SIDEBAR_NETWORK_PARAMETERS)

    @allure.step('Нажимаем на кнопку "Считать данные с устройства" и ждем загрузку таблицы "Параметры сети"')
    def click_button_get_data_and_wait_table(self):
        self.click(*self.BUTTON_GET_DATA)
        try:
            WebDriverWait(self.browser, 20).until(EC.invisibility_of_element_located(self.BLINK_ZONE))
        except Exception as e:
            self.error_action('Таблица параметров сети не загружена', element=e)
            raise

    @allure.step('Нажимаем на кнопку "Сохранить данные"')
    def click_button_save_data(self):
        self.click(*self.BUTTON_SAVE_DATA)

    @allure.step('Считываем параметры сети с WebConfig')
    def network_parameters_webconfig(self):
        ui_param = {self.PHASE_A_CURRENT: 'current',
                    self.PHASE_A_VOLTAGE: 'voltage',
                    self.PHASE_A_ACTIVE_POWER: 'active power',
                    self.PHASE_A_REACTIVE_POWER: 'reactive power',
                    self.PHASE_A_FULL_POWER: 'full power',
                    self.PHASE_A_COEFFICIENT_POWER: 'coefficient power',
                    self.PHASE_A_TANGENT: 'tangent',
                    self.PHASE_A_IN_PHASE_ANGLES: 'in phase angles',
                    self.PHASE_A_MAX_ACTIVE_POWER: 'max active power',
                    self.NEUTRAL_CURRENT: 'neutral current',
                    self.DIFFERENTIAL_CURRENT: 'differential current',
                    self.FREQUENCY: 'frequency',
                    self.TEMPERATURE: 'temperature'}
        result = {}
        try:
            for locator, key in ui_param.items():
                with allure.step(f'Читаем OBIS-код - {locator}'):
                    if key == 'voltage':
                        result[key] = (self.converting_str_in_float(*locator)) * 10
                    elif key == 'frequency':
                        result[key] = (self.converting_str_in_float(*locator)) * 100
                    elif key == 'temperature':
                        result[key] = (self.converting_str_in_float(*locator)) * 10
                    else:
                        result[key] = (self.converting_str_in_float(*locator)) * 1000
        except NoSuchElementException:
            pass
        return result

    @allure.tag('single-phase')
    @allure.step('Формируем данные на основе xlsx  файла')
    def read_xlsx_network_parameters(self, serial_meter_number):
        directory_path = Path.home() / 'Documents' / 'webconfig-user-data'
        excel_data = pd.read_excel(f'{directory_path}/Параметры сети {serial_meter_number}.xlsx',
                                   sheet_name='Параметры сети')
        excel_value = {0: 'current',
                       1: 'voltage',
                       2: 'active power',
                       3: 'reactive power',
                       4: 'full power',
                       5: 'coefficient power',
                       6: 'tangent',
                       7: 'in phase angles',
                       8: 'max active power',
                       10: 'neutral current',
                       11: 'differential current',
                       12: 'frequency',
                       13: 'temperature'}
        data_excel = {}
        for value, key in excel_value.items():
            data_excel[key] = excel_data['Unnamed: 1'].iloc[value]
        return data_excel
