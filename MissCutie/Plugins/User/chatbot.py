import re
import requests
from time import sleep
from MissCutie import AI_API_KEY, dispatcher
from MissCutie.Handlers.validation import bot_admin, is_user_admin, user_admin
from MissCutie.Handlers.filters import CustomFilters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, Filters, MessageHandler, run_async

Kristina_chats = []
BOT_ID = 5071423206

@user_admin
def chatbot_toggle(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("Enable", callback_data="chatbot_enable"),
            InlineKeyboardButton("Disable", callback_data="chatbot_disable"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Choose an option:", reply_markup=reply_markup)

def chatbot_handle_callq(update: Update, context: CallbackContext):
    query = update.callback_query
    user = update.effective_user
    chat = update.effective_chat
    action = query.data.split("_")[1]

    if not is_user_admin(chat, user.id):
        return query.answer("This is not for you.")

    if action == "delete":
        query.message.delete()

    elif action == "enable":
        if chat.id in Kristina_chats:
            return query.answer("Chatbot is already enabled")
        Kristina_chats.append(chat.id)
        query.answer("Chatbot enabled")
        query.message.delete()

    elif action == "disable":
        if chat.id not in Kristina_chats:
            return query.answer("Chatbot is already disabled")
        Kristina_chats.remove(chat.id)
        query.answer("Chatbot disabled")
        query.message.delete()

    else:
        query.answer()


def chatbot_response(query: str, user_id: int) -> str:
    data = requests.get(
        f"http://api.brainshop.ai/get?bid=178&"
        + f"key={AI_API_KEY}&uid=mashape&msg={query}",
    )
    response = data.json()["cnt"]
    return response


def check_message(context: CallbackContext, message):
    reply_msg = message.reply_to_message
    text = message.text
    if re.search("[.|\n]{0,}"+dispatcher.bot.first_name+"[.|\n]{0,}", text, flags=re.IGNORECASE):
        return True
    if reply_msg and reply_msg.from_user.id == BOT_ID:
        return True
    elif message.chat.type == 'private':
        return True
    else:
        return False


def chatbot(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat_id = update.effective_chat.id
    is_chat = chat_id in Kristina_chats
    bot = context.bot
    if not is_chat:
        return
    if msg.text and not msg.document:
        if not check_message(context, msg):
            return
        # lower the text to ensure text replace checks
        query = msg.text.lower()
        botname = bot.first_name.lower()
        if botname in query:
            query = query.replace(botname, "bot.name")
        bot.send_chat_action(chat_id, action="typing")
        user_id = update.message.from_user.id
        response = chatbot_response(query, user_id)
        if "Aco" in response:
            response = response.replace("Aco", bot.first_name)
        if "bot.name" in response:
            response = response.replace("bot.name", bot.first_name)
        sleep(0.3)
        msg.reply_text(response, timeout=60)


def list_all_chats(update: Update, context: CallbackContext):
    text = "<b>MissCutie Enabled Chats</b>\n"
    for chat in Kristina_chats:
        x = context.bot.get_chat(chat)
        name = x.title or x.first_name
        text += f"• <code>{name}</code>\n"
    update.effective_message.reply_text(text, parse_mode="HTML")


__help__ = f"""
Chatbot utilizes the Brainshop's API and allows {dispatcher.bot.first_name} to talk and provides a more interactive group chat experience.
*Commands:*
*Admins only:*
➢ `/chatbot`*:* Shows chatbot control panel
"""

CHATBOT_TOGGLE_COMMAND_HANDLER = CommandHandler("chatbot", chatbot_toggle, run_async=True)
CHATBOT_TOGGLE_CALLBACK_HANDLER = CallbackQueryHandler(chatbot_handle_callq, pattern=r"chatbot_", run_async=True)
CHATBOT_HANDLER = MessageHandler(
    Filters.text & (~Filters.regex(r"^#[^\s]+") & ~Filters.regex(r"^!")
                    & ~Filters.regex(r"^\/")), chatbot, run_async=True)
LIST_ALL_CHATS_HANDLER = CommandHandler(
    "allchats", list_all_chats, filters=CustomFilters.dev_filter, run_async=True)

# Filters for ignoring #note messages, !commands and sed.

dispatcher.add_handler(CHATBOT_TOGGLE_COMMAND_HANDLER)
dispatcher.add_handler(CHATBOT_TOGGLE_CALLBACK_HANDLER)
dispatcher.add_handler(CHATBOT_HANDLER)
dispatcher.add_handler(LIST_ALL_CHATS_HANDLER)

__mod_name__ = "Chatbot"
__command_list__ = ["chatbot", "allchats"]
__handlers__ = [
    CHATBOT_TOGGLE_CALLBACK_HANDLER,
    CHATBOT_TOGGLE_COMMAND_HANDLER,
    CHATBOT_HANDLER,
    LIST_ALL_CHATS_HANDLER,
]
