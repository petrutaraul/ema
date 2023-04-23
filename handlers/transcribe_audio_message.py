import whisper


def transcribe_audio_message(message, bot, os):
    voice_file = bot.get_file(message.reply_to_message.voice.file_id)

    downloaded_file = bot.download_file(voice_file.file_path)
    with open('received_voice.mpga', 'wb') as voice_file:
        # Your code here
        voice_file.write(downloaded_file)

    model = whisper.load_model('medium')
    PATH = 'received_voice.mpga'
    result = model.transcribe(PATH)

    # send the transcribed text to the user as a reply using txt_file.read()
    bot.send_message(chat_id=message.chat.id, text=result["text"],
                     reply_to_message_id=message.message_id)

    # delete all files which starts with received_voice from local directory
    os.system('rm received_voice*')
