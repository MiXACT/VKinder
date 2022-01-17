from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from pick_up import Pick_up
import vkinder_db as vk_db


class Bot_chat:
    def __init__(self, token):
        self.token = token
        self.vk = vk_api.VkApi(token=self.token)
        self.longpoll = VkLongPoll(self.vk)

    def write_msg(self, user_id, message):
        self.vk.method('messages.send', {'user_id': user_id,
                                         'message': message,
                                         'random_id': randrange(10 ** 7)})

    def send_pics(self, user_id, friend):
        self.vk.method('messages.send', {'user_id': user_id,
                                         'attachment': f"photo{friend['f_id']}_{friend['pic']}",
                                         'random_id': randrange(10 ** 7)})

    def best_pics(self, pics: list):
        if len(pics) <= 3:
            return pics
        else:
            worst_pic_num = 0
            worst_pic = pics[0]['likes']['count'] + pics[0]['comments']['count']
            for i in range(1, len(pics)):
                if worst_pic > pics[i]['likes']['count'] + pics[i]['comments']['count']:
                    worst_pic_num = i
                    worst_pic = pics[i]['likes']['count'] + pics[i]['comments']['count']
            pics.pop(worst_pic_num)
        return self.best_pics(pics)

    def check_request(self, ask_for: str, user_id, friend):
        if ask_for == 'пока':
            friend['message'] = 'Пока!'
        elif friend[user_id] == 0:
            friend['message'] = f"Привет, {user_id}! Кого хочешь найти? (м/ж)"
            friend[user_id] += 1
        elif friend[user_id] == 1:
            if ask_for == 'ж':
                friend['sex'] = 1
                friend['message'] = 'Укажи возраст. Лет от:'
                friend[user_id] += 1
            elif ask_for == 'м':
                friend['sex'] = 2
                friend['message'] = 'Укажи возраст. Лет от:'
                friend[user_id] += 1
            else:
                friend['message'] = 'Твой ответ не понятен. Попробуй ещё раз!'
        elif friend[user_id] == 2:
            if isinstance(int(ask_for), int) and \
                    int(ask_for) < 100 and int(ask_for) >= 18:
                friend['age_from'] = int(ask_for)
                friend['message'] = 'Лет до:'
                friend[user_id] += 1
            else:
                friend['message'] = 'Твой ответ не понятен. Попробуй ещё раз!'
        elif friend[user_id] == 3:
            if isinstance(int(ask_for), int) and \
                    int(ask_for) >= friend['age_from'] and \
                    int(ask_for) < 100 and int(ask_for) >= 18:
                friend['age_to'] = int(ask_for)
                friend[user_id] += 1
            else:
                friend['message'] = 'Твой ответ не понятен. Попробуй ещё раз!'
        elif ask_for == 'да':
            friend[user_id] = 1
            friend['message'] = 'Кого хочешь найти? (м/ж)'
            friend['offset'] += 50
        else:
            friend['message'] = 'Пока!'
        return friend

    def start_bot(self, person, user_token, db_init):
        #id для таблиц candidates и photos для БД, чтобы делать любое кол-во записей в пределах сессии
        last_photo_id = 0
        last_pers_id = 0
        pers_num = 1
        vk_db.del_db('photos', db_init)
        vk_db.del_db('candidates', db_init)
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    request = event.text
                    self.check_request(request, event.user_id, person)
                    if person['message'] == 'Пока!':
                        self.write_msg(event.user_id, 'Пока!')
                        break
                    if person[event.user_id] <= 3:  #person['answer_counter'] <= 3:
                        self.write_msg(event.user_id, person['message'])
                    else:
                        user_search = Pick_up(user_token)
                        search_result = user_search.find_friend(person)
                        candidates = search_result['response']['items']
                        last_pers_id = vk_db.candidates_tab(candidates, last_pers_id + 1, db_init)
                        for num, item in enumerate(candidates):
                            try:
                                photos = user_search.friend_pics(item['id'])
                                best_3_pics = self.best_pics(photos['response']['items'])
                                last_photo_id = vk_db.photo_tab(item['id'], best_3_pics, pers_num + num, last_photo_id + 1, db_init)
                                for j in range(3):
                                    try:
                                        friend_photo = {'f_id': item['id'],
                                                        'pic': best_3_pics[j]['id']}
                                        self.send_pics(event.user_id, friend_photo)
                                    except IndexError:
                                        pass
                                self.write_msg(event.user_id, f"https://vk.com/id{item['id']}")
                            except KeyError:
                                print(f"KeyError: https://vk.com/id{item['id']}")
                        pers_num = last_pers_id + 1
                        self.write_msg(event.user_id, 'Повторим? (да/нет)')