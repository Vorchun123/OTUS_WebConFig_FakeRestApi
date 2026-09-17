from frontend.methods.user_data import file_search_without_data, comparing_values
from frontend.page.indication.network_parameters import NetworkParameters
import allure


@allure.tag('functional')
@allure.title('Проверяем сохранение параметров сети без данных')
def test_save_measurement_table_without_data(browser, connection_electricity_meter, com_port):
    network = NetworkParameters(browser)
    network.load_page_sidebar()
    network.click_button_save_data()
    connection_electricity_meter.wait_status('Отсутствуют корректные данные для сохранения')


@allure.tag('smoke')
@allure.title('Проверяем обновление данных параметров сети')
def test_read_measurement_table(browser, connection_electricity_meter, com_port):
    network = NetworkParameters(browser)
    network.load_page_url()
    network.click_button_get_data_and_wait_table()
    connection_electricity_meter.checking_status('Обновление параметров сети завершено')


@allure.tag('smoke')
@allure.title('Проверяем сохранение данных параметров сети')
def test_save_measurement_table(browser, connection_electricity_meter, com_port):
    network = NetworkParameters(browser)
    network.load_page_url()
    network.click_button_get_data_and_wait_table()
    network.click_button_save_data()
    connection_electricity_meter.wait_status('Сохранено успешно')
    file_search_without_data('^Параметры сети')


@allure.tag('single-phase')
@allure.title('Проверяем актуальность данных отображаемых в xlsx')
def test_read_data_in_xlsx(browser, connection_electricity_meter, com_port):
    network = NetworkParameters(browser)
    serial_number = network.serial_meter_number()
    network.load_page_url()
    network.click_button_get_data_and_wait_table()
    webconfig_value = network.network_parameters_webconfig()
    network.click_button_save_data()
    connection_electricity_meter.wait_status('Сохранено успешно')
    data_xlsx = network.read_xlsx_network_parameters(serial_number)
    comparing_values(webconfig_value, data_xlsx)
