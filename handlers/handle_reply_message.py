from conversation_starters import EMA_WITH_TEXT, EMA_WITH_VOICE, EMA_WITH_PHOTO, EMA_WITH_IMAGE_VARIATION, EMA_TRANSCRIBE_AUDIO
from handlers.text_message import text_message
from handlers.audio_message import audio_message
from handlers.photo_generate_message import photo_generate_message
from handlers.image_variation_message import image_variation_image
from handlers.transcribe_audio_message import transcribe_audio_message

def reply_to_message(message, bot, Image, openai, detect, os, subprocess):
    
    if message.reply_to_message.content_type == 'text':
        if message.text.lower().startswith(EMA_WITH_TEXT):
            text_message(bot, message, os, openai, is_reply=True)
        elif message.text.lower().startswith(EMA_WITH_VOICE):
            audio_message(bot, os, subprocess, openai, detect, message, is_reply=True)
        elif message.text.lower().startswith(EMA_WITH_PHOTO):
            photo_generate_message(openai, bot, message, is_reply=True)
        elif message.text.lower().startswith(EMA_WITH_IMAGE_VARIATION):
            bot.send_message(chat_id=message.chat.id, text='I can not generate photo variations based on text.', reply_to_message_id=message.message_id)
    elif message.reply_to_message.content_type == 'photo':
        if message.text.lower().startswith(EMA_WITH_IMAGE_VARIATION):
            image_variation_image(bot, Image, openai, message, is_reply=True)
        else:
            bot.send_message(chat_id=message.chat.id, text='I can not generate text or voice based on photo.', reply_to_message_id=message.message_id)
    elif message.reply_to_message.content_type == 'voice' and message.text.lower().startswith(EMA_TRANSCRIBE_AUDIO):
        transcribe_audio_message(message, bot, os)
    else:
        bot.send_message(chat_id=message.chat.id, text='Other formats are not supported right now.', reply_to_message_id=message.message_id)