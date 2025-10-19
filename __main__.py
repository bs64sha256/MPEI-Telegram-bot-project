from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, LabeledPrice, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

import os
import sys
import logging
import asyncio
import aiosqlite

load_dotenv()
TOKEN = os.getenv('TG_BOT_API_TOKEN')
ADMIN_ID = os.getenv('ADMIN_TG_ID')
PAYMENT_TOKEN = os.getenv('PAYMENT_TOKEN')

STAR_EMOJI = "\u2B50"
DB_PATH = r'db.sql'

prices_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=f'100 {STAR_EMOJI} на чай', callback_data='100'),
        InlineKeyboardButton(text=f'200 {STAR_EMOJI} на шаву ', callback_data='200')
    ],
    [
        InlineKeyboardButton(text=f'300 {STAR_EMOJI} спасибо!', callback_data='300'),
        InlineKeyboardButton(text=f'500 {STAR_EMOJI} СПАСИБО!', callback_data='500')
    ],
    [
        InlineKeyboardButton(text=f'100000 {STAR_EMOJI}\n( На Porshe 930 Turbo )', callback_data='porshe')
    ]
])

start_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Полезные кабинеты'), 
        KeyboardButton(text='Военная кафедра и спорт')
        ],
    [
        KeyboardButton(text='Зачеты и экзамены'), 
        KeyboardButton(text='Переводы'),
        KeyboardButton(text='Сессии и пересдачи')
        ],
    [
        KeyboardButton(text='Поддержать студенческие проекты 💰')
        ]
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Выберите опцию: ')

k_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='ИРЭ'), 
        KeyboardButton(text='ИЭТЭ'),
        KeyboardButton(text='ИГВИЭ'),
        ],
    [
        KeyboardButton(text='ЭнМИ'), 
        KeyboardButton(text='ИТАЭ'),
        KeyboardButton(text='ИЭВТ')
        ],
    [
        KeyboardButton(text='ИЭЭ'), 
        KeyboardButton(text='ИВТИ'),
        KeyboardButton(text='ГПИ')
        ], 
    [
        KeyboardButton(text='ИнЭИ'), 
        KeyboardButton(text='ВИИ')
        ]
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Выберите кафедру: ')

bot = Bot(TOKEN)
dp = Dispatcher()

async def create_table():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                ID INTEGER PRIMARY KEY,
                choose INTEGER DEFAULT 0
            )
        """)
        await db.commit()

async def add_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (ID, choose) VALUES (?, ?)",
            (user_id, 0)
        )
        await db.commit()

async def update_choose(user_id: int, new_value: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET choose = ? WHERE ID = ?",
            (new_value, user_id)
        )
        await db.commit()

async def get_choose(user_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT choose FROM users WHERE ID = ?",
            (user_id,)
        ) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else None

@dp.message(Command('start'))
async def start_command(message: Message):
    await message.answer('Первокурснику полезно знать:', reply_markup=start_keyboard)
    await add_user(message.from_user.id)

@dp.callback_query(F.data == '100')
async def invoice_100(callback: CallbackQuery) -> None:
    await callback.message.answer_invoice(
        photo_url=r'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRoozns7G40O4jq3MIYW2rvxqFyklp-nTTaAw&s',
        title='Поддержать бедных студентов', 
        description='Ведьмаку заплатите чеканой...',
        currency='XTR',
        prices=[LabeledPrice(label='Во благо...', amount=100)],
        protect_content=True,
        payload='100XTR',
        message_effect_id="5104841245755180586"
)
    
@dp.callback_query(F.data == '200')
async def invoice_100(callback: CallbackQuery) -> None:
    await callback.message.answer_invoice(
        photo_url=r'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRoozns7G40O4jq3MIYW2rvxqFyklp-nTTaAw&s',
        title='Поддержать бедных студентов', 
        description='Ведьмаку заплатите чеканой...',
        currency='XTR',
        prices=[LabeledPrice(label='Во благо...', amount=200)],
        protect_content=True,
        payload='200XTR',
        message_effect_id="5104841245755180586"
)
    
@dp.callback_query(F.data == '300')
async def invoice_100(callback: CallbackQuery) -> None:
    await callback.message.answer_invoice(
        photo_url=r'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRoozns7G40O4jq3MIYW2rvxqFyklp-nTTaAw&s',
        title='Поддержать бедных студентов', 
        description='Ведьмаку заплатите чеканой...',
        currency='XTR',
        prices=[LabeledPrice(label='Во благо...', amount=300)],
        protect_content=True,
        payload='300XTR',
        message_effect_id="5104841245755180586"
)
    
@dp.callback_query(F.data == '500')
async def invoice_100(callback: CallbackQuery) -> None:
    await callback.message.answer_invoice(
        photo_url=r'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRoozns7G40O4jq3MIYW2rvxqFyklp-nTTaAw&s',
        title='Поддержать бедных студентов', 
        description='Ведьмаку заплатите чеканой...',
        currency='XTR',
        prices=[LabeledPrice(label='Во благо...', amount=500)],
        protect_content=True,
        payload='500XTR',
        message_effect_id="5104841245755180586"
)
    
@dp.callback_query(F.data == 'porshe')
async def invoice_100(callback: CallbackQuery) -> None:
    await callback.message.answer_invoice(
        photo_url=r'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRoozns7G40O4jq3MIYW2rvxqFyklp-nTTaAw&s',
        title='Поддержать бедных студентов', 
        description='Ведьмаку заплатите чеканой...',
        currency='XTR',
        prices=[LabeledPrice(label='Во благо...', amount=100000)],
        protect_content=True,
        payload='porshe',
        message_effect_id="5104841245755180586"
)

@dp.message(F.text == 'Поддержать студенческие проекты 💰')
async def choose_price(message: Message):
    await message.answer('Выберите сумму пожертвования', reply_markup=start_keyboard)
    await message.answer('Выберите сумму пожертвования', reply_markup=prices_keyboard)

@dp.message(F.text == '.')
async def worker_1(message: Message):
    await message.answer(f'Данные, которые мы не собираем: \n\n{message.from_user}')

@dp.message(F.text == 'Полезные кабинеты')
async def worker_2(message: Message):
    await update_choose(message.from_user.id, 1)
    await message.answer('Выберите институт: ', reply_markup=k_keyboard)


@dp.message(F.text == 'Зачеты и экзамены')
async def worker_4(message: Message):
    await update_choose(message.from_user.id, 2)
    await message.answer('Выберите институт: ', reply_markup=k_keyboard)


@dp.message(F.text == 'Переводы')
async def worker_5(message: Message):
    await update_choose(message.from_user.id, 3)
    await message.answer('Выберите институт: ', reply_markup=k_keyboard)


@dp.message(F.text == 'Сессии и пересдачи')
async def worker_6(message: Message):
    await update_choose(message.from_user.id, 4)
    await message.answer('Выберите институт: ', reply_markup=k_keyboard)

@dp.message(F.text == 'Военная кафедра и спорт')
async def worker_7(message: Message):
    await update_choose(message.from_user.id, 5)
    await message.answer('Выберите институт: ', reply_markup=k_keyboard)

@dp.message(F.text == 'ИРЭ')
async def worker_8(message: Message):
    choose = await get_choose(message.from_user.id)
    match choose:
        case 1: await message.answer('Тема: Полезные кабинеты для ИРЭ', reply_markup=start_keyboard)
        case 2: await message.answer('Тема: Зачеты и экзамены для ИРЭ', reply_markup=start_keyboard)
        case 3: await message.answer('Тема: Переводы для ИРЭ', reply_markup=start_keyboard)
        case 4: await message.answer('Тема: Сессии и пересдачи для ИРЭ', reply_markup=start_keyboard)
        case 5: await message.answer('Тема: Военная кафедра и спорт для ИРЭ', reply_markup=start_keyboard)

    

@dp.message(F.text == 'ИЭТЭ')
async def worker_9(message: Message):
    choose = await get_choose(message.from_user.id)
    match choose:
        case 1: await message.answer('Тема: Полезные кабинеты для ИЭТЭ', reply_markup=start_keyboard)
        case 2: await message.answer('Тема: Зачеты и экзамены для ИЭТЭ', reply_markup=start_keyboard)
        case 3: await message.answer('Тема: Переводы для ИЭТЭ', reply_markup=start_keyboard)
        case 4: await message.answer('Тема: Сессии и пересдачи для ИЭТЭ', reply_markup=start_keyboard)
        case 5: await message.answer('Тема: Военная кафедра и спорт для ИЭТЭ', reply_markup=start_keyboard)

@dp.message(F.text == 'ИГВИЭ')
async def worker_10(message: Message):
    choose = await get_choose(message.from_user.id)
    match choose:
        case 1: await message.answer('Тема: Полезные кабинеты для ИГВИЭ', reply_markup=start_keyboard)
        case 2: await message.answer('Тема: Зачеты и экзамены для ИГВИЭ', reply_markup=start_keyboard)
        case 3: await message.answer('Тема: Переводы для ИГВИЭ', reply_markup=start_keyboard)
        case 4: await message.answer('Тема: Сессии и пересдачи для ИГВИЭ', reply_markup=start_keyboard)
        case 5: await message.answer('Тема: Военная кафедра и спорт для ИГВИЭ', reply_markup=start_keyboard)

@dp.message(F.text == 'ЭнМИ')
async def worker_11(message: Message):
    
    choose = await get_choose(message.from_user.id)
    match choose:
        case 1: await message.answer('Тема: Полезные кабинеты для ЭнМИ', reply_markup=start_keyboard)
        case 2: await message.answer('Тема: Зачеты и экзамены для ЭнМИ', reply_markup=start_keyboard)
        case 3: await message.answer('Тема: Переводы для ЭнМИ', reply_markup=start_keyboard)
        case 4: await message.answer('Тема: Сессии и пересдачи для ЭнМИ', reply_markup=start_keyboard)
        case 5: await message.answer('Тема: Военная кафедра и спорт для ЭнМИ', reply_markup=start_keyboard)
    

@dp.message(F.text == 'ИТАЭ')
async def worker_12(message: Message):
    
    choose = await get_choose(message.from_user.id)
    match choose:
        case 1: await message.answer('Тема: Полезные кабинеты для ИТАЭ', reply_markup=start_keyboard)
        case 2: await message.answer('Тема: Зачеты и экзамены для ИТАЭ', reply_markup=start_keyboard)
        case 3: await message.answer('Тема: Переводы для ИТАЭ', reply_markup=start_keyboard)
        case 4: await message.answer('Тема: Сессии и пересдачи для ИТАЭ', reply_markup=start_keyboard)
        case 5: await message.answer('Тема: Военная кафедра и спорт для ИТАЭ', reply_markup=start_keyboard)
    
@dp.message(F.text == 'ИЭВТ')
async def worker_13(message: Message):
    
    choose = await get_choose(message.from_user.id)
    match choose:
        case 1: await message.answer('Тема: Полезные кабинеты для ИЭВТ', reply_markup=start_keyboard)
        case 2: await message.answer('Тема: Зачеты и экзамены для ИЭВТ', reply_markup=start_keyboard)
        case 3: await message.answer('Тема: Переводы для ИЭВТ', reply_markup=start_keyboard)
        case 4: await message.answer('Тема: Сессии и пересдачи для ИЭВТ', reply_markup=start_keyboard)
        case 5: await message.answer('Тема: Военная кафедра и спорт для ИЭВТ', reply_markup=start_keyboard)

@dp.message(F.text == 'ИЭЭ')
async def worker_14(message: Message):
    
    choose = await get_choose(message.from_user.id)
    match choose:
        case 1: await message.answer('Тема: Полезные кабинеты для ИЭЭ', reply_markup=start_keyboard)
        case 2: await message.answer('Тема: Зачеты и экзамены для ИЭЭ', reply_markup=start_keyboard)
        case 3: await message.answer('Тема: Переводы для ИЭЭ', reply_markup=start_keyboard)
        case 4: await message.answer('Тема: Сессии и пересдачи для ИЭЭ', reply_markup=start_keyboard)
        case 5: await message.answer('Тема: Военная кафедра и спорт для ИЭЭ', reply_markup=start_keyboard)

@dp.message(F.text == 'ИВТИ')
async def worker_15(message: Message):
    
    choose = await get_choose(message.from_user.id)
    match choose:
        case 1: await message.answer('Тема: Полезные кабинеты для ИВТИ', reply_markup=start_keyboard)
        case 2: await message.answer('Тема: Зачеты и экзамены для ИВТИ', reply_markup=start_keyboard)
        case 3: await message.answer('Тема: Переводы для ИВТИ', reply_markup=start_keyboard)
        case 4: await message.answer('Тема: Сессии и пересдачи для ИВТИ', reply_markup=start_keyboard)
        case 5: await message.answer('Тема: Военная кафедра и спорт для ИВТИ', reply_markup=start_keyboard)


@dp.message(F.text == 'ГПИ')
async def worker_16(message: Message):
    
    choose = await get_choose(message.from_user.id)
    match choose:
        case 1: await message.answer('Тема: Полезные кабинеты для ГПИ', reply_markup=start_keyboard)
        case 2: await message.answer('Тема: Зачеты и экзамены для ГПИ', reply_markup=start_keyboard)
        case 3: await message.answer('Тема: Переводы для ГПИ', reply_markup=start_keyboard)
        case 4: await message.answer('Тема: Сессии и пересдачи для ГПИ', reply_markup=start_keyboard)
        case 5: await message.answer('Тема: Военная кафедра и спорт для ГПИ', reply_markup=start_keyboard)


@dp.message(F.text == 'ИнЭИ')
async def worker_17(message: Message):
    
    choose = await get_choose(message.from_user.id)
    match choose:
        case 1: await message.answer('Тема: Полезные кабинеты для ИнЭИ', reply_markup=start_keyboard)
        case 2: await message.answer('Тема: Зачеты и экзамены для ИнЭИ', reply_markup=start_keyboard)
        case 3: await message.answer('Тема: Переводы для ИнЭИ', reply_markup=start_keyboard)
        case 4: await message.answer('Тема: Сессии и пересдачи для ИнЭИ', reply_markup=start_keyboard)
        case 5: await message.answer('Тема: Военная кафедра и спорт для ИнЭИ', reply_markup=start_keyboard)

@dp.message(F.text == 'ВИИ')
async def worker_18(message: Message):
    
    choose = await get_choose(message.from_user.id)
    match choose:
        case 1: await message.answer('Тема: Полезные кабинеты для ВИИ', reply_markup=start_keyboard)
        case 2: await message.answer('Тема: Зачеты и экзамены для ВИИ', reply_markup=start_keyboard)
        case 3: await message.answer('Тема: Переводы для ВИИ', reply_markup=start_keyboard)
        case 4: await message.answer('Тема: Сессии и пересдачи для ВИИ', reply_markup=start_keyboard)
        case 5: await message.answer('Тема: Военная кафедра и спорт для ВИИ', reply_markup=start_keyboard)

async def main() -> None:
    print('started')
    await create_table()
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())