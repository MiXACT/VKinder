import requests
import json


class Pick_up:
    def __init__(self, user_token):
        self.user_token = user_token

    def find_friend(self, pers_info):
        vk_url = 'https://api.vk.com/method/users.search'
        params = {
            'access_token': self.user_token,
            'v': '5.131',
            'fields': 'bdate,sex,city,relation',
            'has_photo': 1,
            'age_from': pers_info['age_from'],
            'age_to': pers_info['age_to'],
            'sex': pers_info['sex'],
            'city': pers_info['city'],
            'status': 1,
            'is_closed': False,
            'offset': pers_info['offset'],
            'count': pers_info['count']
        }
        return requests.get(vk_url, params=params).json()

    def friend_pics(self, id):
        vk_url = 'https://api.vk.com/method/photos.get'
        params = {
            'access_token': self.user_token,
            'v': '5.131',
            'owner_id': id,
            'album_id': 'profile',
            'extended': 1,
        }
        return requests.get(vk_url, params=params).json()