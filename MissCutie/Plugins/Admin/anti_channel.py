import re, html
from telegram import ParseMode, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    run_async,
)
from telegram.utils.helpers import mention_html, mention_markdown, escape_markdown
from MissCutie.Handlers.validation import user_admin, user_admin_no_reply
from MissCutie.Plugins.Admin.log_channel import gloggable




@user_admin_no_reply
@gloggable
def anti_c_mode_off(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"rm_mode\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat
        is_channel = sql.rem_channel(chat.id)
        if is_channel:
            is_channel = sql.rem_channel(user_id)
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"ANTI_CHANNEL_MODE_DISABLED\n"
                f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        else:
            update.effective_message.edit_text(
                "Anti Channel Mode disable by {}.".format(mention_html(user.id, user.first_name)),
                parse_mode=ParseMode.HTML,
            )

    return ""



@user_admin_no_reply
@gloggable
def anti_c_mode_on(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"add_channel\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat
        is_channel = sql.set_misscutie(chat.id)
        if is_channel:
            is_channel = sql.set_misscutie(user_id)
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"AI_ENABLE\n"
                f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        else:
            update.effective_message.edit_text(
                "Anti-Channel enable by {}.".format(mention_html(user.id, user.first_name)),
                parse_mode=ParseMode.HTML,
            )

    return ""

@user_admin
@gloggable
def antichannel(update: Update, context: CallbackContext):
    user = update.effective_user
    message = update.effective_message
    msg = f"Choose an option"
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            text="Enable",
            callback_data="anti_c_mode_on")],
       [
        InlineKeyboardButton(
            text="Disable",
            callback_data="anti_c_mode_off")]])
    message.reply_text(
        msg,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )



__help__ = f"""
Through this menu you can set a punishment for users who write in the group masquerading as a channel.

ℹ️ Telegram allows each user to write to the group by hiding through a channel they own.

👮🏻‍♂️ It's not possible to know which user is writing via a channel and if it is an administrator: this block will apply to whoever writes via a channel.

🏃🏻 If this option is active, a user who was writing via a channel will only be able to continue writing to the group but only via his real identity and no longer via other channels.
*Commands:*
*Admins only:*
➢ `/antichannel`*:* Shows Anti-Channel control panel
"""



ANTICHANNEL_PANEL_COMMAND_HANDLER = CommandHandler("antichannel", run_async=True)
ANTICHANNEL_ON_COMMAND_HANDLER = CommandHandler("antichannelon", anti_c_mode_on, run_async=True)
ANTICHANNEL_OFF_COMMAND_HANDLER = CommandHandler("antichanneloff", anti_c_mode_off, run_async=True)


# Filters for ignoring #note messages, !commands and sed.

dispatcher.add_handler(ANTICHANNEL_PANEL_COMMAND_HANDLER)
dispatcher.add_handler(ANTICHANNEL_ON_COMMAND_HANDLER)
dispatcher.add_handler(ANTICHANNEL_OFF_COMMAND_HANDLER)

__mod_name__ = "Anti-Channel"
__command_list__ = ["antichannel", "antichannelon", "antichanneloff"]
__handlers__ = [
    ANTICHANNEL_PANEL_COMMAND_HANDLER,
    ANTICHANNEL_ON_COMMAND_HANDLER,
    ANTICHANNEL_OFF_COMMAND_HANDLER,
]
