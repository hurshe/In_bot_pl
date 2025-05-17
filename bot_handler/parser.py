from time import sleep
import traceback

import undetected_chromedriver as uc
from selenium.common import StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bot_handler.email_checker import get_latest_code


class RegistrationBot:
    def __init__(self, url, email, password, driver_path):
        self.url = url
        self.email = email
        self.password = password
        self.driver_path = driver_path
        self.driver = self._init_driver()
        self.wait = WebDriverWait(self.driver, 15)
        self.name = None

    def _init_driver(self):
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        return uc.Chrome(service=Service(self.driver_path), options=options)

    def login(self, login_selector, password_selector, submit_selector, code_selector):
        try:
            self.driver.get(self.url)

            try:
                dismiss_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.cc-btn.cc-dismiss')))
                dismiss_button.click()
                sleep(2)
            except:
                print("✅ Cookie кнопка не найдена или уже скрыта")

            login_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, login_selector)))
            login_input.send_keys(self.email)
            sleep(2)

            password_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, password_selector)))
            password_input.send_keys(self.password)
            sleep(3)

            submit_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, submit_selector)))
            ActionChains(self.driver).move_to_element(submit_btn).click().perform()
            print("✅Кнопка подтверждения нажата")
            sleep(2)

            code_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, code_selector)))
            code = None
            for _ in range(12):
                code = get_latest_code()
                if code:
                    break
                sleep(5)

            if code:
                code_input.send_keys(code)
                print(f"✅Код подтверждения введён: {code}")
            else:
                print("❌Код подтверждения не найден.")

            submit_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, submit_selector)))
            ActionChains(self.driver).move_to_element(submit_btn).click().perform()
            print("✅Успешный вход!")
            sleep(5)

        except Exception as e:
            print("❌Ошибка при логине:", e)
            traceback.print_exc()

    def open_cases_page(self):
        try:
            cases_page = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href^="/home/cases"]'))
            )
            cases_page.click()
            print("🔹Перешел на страницу с кейсами")
            sleep(6)
        except Exception as e:
            print("❌Ошибка при переходе на кейсы:", e)

    def read_people_list(self):
        try:
            people_elements = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, '//td[contains(@class, "mat-column-person")]'))
            )
            for person in people_elements:
                self.name = person.text.strip()
                print("Имя и фамилия:", self.name)
        except Exception as e:
            print("❌Ошибка при чтении людей:", e)

    def open_case_details(self):
        try:
            target_row = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//tr[td[contains(text(), '{self.name}')]]"))
            )
            target_row.click()
            print("🔹Перешёл на детали дела")
            sleep(5)
        except Exception as e:
            print("❌Ошибка при переходе на дело:", e)

    def open_appointment_section(self):
        try:
            appointment_header = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//h3[contains(text(), "Umów się na wizytę w urzędzie")]'))
            )
            container = appointment_header.find_element(By.XPATH, './ancestor::div[contains(@class,"accordion__content")]')
            toggle = container.find_element(By.XPATH, './/button[contains(@class, "btn--accordion")]')
            toggle.click()
            print("🔻Секция Umów się на wizytę раскрыта")
            sleep(6)
        except Exception as e:
            print("❌Ошибка при открытии секции визита:", e)

    def select_location(self):
        try:
            location_select = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//mat-label[contains(text(), "Wybierz lokalizację")]/ancestor::mat-form-field//mat-select'))
            )
            location_select.click()
            print("🔻Открыт дропдаун локации")

            location_option = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//mat-option//span[contains(text(), "ul. Marszałkowska 3/5, 00-624 Warszawa")]'))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", location_option)
            sleep(3)
            location_option.click()
            print("✅Выбрана локация")
            sleep(4)
        except Exception as e:
            print("❌Ошибка выбора локации:", e)

    def select_queue(self):
        try:
            line_select = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//mat-label[contains(text(), "Wybierz kolejkę")]/ancestor::mat-form-field//mat-select'))
            )
            line_select.click()
            print("🔻Открыт дропдаун очереди")

            options = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//mat-option//span')))
            for opt in options:
                text = opt.text.replace('\u00A0', ' ').strip()
                if "X - Wnioski o POBYT CZASOWY" in text:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", opt)
                    opt.click()
                    print("✅ Выбрана очередь:", text)
                    break
        except Exception as e:
            print("❌Ошибка выбора очереди:", e)

    def find_available_dates_and_check_slots(self, max_months=6, max_retries=3):
        global aria_label
        wait = WebDriverWait(self.driver, 10)

        for month_index in range(max_months):
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'td.mat-calendar-body-cell')))
            sleep(1)

            retries = 0
            available_dates = []

            while retries < max_retries:
                try:
                    cells = self.driver.find_elements(By.CSS_SELECTOR, 'td.mat-calendar-body-cell')
                    available_dates = []
                    for cell in cells:
                        aria_disabled = cell.get_attribute('aria-disabled')
                        classes = cell.get_attribute('class')
                        if aria_disabled != 'true' and 'mat-calendar-body-disabled' not in classes:
                            available_dates.append(cell)
                    break
                except StaleElementReferenceException:
                    retries += 1
                    print(f"StaleElementReferenceException при получении ячеек (попытка {retries}/{max_retries})")
                    sleep(0.5)

            if retries == max_retries:
                print("Не удалось получить актуальные ячейки календаря после нескольких попыток")
                return

            if not available_dates:
                try:
                    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div.spinner')))
                    next_button = self.driver.find_element(By.CSS_SELECTOR, 'button.mat-calendar-next-button')
                    next_button.click()
                    sleep(1.5)
                    print(f"Месяц {month_index + 1}: свободных дат нет, переходим к следующему месяцу")
                except Exception as e:
                    print("Не удалось перейти на следующий месяц:", e)
                    break
                continue

            print(f"Найдены свободные даты в месяце {month_index + 1}: {len(available_dates)} шт.")

            found_time_window = False

            for i in range(len(available_dates)):
                retries = 0
                while retries < max_retries:
                    try:
                        cells = self.driver.find_elements(By.CSS_SELECTOR, 'td.mat-calendar-body-cell')
                        available_dates = [cell for cell in cells if cell.get_attribute(
                            'aria-disabled') != 'true' and 'mat-calendar-body-disabled' not in cell.get_attribute(
                            'class')]
                        date_cell = available_dates[i]

                        aria_label = date_cell.get_attribute('aria-label')
                        print(f"Проверяем дату: {aria_label}")

                        date_cell.click()
                        sleep(1)

                        time_window = self.driver.find_elements(By.CSS_SELECTOR, '.time-selection-window')
                        if time_window:
                            print(f"Для даты {aria_label} окно выбора времени найдено!")
                            found_time_window = True
                            if self.select_available_time_slot():
                                print("✅ Время успешно выбрано")
                            else:
                                print("❌ Не удалось выбрать время")
                            return  # Выходим из функции после успешного выбора
                        else:
                            print(f"Окно выбора времени не найдено для даты {aria_label}, пробуем следующую")
                        break
                    except StaleElementReferenceException:
                        retries += 1
                        print(
                            f"StaleElementReferenceException при работе с датой {aria_label} (попытка {retries}/{max_retries})")
                        sleep(0.5)
                    except Exception as e:
                        print(f"Ошибка при клике по дате {aria_label}: {e}")
                        break

            if not found_time_window:
                try:
                    next_button = self.driver.find_element(By.CSS_SELECTOR, 'button.mat-calendar-next-button')
                    next_button.click()
                    sleep(1.5)
                    print(
                        f"В месяце {month_index + 1} не найдено доступных временных окон, переходим к следующему месяцу")
                except Exception as e:
                    print("Не удалось перейти на следующий месяц:", e)
                    break

    def select_available_time_slot(self):
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.time-selection-window')))

            time_slots = self.driver.find_elements(By.CSS_SELECTOR, '.time-slot')

            for slot in time_slots:
                classes = slot.get_attribute('class')
                if 'disabled' not in classes:
                    slot.click()
                    print(f"Выбрано время: {slot.text}")
                    return True

            print("Свободных слотов времени не найдено.")
            return False

        except Exception as e:
            print(f"Ошибка при выборе времени: {e}")
            return False

    def quit(self):
        self.driver.quit()
