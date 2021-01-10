from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


button_hi = KeyboardButton('/help')

greet_kb = ReplyKeyboardMarkup()
greet_kb.add(button_hi)


greet_kb1 = ReplyKeyboardMarkup(resize_keyboard=True).add(button_hi)

greet_kb2 = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(button_hi)

button1 = KeyboardButton('/исследования')
button2 = KeyboardButton('/новость')
button3 = KeyboardButton('/блог')

markup3 = ReplyKeyboardMarkup().add(
    button1).add(button2).add(button3)

greet_kb1= ReplyKeyboardMarkup(resize_keyboard=True).row(
    button1, button2, button3
).add(button_hi)

markup5 = ReplyKeyboardMarkup().row(
    button1, button2, button3
).add(KeyboardButton('Команды'))

button4 = KeyboardButton('4️⃣')
button5 = KeyboardButton('5️⃣')
button6 = KeyboardButton('6️⃣')
markup5.row(button4, button5)
markup5.insert(button6)

markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отправить свой контакт ☎️', request_contact=True)
).add(
    KeyboardButton('Отправить свою локацию 🗺️', request_location=True)
)

markup_big = ReplyKeyboardMarkup()

markup_big.add(
    button1, button2, button3, button4, button5, button6
)
markup_big.row(
    button1, button2, button3, button4, button5, button6
)

markup_big.row(button4, button2)
markup_big.add(button3, button2)
markup_big.insert(button1)
markup_big.insert(button6)
markup_big.insert(KeyboardButton('9️⃣'))

import requests
import json



inline_kb_start = InlineKeyboardMarkup(row_width=2)
inline_btn_1 = InlineKeyboardButton('/research')
inline_btn_2 = InlineKeyboardButton('/news')
inline_btn_3 = InlineKeyboardButton('/post')

inline_kb_start.add(inline_btn_1, inline_btn_2, inline_btn_3)

inline_kb_full = InlineKeyboardMarkup(row_width=2)
inline_btn_3 = InlineKeyboardButton('кнопка 3', callback_data='btn3')
inline_btn_4 = InlineKeyboardButton('кнопка 4', callback_data='btn4')
inline_btn_5 = InlineKeyboardButton('кнопка 5', callback_data='btn5')


r = requests.get('https://back.qliento.com/research/')
data = json.loads(r.text)
inline_kb = []
for research in data:
	msg = research['name']
	url = 'https://back.qliento.com/researches/' + str(research['id'])
	inline = InlineKeyboardButton(research['name'],url=url)
	inline_kb_full.add(inline)



