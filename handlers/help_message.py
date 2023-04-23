def help_message(bot, message):
    
    help_message = """
    
    @ema - Receive a text message from Ema
    @vema - Receive a vocal message from Ema
    @pema - Receive a generated photo from Ema
    @iema - Receive an variation image from Ema (Only applicable on photos)
    @tema - Receive a vocal transcribe text from Ema (Only applicable on vocals)
    
    """

    bot.send_message(chat_id=message.chat.id, text=help_message, reply_to_message_id=message.message_id)