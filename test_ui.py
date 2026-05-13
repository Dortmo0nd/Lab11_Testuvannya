import allure
from selenium.webdriver.common.by import By


@allure.title("Forgot password basic test")
def test_forgot_password(driver):
    # Відкрити сторінку
    driver.get("https://the-internet.herokuapp.com/forgot_password")

    # Ввести пошту і натиснути кнопку
    driver.find_element(By.ID, "email").send_keys("test@test.com")
    driver.find_element(By.ID, "form_submit").click()

    # Навмисна помилка для перевірки генерації скріншоту при падінні
    assert False