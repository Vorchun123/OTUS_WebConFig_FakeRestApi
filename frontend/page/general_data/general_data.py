from frontend.page.connection_page.connection_page_electricity_meter import ConnectionPageElectricityMeter
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

COM_PORT = 'COM26'
CLIENT_ADDRESS = 48
SERVER_ADDRESS = 145
PASSWORD = '0000000100000001'


class General(ConnectionPageElectricityMeter):
    BUTTON_SAVE_DATA = (By.ID, 'readAllObjectModelButton')
    PASSPORT_METER_TYPE = (
        By.CSS_SELECTOR, '[class = "container-fluid"] > [class="row mb-3"]:nth-child(2) > [class="col-sm-5"]')
    BUTTON_READ_PASSPORT_DATA = (By.ID, 'readByPassportDataButton')
    ALL_PASSPORT_DATA = (By.CSS_SELECTOR, '[class="container-fluid"]')
    SERIAL_NUMBER = (By.ID, 'SerialNumber')
    METER_TYPE = (By.ID, 'MeterType')
    METER_RELEASE_DATE = (By.ID, 'ProductionDate')
    MANUFACTURER = (By.ID, 'Manufacturer')
    METROLOGICAL_SOFTWARE_VERSION = (By.ID, 'SoftwareVersionMetrological')
    INSIGNIFICANT_SOFTWARE_VERSION = (By.ID, 'SoftwareVersionInsignificant')
    FIRMWARE_VERSION = (By.ID, 'FirmwareVersion')
    MI_VERSION = (By.ID, 'InterfaceModuleVersion')
    CURRENT_TARIFF = (By.ID, 'CurrentTariff')
    CHECKSUM_METROLOGICAL_SOFTWARE = (By.ID, 'Crc')
    CHECKSUM_INSIGNIFICANT_SOFTWARE = (By.ID, 'CrcInsignificant')
    AMPERAGE_TRANSFORM_COEFFICIENT = (By.ID, 'TransformCoefficientAmperage')
    VOLTAGE_TRANSFORM_COEFFICIENT = (By.ID, 'TransformCoefficientVoltage')
    FIRMWARE_NAME = (By.ID, 'FirmwareName')
    PROTOCOL_SPODES_VERSION = (By.ID, 'ProtocolVersion')
    PROTOCOL_EXTENDED_SPODES_VERSION = (By.ID, 'ProtocolExtendedVersion')
    SWITCHING_SCHEME = (By.ID, 'SwitchingScheme')

    def load_page_url(self):
        self.visit_page(f'http://host.docker.internal:5004/{self.get_meter_id()}/general_data')

    def refresh_page_and_wait_button(self):
        self.refresh()
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located(self.BUTTON_SAVE_DATA))

    def save_data(self):
        self.click(*self.BUTTON_SAVE_DATA)

    def get_meter_type(self):
        return self.get_text(*self.METER_TYPE)

    def get_passport_meter_type(self):
        return self.get_text(*self.PASSPORT_METER_TYPE)

    def read_passport_data(self):
        self.click(*self.BUTTON_READ_PASSPORT_DATA)

    def get_all_passport_data(self):
        return self.get_text(*self.ALL_PASSPORT_DATA)

    @allure.step('Считываем общие данные с ПУ')
    def general_data_gurux(self, com_port):
        with allure.step(f'Подключаемся к ПУ с параметрами: com port - {com_port}, client address - {CLIENT_ADDRESS},'
                         f' server address - {SERVER_ADDRESS}, password - {PASSWORD}'):
            self.open_gurux(com_port, CLIENT_ADDRESS, SERVER_ADDRESS, PASSWORD)
        obis_param = {'0.0.96.1.0.255': 'serial_number',
                      '0.0.96.1.1.255': 'meter_type',
                      '0.0.96.1.4.255': 'meter_release_date',
                      '0.0.96.1.3.255': 'manufacturer',
                      '0.0.96.1.2.255': 'ver_metrological_software',
                      '1.1.0.2.0.255': 'metrological_insignificant_part',
                      '0.0.96.1.8.255': 'software_version',
                      '1.0.0.2.1.254': 'mi_version',
                      '0.0.96.14.0.255': 'current_tariff',
                      '1.0.0.2.8.255': 'checksum_metrological_software',
                      '0.0.96.1.128.255': 'checksum_metrological_significant_software',
                      '1.0.0.4.2.255': 'amperage_transformation_coefficient',
                      '1.0.0.4.3.255': 'voltage_transformation_coefficient',
                      '0.0.96.1.130.255': 'software_name',
                      '0.0.96.1.6.255': 'SPODES_specification_version',
                      '0.0.96.1.254.255': 'extended_SPODES_specification_version',
                      '0.0.96.6.3.255': 'switching_scheme'
                      }
        return self.generating_data_for_comparison_gurux(obis_param, GXDLMSData, 2)

    @allure.step('Считываем показания энергии с WebConfig')
    def general_data_webconfig(self, for_what):
        ui_param = {self.SERIAL_NUMBER: 'serial_number',
                    self.METER_TYPE: 'meter_type',
                    self.METER_RELEASE_DATE: 'meter_release_date',
                    self.MANUFACTURER: 'manufacturer',
                    self.METROLOGICAL_SOFTWARE_VERSION: 'ver_metrological_software',
                    self.INSIGNIFICANT_SOFTWARE_VERSION: 'metrological_insignificant_part',
                    self.FIRMWARE_VERSION: 'software_version',
                    self.MI_VERSION: 'mi_version',
                    self.CURRENT_TARIFF: 'current_tariff',
                    self.CHECKSUM_METROLOGICAL_SOFTWARE: 'checksum_metrological_software',
                    self.CHECKSUM_INSIGNIFICANT_SOFTWARE: 'checksum_metrological_significant_software',
                    self.AMPERAGE_TRANSFORM_COEFFICIENT: 'amperage_transformation_coefficient',
                    self.VOLTAGE_TRANSFORM_COEFFICIENT: 'voltage_transformation_coefficient',
                    self.FIRMWARE_NAME: 'software_name',
                    self.PROTOCOL_SPODES_VERSION: 'SPODES_specification_version',
                    self.PROTOCOL_EXTENDED_SPODES_VERSION: 'extended_SPODES_specification_version',
                    self.SWITCHING_SCHEME: 'switching_scheme'}
        return self.generating_data_for_comparison_ui(ui_param, for_what)
