import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
from time import sleep

from bot_handler.email_checker import get_latest_code


def login_to_site(url, username, password, login_selector, password_selector, submit_selector, code_selector, driver_path):
    options = uc.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = uc.Chrome(service=Service(driver_path), options=options)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 15)

        try:
            dismiss_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.cc-btn.cc-dismiss')))
            dismiss_button.click()
            sleep(2)
        except:
            print("Кнопка cookie не найдена или уже скрыта")

        login_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, login_selector)))
        login_input.send_keys(username)
        sleep(2)

        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, password_selector)))
        password_input.send_keys(password)
        sleep(2)

        submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, submit_selector)))
        actions = ActionChains(driver)
        actions.move_to_element(submit_btn).click().perform()
        print("Кнопка подтверждения нажата")
        sleep(2)

        code_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, code_selector)))

        code = None

        for _ in range(12):
            code = get_latest_code()
            if code:
                break
            sleep(5)

        if code:
            code_input.send_keys(code)
            print(f"Код подтверждения введён: {code}")
        else:
            print("Код подтверждения не найден в почте.")
        submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, submit_selector)))
        actions = ActionChains(driver)
        actions.move_to_element(submit_btn).click().perform()
        print("Успешный вход!")
        sleep(30)

    except Exception as e:
        print("Ошибка входа:", e)
        traceback.print_exc()

    finally:
        print("Окна браузера:", driver.window_handles)
        if driver.window_handles:
            driver.switch_to.window(driver.window_handles[0])
        else:
            print("Окна закрыты!")
        driver.quit()
