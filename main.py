import vk_api, time, json

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from config import token, my_id
session = vk_api.VkApi(token=token)

def get_user_status(user_id):
    status = session.method('status.get', {'user_id': user_id})
    if status['text'] == '': status['text'] = 'Статус отсутствует!'
    return status['text']

def get_list_online_friend(user_id):
    friends = session.method('friends.getOnline', {'user_id': user_id})
    print('Друзей онлайн :', len(friends))
    for friend in friends:
        person = session.method('users.get', {'user_ids': friend})
        person_status = get_user_status(friend)
        print(f'{person[0]['first_name']} {person[0]['last_name']} - "{person_status}"')

def send_message(user_id, text):
    session.method('messages.send', {'user_id' : user_id, 'random_id' : get_random_id(), 'message': text})

get_list_online_friend(my_id)

for event in VkLongPoll(session).listen():
    # Если это новое сообщения и ДЛЯ меня
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:

        name = session.method('users.get', {'user_ids' : event.user_id})
        print(f'Входящее сообщение | от {name[0]['first_name']} {name[0]['last_name']} : {event.message}')

    # Если это новое сообщения и ОТ меня
    elif event.type == VkEventType.MESSAGE_NEW and event.from_me and event.text:

        name = session.method('users.get', {'user_ids' : event.user_id})
        print(f'Исходящее сообщение | для {name[0]['first_name']} {name[0]['last_name']} : {event.message}')