import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    # Налаштовуємо опції Chrome
    options = Options()

    # Обов'язкові налаштування для запуску в CI/CD (на серверах GitHub)
    options.add_argument("--headless=new")  # Запуск без візуального інтерфейсу
    options.add_argument("--window-size=1920,1080")  # Встановлення стандартного розміру вікна
    options.add_argument("--no-sandbox")  # Вимкнення ізоляції (потрібно для Linux-серверів)
    options.add_argument("--disable-dev-shm-usage")  # Подолання обмежень пам'яті у контейнерах

    # Ініціалізація драйвера з переданими опціями
    driver = webdriver.Chrome(options=options)

    # Передаємо драйвер у тест
    yield driver

    # Гарантовано закриваємо браузер після завершення тесту
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Отримуємо результати виконання хука
    outcome = yield
    report = outcome.get_result()

    # Перевіряємо, чи сталася помилка саме під час виконання самого тесту (етап "call")
    if report.when == "call" and report.failed:
        # Намагаємося отримати об'єкт драйвера з фікстур поточного тесту
        driver = item.funcargs.get("driver")

        if driver:
            # Зберігаємо скріншот у пам'ять у форматі PNG
            screenshot = driver.get_screenshot_as_png()

            # Прикріплюємо скріншот до звіту Allure
            allure.attach(
                screenshot,
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG
            )