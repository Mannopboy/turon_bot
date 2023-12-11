from aiogram import Dispatcher, Bot, types
from aiogram.utils import executor
from aiogram.types.web_app_info import WebAppInfo
import json
import requests

bot = Bot('6959993559:AAHQKkBdT5MBPwzvSw0asEcl3x-2TR7F6n8')
dp = Dispatcher(bot)
login_web_link = 'https://mannopboy.github.io/register_bot/'
login_link = 'http://127.0.0.1:5000/login_bot'
student_daily_table_link = 'http://127.0.0.1:5000/student_daily_table_bot'
user = {
    'username': None, 'role': None
}


def button_text_start():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Login', web_app=WebAppInfo(url=login_web_link)))
    return markup


def button_keyboard_start():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Login', web_app=WebAppInfo(url=login_web_link)))
    return markup


def button_keyboard_student():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton('Mening sinfim 🏰'), types.KeyboardButton("Mening o'qtuvchilarim 👨🏻‍🏫"))
    markup.add(types.KeyboardButton('Mening profilim 🙍🏻‍♂️'))
    markup.add(types.KeyboardButton('Dars jadvali 📑'), types.KeyboardButton('Bugungi dars jadvali 📅'))
    markup.add(types.KeyboardButton("Oylik to'lovlar 📄"), types.KeyboardButton("Mening to'lovlarim 💳"))
    markup.add(types.KeyboardButton("Baholarim 📈"))
    return markup


@dp.message_handler()
async def start(massage: types.Message):
    if massage.text == 'Bugungi dars jadvali 📅':
        request = requests.post(student_daily_table_link, json=user)
        print(request)
        print(request.json())


@dp.message_handler(commands=['start'])
async def start(massage: types.Message):
    markup = button_keyboard_start()
    await massage.answer('Salom !!!', reply_markup=markup)


@dp.message_handler(content_types=['web_app_data'])
async def web_app(massage: types.Message):
    username = json.loads(massage.web_app_data.data)['name']
    password = json.loads(massage.web_app_data.data)['password']
    data = {
        'username': username, 'password': password
    }
    request = requests.post(login_link, json=data)
    if request.status_code == 200:
        user['username'] = request.json()['data']['username']
        user['role'] = request.json()['data']['role']
        markup = button_keyboard_student()
        await massage.reply(f"Salom  {user['username']}, bo'taga kirdingiz ishlatishingiz munkin.", reply_markup=markup)
    else:
        await massage.reply("Bo'taga kira olmadingiz qayta urining.")


executor.start_polling(dp)
