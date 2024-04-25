from flask import Flask, request
from .gemini import Gemini
from md2tgmd import escape
from telegram.ext import ApplicationBuilder
from telegram import Update
from os import getenv
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image

load_dotenv()


app = Flask(__name__)

gemini = Gemini()

telegram_app = ApplicationBuilder().token(getenv('TELEGRAM_BOT_TOKEN')).build()


@app.get('/')
def hello_world():
    return 'Hello, World!'


@app.post('/webhook')
def webhook():
    chat_id = None
    try:
        body = request.get_json()

        update = Update.de_json(body, telegram_app.bot)

        chat_id = update.message.chat_id

        if update.edited_message:
            return 'OK'

        if update.message.text == '/start':
            return {
                "method": "sendMessage",
                "chat_id": chat_id,
                "text": 'Welcome!'
            }

        

        
        if update.message.photo:
            file_id = update.message.photo[-1].file_id
            file = telegram_app.bot.get_file(file_id)
            bytesIO = BytesIO(file.download_as_bytearray())

            image = Image.open(bytesIO)

            prompt = 'Describe the image'

            if update.message.caption:
                prompt = update.message.caption

            text = gemini.send_image(prompt, image)

            return {
                "method": "sendMessage",
                "chat_id": chat_id,
                "text": escape(text),
                "parse_mode": "MarkdownV2"
            }
        else:
            chat = gemini.get_model().start_chat()
            text = gemini.send_message(update.message.text, chat)

        return {
            "method": "sendMessage",
            "chat_id": chat_id,
            "text": escape(text),
            "parse_mode": "MarkdownV2"
        }
    except Exception as error:
        return {
            "method": "sendMessage",
            "chat_id": chat_id,
            "text": 'Sorry, I am not able to generate content for you right now. Please try again later. '
        }
