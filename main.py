from aiogram import Dispatcher, Bot, types
from aiogram.utils import executor
from aiogram.types.web_app_info import WebAppInfo
import json
import requests

bot = Bot('6959993559:AAHQKkBdT5MBPwzvSw0asEcl3x-2TR7F6n8')
dp = Dispatcher(bot)
login_web_link = 'https://mannopboy.github.io/register_bot/'
login_link = 'http://127.0.0.1:5000/login_bot'
get_student_daily_table_bot = 'http://127.0.0.1:5000/get_student_daily_table_bot'
get_student_table_bot = 'http://127.0.0.1:5000/get_student_table_bot'
get_class_student_bot = 'http://127.0.0.1:5000/get_class_student_bot'
get_class_teacher_bot = 'http://127.0.0.1:5000/get_class_teacher_bot'
get_student_month_payments_bot = 'http://127.0.0.1:5000/get_student_month_payments_bot'
get_student_month_in_payments_bot = 'http://127.0.0.1:5000/get_student_month_in_payments_bot'
get_student_data_bot = 'http://127.0.0.1:5000/get_student_data_bot'
user = {
    'user_id': None, 'username': None, 'role': None}


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
    markup.add(types.KeyboardButton('Mening sinfim 🏰'), types.KeyboardButton("Mening o'qituvchilarim 👨🏻‍🏫"))
    markup.add(types.KeyboardButton('Mening profilim 🙍🏻‍♂️'))
    markup.add(types.KeyboardButton('Dars jadvali 📑'), types.KeyboardButton('Bugungi dars jadvali 📅'))
    markup.add(types.KeyboardButton("Oylik to'lovlar 📄"), types.KeyboardButton("Mening to'lovlarim 💳"))
    markup.add(types.KeyboardButton("Baholarim 📈"))
    return markup


@dp.message_handler(commands=['start'])
async def start(massage: types.Message):
    markup = button_keyboard_start()
    await massage.answer('Salom botdan foydalanish uchun login tugmasini bosing', reply_markup=markup)


@dp.message_handler(content_types=['web_app_data'])
async def web_app(massage: types.Message):
    username = json.loads(massage.web_app_data.data)['name']
    password = json.loads(massage.web_app_data.data)['password']
    data = {
        'username': username, 'password': password
    }
    request = requests.post(login_link, json=data)
    if request.status_code == 200:
        user['user_id'] = request.json()['data']['user_id']
        user['username'] = request.json()['data']['username']
        user['role'] = request.json()['data']['role']
        markup = button_keyboard_student()
        print(user['username'])
        await massage.reply(f"Salom  {user['username']}, bo'taga kirdingiz ishlatishingiz munkin.", reply_markup=markup)
    else:
        await massage.reply("Bo'taga kira olmadingiz qayta urining.")


@dp.message_handler()
async def start(massage: types.Message):
    if massage.text == 'Bugungi dars jadvali 📅' and user['role'] == 'Student':
        request = requests.post(get_student_daily_table_bot, json=user)
        if request.status_code == 200 and request.json()['data']:
            for lesson in request.json()['data']:
                text = f"{lesson['lesson_time']}-Dars: {lesson['lesson']} \nO'qituvchi: {lesson['teacher']} \nBoshlanish vaqti: {lesson['time']['start']} \nTugash vaqti: {lesson['time']['end']} \nXona: {lesson['rome']}"
                await massage.answer(text)
        else:
            await massage.answer("Bugun dars yo'q")
    elif massage.text == 'Dars jadvali 📑' and user['role'] == 'Student':
        request = requests.post(get_student_table_bot, json=user)
        if request.status_code == 200 and request.json()['data']:
            for day in request.json()['data']:
                kun = f"Kun: {day['day_name']} \n"
                lessons = ''
                for lesson in day['day_lessons']:
                    lessons += f"{lesson['lesson_time']}-Dars: {lesson['lesson']} \n   O'qituvchi: {lesson['teacher']} \n   Xona: {lesson['rome']} \n"
                text = kun + lessons
                await massage.reply(text)
        else:
            await massage.reply("Bu hafta dars yo'q")
    elif massage.text == 'Mening sinfim 🏰' and user['role'] == 'Student':
        request = requests.post(get_class_student_bot, json=user)
        if request.status_code == 200 and request.json()['data']:
            classes = request.json()['data']
            student_len = f"Sinf nomi: {classes['class_name']}  O'quvchilar soni : {classes['student_len']} \nO'quvchilar:\n"
            students = ''
            number = 0
            for student in classes['students']:
                number += 1
                students += f"  {number}-O'quvchi: {student['student_name']} \n"
            text = student_len + students
            await massage.reply(text)
        else:
            await massage.reply("Sinfing yo'q")
    elif massage.text == "Mening o'qituvchilarim 👨🏻‍🏫" and user['role'] == 'Student':
        request = requests.post(get_class_teacher_bot, json=user)
        if request.status_code == 200 and request.json()['data']:
            classes = request.json()['data']
            teacher_len = f"Sinf nomi: {classes['class_name']}  O'qituvchilar soni : {classes['teacher_len']} \nO'qituvchilar:\n"
            teachers = ''
            number = 0
            for teacher in classes['teachers']:
                number += 1
                teachers += f"  {number}-O'quvchi: {teacher['teacher_name']}  Fan: {teacher['teacher_subject']}\n"
            text = teacher_len + teachers
            await massage.reply(text)
        else:
            await massage.reply("O'qituvchilar yo'q")
    elif massage.text == "Oylik to'lovlar 📄" and user['role'] == 'Student':
        request = requests.post(get_student_month_payments_bot, json=user)
        if request.status_code == 200 and request.json()['data']:
            text = "To'lovlar \n\n"
            for pay in request.json()['data']:
                text += f"  Oy: {pay['month']}\n  Umumiy summa: {pay['class_price']}\n  To'langan: {pay['payed']}\n\n"
            await massage.reply(text)
        else:
            await massage.reply("To'lovlar yo'q")
    elif massage.text == "Mening to'lovlarim 💳" and user['role'] == 'Student':
        request = requests.post(get_student_month_in_payments_bot, json=user)
        if request.status_code == 200 and request.json()['data']:
            text = "To'lovlaringiz  \n\n"
            for pay in request.json()['data']:
                for pay_in in pay['payments']:
                    text += f"  Oy: {pay['month']}\n  To'langan summa: {pay_in['payed']}\n  To'lov turi: {pay_in['account_type']}\n  To'lov vaqti: {pay_in['date']}\n\n"
            await massage.reply(text)
        else:
            await massage.reply("To'lov qilmagansiz")
    elif massage.text == "Mening profilim 🙍🏻‍♂️" and user['role'] == 'Student':
        request = requests.post(get_student_data_bot, json=user)
        if request.status_code == 200 and request.json()['data']:
            user_b = request.json()['data']
            text = f"Foydalanuvchi nomingiz: {user_b['username']}\n\n  Ismingiz: {user_b['name']}\n  Familyangiz: {user_b['surname']}\n  Otangizning ismi: {user_b['parent_name']}\n  Raqamingiz: {user_b['number']}\n  Emailingiz: {user_b['email']}\n  Yoshingiz: {user_b['age']}\n"
            await massage.reply(text)
        else:
            await massage.reply("Malumotlar yo'q")


executor.start_polling(dp)
