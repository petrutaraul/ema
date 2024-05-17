from conversation_starters import EMA_WITH_PHOTO

def photo_generate_message(openai, bot, message, is_reply=False):
    message_without_conversation_starter = message.text.replace(EMA_WITH_PHOTO, '')
    
    message_for_openai = message_without_conversation_starter
    
    if is_reply:
        reply_message = message.reply_to_message.text
        message_for_openai = reply_message
    
    response = openai.images.generate(
        prompt=message_for_openai,
        n=1
    )
    print(response);
    image_url = response.data[0].url
    
    bot.send_photo(chat_id=message.chat.id, photo=image_url, reply_to_message_id=message.message_id)