# Запуск автотестов PrestaShop через Jenkins

Jenkins поднимается в Docker вместе с окружением для тестов: MariaDB, PrestaShop 9,
Selenoid и Selenoid UI. Джоба (pipeline) подтягивает репозиторий автотестов из GitHub,
запускает их на Selenoid с параметрами и публикует отчёт Allure.

## Состав стека

| Сервис      | Адрес               | Назначение                        |
|-------------|---------------------|-----------------------------------|
| jenkins     | http://localhost:8081 | Jenkins UI                       |
| prestashop  | http://localhost:8080 | Магазин под тест                 |
| selenoid    | localhost:4444      | Грид с браузерами                 |
| selenoid-ui | http://localhost:8090 | VNC-просмотр сессий               |

Все сервисы работают в общей docker-сети `selenoid`, поэтому браузеры Selenoid
открывают магазин по адресу `http://prestashop`, а Jenkins ходит в грид по имени
`http://selenoid:4444/wd/hub`.

Образ Jenkins собирается из Dockerfile: JDK + Python с зависимостями тестов
(pytest, selenium, allure-pytest, pytest-xdist) + плагины из plugins.txt.
Тесты выполняются прямо в контейнере Jenkins и обращаются к удалённому гриду,
поэтому локальные браузеры не нужны.

## Запуск окружения

```shell
docker compose -f jenkins/jenkins-compose.yml up -d --build
```

Сборка образа Jenkins занимает несколько минут, при первом старте он доустанавливает
плагины. Дождитесь в логах строки `Jenkins is fully up and running`:

```shell
docker compose -f jenkins/jenkins-compose.yml logs -f jenkins
```

## Первичная настройка Jenkins

1. Начальный пароль администратора:

```shell
docker compose -f jenkins/jenkins-compose.yml exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

2. Открыть http://localhost:8081, ввести пароль.
3. «Install suggested plugins», затем создать пользователя-админа.

## Создание джобы

1. **New Item** → имя `PrestashopTests` → тип **Pipeline** → OK.
2. В секции Pipeline:
   - Definition: **Pipeline script from SCM**
   - SCM: **Git**
   - Repository URL: `https://github.com/<логин>/OtusQAhomeworkSelenoid.git`
   - Branch Specifier: `*/main`
   - Script Path: `Jenkinsfile`
3. Save.

Джоба берёт Jenkinsfile из репозитория тестов и при каждом запуске подтягивает
актуальные автотесты из GitHub.

4. Нажмите **Build Now** — первый прогон выполнится с параметрами по умолчанию.
   Это особенность Jenkins: параметры из Jenkinsfile появляются в интерфейсе
   только после первого запуска.
5. Теперь доступна кнопка **Build with Parameters**.

## Параметры джобы

| Параметр          | По умолчанию        | Описание                                                             |
|-------------------|---------------------|----------------------------------------------------------------------|
| `EXECUTOR`        | `selenoid`          | Адрес executor (грида)                                               |
| `APP_URL`         | `http://prestashop` | Адрес приложения PrestaShop                                          |
| `BROWSER`        | `chrome`            | Браузер: `chrome` или `firefox`                                      |
| `BROWSER_VERSION` | `128.0`             | Версия браузера на Selenoid: Chrome 128.0/127.0, Firefox 125.0/124.0 |
| `THREADS`         | `2`                 | Количество потоков (`pytest -n`, pytest-xdist)                       |

Прогон виден в Selenoid UI: http://localhost:8090 (VNC активных сессий браузеров).

## Отчёт Allure

После каждого прогона Jenkins публикует отчёт Allure: на странице джобы —
график тренда, в меню сборки — ссылка **Allure Report** с полным отчётом
(сводка, suites, шаги, скриншоты упавших тестов прикладываются conftest'ом).

Для сдачи понадобятся скриншоты: джоба с открытыми параметрами, выполненный
прогон и страница отчёта Allure.

## Очистка

```shell
docker compose -f jenkins/jenkins-compose.yml down      # остановить стек (данные останутся в volumes)
docker compose -f jenkins/jenkins-compose.yml down -v  # полная очистка, включая данные Jenkins и магазина
```

## Примечания

- Не запускайте этот стек одновременно со стеком из корня репозитория
  (`docker compose up` из Selenoid-задания) — оба публикуют магазин на порт 8080 хоста.
- При первом прогоне Selenoid скачивает браузерные образы (~0.5 ГБ на версию).
- Установка PrestaShop при первом старте занимает 1–2 минуты.
- `Jenkinsfile` находится в корне этого же репозитория — PR с его добавлением
  сдаётся по пункту про Jenkinsfile.
