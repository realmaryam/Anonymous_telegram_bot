from loguru import logger
from src.utils.io import write_json, read_json, set_json_file
from src.constants import keyboards, keys, states
from src.filters import IsAdmin
from src.bot import bot
import emoji

DATA_DIR = "src/data/data.json"


class Bot:
    """
    Telegram bot to connect two people randomly
    """
    def __init__(self, telebot):
        # initialize bot and data base
        self.bot = telebot
        set_json_file(DATA_DIR)

        # add custom filters
        self.bot.add_custom_filter(IsAdmin())

        # register handlers
        self.handlers()

        # run bot
        logger.info("Bot is running...")
        self.bot.infinity_polling()

    def handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            """
            /start command
            """
            self.send_message(
                message.chat.id,
                f"Hey <strong>{message.chat.first_name}</strong>",
                reply_markup=keyboards.main
            )
            self.db.users.update_one(
                {'chat.id': message.chat.id},
                {'$set': message.json},
                upsert=True
            )
            self.update_state(message.chat.id, states.main)

        @self.bot.message_handler(regexp=emoji.emojize(keys.random_connect))
        def random_connect(message):
            """
            Randomly connect to another user
            """
            self.send_message(message.chat.id,
                              ":busts_in_silhouette: Connecting to a stranger...",
                              reply_markup=keyboards.exit
                              )
            self.update_state(message.chat.id, states.random_connect)

            other_user = self.db.users.find_one(
                {
                    'state': states.random_connect,
                    'chat.id': {'$ne': message.chat.id}
                }
            )
            if not other_user:
                return
            
            # update other user state
            self.update_state(other_user["chat"]["id"], states.connected)
            self.send_message(
                other_user["chat"]["id"], 
                f'Connected to {message.chat.id}...'
            )

            # update current user state
            self.update_state(message.chat.id, states.connected)
            self.send_message(
                message.chat.id, 
                f'Connected to {other_user["chat"]["id"]}...'
            )

            # store connected user
            self.db.users.update_one(
                {'chat.id': message.chat.id},
                {'$set': {'connected_to': other_user["chat"]["id"]}}
            )
            self.db.users.update_one(
                {'chat.id': other_user["chat"]["id"]},
                {'$set': {'connected_to': message.chat.id}}
            )

        @self.bot.message_handler(regexp=emoji.emojize(keys.exit))
        def exit(message):
            """
            Exit from chat
            """
            self.send_message(message.chat.id,
                              keys.exit,
                              reply_markup=keyboards.main
                              )
            self.update_state(message.chat.id, states.main)

            # update other user state
            connected_to = self.db.user.find_one(
                {'chat.id': message.chat.id}
            )
            if not connected_to:
                return
            other_user = connected_to['connected_to']
            self.update_state(other_user. state.main)
            self.send_message(other_user, keys.exit,
                              reply_markup=keyboards.main
            )

            # remove vonnected user
            self.db.users.update_one(
                {'chat.id': message.chat.id},
                {'$set': {'connected_to': None}}
            )
            self.db.users.update_one(
                {'chat.id': other_user},
                {'$set': {'connected_to': None}}
            )

        @self.bot.message_handler(func=lambda message: True)
        def echo(message):
            """
            Echo message to other connected user
            """
            user = self.db.user.find_one(
                {'chat.id': message.chat.id}
            )
            if (user['state'] != states.connect) or\
                (user['connected_to'] is None):
                return
            
            self.send_message(user["connected_to"], message.text)
        
        @self.bot.message_handler(is_admin=True)
        def admin_of_group(message):
            write_json(message.json, "message.json")
            self.send_message(message.chat.id, "You are admin!")


    def send_message(self, chat_id, text, reply_markup=None, emojize=True):
        """
        send message to telegram bot
        """
        if emojize:
            text = emoji.emojize(text)

        self.bot.send_message(chat_id, text, reply_markup=reply_markup)


    def update_state(self, chat_id, state):
        """
        Update user state
        """
        self.db.users.update_one(
            {'chat.id': chat_id},
            {'$set': {'state': state}}
        )


if __name__ == '__main__':
    logger.info('Bot started')
    A_bot = Bot(telebot=bot)

