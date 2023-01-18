from telegram.ext.filters import Filters
from telegram import Update, message
from MissCutie import dispatcher
from telegram.ext import CallbackContext, CommandHandler
from telegram.ext.messagehandler import MessageHandler
import html
from MissCutie.Plugins.disable import DisableAbleCommandHandler
from MissCutie.Database.antichannel_sql import antichannel_status, disable_antichannel, enable_antichannel
from MissCutie.Handlers.validation import user_admin

@user_admin
def set_antichannel(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    args = context.args
    if len(args) > 0:
        s = args[0].lower()
        if s in ["yes", "on"]:
            enable_antichannel(chat.id)
            message.reply_html(f"Enabled antichannel in {html.escape(chat.title)}")
        elif s in ["off", "no"]:
            disable_antichannel(chat.id)
            message.reply_html(f"Disabled antichannel in {html.escape(chat.title)}")
        else:
            message.reply_text(f"Unrecognized arguments {s}")
        return
    message.reply_html(
        f"Antichannel setting is currently {antichannel_status(chat.id)} in {html.escape(chat.title)}"
    )

def eliminate(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    bot = context.bot
    if not antichannel_status(chat.id):
        return
    if message.sender_chat and message.sender_chat.type == "channel" and not message.is_automatic_forward:
        message.delete()
        sender_chat = message.sender_chat
        bot.ban_chat_sender_chat(sender_chat_id=sender_chat.id, chat_id=chat.id)
        
dispatcher.add_handler(MessageHandler(filters=Filters.chat_type.groups, callback=eliminate), group=101)
dispatcher.add_handler(
    CommandHandler(command="antichannel", callback=set_antichannel, run_async=True, filters=Filters.chat_type.groups),
    group=100)


__help__ = """
Through this menu you can set a punishment for users who write in the group masquerading as a channel.

ℹ️ Telegram allows each user to write to the group by hiding through a channel they own.

👮🏻‍♂️ It's not possible to know which user is writing via a channel and if it is an administrator: this block will apply to whoever writes via a channel.

🏃🏻 If this option is active, a user who was writing via a channel will only be able to continue writing to the group but only via his real identity and no longer via other channels.
*Commands:*
*Admins only:*
➢ `/antichannel on`*:* Anti-Channel service on
➢ `/antichannel off`*:* Anti-Channel service off
"""

__mod_name__ = "Anti-Channel"
__command_list__ = ["antichannel", "antichannelon", "antichanneloff"]
