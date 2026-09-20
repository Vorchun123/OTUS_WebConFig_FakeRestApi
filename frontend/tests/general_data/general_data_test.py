import allure
import pytest
from frontend.page.general_data.general_data import General


@pytest.mark.ui
@allure.title('Проверяем корректное подключение к ПУ')
def test_connection_meter(browser, connection_electricity_meter, com_port):
    general_data = General(browser)
    general_data.load_page_url()
    connection_electricity_meter.checking_status("Подключение успешно")


@pytest.mark.ui
@allure.title('Обновление данных')
def test_refresh_page(browser, connection_electricity_meter, com_port):
    general_data = General(browser)
    general_data.load_page_url()
    general_data.refresh_page_and_wait_button()
    meter_type = general_data.get_meter_type()
    assert meter_type.startswith('НАРТИС')


@pytest.mark.ui
@allure.title('Обновление паспортных данных')
def test_read_passport_data(browser, connection_electricity_meter, com_port):
    general_data = General(browser)
    general_data.load_page_url()
    general_data.read_passport_data()
    connection_electricity_meter.wait_status("Чтение профиля общих данных завершено")
    all_data = general_data.get_all_passport_data()
    assert 'Максимальный ток' in all_data


@pytest.mark.ui
@allure.title('Проверяем актуальность данных отображаемых в WebConfig')
def test_actual_data_value(browser, connection_electricity_meter, com_port):
    general_data = General(browser)
    general_data.load_page_url()
    webconfig_value = general_data.general_data_webconfig('web')
    print(webconfig_value)
