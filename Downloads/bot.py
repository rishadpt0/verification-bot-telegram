import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import (Update, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup,
    ChatPermissions, ParseMode)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def button(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer("clicked")
    update_msg = getattr(update, "message", None)
    chat = getattr(update_msg, "chat", None)
    chat_id = getattr(update_msg, "chat_id", None)
    update.message.reply_text("Added new user")
    user_id = update_msg.from_user.id
    msg_id = update_msg.message_id
    permissions = ChatPermissions(True, True, True, True,
                                    True, True, True, True)
    bot = context.bot
    result = bot.restrictChatMember(chat_id, user_id, permissions)

def echo(update, context):
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def msg_new_user(update, context):
    update_msg = getattr(update, "message", None)
    chat_id = getattr(update_msg, "chat_id", None)
   
    user_id = update_msg.from_user.id
    permissions = ChatPermissions(False, False, False, False,
                                    False, False, False, False)
    bot = context.bot
    result = bot.restrictChatMember(chat_id, user_id, permissions)

    keyboard = [[InlineKeyboardButton("Option 1", callback_data='1' ,url='https://google.com')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def main():
    logger.warning("Started")
    updater = Updater("1313257034:AAE_RD0y__ITWukhgJrUkrcV_jSeJKDKy2Y", use_context=True)

    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, msg_new_user))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
