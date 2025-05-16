import os
import dotenv
from typing import Final

from telegram.ext import Application, CommandHandler
from telegram import Update

from bot_handler import notification_services
from bot_handler import parser


dotenv.load_dotenv()

TOKEN: Final = os.getenv('BOT_API')
BOT_USERNAME: Final = os.getenv('BOT_USERNAME')

EMAIL: Final = os.getenv('EMAIL')
PASSWORD: Final = os.getenv('PASSWORD')

URL: Final = os.getenv('URL')
DRIVER: Final = os.getenv('DRIVER_PATH')

if __name__ == '__main__':
    print("Start polling ...")

    parser.login_to_site(
        url=URL,
        username=EMAIL,
        password=PASSWORD,
        login_selector="input[formcontrolname='email']",
        password_selector='input[formcontrolname="password"]',
        submit_selector='button.btn.btn--submit',
        code_selector='input[formcontrolname="code"]',
        driver_path=DRIVER,
    )

    bot_app = Application.builder().token(TOKEN).build()

    bot_app.add_handler(CommandHandler('start', notification_services.start))

    print("Polling ...")
    bot_app.run_polling(allowed_updates=Update.ALL_TYPES)