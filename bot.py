from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from emoji import emojize
from mp3downloader import Mp3Downloader
from re import match
import os
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


class Bcyt3Bot:
    def __init__(self, token):
        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.downloader = Mp3Downloader()
        self.url_regex = r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"
        self.set_handlers()

    def set_handlers(self):
        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)

        echo_handler = MessageHandler(Filters.text, self.echo)
        self.dispatcher.add_handler(echo_handler)

        self.updater.start_polling()

    def start(self, update, context):
        blush = emojize(":blush:", use_aliases=True)
        message = ("Olá! Eu sou o Bcyt3Bot, meu nome é a abreviatura de Bot Converter Youtube to Mp3. "
                   "Pelo que você deve ter percebido eu converto músicas do youtube para mp3 e te envio, "
                   f"basta me enviar o link das suas músicas preferidas que te enviarei aqui mesmo {blush}")
        context.bot.send_message(chat_id=update.message.chat_id, text=message)

    def echo(self, update, context):
        msg = update.message.text
        chat_id = update.message.chat_id
        bot = context.bot

        if match(self.url_regex, msg) and "youtube" in msg:
            arrow_heading_down = emojize(
                ":arrow_heading_down:", use_aliases=True)
            text_sending = f"Ok! Recebi a sua música, baixando em 3...2...1... {arrow_heading_down}"
            bot.send_message(chat_id=chat_id, text=text_sending)

            self.downloader.download(msg)

            text_sending = "Olha só! Consegui baixar a sua música, estou te enviando! Pode ser que demore um pouco."
            bot.send_message(chat_id=chat_id, text=text_sending)

            music_name = self.getting_music_name()
            audio = open(music_name, 'rb')
            bot.send_audio(chat_id=chat_id, audio=audio, timeout=5000)

            audio.close()
            os.remove(music_name)

            smirk = emojize(":smirk:", use_aliases=True)
            musical_note = emojize(":musical_note:", use_aliases=True)
            text_sending = f"Pronto, ai está a sua música {musical_note} ! Pode me enviar mais links se quiser. {smirk}"
            bot.send_message(chat_id=chat_id, text=text_sending)
        else:
            bot.send_message(
                chat_id=chat_id, text="Desculpa, eu baixo apenas músicas do youtube, esta URL não é válida =/")

    def getting_music_name(self):
        for file in os.listdir():
            if ".mp3" in file:
                return file


bot = Bcyt3Bot("INSERT YOUR TELEGRAM TOKEN HERE")
