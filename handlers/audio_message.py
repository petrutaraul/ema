from conversation_starters import EMA_WITH_VOICE
from config import BOT_VOICE
from openai_chat_completion import openai_chat_completion
import requests
import json

def audio_message(bot, os, subprocess, openai, detect, message, is_reply=False):
    # URL from https://github.com/rany2/edge-tts/blob/master/src/edge_tts/constants.py
    EDGE_TTS_URL = "https://speech.platform.bing.com/consumer/speech/synthesize/readaloud/voices/list?trustedclienttoken=6A5AA1D4EAFF4E9FB37E23D68491D6F4"

    response = requests.get(EDGE_TTS_URL)
    data = response.json()

    message_without_conversation_starter = message.text.replace(
        EMA_WITH_VOICE, '')

    message_for_openai = message_without_conversation_starter

    if is_reply:
        reply_message = message_without_conversation_starter + \
            " " + message.reply_to_message.text
        message_for_openai = reply_message

    response = openai_chat_completion(message_for_openai, message, openai)

    fileName = "Emato" + message.from_user.username + ".mp3"

    text = response

    lang = detect(text)
    language = ''

    for obj in data:
        # Check if the ShortName starts with 'lang'
            if obj['ShortName'].startswith(lang) and obj['Gender'] == BOT_VOICE:
                # Set language to the ShortName
                language = obj['ShortName']
                # Stop looping since we only want the first object
                break

    # use edge-tts to convert text to speech and save it as an mp3 file. Remove special characters from text
    removeSpecialChars = text.replace("'", "")
    edgeCommand = f"edge-tts -v '{language}' -t '{removeSpecialChars}' --write-media {fileName}"

    try:
        subprocess.run(edgeCommand, shell=True, check=True)
        with open(fileName, "rb") as f:
            audio_buffer = f.read()
        os.remove(fileName)
        bot.send_voice(chat_id=message.chat.id, voice=audio_buffer,
                       reply_to_message_id=message.message_id)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred (TTS request): {e}")
