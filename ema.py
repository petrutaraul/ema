from bot_started import bot_started

bot_started()

import os
import telebot
import openai
import subprocess
from langdetect import detect
from PIL import Image

from handlers.text_message import text_message
from handlers.audio_message import audio_message
from handlers.photo_generate_message import photo_generate_message
from handlers.image_variation_message import image_variation_image
from handlers.handle_reply_message import reply_to_message
from handlers.help_message import help_message
from config import OPEN_API_KEY, TELEGRAM_BOT_TOKEN
from conversation_starters import EMA_WITH_TEXT, EMA_WITH_VOICE, EMA_WITH_PHOTO, EMA_WITH_IMAGE_VARIATION, EMA_HELP

# Initialize the Telegram bot with your bot token
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Initialize the OpenAI API with your API key
openai.api_key = OPEN_API_KEY

# Define a function to handle incoming text messages

@bot.message_handler(func=lambda message: message.text and message.text.lower().startswith(EMA_WITH_TEXT) and not message.reply_to_message)
def text_message_handler(message):
    text_message(bot, message, os, openai)


@bot.message_handler(func=lambda message: message.text and message.text.lower().startswith(EMA_WITH_VOICE) and not message.reply_to_message)
def audio_message_handler(message):
    audio_message(bot, os, subprocess, openai, detect, message)


@bot.message_handler(func=lambda message: message.text and message.text.lower().startswith(EMA_WITH_PHOTO) and not message.reply_to_message)
def photo_generate_message_handler(message):
    photo_generate_message(openai, bot, message)


@bot.message_handler(func=lambda message: message.photo and not message.reply_to_message and message.caption and message.caption.lower().startswith(EMA_WITH_IMAGE_VARIATION), content_types=['photo'])
def image_variation_image_handler(message):
    image_variation_image(bot, Image, openai, message)


@bot.message_handler(func=lambda message: message.reply_to_message)
def reply_to_message_handler(message):
    reply_to_message(message, bot, Image, openai, detect, os, subprocess)


@bot.message_handler(func=lambda message: message.text and message.text.lower().startswith(EMA_HELP))
def help_message_handler(message):
    help_message(bot, message)


# Start the Telegram bot
bot.polling()
