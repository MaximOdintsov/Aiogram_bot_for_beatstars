from selenium import webdriver
from selenium.webdriver.common.by import By

import logging
from aiogram import types, Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text, state
from aiogram.dispatcher import FSMContext


import os
import time
import random

from colorama import Back, Fore

from create_bot import bot, dp

from keyboard import *
from comments import list_comments


username = None
password = None
code = None
username_inp = None
password_inp = None
code_inp = None



class Form_0(StatesGroup):
    username_inp = State()
    password_inp = State()


class Form_1(StatesGroup):
    code_inp = State()


# начинаем собирать данные для авторизации от пользователя
# @dp.message_handler(commands='start_input_data', state=None)
async def start_input_data(message: types.Message):
    await Form_0.username_inp.set()


# выход из машинных состояний
# @dp.message_handler(state="*", commands='Отменить запись данных')
# @dp.message_handler(Text(equals='Отменить запись данных', ignore_case=True), state="*")
async def cancel_input_data(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Ввод данных отменён!', reply_markup=keyboard_send_data)


# ловим имя пользователя и записываем его в словарь
# @dp.message_handler(state=Form_0.username_inp)
async def input_username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username_inp'] = message.text
    await Form_0.next()
    await message.reply('Теперь введи пароль')


# ловим пароль, записываем его в словарь и записываем полученные данные (имя пользователя и пароль) в переменные
# @dp.message_handler(state=Form_0.password_inp)
async def input_password(message: types.Message, state: FSMContext):
    global username, password

    async with state.proxy() as data:
        data['password_inp'] = message.text
        username = str(data['username_inp'])
        password = str(data['password_inp'])
        await bot.send_message(message.from_user.id, 'Отлично, данные для авторизации введены!\nТеперь нажми на "Отправить данные на сайт.\n"'
                                                     'Если данные введены неверно, то нажмите на кнопку "Ввести данные авторизации" еще раз.',
                               reply_markup=keyboard_send_data)

    await state.finish()


# запрашиваем от пользователя код подтверждения (входим в машинные состояния)
# @dp.message_handler(commands='input_code', state=None)
async def start_input_code(message: types.Message):
    await Form_1.code_inp.set()


# выход из машинных состояний
# @dp.message_handler(state="*", commands='Отменить ввод кода')
# @dp.message_handler(Text(equals='Отменить ввод кода', ignore_case=True), state="*")
async def cancel_input_code(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Отправка кода верификации отменена", reply_markup=keyboard_send_code)



# ловим код и записываем его в переменную
# @dp.message_handler(state=Form_1.code_inp)
async def input_code(message: types.Message, state: FSMContext):
    global code

    async with state.proxy() as data:
        data['code_inp'] = message.text
        code = str(data['code_inp'])
    num = len(code)
    if num == 4:

        await message.reply('Отлично, код записан!\nПроверьте правильность введенных данных\nЕсли код записан верно, то нажми на "Отправить код"\nЕсли код записан неверно, то нажмите "Назад" ',
                            reply_markup=keyboard_send_code)
        await state.finish()
    else:
        await message.reply("Введен неверный код!")
        await start_input_code(message)


# регистрируем хэндлеры
def register_handlers_fsm(dp: Dispatcher):
    dp.register_message_handler(start_input_data, commands=['start_input_data'], state=None)
    dp.register_message_handler(cancel_input_data, commands=['Отменить запись данных'], state="*")
    dp.register_message_handler(cancel_input_data, (Text(equals='Отменить запись данных', ignore_case=True)))
    dp.register_message_handler(input_username, state=Form_0.username_inp)
    dp.register_message_handler(input_password, state=Form_0.password_inp)
    dp.register_message_handler(start_input_code, commands='input_code', state=None)
    dp.register_message_handler(cancel_input_code, commands='Отменить ввод кода', state="*")
    dp.register_message_handler(cancel_input_code, Text(equals='Отменить ввод кода', ignore_case=True), state="*")
    dp.register_message_handler(input_code, state=Form_1.code_inp)


