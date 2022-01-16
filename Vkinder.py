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
    group_token = '105ab594a8bc0c7a479914e19e7e8ac1874cd5953c6a583939db8216170a80ef736fc852028b1ad6df55c'#input('Group token (для активации бота из группы ВК): ')
    token = 'e956b1393cf6228446e4c82aa7fb198487b4cc6bdbd63ee3027cfe21dfc1403ea1d0650bce59d6b5feed9'#input('Personal token (для доступа к поиску людей ВК): ')
    user_id = 24308#int(input('Ваш id ВК: '))#24308

    session = requests.Session()
    login, password = 'Ваш телефон', 'Ваш пароль'


    db_init = db_gen.get_db_info()

    partner = {'sex': 0, 'age_from': 18, 'age_to': 100, 'message': '', 'offset': 0, 'count': 10}
    partner['city'] = user_info(user_id, group_token)['response'][0]['city']['id']
    #вместо 'answer_counter': 0 использован ключ - ID пользователя ВК: 0
    partner[user_id] = 0

    bot = Bot_chat(group_token)
    bot.start_bot(partner, token, db_init)