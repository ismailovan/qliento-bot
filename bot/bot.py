import logging
import asyncio

from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions
import kb

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import requests
import json


from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from bot.settings import (BOT_TOKEN, HEROKU_APP_NAME,
                          WEBHOOK_URL, WEBHOOK_PATH,
                          WEBAPP_HOST, WEBAPP_PORT)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())





async def on_startup(dp):
    logging.warning(
        'Starting connection. ')
    await bot.set_webhook(WEBHOOK_URL,drop_pending_updates=True)

@dp.message_handler(commands=['новость'])
async def process_help_command(message: types.Message):
    r = requests.get('https://back.qliento.com/news/')
    data = json.loads(r.text)
    msg = data[0]
    picture = msg['image']
    msgg = text(bold(msg['name'])) + '\n' + text(italic(msg['description']))
    await message.reply(msgg, parse_mode=ParseMode.MARKDOWN)
    await bot.send_photo(message.chat.id, types.InputFile.from_url(picture))


@dp.message_handler(commands=['блог'])
async def process_help_command(message: types.Message):
    r = requests.get('https://back.qliento.com/blog/')
    data = json.loads(r.text)
    msg = data[0]
    msgg = text(bold(msg['header'])) + '\n' + text(italic(msg['description']))
    await message.reply(msgg, parse_mode=ParseMode.MARKDOWN)



@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Здравствуйте! Чтобы найти исследование, отправьте его название", reply_markup=kb.greet_kb1)



@dp.message_handler(commands=['исследования'])
async def process_command_2(message: types.Message):
    await message.reply("Отправляю все возможные исследования",
                        reply_markup=kb.inline_kb_full)

help_message = text(
    "/исследования - ссылки на все исследования",
    "/блог - самая свежая аналитика",
    "/новость - самая свежая новость",
    "Чтобы найти исследование, отправьте его название",
    sep="\n"
)

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(help_message)

@dp.message_handler()
async def echo(message: types.Message):
    url = 'https://back.qliento.com/researches/?name__icontains=' + message.text
    r = requests.get(url)
    data = json.loads(r.text)

    if len(data) != 0:
        inline_kb = []
        inline_kb_full = InlineKeyboardMarkup(row_width=2)
        for research in data:
            msg = research['name']
            url = 'https://back.qliento.com/researches/' + str(research['id'])
            inline = InlineKeyboardButton(research['name'],url=url)
            inline_kb_full.add(inline)
        await message.answer('Вот, что мне удалось найти: ', reply_markup=inline_kb_full)
    else:
        await message.answer('К сожалению, ничего не нашлось. Закажите ваше персональное исследование у нас на сайте:\nhttps://www.qliento.com/order-research')



async def on_shutdown(dp):
    logging.warning('Bye! Shutting down webhook connection')


def main():
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
