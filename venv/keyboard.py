from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bt_stop = KeyboardButton('Стоп')
bt_again = KeyboardButton('Начать всё заново')
bt_start = KeyboardButton('Начать авторизацию')


bt_input_data = KeyboardButton('Ввести данные для авторизации')
bt_send_data = KeyboardButton('Отправить данные на сайт')
bt_login = KeyboardButton('Войти')
cansel_input_data = KeyboardButton('Отменить запись данных')

bt_input_code = KeyboardButton('Ввести код')
cansel_input_code = KeyboardButton('Отменить ввод кода')
bt_send_code = KeyboardButton('Отправить код')
bt_agree_to_cookies = KeyboardButton('Согласиться с куки')
bt_back = KeyboardButton('Назад')

bt_start_bot = KeyboardButton('Запустить бота')
bt_stop_bot = KeyboardButton('Остановить бота')


'''Клавиатура после /start'''
# первый аргумент в параметре - уменьшает клавиатуру, второй - выключает клавиатуру после выбора one_time_keyboard=True
keyboard_start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard_start.add(bt_start).insert(bt_stop)


'''Клавиатура для ввода имени и пароля'''
keyboard_input_data = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_input_data.add(cansel_input_data)

'''Клавиатура для авторизации'''
keyboard_send_data = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_send_data.row(bt_input_data, bt_send_data).add(bt_login).row(bt_again)

'''Клавиатура для выбора: либо соглашение с куки, либо ввод кода'''
keyboard_code_or_cookie = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_code_or_cookie.row(bt_input_code, bt_agree_to_cookies).add(bt_back).add(bt_again)


'''Клавиатура для ввода кода'''
keyboard_input_code = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_input_code.add(cansel_input_code)

'''Клавиатура отправки кода'''
keyboard_send_code = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_send_code.row(bt_input_code, bt_send_code).add(bt_back).row(bt_again)

'''Клавиатура для соглашения с куки после ввода кода'''
keyboard_cookie = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard_cookie.add(bt_agree_to_cookies).add(bt_back).add(bt_again)

'''Клавиатура для запуска бота'''
keyboard_start_bot = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_start_bot.add(bt_start_bot).add(bt_stop_bot).insert(bt_again)

'''Клавиатура после запуска бота'''
keyboard_after_the_start = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_after_the_start.add(bt_stop_bot).insert(bt_again)










