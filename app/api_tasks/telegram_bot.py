import os
import logging
from dotenv import load_dotenv
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
)

load_dotenv()

auth_key = os.environ.get("TELEGRAM_BOT_TOKEN")
app_url = os.environ.get("APP_URL")


class TelegramBot:
    def __init__(self):
        self.auth_key = auth_key
        self.app_url = app_url
        self.PORT = int(os.environ.get("PORT", "8443"))

    def logging(self):

        # Enable Logging
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=logging.INFO,
        )
        logger = logging.getLogger(__name__)

    def send_logo(self, update, context):
        """Send ye old phish logo"""
        logo_url = "http://4.bp.blogspot.com/_2CnQWIZQ3NY/SoDbSGrZnxI/AAAAAAAABVQ/tZ6OTg-AzyM/s320/phi.jpg"
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=logo_url)

    def main(self):
        # initialize bot
        self.logging()
        updater = Updater(self.auth_key, use_context=True)
        dispatcher = updater.dispatcher

        # handlers
        dispatcher.add_handler(CommandHandler("logo", self.send_logo))

        # Start bot
        updater.start_webhook(listen="0.0.0.0", port=self.PORT, url_path=auth_key)
        updater.bot.set_webhook(self.app_url + self.auth_key)


# load_dotenv()

# auth_key = os.environ.get("TELEGRAM_BOT_TOKEN")
# app_url = os.environ.get("APP_URL")

# # Enable Logging
# logging.basicConfig(
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
# )
# logger = logging.getLogger(__name__)
# PORT = int(os.environ.get("PORT", "8443"))

# # Send logo
# def send_logo(update, context):
#     """Send ye old phish logo"""
#     logo_url = "http://4.bp.blogspot.com/_2CnQWIZQ3NY/SoDbSGrZnxI/AAAAAAAABVQ/tZ6OTg-AzyM/s320/phi.jpg"
#     context.bot.send_photo(chat_id=update.effective_chat.id, photo=logo_url)


# def main():
#     # initialize bot
#     updater = Updater(auth_key, use_context=True)
#     dispatcher = updater.dispatcher

#     # handlers
#     dispatcher.add_handler(CommandHandler("logo", send_logo))

#     # Start bot
#     updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=auth_key)
#     updater.bot.set_webhook(app_url + auth_key)


if __name__ == "__main__":
    TelegramBot = TelegramBot()
    TelegramBot.main()
