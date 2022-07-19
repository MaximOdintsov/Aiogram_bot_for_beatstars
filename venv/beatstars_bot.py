from selenium import webdriver
from selenium.webdriver.common.by import By

import logging
from aiogram import types
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
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

logging.basicConfig(level=logging.INFO)


class Form_0(StatesGroup):
    username_inp = State()
    password_inp = State()


class Form_1(StatesGroup):
    code_inp = State()


class BeatstarsBot():
    """Класс работы бота"""

    def __init__(self):
        """Переменные для входа в аккаунт"""

        self.data = None
        self.list_comment = None
        self.profile_urls = None
        self.profile_url = None
        self.sleep_1_cycle = None
        self.sleep_day_cycle = None
        self.number = None
        self.browser = None

    def oauth_beatstars(self, message):
        """Открывает страницу авторизации в битстарс"""

        try:
            bot.send_message(message.from_user.id, "Привет! Захожу в браузер, подождите...")
            chrome_options = webdriver.ChromeOptions()
            chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            self.browser = webdriver.Firefox()
            self.browser.get('https://oauth.beatstars.com/')
            time.sleep(random.randrange(5, 15))

        except Exception as ex:
            bot.send_message(message.from_user.id, 'Не получилось открыть битстарс, запускаю авторизацию заново')
            print('Не получилось открыть битстарс, запускаю авторизацию заново')
            print(Fore.RED, 'Описание ошибки: ', ex)
            time.sleep(random.randrange(5, 10))
            self.oauth_beatstars(message)

    def username_input(self, message):
        """Вводит логин"""

        username_input = self.browser.find_element(By.XPATH, '/html/body/oauth-root/ng-component/section/div[2]/div[2]/form/div[1]/bs-text-input/input')
        username_input.click()
        time.sleep(random.randrange(2, 5))
        username_input.clear()
        username_input.send_keys(username)

        bot.send_message(message.from_user.id, "Бот ввёл имя пользователя!")
        time.sleep(random.randrange(1, 3))

    def password_input(self, message):
        """Вводит пароль"""
        password_input = self.browser.find_element(By.XPATH, '/html/body/oauth-root/ng-component/section/div[2]/div[2]/form/div[2]/bs-text-input/input')
        password_input.click()
        time.sleep(random.randrange(2, 5))
        password_input.clear()
        password_input.send_keys(password)

        bot.send_message(message.from_user.id, "Бот ввёл пароль!")
        time.sleep(random.randrange(1, 3))

    def login_button(self, message):
        """Нажимает на кнопку 'Войти' """

        try:
            login_button = self.browser.find_element(By.XPATH,
                                                     '/html/body/oauth-root/ng-component/section/div[2]/div[2]/form/bs-square-button/button')
            login_button.click()
            bot.send_message(message.from_user.id, "Нажал на кнопку войти. Пожалуйста, подождите...")
            time.sleep(random.randrange(20, 30))
            bot.send_message(message.from_user.id,
                             "Посмотри, пришло ли тебе письмо с кодом подтверждения на почту, если да, то вводи код подтверждения, если нет, то соглашайся с куки")
        except Exception as ex:
            bot.send_message(message.from_user.id, 'Не получилось нажать на кнопку "Войти", запускаю алгоритм заново')
            print('Не получилось нажать на кнопку "Войти", запускаю алгоритм заново')
            print(Fore.RED, 'Описание ошибки: ', ex)
            time.sleep(random.randrange(5, 10))
            self.oauth_beatstars(message)

    def send_code(self, message):

        try:
            amount_numbers = len(code)

            if amount_numbers == 4:
                code_1 = self.browser.find_element(By.XPATH, '//*[@id="mat-dialog-0"]/ng-component/bs-dialog/div[2]/div/bs-code-input/form/div/input[3]')
                code_1.click()
                code_1.send_keys(code[0])

                code_2 = self.browser.find_element(By.XPATH, '//*[@id="mat-dialog-0"]/ng-component/bs-dialog/div[2]/div/bs-code-input/form/div/input[4]')
                code_2.click()
                code_2.send_keys(code[1])

                code_3 = self.browser.find_element(By.XPATH, '//*[@id="mat-dialog-0"]/ng-component/bs-dialog/div[2]/div/bs-code-input/form/div/input[5]')
                code_3.click()
                code_3.send_keys(code[2])

                code_4 = self.browser.find_element(By.XPATH, '//*[@id="mat-dialog-0"]/ng-component/bs-dialog/div[2]/div/bs-code-input/form/div/input[6]')
                code_4.click()
                code_4.send_keys(code[3])

            else:
                message.reply('Введён неверный код, введите код заново')

        except Exception as ex:
            bot.send_message(message.from_user.id, 'Не получилось ввести код верификации')
            print(Fore.RED, 'Описание ошибки: ', ex)

    def consent_to_cookies(self, message):
        """Нажимает на кнопку 'Согласиться с куки' """

        try:
            cookie_consent = self.browser.find_element(By.XPATH,
                                                       '/html/body/mp-root/mp-snackbar-info-messages/div/mp-cookies-snackbar/mp-snackbar-info-message-template/div/button')
            cookie_consent.click()
            time.sleep(random.randrange(2, 4))

        except Exception as ex:
            bot.send_message(message.from_user.id,
                             'Не получилось согласиться с куки, попробуйте еще раз через некоторое время')
            print(Fore.RED, 'Не получилось согласиться с куки, попробуйте еще раз через некоторое время')
            print(Fore.RED, 'Описание ошибки: ', ex)
            time.sleep(random.randrange(10, 15))

    def homepage(self, message):
        """Открывает начальную страницу битстарс"""

        try:
            self.browser.get('https://beatstars.com/')
            bot.send_message(message.from_user.id, 'Открыл начальную страницу, т.к. не получилось согласиться с куки')
            time.sleep(random.randrange(5, 15))

            self.consent_to_cookies(message)
        except Exception as ex:
            bot.send_message(message.from_user.id, 'Снова не получилось согласиться с куки, запускаю алгоритм заново')
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
            bot.send_message(message.chat.id,
                             'Не получилось нажать на кнопку включения бита, запускаю алгоритм заново.')
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
            print(
                'Не получилось запустить цикл подписки на пользователей, которые лайкнули бит, запускаю алгоритм заново.')
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
            bot.send_message(message.chat.id,
                             'Что-то пошло не так, перехожу на начальную страницу гугл, запусти бота заново!')
            print(Fore.RED, 'Что-то пошло не так, перехожу на начальную страницу гугл, запусти бота заново!')
            print(Fore.RED, 'Описание ошибки: ', ex)
            self.browser.get('https://google.com/')

beat_bot = BeatstarsBot()


# уведомляет об успешном запуске бота
async def on_startup(message):
    print(Back.BLACK, "Бот вышел в онлайн!")


# отвечает на команду /start и /help
@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, "Привет, я бот, помогающий раскрутить твой битстарс аккаунт!", reply_markup=keyboard_start)


# начинаем собирать данные для авторизации от пользователя
@dp.message_handler(commands='start_input_data', state=None)
async def start_input_data(message: types.Message):
    await Form_0.username_inp.set()
    await message.reply('Введи имя пользователя')


# выход из машинных состояний
@dp.message_handler(state="*", commands='cancel_input_data')
@dp.message_handler(Text(equals='cancel_input_data', ignore_case=True), state="*")
async def cancel_input_data(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('ОК')


# ловим первый ответ и пишем его в словарь
@dp.message_handler(state=Form_0.username_inp)
async def input_username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username_inp'] = message.text
    await Form_0.next()
    await message.reply('Теперь введи пароль')


# ловим второй ответ и записываем полученные данные в переменные
@dp.message_handler(state=Form_0.password_inp)
async def input_password(message: types.Message, state: FSMContext):
    global username, password

    async with state.proxy() as data:
        data['password_inp'] = message.text
        username = str(data['username_inp'])
        password = str(data['password_inp'])

    await state.finish()


# запрашиваем от пользователя код подтверждения (входим в машинные состояния)
@dp.message_handler(commands='input_code', state=None)
async def start_input_code(message: types.Message):
    await Form_1.code_inp.set()
    await message.reply('Введи код подтверждения')


# выход из машинных состояний
@dp.message_handler(state="*", commands='cancel_input_code')
@dp.message_handler(Text(equals='cancel_input_code', ignore_case=True), state="*")
async def cancel_input_code(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('ОК')


# ловим код и записываем его в переменную
@dp.message_handler(state=Form_1.code_inp)
async def input_code(message: types.Message, state: FSMContext):
    global code

    async with state.proxy() as data:
        data['code_inp'] = message.text
        code = str(data['code_inp'])

    await state.finish()

# отвечает на текст
@dp.message_handler()
async def text(message: types.Message):
    if message.text == 'Привет':
        await message.reply("И тебе привет!", )

    elif message.text == 'Стоп':
        beat_bot.stop_bot(message)
        await message.reply("Бот остановлен!", reply_markup=keyboard_start)

    elif message.text == 'Начать авторизацию':
        beat_bot.oauth_beatstars(message)
        await message.reply("Бот запущен!", reply_markup=keyboard_oauth)

    elif message.text == 'Ввести данные':
        await start_input_data(message)

    elif message.text == 'Отправить имя пользователя':
        beat_bot.username_input(message)

    elif message.text == 'Отправить пароль':
        beat_bot.password_input(message)

    elif message.text == 'Войти':
        beat_bot.login_button(message)
        await message.reply("Бот вошел")

    elif message.text == 'Ввести код':
        await start_input_code(message)

    elif message.text == 'Отправить код':
        beat_bot.send_code(message)

    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     button1 = types.KeyboardButton("Согласиться с куки")
    #     button2 = types.KeyboardButton("Ввести код подтверждения")
    #     again_button = types.KeyboardButton("Начать заново")
    #     markup.add(button1, button2, again_button)
    #     bot.send_message(message.chat.id, 'Страница успешно загружена!', reply_markup=markup)
    #
    # elif message.text == 'Согласиться с куки':
    #     BS_bot.consent_to_cookies(message)
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     start_button = types.KeyboardButton("Запустить бота")
    #     again_button = types.KeyboardButton("Начать заново")
    #     markup.add(start_button, again_button)
    #     bot.send_message(message.chat.id, 'Согласился с куки. Теперь можешь запускать бота!', reply_markup=markup)
    #
    # elif message.text == 'Ввести код подтверждения':
    #     BS_bot.first_code(message)
    #
    # elif message.text == 'Запустить бота':
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     stop_button = types.KeyboardButton("Стоп")
    #     again_button = types.KeyboardButton("Начать заново")
    #     start_button = types.KeyboardButton("Запустить бота")
    #     markup.add(stop_button, again_button, start_button)
    #     bot.send_message(message.chat.id, 'Бот начал свою работу!', reply_markup=markup)
    #     BS_bot.start_bot(message)
    #
    # elif message.text == 'Стоп':
    #     BS_bot.stop_bot(message)
    #     start(message)
    #
    # elif message.text == 'Начать заново':
    #     start(message)
    # elif message.text == '':

    else:
        await message.reply("Что ты хотел?")


if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

    except Exception as ex:
        print(Fore.RED, ex)
