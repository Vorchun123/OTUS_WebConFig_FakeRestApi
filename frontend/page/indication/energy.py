from selenium.common import NoSuchElementException
from frontend.page.connection_page.connection_page_electricity_meter import ConnectionPageElectricityMeter
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import allure

COM_PORT = 'COM26'
CLIENT_ADDRESS = 48
SERVER_ADDRESS = 145
PASSWORD = '0000000100000001'


class Energy(ConnectionPageElectricityMeter):
    BUTTON_SIDEBAR_INDICATIONS = (By.ID, 'indications-link')
    BUTTON_SIDEBAR_ENERGY = (By.ID, 'indications-energy-link')
    BUTTON_GET_DATA = (By.ID, 'getFromMeterButton')
    BUTTON_SAVE_DATA = (By.ID, 'saveDataToFileButton')
    TARIFF_TABLE = (By.CSS_SELECTOR, '#tariffTable > tbody > tr')
    TARIFF_1_ACTIVE_IMPORT = (By.ID, 'tariff1ActiveImportValue')
    TARIFF_1_ACTIVE_EXPORT = (By.ID, 'tariff1ActiveExportValue')
    TARIFF_1_REACTIVE_IMPORT = (By.ID, 'tariff1ReactiveImportValue')
    TARIFF_1_REACTIVE_EXPORT = (By.ID, 'tariff1ReactiveExportValue')
    TARIFF_2_ACTIVE_IMPORT = (By.ID, 'tariff2ActiveImportValue')
    TARIFF_2_ACTIVE_EXPORT = (By.ID, 'tariff2ActiveExportValue')
    TARIFF_2_REACTIVE_IMPORT = (By.ID, 'tariff2ReactiveImportValue')
    TARIFF_2_REACTIVE_EXPORT = (By.ID, 'tariff2ReactiveExportValue')
    TARIFF_3_ACTIVE_IMPORT = (By.ID, 'tariff3ActiveImportValue')
    TARIFF_3_ACTIVE_EXPORT = (By.ID, 'tariff3ActiveExportValue')
    TARIFF_3_REACTIVE_IMPORT = (By.ID, 'tariff3ReactiveImportValue')
    TARIFF_3_REACTIVE_EXPORT = (By.ID, 'tariff3ReactiveExportValue')
    TARIFF_4_ACTIVE_IMPORT = (By.ID, 'tariff4ActiveImportValue')
    TARIFF_4_ACTIVE_EXPORT = (By.ID, 'tariff4ActiveExportValue')
    TARIFF_4_REACTIVE_IMPORT = (By.ID, 'tariff4ReactiveImportValue')
    TARIFF_4_REACTIVE_EXPORT = (By.ID, 'tariff4ReactiveExportValue')
    TARIFF_5_ACTIVE_IMPORT = (By.ID, 'tariff5ActiveImportValue')
    TARIFF_5_ACTIVE_EXPORT = (By.ID, 'tariff5ActiveExportValue')
    TARIFF_5_REACTIVE_IMPORT = (By.ID, 'tariff5ReactiveImportValue')
    TARIFF_5_REACTIVE_EXPORT = (By.ID, 'tariff5ReactiveExportValue')
    TARIFF_6_ACTIVE_IMPORT = (By.ID, 'tariff6ActiveImportValue')
    TARIFF_6_ACTIVE_EXPORT = (By.ID, 'tariff6ActiveExportValue')
    TARIFF_6_REACTIVE_IMPORT = (By.ID, 'tariff6ReactiveImportValue')
    TARIFF_6_REACTIVE_EXPORT = (By.ID, 'tariff6ReactiveExportValue')
    TARIFF_7_ACTIVE_IMPORT = (By.ID, 'tariff7ActiveImportValue')
    TARIFF_7_ACTIVE_EXPORT = (By.ID, 'tariff7ActiveExportValue')
    TARIFF_7_REACTIVE_IMPORT = (By.ID, 'tariff7ReactiveImportValue')
    TARIFF_7_REACTIVE_EXPORT = (By.ID, 'tariff7ReactiveExportValue')
    TARIFF_8_ACTIVE_IMPORT = (By.ID, 'tariff8ActiveImportValue')
    TARIFF_8_ACTIVE_EXPORT = (By.ID, 'tariff8ActiveExportValue')
    TARIFF_8_REACTIVE_IMPORT = (By.ID, 'tariff8ReactiveImportValue')
    TARIFF_8_REACTIVE_EXPORT = (By.ID, 'tariff8ReactiveExportValue')
    TARIFF_SIGMA_ACTIVE_IMPORT = (By.ID, 'tariffSigmaActiveImportValue')
    TARIFF_SIGMA_ACTIVE_EXPORT = (By.ID, 'tariffSigmaActiveExportValue')
    TARIFF_SIGMA_REACTIVE_IMPORT = (By.ID, 'tariffSigmaReactiveImportValue')
    TARIFF_SIGMA_REACTIVE_EXPORT = (By.ID, 'tariffSigmaReactiveExportValue')

    @allure.step('Переходим на страницу "Энергия"')
    def load_page_url(self):
        self.visit_page(f'http://localhost:5004/{self.get_meter_id()}/energy')

    @allure.step('Переходим на страницу "Энергия" через боковую панель')
    def load_page_sidebar(self):
        self.click(*self.BUTTON_SIDEBAR_INDICATIONS)
        self.click(*self.BUTTON_SIDEBAR_ENERGY)

    @allure.step('Нажимаем на кнопку "Считать данные с устройства"')
    def click_button_get_data_and_wait_table(self):
        self.click(*self.BUTTON_GET_DATA)
        try:
            WebDriverWait(self.browser, 20).until(lambda browser: self.count_elements(*self.TARIFF_TABLE) > 4)
        except Exception as e:
            self.error_action('Таблица по тарифам не загружена', element=e)
            raise

    @allure.step('Нажимаем на кнопку "Сохранить данные"')
    def click_button_save_data(self):
        self.click(*self.BUTTON_SAVE_DATA)

    @allure.step('Проверяем кол-во тарифов на ПУ')
    def count_tariff(self):
        count_tariff = self.count_elements(*self.TARIFF_TABLE)
        if count_tariff == 5:
            with allure.step('Кол-во тарифов = 4'):
                print('\nКол-во тарифов = 4')
        elif count_tariff == 9:
            with allure.step('Кол-во тарифов = 8'):
                print('\nКол-во тарифов = 8')
        else:
            with allure.step(f'Кол-во тарифов = {self.count_elements(*self.TARIFF_TABLE) - 1}'):
                print(f'\nКол-во тарифов = {self.count_elements(*self.TARIFF_TABLE) - 1}')

    @allure.step('Считываем показания энергии с WebConfig')
    def tariff_table_webconfig(self, for_what):
        ui_param = {'ТарифT1': {self.TARIFF_1_ACTIVE_IMPORT: 'A+ (кВт⋅ч)', self.TARIFF_1_ACTIVE_EXPORT: 'A- (кВт⋅ч)',
                                self.TARIFF_1_REACTIVE_IMPORT: 'R+ (кВар⋅ч)',
                                self.TARIFF_1_REACTIVE_EXPORT: 'R- (кВар⋅ч)'},
                    'ТарифT2': {self.TARIFF_2_ACTIVE_IMPORT: 'A+ (кВт⋅ч)', self.TARIFF_2_ACTIVE_EXPORT: 'A- (кВт⋅ч)',
                                self.TARIFF_2_REACTIVE_IMPORT: 'R+ (кВар⋅ч)',
                                self.TARIFF_2_REACTIVE_EXPORT: 'R- (кВар⋅ч)'},
                    'ТарифT3': {self.TARIFF_3_ACTIVE_IMPORT: 'A+ (кВт⋅ч)', self.TARIFF_3_ACTIVE_EXPORT: 'A- (кВт⋅ч)',
                                self.TARIFF_3_REACTIVE_IMPORT: 'R+ (кВар⋅ч)',
                                self.TARIFF_3_REACTIVE_EXPORT: 'R- (кВар⋅ч)'},
                    'ТарифT4': {self.TARIFF_4_ACTIVE_IMPORT: 'A+ (кВт⋅ч)', self.TARIFF_4_ACTIVE_EXPORT: 'A- (кВт⋅ч)',
                                self.TARIFF_4_REACTIVE_IMPORT: 'R+ (кВар⋅ч)',
                                self.TARIFF_4_REACTIVE_EXPORT: 'R- (кВар⋅ч)'},
                    'ТарифT5': {self.TARIFF_5_ACTIVE_IMPORT: 'A+ (кВт⋅ч)', self.TARIFF_5_ACTIVE_EXPORT: 'A- (кВт⋅ч)',
                                self.TARIFF_5_REACTIVE_IMPORT: 'R+ (кВар⋅ч)',
                                self.TARIFF_5_REACTIVE_EXPORT: 'R- (кВар⋅ч)'},
                    'ТарифT6': {self.TARIFF_6_ACTIVE_IMPORT: 'A+ (кВт⋅ч)', self.TARIFF_6_ACTIVE_EXPORT: 'A- (кВт⋅ч)',
                                self.TARIFF_6_REACTIVE_IMPORT: 'R+ (кВар⋅ч)',
                                self.TARIFF_6_REACTIVE_EXPORT: 'R- (кВар⋅ч)'},
                    'ТарифT7': {self.TARIFF_7_ACTIVE_IMPORT: 'A+ (кВт⋅ч)', self.TARIFF_7_ACTIVE_EXPORT: 'A- (кВт⋅ч)',
                                self.TARIFF_7_REACTIVE_IMPORT: 'R+ (кВар⋅ч)',
                                self.TARIFF_7_REACTIVE_EXPORT: 'R- (кВар⋅ч)'},
                    'ТарифT8': {self.TARIFF_8_ACTIVE_IMPORT: 'A+ (кВт⋅ч)', self.TARIFF_8_ACTIVE_EXPORT: 'A- (кВт⋅ч)',
                                self.TARIFF_8_REACTIVE_IMPORT: 'R+ (кВар⋅ч)',
                                self.TARIFF_8_REACTIVE_EXPORT: 'R- (кВар⋅ч)'},
                    'ТарифΣT': {self.TARIFF_SIGMA_ACTIVE_IMPORT: 'A+ (кВт⋅ч)',
                                self.TARIFF_SIGMA_ACTIVE_EXPORT: 'A- (кВт⋅ч)',
                                self.TARIFF_SIGMA_REACTIVE_IMPORT: 'R+ (кВар⋅ч)',
                                self.TARIFF_SIGMA_REACTIVE_EXPORT: 'R- (кВар⋅ч)'}}
        result = {}
        try:
            for tariff, keys in ui_param.items():
                result[tariff] = {}
                with allure.step(f'Формируем - {tariff}'):
                    for locator, key in keys.items():
                        with allure.step(f'Читаем параметр - {locator}'):
                            if for_what == 'gurux':
                                result[tariff][key] = (self.converting_str_in_float(*locator)) * 1000
                            else:
                                result[tariff][key] = self.get_text(*locator)
        except NoSuchElementException:
            pass
        return result
