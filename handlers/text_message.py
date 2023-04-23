from conversation_starters import EMA_WITH_TEXT
from openai_chat_completion import openai_chat_completion

def text_message(bot, message, os, openai, is_reply=False):

    message_without_conversation_starter = message.text.replace(
        EMA_WITH_TEXT, '')

    message_for_openai = message_without_conversation_starter

    if is_reply:
        reply_message = message_without_conversation_starter + \
            " " + message.reply_to_message.text
        message_for_openai = reply_message

    response = openai_chat_completion(message_for_openai, message, openai)

    bot.send_message(chat_id=message.chat.id, text=response, reply_to_message_id=message.message_id)
