import os
import dotenv
from typing import Final

from telegram.ext import Application, CommandHandler
from telegram import Update

from bot_handler import notification_services
from bot_handler.parser import RegistrationBot


dotenv.load_dotenv()

TOKEN: Final = os.getenv('BOT_API')
BOT_USERNAME: Final = os.getenv('BOT_USERNAME')

EMAIL: Final = os.getenv('EMAIL')
PASSWORD: Final = os.getenv('PASSWORD')

URL: Final = os.getenv('URL')
DRIVER: Final = os.getenv('DRIVER_PATH')

if __name__ == '__main__':
    print("Start polling ...")

    if __name__ == "__main__":
        bot = RegistrationBot(
            url=os.getenv("URL"),
            email=os.getenv("EMAIL"),
            password=os.getenv("PASSWORD"),
            driver_path=os.getenv("DRIVER_PATH")
        )

        bot.login(
            login_selector="input[formcontrolname='email']",
            password_selector='input[formcontrolname="password"]',
            submit_selector='button.btn.btn--submit',
            code_selector='input[formcontrolname="code"]'
        )

        bot.open_cases_page()
        bot.read_people_list()
        bot.open_case_details()
        bot.open_appointment_section()
        bot.select_location()
        bot.select_queue()
        bot.find_available_dates_and_check_slots()

        bot.quit()

    bot_app = Application.builder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler('start', notification_services.start))

    print("Polling ...")
    bot_app.run_polling(allowed_updates=Update.ALL_TYPES)

