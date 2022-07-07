import os

import requests
import telebot
from telebot import types
from selenium import webdriver
from selenium.webdriver.common.by import By

from colorama import Fore

import time
import random

from comments import list_comments
from database import *

bot = telebot.TeleBot(TOKEN)
TOKEN = "https://api.telegram.org/bot5478151046:AAFqMhNrppTeUD2fG34dIiPE-uV0TsiYvfY/setWebhook"


class BeatstarsBot:
    """Класс работы бота"""

    def __init__(self):
        """Переменные для входа в аккаунт"""

        self.list_comment = None
        self.profile_urls = None
        self.profile_url = None
        self.sleep_1_cycle = None
        self.sleep_day_cycle = None
        self.number = None
        self.browser = None
        print(Fore.LIGHTCYAN_EX, 'БОТ НАЧАЛ СВОЮ РАБОТУ!')

    def oauth_beatstars(self, message):
        """Открывает страницу авторизации в битстарс"""

        try:
            bot.send_message(message.chat.id, "Привет! Захожу в браузер, подождите...")
            chrome_options = webdriver.ChromeOptions()
            chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            self.browser = webdriver.Firefox()
            self.browser.get('https://oauth.beatstars.com/')
            time.sleep(random.randrange(5, 15))

        except Exception as ex:
            bot.send_message(message.chat.id, 'Не получилось открыть битстарс, запускаю авторизацию заново')
            print('Не получилось открыть битстарс, запускаю авторизацию заново')
            print(Fore.RED, 'Описание ошибки: ', ex)
            time.sleep(random.randrange(5, 10))
            self.oauth_beatstars(message)

    def username(self, message):
        """Функция перенаправляет на ввод имени пользователя"""

        user_name = bot.send_message(message.chat.id, "Введи имя пользователя")
        bot.register_next_step_handler(user_name, self.username_input)

    def password(self, message):
        """Функция перенаправляет на ввод пароля"""

        pass_word = bot.send_message(message.chat.id, "Введи пароль")
        bot.register_next_step_handler(pass_word, self.password_input)

    def username_input(self, message):
        """Вводит логин"""

        username_inp = self.browser.find_element(By.XPATH,
                                                 '/html/body/oauth-root/ng-component/section/div[2]/div[2]/form/div[1]/bs-text-input/input')
        username_inp.click()
        time.sleep(random.randrange(2, 5))
        username_inp.clear()
        username_inp.send_keys(message.text)

        bot.send_message(message.chat.id, "Бот ввёл имя пользователя!")
        time.sleep(random.randrange(1, 3))

    def password_input(self, message):
        """Вводит пароль"""
        password_inp = self.browser.find_element(By.XPATH,
                                                 '/html/body/oauth-root/ng-component/section/div[2]/div[2]/form/div[2]/bs-text-input/input')
        password_inp.click()
        time.sleep(random.randrange(2, 5))
        password_inp.clear()
        password_inp.send_keys(message.text)

        bot.send_message(message.chat.id, "Бот ввёл пароль!")
        time.sleep(random.randrange(1, 3))

    def login_button(self, message):
        """Нажимает на кнопку 'Войти' """

        try:
            login_button = self.browser.find_element(By.XPATH,
                                                     '/html/body/oauth-root/ng-component/section/div[2]/div[2]/form/bs-square-button/button')
            login_button.click()
            bot.send_message(message.chat.id, "Нажал на кнопку войти. Пожалуйста, подождите...")
            time.sleep(random.randrange(20, 30))
            bot.send_message(message.chat.id, "Посмотри, пришло ли тебе письмо с кодом подтверждения на почту, если да, то вводи код подтверждения(кнопка), если нет, то соглашайся с куки")
        except Exception as ex:
            bot.send_message(message.chat.id, 'Не получилось нажать на кнопку "Войти", запускаю алгоритм заново')
            print('Не получилось нажать на кнопку "Войти", запускаю алгоритм заново')
            print(Fore.RED, 'Описание ошибки: ', ex)
            time.sleep(random.randrange(5, 10))
            self.oauth_beatstars(message)

    def first_code(self, message):
        """Переводит на функцию ввода 1 цифры кода подтверждения"""

        try:
            code_1 = bot.send_message(message.chat.id, 'Введите первую цифру кода подтверждения')
            bot.register_next_step_handler(code_1, self.first_code_input)

        except Exception as ex:
            bot.send_message(message.chat.id, 'Не получилось ввести код верификации')
            print('Не получилось ввести код верификации')
            print(Fore.RED, 'Описание ошибки: ', ex)
            time.sleep(random.randrange(5, 10))

    def first_code_input(self, message):
        """Вводит 1 цифру кода подтверждения"""

        try:
            confirmation_code_1 = self.browser.find_element(By.XPATH,
                                                            '//*[@id="mat-dialog-0"]/ng-component/bs-dialog/div[2]/div/bs-code-input/form/div/input[3]')
            confirmation_code_1.click()
            confirmation_code_1.send_keys(message.text)
            self.second_code(message)

        except Exception as ex:
            bot.send_message(message.chat.id, 'Не получилось ввести код верификации')
            print(Fore.RED, 'Описание ошибки: ', ex)

    def second_code(self, message):
        """Переводит на функцию ввода 2 цифры кода подтверждения"""

        try:
            code_2 = bot.send_message(message.chat.id, "Введите следующую цифру кода подтверждения!")
            bot.register_next_step_handler(code_2, self.second_code_input)
        except Exception as ex:
            bot.send_message(message.chat.id, 'Не получилось ввести код верификации')
            print(Fore.RED, 'Описание ошибки: ', ex)

    def second_code_input(self, message):
        """Вводит 2 цифру кода подтверждения"""

        try:
            confirmation_code_2 = self.browser.find_element(By.XPATH,
                                                            '//*[@id="mat-dialog-0"]/ng-component/bs-dialog/div[2]/div/bs-code-input/form/div/input[4]')
            confirmation_code_2.click()
            confirmation_code_2.send_keys(message.text)
            self.third_code(message)
        except Exception as ex:
            bot.send_message(message.chat.id, 'Не получилось ввести код верификации')
            print(Fore.RED, 'Описание ошибки: ', ex)

    def third_code(self, message):
        """Переводит на функцию ввода 3 цифры кода подтверждения"""

        try:
            code_3 = bot.send_message(message.chat.id, "Введите следующую цифру кода подтверждения!")
            bot.register_next_step_handler(code_3, self.third_code_input)
        except Exception as ex:
            bot.send_message(message.chat.id, 'Не получилось ввести код верификации')
            print(Fore.RED, 'Описание ошибки: ', ex)

    def third_code_input(self, message):
        """Вводит 3 цифру кода подтверждения"""

        try:
            confirmation_code_3 = self.browser.find_element(By.XPATH,
                                                            '//*[@id="mat-dialog-0"]/ng-component/bs-dialog/div[2]/div/bs-code-input/form/div/input[5]')
            confirmation_code_3.click()
            confirmation_code_3.send_keys(message.text)
            self.fourth_code(message)
        except Exception as ex:
            bot.send_message(message.chat.id, 'Не получилось ввести код верификации')
            print(Fore.RED, 'Описание ошибки: ', ex)

    def fourth_code(self, message):
        """Переводит на функцию ввода 4 цифры кода подтверждения"""

        try:
            code_4 = bot.send_message(message.chat.id, "Введите следующую цифру кода подтверждения!")
            bot.register_next_step_handler(code_4, self.fourth_code_input)
        except Exception as ex:
            bot.send_message(message.chat.id, 'Не получилось ввести код верификации')
            print(Fore.RED, 'Описание ошибки: ', ex)

    def fourth_code_input(self, message):
        """Вводит 4 цифру кода подтверждения"""

        try:
            confirmation_code_4 = self.browser.find_element(By.XPATH,
                                                            '//*[@id="mat-dialog-0"]/ng-component/bs-dialog/div[2]/div/bs-code-input/form/div/input[6]')
            confirmation_code_4.click()
            confirmation_code_4.send_keys(message.text)
            bot.send_message(message.chat.id, "Ввёл код подтверждения, дождитесь загрузки браузера")

        except Exception as ex:
            bot.send_message(message.chat.id, 'Не получилось ввести код верификации')
            print(Fore.RED, 'Описание ошибки: ', ex)

    def consent_to_cookies(self, message):
        """Нажимает на кнопку 'Согласиться с куки' """

        try:
            cookie_consent = self.browser.find_element(By.XPATH,
                                                       '/html/body/mp-root/mp-snackbar-info-messages/div/mp-cookies-snackbar/mp-snackbar-info-message-template/div/button')
            cookie_consent.click()
            time.sleep(random.randrange(2, 4))

        except Exception as ex:
            bot.send_message(message.chat.id,
                             'Не получилось согласиться с куки, попробуйте еще раз через некоторое время')
            print(Fore.RED, 'Не получилось согласиться с куки, попробуйте еще раз через некоторое время')
            print(Fore.RED, 'Описание ошибки: ', ex)
            time.sleep(random.randrange(10, 15))

    def homepage(self, message):
        """Открывает начальную страницу битстарс"""

        try:
            self.browser.get('https://beatstars.com/')
            bot.send_message(message.chat.id, 'Открыл начальную страницу, т.к. не получилось согласиться с куки')
            time.sleep(random.randrange(5, 15))

            self.consent_to_cookies(message)
        except Exception as ex:
            bot.send_message(message.chat.id, 'Снова не получилось согласиться с куки, запускаю алгоритм заново')
            print('Снова не получилось согласиться с куки, запускаю алгоритм заново')
            print(Fore.RED, 'Описание ошибки: ', ex)
            time.sleep(random.randrange(5, 10))
            self.oauth_beatstars(message)

    def open_feed(self, message):
        """Открывает фид"""

        try:
            self.browser.get('https://www.beatstars.com/feed')
            bot.send_message(message.chat.id, ' Открыл фид!')
            time.sleep(random.randrange(10, 20))

            self.play_beat(message)
        except Exception as ex:
            bot.send_message(message.chat.id, 'Не получилось открыть фид, пробую заново.')
            print('Не получилось открыть фид, пробую заново.')
            print(Fore.RED, 'Описание ошибки: ', ex)
            self.open_feed(message)

    def play_beat(self, message):
        """Нажимает на кнопку включения бита"""

        try:
            play_button = self.browser.find_element(By.XPATH,
                                                    '/html/body/mp-root/div/div/ng-component/mp-feed/div/section[2]/div[1]/mp-track-post/mp-feed-card/div/div[2]/div[1]/div[2]/div[1]/bs-button-play-item/button')
            play_button.click()
            bot.send_message(message.chat.id, 'Включил бит')
            time.sleep(random.randrange(5, 10))

            self.open_beat(message)
        except Exception as ex:
            bot.send_message(message.chat.id, 'Не получилось нажать на кнопку включения бита, запускаю алгоритм заново.')
            print('Не получилось нажать на кнопку включения бита, запускаю алгоритм заново')
            print(Fore.RED, 'Описание ошибки: ', ex)
            self.open_feed(message)

    def open_beat(self, message):
        """Открывает описание бита"""

        try:
            opening_beat = self.browser.find_element(By.XPATH,
                                                     '//*[@id="player-container"]/div/div[1]/div[1]/bs-playable-item-info/div[2]/div[1]/a')
            opening_beat.click()

            bot.send_message(message.chat.id, 'Открыл описание бита')
            time.sleep(random.randrange(10, 15))

            self.comments(message)
        except Exception as ex:
            bot.send_message(message.chat.id, 'Не получилось открыть описание бита, запускаю алгоритм заново')
            print('Не получилось открыть описание бита, запускаю алгоритм заново')
            print(Fore.RED, 'Описание ошибки: ', ex)
            self.open_feed(message)

    def like(self, message):
        """Нажимает на кнопку лайка в описании бита"""

        try:
            like_button = self.browser.find_element(By.XPATH,
                                                    '/html/body/mp-root/div/div/ng-component/mp-wrapper-member-track-content/mp-member-content-item-template/bs-container-grid/div[1]/section/mp-member-content-item-header-template/div[4]/mp-button-like-action-template')
            like_button.click()
            bot.send_message(message.chat.id, 'Поставил лайк')
            time.sleep(random.randrange(3, 7))

            self.cycle_to_liked(message)
        except Exception as ex:
            bot.send_message(message.chat.id, 'Не получилось поставить лайк, пишу комментарий.')
            print('Не получилось поставить лайк, пишу комментарий.')
            print(Fore.RED, 'Описание ошибки: ', ex)
            self.cycle_to_liked(message)

    def comment(self):
        """Определяет рандомный комментарий"""

        self.list_comment = random.choice(list_comments)

    def comments(self, message):
        """Печатает и отправляет комментарии"""

        try:
            self.comment()

            # нажимает на поле ввода и пишет рандомный комментарий
            input_comments = self.browser.find_element(By.XPATH,
                                                       '/html/body/mp-root/div/div/ng-component/mp-wrapper-member-track-content/mp-member-content-item-template/bs-container-grid/div[3]/div[2]/mp-comments-panel-box/mp-open-close-panel-template/div/article/div[2]/mp-create-new-comment-input/mp-musician-autocomplete-wrapper/mp-autocomplete-dropdown-template/div/div[2]/mp-compose-new-message-input/form/div[2]/input')
            time.sleep(random.randrange(5, 10))
            input_comments.send_keys(self.list_comment)
            bot.send_message(message.chat.id, "Ввёл комментарий")

            # нажимает на кнопку отправки комментария
            comment_button = self.browser.find_element(By.XPATH,
                                                       '/html/body/mp-root/div/div/ng-component/mp-wrapper-member-track-content/mp-member-content-item-template/bs-container-grid/div[3]/div[2]/mp-comments-panel-box/mp-open-close-panel-template/div/article/div[2]/mp-create-new-comment-input/mp-musician-autocomplete-wrapper/mp-autocomplete-dropdown-template/div/div[2]/mp-compose-new-message-input/form/bs-square-button')
            comment_button.click()
            bot.send_message(message.chat.id, 'Отправил комментарий!')
            time.sleep(random.randrange(5, 15))

            self.open_profile(message)
        except Exception as ex:
            bot.send_message(message.chat.id, 'Не получилось отправить комментарий, открываю профиль')
            print('Не получилось отправить комментарий, открываю профиль')
            print(Fore.RED, 'Описание ошибки: ', ex)
            self.open_profile(message)

    def open_profile(self, message):
        """Открывает профиль"""

        try:
            go_to_the_profile = self.browser.find_element(By.XPATH,
                                                          '/html/body/mp-root/div/div/ng-component/mp-wrapper-member-track-content/mp-member-content-item-template/bs-container-grid/div[1]/section/mp-member-content-item-header-template/div[2]/mp-caption-figure-template[2]/a')
            go_to_the_profile.click()
            bot.send_message(message.chat.id, 'Открыл профиль, сейчас посмотрим, что тут у нас')
            time.sleep(random.randrange(15, 25))

            self.subscription(message)
        except Exception as ex:
            bot.send_message(message.chat.id, 'Не получилось открыть профиль, запускаю алгоритм заново.')
            print('Не получилось открыть профиль, запускаю алгоритм заново.')
            print(Fore.RED, 'Описание ошибки: ', ex)
            self.open_feed(message)

    def subscription(self, message):
        """Подписывается на пользователя"""

        try:
            follow_button = self.browser.find_element(By.XPATH,
                                                      '/html/body/mp-root/div/div/ng-component/ng-component/mp-wrapper-member-profile-content/main/bs-container-grid/mp-profile-header/mp-profile-visitor-actions/div/mp-button-follow-text-template/mp-button-item-action-text-template')
            follow_button.click()
            bot.send_message(message.chat.id, 'Оформил подписку!')
            time.sleep(random.randrange(5, 15))

            self.back(message)
            self.open_liked(message)
        except Exception as ex:
            bot.send_message(message.chat.id, 'Подписаться не получилось, нажимаю кнопку "Назад".')
            print('Подписаться не получилось, нажимаю кнопку "Назад".')
            print(Fore.RED, 'Описание ошибки: ', ex)
            self.back(message)

    def back(self, message):
        """Нажимает на кнопку 'Назад' в браузере"""

        try:
            self.browser.back()
            bot.send_message(message.chat.id, 'Нажал на кнопку "Назад"')
            time.sleep(random.randrange(10, 15))

        except Exception as ex:
            bot.send_message(message.chat.id, 'Не получилось нажать на кнопку "Назад", запускаю алгоритм заново.')
            print('Не получилось нажать на кнопку "Назад", запускаю алгоритм заново.')
            print(Fore.RED, 'Описание ошибки: ', ex)
            self.open_feed(message)

    def close_menu(self, message):
        """Закрывает меню с лайнкувшими"""

        try:
            self.browser.find_element(By.CSS_SELECTOR, '.close-button').click()
            bot.send_message(message.chat.id, 'Закрыл меню с лайкнувшими')
            time.sleep(random.randrange(2, 4))
        except Exception as ex:
            bot.send_message(message.chat.id, 'Не получилось закрыть меню, запускаю алгоритм подписки на лайкнувших.')
            print('Не получилось закрыть меню, запускаю алгоритм подписки на лайкнувших.')
            print(Fore.RED, 'Описание ошибки: ', ex)
            self.cycle_to_liked(message)

    def open_liked(self, message):
        """Открывает меню с лайкнувшими"""
        try:
            likes = self.browser.find_element(By.XPATH,
                                              '/html/body/mp-root/div/div/ng-component/mp-wrapper-member-track-content/mp-member-content-item-template/bs-container-grid/div[1]/section/mp-member-content-item-header-template/div[4]/mp-button-like-action-template/mp-button-item-action-icon-template/span')
            likes.click()
            bot.send_message(message.chat.id, 'Открыл меню с лайкнувшими!')
            time.sleep(random.randrange(7, 15))

            self.parsing(message)
        except Exception as ex:
            bot.send_message(message.chat.id, 'Не получилось открыть меню лайкнувших, запускаю цикл заново.')
            print('Не получилось открыть меню лайкнувших, запускаю цикл заново.')
            print(Fore.RED, 'Описание ошибки: ', ex)
            self.open_feed(message)

    def parsing(self, message):
        """Парсит ссылки на тех, кто лайкнул бит"""

        try:

            # ищет элементы только в окне с теми, кто лайкнул бит
            window_with_liked = self.browser.find_element(By.CLASS_NAME, 'body-container')

            # ищет элементы с тегом "а"
            elements = window_with_liked.find_elements(By.TAG_NAME, 'a')

            # собирает ссылки на элементы только 'href'
            self.profile_urls = [item.get_attribute('href') for item in elements]
            bot.send_message(message.chat.id, 'Спарсил ссылки на профили!')
            print(Fore.LIGHTCYAN_EX, 'Спарсил ссылки на профили: ', Fore.LIGHTYELLOW_EX, self.profile_urls)

            self.close_menu(message)
            self.like(message)
        except Exception as ex:
            bot.send_message(message.chat.id,
                             'Не получилось спарсить пользователей, которые лайкнули бит, запускаю алгоритм заново.')
            print('Не получилось спарсить пользователей, которые лайкнули бит, запускаю алгоритм заново.')
            print(Fore.RED, 'Описание ошибки: ', ex)
            self.open_feed(message)

    def cycle_to_liked(self, message):
        """Запускает цикл подписки на лайкнувших"""

        try:
            for self.profile_url in self.profile_urls[0:random.randrange(4, 8)]:  # 5-15 было
                self.browser.get(self.profile_url)
                time.sleep(random.randrange(10, 15))

                self.subscription_to_liked(message)
        except Exception as ex:
            bot.send_message(message.chat.id,
                             'Не получилось запустить цикл подписки на пользователей, которые лайкнули бит, запускаю алгоритм заново.')
            print('Не получилось запустить цикл подписки на пользователей, которые лайкнули бит, запускаю алгоритм заново.')
            print(Fore.RED, 'Описание ошибки: ', ex)
            self.open_feed(message)

    def subscription_to_liked(self, message):
        """Подписывается на лайкнувших"""

        try:

            follow_button = self.browser.find_element(By.XPATH,
                                                      '/html/body/mp-root/div/div/ng-component/ng-component/mp-wrapper-member-profile-content/main/bs-container-grid/mp-profile-header/mp-profile-visitor-actions/div/mp-button-follow-text-template/mp-button-item-action-text-template')
            follow_button.click()
            bot.send_message(message.chat.id, 'Оформил подписку!')
            print(Fore.LIGHTGREEN_EX, 'Оформил', Fore.LIGHTBLUE_EX, 'подписку', Fore.LIGHTGREEN_EX, 'на:',
                  Fore.LIGHTYELLOW_EX, self.profile_url)

            time.sleep(random.randrange(30, 45))
        except Exception as ex:
            bot.send_message(message.chat.id, 'Подписаться не получилось, подписываюсь на другой профиль')
            print(Fore.LIGHTRED_EX, 'Не получилось подписаться на "', self.profile_url,
                  '", подписываюсь на следующего пользователя.')
            print(Fore.RED, 'Описание ошибки: ', ex)
            time.sleep(10)

    def close_beatstars(self, message):
        """Открывает страницу гугл, якобы для закрытия битстарса"""

        self.browser.get('https://google.com/')
        bot.send_message(message.chat.id, 'Бот закрыл битстарс')

    def sleep(self):
        """Рандомизирует переменные сна"""

        self.sleep_1_cycle = random.randrange(3500, 5500)
        self.sleep_day_cycle = random.randrange(27000, 40000)

    def repost_beat(self, message):
        """Делает репост моих битов"""
        try:
            self.browser.get('https://www.beatstars.com/flipsidebeats/tracks')
            time.sleep(random.randrange(30, 40))

            self.browser.find_element(By.XPATH,
                                      '/html/body/mp-root/div/div/ng-component/ng-component/mp-search-v3/div/div/section/mp-search-results/mp-list-card-track/div/mp-list-card-template/div/mp-card-figure-track[1]/mp-card-figure-template/figure/div/div[2]/div[2]/mp-button-play-track-on-algolia-v3/bs-vb-button-play-item').click()
            time.sleep(random.randrange(3, 5))

            for i in range(0, random.randrange(1, 4)):
                # открывает описание бита
                self.browser.find_element(By.XPATH,
                                          '//*[@id="player-container"]/div/div[1]/div[1]/bs-playable-item-info/div[2]/div[1]/a').click()
                bot.send_message(message.chat.id, 'Открыл описание бита')
                time.sleep(random.randrange(15, 20))

                # нажимает на кнопку репоста (2 раза)
                self.browser.find_element(By.XPATH,
                                          '/html/body/mp-root/div/div/ng-component/mp-wrapper-member-track-content/mp-member-content-item-template/bs-container-grid/div[1]/section/mp-member-content-item-header-template/div[4]/mp-button-repost-icon-template/mp-button-item-action-icon-template/button').click()
                time.sleep(random.randrange(2, 4))
                bot.send_message(message.chat.id, 'Сделал репост')

                # переключает на следующий бит
                self.browser.find_element(By.XPATH,
                                          '/html/body/mp-root/mp-player-wrapper/bs-player/div/div/div[2]/bs-player-next/button').click()
                bot.send_message(message.chat.id, 'Переключился на следующий бит')
                time.sleep(random.randrange(5, 10))
        except Exception as ex:
            bot.send_message(message.chat.id, 'Не получилось сделать репост')
            print('Не получилось сделать репост')
            print(Fore.RED, 'Описание ошибки: ', ex)
            time.sleep(10)

    def stop_bot(self, message):
        self.browser.close()
        self.browser.quit()
        bot.send_message(message.chat.id, 'Бот закрыл браузер')

    def start_bot(self, message):
        """Запускает бота в цикл"""
        try:
            work_bot = True

            while work_bot:
                """Бесконечный цикл"""

                self.sleep()

                for main_cycle in range(0, 1):
                    """Выполняется 1 раз в день, засыпает на 8-12 часов"""

                    # bot.send_message(message.chat.id, "Бот начал репостить твои биты!")
                    self.sleep()
                    # self.repost_beat(message)

                    for self.number in range(0, random.randrange(3, 7)):
                        """Выполняется 3, 7 раз в день, каждый раз засыпает на 1-1,5 часа"""

                        self.sleep()

                        for i in range(0, random.randrange(9, 21)):  # 10-16
                            """Сам цикл, выполняется 4-7 раз за 1 цикл"""

                            bot.send_message(message.chat.id, 'Начался новый цикл!')
                            self.open_feed(message)
                            bot.send_message(message.chat.id, 'Цикл успешно завершён! Продолжаем..')
                            print(Fore.LIGHTYELLOW_EX, 'Цикл номер', i + 1, 'успешно завершён! Продолжаем..')
                            time.sleep(random.randrange(5, 15))

                        self.close_beatstars(message)
                        bot.send_message(message.chat.id, 'Циклы завершены. Боту нужно немного отдохнуть...')
                        print(Fore.LIGHTMAGENTA_EX, 'Циклы завершены. Боту нужно немного отдохнуть...'
                              'Он продолжит работу через: ', self.sleep_1_cycle)
                        time.sleep(self.sleep_1_cycle)

                    # self.repost_beat(message)
                    print(Fore.LIGHTYELLOW_EX, 'Бот провёл', self.number, 'циклов за день!')
                print('Боту тоже нужен сон! Он проснётся через: ', self.sleep_day_cycle)
                bot.send_message(message.chat.id, 'Все циклы на сегодняшний день завершены.')
                time.sleep(self.sleep_day_cycle)
                
        except Exception as ex:
            bot.send_message(message.chat.id, 'Что-то пошло не так, перехожу на начальную страницу гугл, запусти бота заново!')
            print(Fore.RED, 'Что-то пошло не так, перехожу на начальную страницу гугл, запусти бота заново!')
            print(Fore.RED, 'Описание ошибки: ', ex)
            self.browser.get('https://google.com/')


def unrecognized_text(message):
    """Отвечает на нераспознанную команду"""

    bot.send_message(message.chat.id, "Я тебя не понял... Введи корректную команду")


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Начать аутентификацию')
    markup.add(button1)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я бот для раскрутки твоего профиля Beatstars".format(message.from_user), reply_markup=markup)


@bot.message_handler(commands=['username'])  # перенаправляет на ввод имени пользователя
def username(message):
    BS_bot.username(message)


@bot.message_handler(commands=['password'])  # перенаправляет на ввод пароля
def password(message):
    BS_bot.password(message)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == 'Начать аутентификацию':
        BS_bot.oauth_beatstars(message)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Ввести логин")
        button2 = types.KeyboardButton("Ввести пароль")
        button3 = types.KeyboardButton("Войти")
        again_button = types.KeyboardButton("Начать заново")
        markup.add(button1, button2, button3, again_button)
        bot.send_message(message.chat.id, 'Страница успешно загружена!', reply_markup=markup)

    elif message.text == 'Ввести логин':
        username(message)

    elif message.text == 'Ввести пароль':
        password(message)

    elif message.text == 'Войти':
        BS_bot.login_button(message)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Согласиться с куки")
        button2 = types.KeyboardButton("Ввести код подтверждения")
        again_button = types.KeyboardButton("Начать заново")
        markup.add(button1, button2, again_button)
        bot.send_message(message.chat.id, 'Страница успешно загружена!', reply_markup=markup)

    elif message.text == 'Согласиться с куки':
        BS_bot.consent_to_cookies(message)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        start_button = types.KeyboardButton("Запустить бота")
        again_button = types.KeyboardButton("Начать заново")
        markup.add(start_button, again_button)
        bot.send_message(message.chat.id, 'Согласился с куки. Теперь можешь запускать бота!', reply_markup=markup)

    elif message.text == 'Ввести код подтверждения':
        BS_bot.first_code(message)

    elif message.text == 'Запустить бота':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        stop_button = types.KeyboardButton("Стоп")
        again_button = types.KeyboardButton("Начать заново")
        start_button = types.KeyboardButton("Запустить бота")
        markup.add(stop_button, again_button, start_button)
        bot.send_message(message.chat.id, 'Бот начал свою работу!', reply_markup=markup)
        BS_bot.start_bot(message)

    elif message.text == 'Стоп':
        BS_bot.stop_bot(message)
        start(message)

    elif message.text == 'Начать заново':
        start(message)

    else:
        unrecognized_text(message)


def username_input(message):  # ввод логина
    BS_bot.login_button(message)


def password_input(message):  # ввод пароля
    BS_bot.password_input(message)


BS_bot = BeatstarsBot()
req = requests.get('https://beatstars.com', verify=False)
print(req)
if __name__ == '__main__':  # чтобы код выполнялся только при запуске в виде сценария, а не при импорте модуля

    try:
        bot.polling(none_stop=True, timeout=123)  # запуск бота
    except Exception as ex:
        print(ex)
        time.sleep(15)
