from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

bt_stop = KeyboardButton('Стоп')


bt_start = KeyboardButton('Начать авторизацию')
keyboard_start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard_start.add(bt_start).insert(bt_stop)


bt_username = KeyboardButton('Ввести имя пользователя')
bt_password = KeyboardButton('Ввести пароль')
bt_login = KeyboardButton('Войти')




# первый аргумент в параметре - уменьшает клавиатуру, второй - выключает клавиатуру после выбора one_time_keyboard=True
keyboard_oauth = ReplyKeyboardMarkup(resize_keyboard=True)

# keyboard.add(button_1).add(button_2).insert(button_3)
keyboard_oauth.row(bt_username, bt_password).add(bt_login).add(bt_stop)











