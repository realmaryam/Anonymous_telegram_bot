from loguru import logger
from src.utils.io import write_json
from src.constants import keyboards
from src.filters import IsAdmin
from src.bot import bot
import emoji


class Bot:
    """
    Template for telegram bot
    """
    def __init__(self, telebot):
        self.bot = telebot

        # add custom filters
        self.bot.add_custom_filter(IsAdmin())

        # register handlers
        self.handlers()

        # run bot
        logger.info("Bot is running...")
        self.bot.infinity_polling()

    def handlers(self):
        @self.bot.message_handler(is_admin=True)
        def admin_of_group(message):
            write_json(message.json, "message.json")
            self.bot.send_message(message.chat.id, "You are admin!")

        @self.bot.message_handler(func=lambda message: True)
        def echo(message):
            write_json(message.json, "message.json")
            self.bot.send_message(
                message.chat.id, message.text,
                reply_markup=keyboards.main
            )

    def send_message(self, chat_id, text, reply_markup=None, emojize=True):
        """
        send message to telegram bot
        """
        if emojize:
            text = emoji.emojize(text, use_aliases=True)

        self.bot.send_message(chat_id, text, reply_markup=reply_markup)


if __name__ == '__main__':
    logger.info('Bot started')
    A_bot = Bot(telebot=bot)

