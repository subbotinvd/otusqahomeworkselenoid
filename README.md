# UI-автотесты PrestaShop: локальный и удалённый запуск на Selenoid

Автоматизированные UI-тесты интернет-магазина [PrestaShop](https://www.prestashop.com/) 9 (тема Hummingbird).
Стек: Selenium WebDriver, pytest, Allure, паттерн Page Object.

Тесты запускаются как удалённо — в [Selenoid](https://aerokube.com/selenoid/) (грид в Docker с VNC),
так и локально — браузером на машине или внутри контейнера с тестами.

## Структура проекта

```
tests/
  conftest.py            # опции запуска и фикстуры: --browser, --browser_version, --url, --executor, --headless
  pages/                 # Page Object: страницы витрины и админки
  test_elements.py       # проверка элементов страниц
  test_search.py         # поиск по каталогу
  test_registration.py   # регистрация нового покупателя
  test_scenarios.py      # e2e-сценарии: логин/логаут админа, корзина
  test_admin_product.py  # CRUD товаров в админке
config/
  browsers.json          # браузеры для Selenoid: Chrome и Firefox, по две версии
selenoid-compose.yml     # Selenoid + Selenoid UI
docker-compose.yml       # MariaDB + PrestaShop + контейнер тестов
Dockerfile               # образ с тестами (Python + Chromium + Firefox)
```

## Подготовка

### 1. Selenoid

```shell
docker compose -f selenoid-compose.yml up -d
```

Поднимаются `selenoid` (порт 4444) и `selenoid-ui` (http://localhost:8090) в сети `selenoid`.
Список браузеров и версий задаётся в `config/browsers.json`; при первой сессии браузерные
образы скачиваются автоматически (около 0.5 ГБ на версию).

Если Selenoid уже развёрнут отдельно (например, по инструкции урока) — этот шаг можно
пропустить: достаточно, чтобы контейнеры были в сети `selenoid` (`docker network ls`).

### 2. Магазин

```shell
docker compose up -d db prestashop
```

Установка PrestaShop занимает 1–2 минуты при первом старте, витрина — http://localhost:8080.
Окружение подключается к внешней сети `selenoid`, поэтому браузеры Selenoid открывают магазин
по адресу `http://prestashop`, а контейнер с тестами ходит в грид по `http://selenoid:4444/wd/hub`.

## Запуск тестов на Selenoid

Полный прогон: одна команда собирает образ тестов, дожидается готовности магазина
и запускает весьuite на Selenoid:

```shell
docker compose up --build
```

Прогон виден в selenoid-ui: http://localhost:8090 → VNC активной сессии.
Связность можно проверить там же: открыть сессию браузера и перейти на http://prestashop.

Запуск тестового контейнера с параметрами:

```shell
docker compose run --rm tests --browser firefox
docker compose run --rm tests --browser chrome --browser_version 127.0
```

Доступные версии берутся из `config/browsers.json`: Chrome 128.0/127.0, Firefox 125.0/124.0.

Тот же образ можно запустить на Selenoid вручную, без compose:

```shell
docker run --rm --network selenoid -e HEADLESS=0 tests -v \
  --url http://prestashop --browser chrome --browser_version 128.0 --executor selenoid
```

## Запуск тестов локально

### На хосте

Магазин уже должен работать на http://localhost:8080.

```shell
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/macOS

pip install -r requirements.txt

pytest --browser=chrome --url=http://localhost:8080 -v
pytest --browser=firefox -v
pytest --browser=chrome --headless -v
```

Без опции `--executor` тесты выполняются через локальный WebDriver: Chrome и Firefox
запускаются на машине, где запущен pytest.

### В собственном контейнере

```shell
docker build -t tests .

docker run -it tests
docker run -it tests --browser firefox
```

Образ по умолчанию работает в headless-режиме и обращается к магазину,
опубликованному на хосте `http://host.docker.internal:8080`.

> На Linux `host.docker.internal` не резолвится из коробки — добавьте
> `--add-host=host.docker.internal:host-gateway` к `docker run`.

## Параметры запуска (conftest.py)

| Параметр            | Значение по умолчанию                   | Описание                                               |
|---------------------|-----------------------------------------|--------------------------------------------------------|
| `--browser`         | `chrome`                                | Браузер: `chrome` или `firefox`                        |
| `--browser_version` | `$BROWSER_VERSION`                      | Версия браузера на Selenoid (из `config/browsers.json`) |
| `--url`             | `$SHOP_URL` или `http://localhost:8080` | Адрес магазина                                          |
| `--executor`        | `$EXECUTOR`                             | Хост грида (например, `selenoid`); без него — локально |
| `--headless`        | `$HEADLESS` или выкл.                   | Headless-режим                                          |

Переменные окружения для админки: `ADMIN_EMAIL`, `ADMIN_PASSWORD`, `ADMIN_FOLDER`
(значения по умолчанию заданы в conftest.py).

## Магазин и админка

- Витрина: http://localhost:8080
- Админка: http://localhost:8080/admin — `admin@prestashop.com` / `AdminDemo-2026-Pass`

## Отчёт Allure

```shell
pytest --alluredir=allure-results
allure serve allure-results
```

При запуске через docker compose результаты складываются в volume `allure_results`.

Остановка: `docker compose down` (данные магазина остаются в volumes, полная очистка —
`docker compose down -v`), Selenoid — `docker compose -f selenoid-compose.yml down`.
