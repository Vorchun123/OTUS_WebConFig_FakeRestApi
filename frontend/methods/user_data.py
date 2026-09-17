import os
import re
import csv
from datetime import date
from datetime import datetime
from pathlib import Path
import allure


@allure.step('Поиск файла с датой в названии')
def file_search_with_data(file_name):
    today = date.today().strftime("%d-%m-%y")
    directory_path = Path.home() / 'Documents' / 'webconfig-user-data'
    pattern = rf'^{file_name}.*{today}'
    file_found = False
    for filename in os.listdir(directory_path):
        if re.match(pattern, filename):
            print(f'\nФайл найден:{filename}')
            file_found = True
    if not file_found:
        print("\nФайл не найден")


@allure.step('Поиск файла без даты в названии')
def file_search_without_data(file_name):
    directory_path = Path.home() / 'Documents' / 'webconfig-user-data'
    pattern = rf'^{file_name}.*'
    file_found = False
    for filename in os.listdir(directory_path):
        if re.match(pattern, filename):
            print(f'\nФайл найден:{filename}')
            file_found = True
    if not file_found:
        print("\nФайл не найден")


@allure.step('Формируем данные на основе csv файла')
def read_csv_energy(file_name):
    today = datetime.now().strftime("%d-%m-%y")
    directory_path = Path.home() / 'Documents' / 'webconfig-user-data'
    pattern = rf'^{file_name}.*{today}'
    new_file_name = None
    for filename in os.listdir(directory_path):
        if re.match(pattern, filename):
            new_file_name = filename
    file_path = directory_path / new_file_name
    data_csv = {}
    with open(file_path, "r", encoding='utf-8-sig', newline='') as f:
        default_csv = csv.DictReader(f, delimiter=';')
        for column in default_csv:
            tariff = f'Тариф{column['Тариф']}'
            data_csv[tariff] = {'A+ (кВт⋅ч)': column['A+ (кВт⋅ч)'], 'A- (кВт⋅ч)': column['A- (кВт⋅ч)'],
                                'R+ (кВар⋅ч)': column['R+ (кВар⋅ч)'], 'R- (кВар⋅ч)': column['R- (кВар⋅ч)']}
    return data_csv


def comparing_values_tariff(value_1, value_2):
    for tariff in value_1.keys():
        with allure.step(f'Проверка {tariff}'):
            for key in value_1[tariff].keys():
                try:
                    with allure.step(
                            f'Проверяем соответствие значений {value_1[tariff][key]} = {value_2[tariff][key]}'):
                        assert value_1[tariff][key] == value_2[tariff][key]
                except AssertionError:
                    with allure.step(
                            f'Не совпадает значение для {key}: Gurux={value_1[tariff][key]}, WebConfig={value_2[tariff][key]}'):
                        print(
                            f'Не совпадает значение для {key}: Gurux={value_1[tariff][key]}, WebConfig={value_2[tariff][key]}')
                        continue
                except KeyError:
                    with allure.step(f'Остальные тарифы, начиная с {tariff} отсутствует на ПУ'):
                        print(f'Остальные тарифы, начиная с {tariff} отсутствует на ПУ')


def comparing_values(value_1, value_2):
    for key in value_1.keys():
        try:
            with allure.step(f'Проверяем соответствие значений {value_1[key]} = {value_2[key]}'):
                assert value_1[key] == value_2[key]
        except AssertionError:
            with allure.step(f'Не совпадает значение для {key}: Gurux={value_1[key]}, WebConfig={value_2[key]}'):
                print(f'Не совпадает значение для {key}: Gurux={value_1[key]}, WebConfig={value_2[key]}')
                continue
