from vk_api.bot_longpoll import VkBotLongPoll
import vk_api as vk
from datetime import datetime
from google_currency import convert
import json
import requests
import os
import database
import distortion
import demotivator


class Bot:
    def __init__(self):
        self.token = 'kek'
        self.api = vk.VkApi(token=self.token)
        self.session_api = self.api.get_api()
        self.longpoll = VkBotLongPoll(group_id='198432189', vk=self.api)
        self.help_message = 'В начале каждой команды пишется обращение: фл или феликс\n' \
                            '1. Помощь: /help\n2. Дисторшн: жмых либо жмых + степень жмыха от 1 до 5\n' \
                            '3. Курс доллара: /usd\n4. Курс евро: /eur\n' \
                            '5. Курс битка: /btc\n' \
                            '6. Демотиватор: демотиватор + две новых строки\n' \
                            '7. Ник: /setnick + ник, /changenick + ник, /mynick'

    def send_message_picture(self, event, image_name, message):
        output_url = self.session_api.photos.getMessagesUploadServer()
        post = requests.post(output_url['upload_url'], files={'photo': open(image_name, 'rb')}).json()
        saved_photo = self.session_api.photos.saveMessagesPhoto(photo=post['photo'], server=post['server'], hash=post['hash'])[0]
        saved_photo_url = 'photo{}_{}'.format(saved_photo['owner_id'], saved_photo['id'])
        self.send_message(event, message, attachment=saved_photo_url)
        os.remove(image_name)

    def send_message(self, event, message, attachment=None):
        if attachment is not None:
            self.session_api.messages.send(peer_id=event.message.peer_id, message=message, attachment=attachment, random_id=0)
        else:
            self.session_api.messages.send(peer_id=event.message.peer_id, message=message, random_id=0)

    def send_currency(self, event, currency_long, currency_short):
        date = str(datetime.strftime(datetime.now(), '%d.%m.%Y'))
        time = str(datetime.strftime(datetime.now(), '%X'))
        currency = json.loads(convert(currency_short, 'rub', 1))['amount']
        message = 'На ' + date + ' ' + time + f' {currency_long} по ' + currency + 'р.'
        self.send_message(event, message)

    def get_name(self, event):
        try:
            user_id = event.message.from_id
            user_get = self.session_api.users.get(user_ids=user_id)
            id = user_get[0]['id']
            return database.get(id)
        except:
            try:
                user_id = event.message.from_id
                user_get = self.session_api.users.get(user_ids=user_id)
                return user_get[0]['first_name']
            except:
                return ''

    def set_nickname(self, event):
        try:
            text = event.message.text.split()
            user_id = event.message.from_id
            user_get = self.session_api.users.get(user_ids=user_id)
            id = user_get[0]['id']
            try:
                nickname = database.get(id)
                self.send_message(event, 'У тебя уже установлен ник: ' + nickname)
            except:
                nickname = ''
                for nickname_part_num in range(2, len(text)):
                    nickname += text[nickname_part_num] + ' '

                name = user_get[0]['first_name']
                surname = user_get[0]['last_name']
                database.append(id, name, surname, nickname)
                self.send_message(event, 'Ник установлен: ' + nickname)
        except:
            self.send_message(event, 'Ошибочка вышла')

    def change_nickname(self, event):
        try:
            text = event.message.text.split()
            nickname = ''
            for nickname_part_num in range(2, len(text)):
                nickname += text[nickname_part_num] + ' '

            user_id = event.message.from_id
            user_get = self.session_api.users.get(user_ids=user_id)
            id = user_get[0]['id']
            database.update(id, nickname)
            self.send_message(event, 'Ник установлен: ' + nickname)
        except:
            self.send_message(event, 'Ошибочка вышла')

    def get_nickname(self, event):
        try:
            user_id = event.message.from_id
            user_get = self.session_api.users.get(user_ids=user_id)
            id = user_get[0]['id']
            self.send_message(event, 'Твой ник: ' + database.get(id))
        except:
            self.send_message(event, 'У тебя нет ника')

    def send_distortion(self, event, spl_response):
        try:
            percent = 1
            try:
                percent = int(spl_response[2])
            except:
                pass

            input_url = event.message['attachments'][0]['photo']['sizes'][-1]['url']
            message = 'Жмыхнуло, ' + self.get_name(event)
            image_name = distortion.do_distortion(input_url, percent)
            self.send_message_picture(event, image_name, message)
        except:
            message = 'Ошибочка вышла'
            self.send_message(event, message)

    def send_demotivator(self, event, response):
        spl = response.split('\n')
        try:
            first_phrase, second_phrase = spl[1], spl[2]
            input_url = event.message['attachments'][0]['photo']['sizes'][-1]['url']
            image_name = demotivator.get_demotivator(input_url, first_phrase, second_phrase)
            message = 'Готово, ' + self.get_name(event)
            self.send_message_picture(event, image_name, message)
        except:
            self.send_message(event, 'Ошибочка вышла')

    def send_help(self, event):
        self.send_message(event, self.help_message)
