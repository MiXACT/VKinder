import requests, vk_api
import db_gen
from bot import Bot_chat


def user_info(id, user_token):
    vk_url = 'https://api.vk.com/method/users.get'
    params = {
        'user_ids': id,
        'access_token': user_token,
        'v': '5.131',
        'fields': 'bdate,sex,city,relation'
    }
    return requests.get(vk_url, params=params).json()


if __name__ == '__main__':
    group_token = input('Group token (для активации бота из группы ВК): ')
    token = input('Personal token (для доступа к поиску людей ВК): ')
    user_id = int(input('Ваш id ВК: '))#24308

    session = requests.Session()
    login, password = 'Ваш телефон', 'Ваш пароль'


    db_init = db_gen.get_db_info()

    partner = {'sex': 0, 'age_from': 18, 'age_to': 100, 'message': '', 'offset': 0, 'count': 10}
    partner['city'] = user_info(user_id, group_token)['response'][0]['city']['id']
    #вместо 'answer_counter': 0 использован ключ - ID пользователя ВК: 0
    partner[user_id] = 0

    bot = Bot_chat(group_token)
    bot.start_bot(partner, token, db_init)