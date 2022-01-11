from random import randrange
from pprint import pprint
import requests
import json
from pick_up import Pick_up
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
    partner = {'sex': 0, 'age_from': 18, 'age_to': 100, 'answer_counter': 0, 'message': ''}
    partner['city'] = user_info(user_id, group_token)['response'][0]['city']['id']

    bot = Bot_chat(group_token)
    bot.start_bot(partner, token)