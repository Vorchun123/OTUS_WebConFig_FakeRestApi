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
        self.visit_page(f'http://localhost:5004/{self.get_meter_id()}/general_data')

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
