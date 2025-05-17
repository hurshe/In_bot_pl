from imapclient import IMAPClient
import pyzmail
import re
import os
from typing import Final
from dotenv import load_dotenv

load_dotenv()

EMAIL: Final = os.getenv('EMAIL')
APP_PASSWORD: Final = os.getenv('APP_PASSWORD')


def get_latest_code():
    with IMAPClient("imap.gmail.com", ssl=True) as client:
        client.login(EMAIL, APP_PASSWORD)
        client.select_folder("INBOX")

        messages = client.search(['UNSEEN', 'SINCE', '05-May-2025'])
        messages.reverse()

        for uid in messages:
            raw_message = client.fetch([uid], ['BODY[]', 'FLAGS'])
            message = pyzmail.PyzMessage.factory(raw_message[uid][b'BODY[]'])

            if message.text_part:
                text = message.text_part.get_payload().decode(message.text_part.charset)
            elif message.html_part:
                text = message.html_part.get_payload().decode(message.html_part.charset)
            else:
                continue

            match = re.search(r"\b\d{6}\b", text)
            if match:
                return match.group()

        return None


if __name__ == "__main__":
    code = get_latest_code()
    if code:
        print("Ваш код:", code)
    else:
        print("Код не найден.")