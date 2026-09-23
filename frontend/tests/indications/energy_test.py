import allure
import pytest
from frontend.methods.user_data import file_search_with_data, read_csv_energy, comparing_values_tariff
from frontend.page.indication.energy import Energy


@pytest.mark.ui
@allure.tag('smoke')
@allure.title('Обновление данных энергии нарастающим током')
def test_read_tariff_table(browser, connection_electricity_meter, com_port):
    energy = Energy(browser)
    energy.load_page_url()
    energy.click_button_get_data_and_wait_table()
    energy.count_tariff()
    connection_electricity_meter.checking_status('Обновление энергии завершено')


@pytest.mark.ui
@allure.tag('smoke')
@allure.title('Сохранение данных энергии нарастающим током')
def test_save_tariff_table(browser, connection_electricity_meter, com_port):
    energy = Energy(browser)
    energy.load_page_url()
    energy.click_button_get_data_and_wait_table()
    energy.click_button_save_data()
    connection_electricity_meter.wait_status('Сохранено успешно')
    file_search_with_data('^Энергия')


@pytest.mark.ui
@allure.tag('functional')
@allure.title('Сохранение энергии нарастающим током без данных')
def test_save_tariff_table_without_data(browser, connection_electricity_meter, com_port):
    energy = Energy(browser)
    energy.load_page_sidebar()
    energy.click_button_save_data()
    connection_electricity_meter.wait_status('Отсутствует информация для сохранения, обновите данные')


@pytest.mark.ui
@allure.tag('smoke')
@allure.title('Проверяем актуальность данных отображаемых в csv')
def test_read_data_in_csv(browser, connection_electricity_meter, com_port):
    energy = Energy(browser)
    energy.load_page_url()
    energy.click_button_get_data_and_wait_table()
    energy.click_button_save_data()
    connection_electricity_meter.wait_status('Сохранено успешно')
    data_csv = read_csv_energy('Энергия')
    webconfig_value = energy.tariff_table_webconfig('web')
    comparing_values_tariff(webconfig_value, data_csv)
