from threading import Thread
from telegram import InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler

from bot import LOGGER, dispatcher
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from bot.helper.telegram_helper.message_utils import sendMessage, editMessage, sendMarkup
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper import button_build

drive = ["nxUpload", "hnUpload", "bzUpload", "lnUpload"]

def list_buttons(update, context):
    user_id = update.message.from_user.id
    try:
        key = update.message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return sendMessage('Send a search key along with command', context.bot, update)
    buttons = button_build.ButtonMaker()
    buttons.sbutton(drive[0], 0)
    buttons.sbutton(drive[1], 1)
    buttons.sbutton(drive[2], 2)
    buttons.sbutton(drive[3], 3)
    button = InlineKeyboardMarkup(buttons.build_menu(2))
    sendMarkup('Choose option to upload.', context.bot, update, button)

def select_type(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    msg = query.message
    key = msg.reply_to_message.text.split(" ", maxsplit=1)[1]
    data = query.data
    data = data.split(" ")
    if data[2] in [0,1,2,3]:
        query.answer()
        editMessage(f"<b>Uploading to <i>{drive[data[2]]}</i></b>", msg)
        return data[2]
    else:
        query.answer()
        editMessage("Error", msg)

list_handler = CommandHandler(BotCommands.ListCommand, list_buttons, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
list_type_handler = CallbackQueryHandler(select_type, pattern="types", run_async=True)
dispatcher.add_handler(list_handler)
dispatcher.add_handler(list_type_handler)
