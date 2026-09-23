# OTUS WebConfig / FakeRESTApi — QA Automation Project

Учебный проект по автоматизации тестирования, включающий два направления:

- **UI-тестирование** десктопного приложения конфигурирования IoT-устройств и приборов учёта (WebConfig).
- **API-тестирование** публичного сервиса [FakeRESTApi.azurewebsites.net](https://fakerestapi.azurewebsites.net/).

Проект написан на Python с использованием `pytest`, `Selenium`, `requests` и `allure`. Сборка и запуск тестов
автоматизированы через Jenkins.

---

## Содержание

- [Технологии](#технологии)
- [Требования](#требования)
- [Установка](#установка)
- [Запуск тестов](#запуск-тестов)
    - [API-тесты](#api-тесты)
    - [UI-тесты](#ui-тесты)
- [Параметры запуска pytest](#параметры-запуска-pytest)
- [Отчёты Allure](#отчёты-allure)
- [CI/CD (Jenkins)](#cicd-jenkins)
- [Линтинг](#линтинг)
- [Особенности UI-тестов](#особенности-ui-тестов)

---

## Технологии

| Компонент          | Версия / инструмент  |
|--------------------|----------------------|
| Язык               | Python 3.12          |
| Тестовый фреймворк | pytest 8.3.3         |
| UI-автоматизация   | Selenium 4.25.0      |
| API-клиент         | requests             |
| Отчётность         | allure-pytest 2.16.0 |
| Работа с данными   | pandas, openpyxl     |
| Дополнительно      | PyAutoGUI, pywinauto |
| CI                 | Jenkins              |
| Линтер             | flake8               |

---

## Требования

- **Python 3.12+**
- **Google Chrome** (или Edge/Firefox) — для UI-тестов
- **Allure Commandline** — для генерации отчётов
- **Jenkins** — для CI
- **Прибор учёта / эмулятор**, подключённый по COM-порту (для UI-тестов WebConfig)
- **Запущенный WebConfig** на `http://localhost:5004`

---

## Установка

```bash
# 1. Клонировать репозиторий
git clone https://github.com/Vorchun123/OTUS_WebConFig_FakeRestApi.git
cd OTUS_WebConFig_FakeRestApi

# 2. Создать виртуальное окружение
python -m venv venv

# Windows
venv\Scripts\activate.bat

# 3. Установить зависимости
pip install -r requirements.txt
pip install pytest pytest-cov allure-pytest flake8
```

---

## Запуск тестов

### API-тесты

Тестируют публичный сервис [FakeRESTApi.azurewebsites.net](https://fakerestapi.azurewebsites.net/api/v1/).

```bash
pytest -m api --alluredir=allure-results
```

#### Покрытые эндпоинты

|  Метод   | Endpoint                          | Описание              |
|:--------:|:----------------------------------|:----------------------|
|  `GET`   | `/Authors`                        | Список всех авторов   |
|  `GET`   | `/Authors/{id}`                   | Автор по id           |
|  `GET`   | `/Authors/authors/books/{bookId}` | Автор по id книги     |
|  `POST`  | `/Authors`                        | Добавить автора       |
| `DELETE` | `/Authors/{id}`                   | Удалить автора        |
|  `GET`   | `/Books`                          | Список книг           |
|  `GET`   | `/Books/{id}`                     | Книга по id           |
|  `POST`  | `/Books`                          | Добавить книгу        |
|  `PUT`   | `/Books/{id}`                     | Изменить книгу        |
| `DELETE` | `/Books/{id}`                     | Удалить книгу         |
|  `GET`   | `/Users`                          | Список пользователей  |
|  `GET`   | `/Users/{id}`                     | Пользователь по id    |
|  `POST`  | `/Users`                          | Добавить пользователя |
|  `PUT`   | `/Users/{id}`                     | Изменить пользователя |
| `DELETE` | `/Users/{id}`                     | Удалить пользователя  |

---

### UI-тесты

Тестируют десктопное приложение **WebConfig** (доступно на `http://localhost:5004`).

```bash
pytest -m ui --headless --alluredir=allure-results
```

#### Покрытые сценарии

- **Подключение к ПУ** — интерфейсы `Opto` / `RS-485` / `TCP-IP`, разные типы авторизации.
- **Страница «Общие данные»** — обновление, чтение паспортных данных, сверка значений.
- **Страница «Энергия»** — чтение тарифов, сохранение CSV, сверка с UI.
- **Страница «Параметры сети»** — чтение, сохранение XLSX, сверка с UI.

---

## Параметры запуска pytest

Параметры задаются в `conftest.py`:

| Параметр      | По умолчанию | Описание                             |
|:--------------|:------------:|:-------------------------------------|
| `--browser`   |   `chrome`   | Браузер: `chrome`, `edge`, `firefox` |
| `--headless`  |    выкл.     | Запуск без GUI                       |
| `--log_level` |    `INFO`    | Уровень логирования                  |
| `--com_port`  |    `COM5`    | COM-порт подключения к прибору учёта |

**Пример:**

```bash
pytest -m ui --browser=chrome --headless --com_port=COM5
```

---

## Отчёты Allure

Результаты складываются в `allure-results/`.

```bash
# Просмотр отчёта
allure serve allure-results

# Или генерация статического отчёта
allure generate allure-results -o allure-report --clean
allure open allure-report
```

В отчёте доступны шаги (`@allure.step`), заголовки тестов (`@allure.title`) и теги (`smoke`, `functional`).

---

## CI/CD (Jenkins)

Пайплайн описан в `Jenkinsfile` и состоит из стадий:

| № | Стадия        | Что делает                                      |
|:-:|:--------------|:------------------------------------------------|
| 1 | **Setup**     | Создание `venv`, установка зависимостей         |
| 2 | **API Tests** | `pytest -m api`                                 |
| 3 | **UI Tests**  | `pytest -m ui --headless`                       |
| 4 | **Lint**      | `flake8` с сохранением в `flake8.log`           |
| 5 | **Post**      | Публикация Allure-отчёта и результатов `flake8` |

**Требуемые плагины Jenkins:**

- [Allure Jenkins Plugin](https://plugins.jenkins.io/allure-jenkins-plugin/)
- [Warnings Next Generation Plugin](https://plugins.jenkins.io/warnings-ng/)

---

## Линтинг

```bash
flake8 backend frontend --max-line-length=100 --format=pylint
```

---

## Особенности UI-тестов

- Используется паттерн **Page Object
  ** (`BasePage` → `ConnectionPageElectricityMeter` → `General` / `Energy` / `NetworkParameters`).
- Для подключения к прибору учёта применён **Builder** (`ElectricityMeterConnectionBuilder`) — позволяет гибко
  настраивать интерфейс, авторизацию и адресацию.
- Данные, сохранённые из WebConfig (CSV / XLSX), читаются из `~/Documents/webconfig-user-data` и сравниваются со
  значениями из UI.
- Скриншоты при ошибках автоматически прикрепляются к Allure-отчёту.

---
