import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from config import acces_token, comunity_token
import core
import data_store
import datetime
import psycopg2
conn = psycopg2.connect(database="postgres", user="postgres", password="*6352a17")
current_year = datetime.datetime.now().year

class BotInterface:
    def __init__(self, token):
        self.bot = vk_api.VkApi(token=token)


    def message_send(self, user_id, message=None, attachment=None):
        self.bot.method('messages.send',
                        {'user_id': user_id,
                         'message': message,
                         'random_id': get_random_id(),
                         'attachment': attachment
                         }
                        )

    def prof_info(self, event_user_id):
        global city_id
        global birthday
        global birth_year
        global age_from
        global age_to
        global sex
        prof_info = core.tools.get_profile_info(event_user_id)
        city_id = prof_info[0].get('city').get('id')
        birthday = prof_info[0].get('bdate')
        birth_year = birthday.split('.')[2]
        age_from = current_year - int(birth_year) - 5
        age_to = current_year - int(birth_year) + 5
        sex = prof_info[0].get('sex')
        if sex == 1:
            sex = 2
            self.message_send(event_user_id, 'Вы женщина, ищем мужчину, возраст: +- 5 лет :-)')
        elif sex == 2:
            self.message_send(event_user_id, 'Вы мужчина, ищем женщину, возраст: +- 5 лет :-)')
            sex = 1
        else:
            sex = int(input('ошибка определения пола, введите Ваш пол:'
                            ' 1 - если Вы женщина, 2 - если Вы мужчина'))

    def handler(self):
        longpull = VkLongPoll(self.bot)
        offset = 0
        for event in longpull.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                data_store.create_table(conn)
                data_store.clear_table(conn)
                if event.text.lower() == 'привет':
                    self.message_send(event.user_id, 'Добрый день, напишите команду "поиск" чтобы увидеть результат!')
                elif event.text.lower() == 'поиск':
                    self.prof_info(event.user_id)
                    data_store.create_table(conn)
                    data_store.clear_table(conn)
                    result_prof = core.tools.user_serch(city_id, age_from, age_to, sex, 6, offset)
                    for profile in result_prof:
                        id_found = profile.get('id')
                        id_list = data_store.from_db(conn, event.user_id)
                        if id_found in id_list:
                            continue
                        else:
                            data_store.to_bd(conn, event.user_id, id_found)
                            self.message_send(event.user_id, 'https://vk.com/id' + str(id_found))
                            result_photos_get = core.tools.photos_get(id_found)
                            for photo in result_photos_get:
                                photo_id = photo.get('id')
                                owner_id = photo.get('owner_id')
                                media = 'photo' + str(owner_id) + '_' + str(photo_id)
                                self.message_send(event.user_id, attachment= media)
                    self.message_send(event.user_id, 'Напишите "далее", если хотите продолжить поиск!')
                elif event.text.lower() == 'далее':
                    if offset >= 1000:
                        self.message_send(event.user_id, 'Вы исчерпали лимит в 1000 запросов!')
                    else:
                        self.prof_info(event.user_id)
                        offset += 25
                        result_prof = core.tools.user_serch(city_id, age_from, age_to, sex, 6, offset)
                        for profile in result_prof:
                            id_found = profile.get('id')
                            id_list = data_store.from_db(conn, event.user_id)
                            if id_found in id_list:
                                continue
                            else:
                                data_store.to_bd(conn, event.user_id, id_found)
                                self.message_send(event.user_id, 'https://vk.com/id' + str(id_found))
                                result_photos_get = core.tools.photos_get(id_found)
                                for photo in result_photos_get:
                                    photo_id = photo.get('id')
                                    owner_id = photo.get('owner_id')
                                    media = 'photo' + str(owner_id) + '_' + str(photo_id)
                                    self.message_send(event.user_id, attachment= media)
                else:
                    self.message_send(event.user_id, 'извините, пока я знаю только "привет", "поиск", '
                                                     '"далее" и "пока" :-)')


if __name__ == '__main__':
    bot = BotInterface(comunity_token)
    bot.handler()
