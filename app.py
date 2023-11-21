from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo
import sqlite3

bot = Bot("")
dp = Dispatcher(bot)

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

def check_role(user_id):
    query = "SELECT role FROM users WHERE user_id = ?"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    return None

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Сайт", url="https://electronxray.com/?ysclid=lgcb4ets7a378836788"))

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Зарегистрироваться", web_app=WebAppInfo(url="http://127.0.0.1:5000")))
    keyboard.add(types.KeyboardButton("Войти", web_app=WebAppInfo(url="http://127.0.0.1:5000/login")))

    await message.answer("Добро пожаловать!", reply_markup=markup)
    await message.answer("Выберете действие", reply_markup=keyboard)

async def reg(message: types.Message):
    user_id = message.from_user.id
    role = check_role(user_id)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if role == "user":
        keyboard.add(types.KeyboardButton("Создать запрос"))

    await message.answer("Выберете дейстие")

@dp.message_handler(lambda message: message.text == "Создать запрос")
async def create_request(message: types.Message):
    await message.answer("Ваш запрос был успешно создан!")


if __name__ == "__main__":
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
