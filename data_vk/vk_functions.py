import datetime

from main import session
from vk_api.utils import get_random_id

def get_user_status(user_id):
    status = session.method('status.get', {'user_id': user_id})
    if status['text'] == '': status['text'] = 'Статус отсутствует!'
    return status['text']

def get_list_online_friend(user_id):
    friends = session.method('friends.getOnline', {'user_id': user_id})
    print('Friends online :', len(friends))
    for friend in friends:
        person = session.method('users.get', {'user_ids': friend})
        person_status = get_user_status(friend)
        print(f'{person[0]['first_name']} {person[0]['last_name']} - "{person_status}"')

def get_username(user_id):
    name = session.method('users.get', {'user_ids' : user_id})
    name = name[0]['first_name'] + ' ' + name[0]['last_name']
    return name

def send_message(user_id, text):
    session.method('messages.send', {'user_id' : user_id, 'random_id' : get_random_id(), 'message': text})

def get_current_time():
    delta = datetime.timedelta( hours=3 )
    utc = datetime.timezone.utc
    fmt = '%H:%M:%S'
    time = ( datetime.datetime.now(utc) + delta )
    timestr = time.strftime(fmt)
    return timestr

def get_history_messages(user_id):
    output = session.method('messages.getHistory', 
                            {'user_id' : user_id,
                             'count' : 1,
                             'extended' : 1})
    print(f'Автор сообщения : {get_username((output['items'])[0]['from_id'])}')
    print(f'Содержимое : {(output['items'])[0]['text']}')
    if (len((output['items'])[0]['attachments']) != 0):

        # Фото
        if (((output['items'])[0]['attachments'])[0]['type'] == 'photo'):
            for count in range (0,len((output['items'])[0]['attachments'])):
                print('Фото : ', ((((output['items'])[0]['attachments'])[count]['photo'])['sizes'])[-1]['url'])
        
        # Аудио-сообщение
        elif (((output['items'])[0]['attachments'])[0]['type'] == 'audio_message'):
            print('Аудио : ', (((output['items'])[0]['attachments'])[0]['audio_message'])['link_mp3'])

        # Видеозаписи
        elif (((output['items'])[0]['attachments'])[0]['type'] == 'video'):
            print('Видео : ', output['items'])

        # Стикеры
        elif (((output['items'])[0]['attachments'])[0]['type'] == 'sticker'):
            print('Стикер : ', ((((output['items'])[0]['attachments'])[0]['sticker'])['images'])[-1]['url'])

def check_attachments( event ):
    if event.attachments:
        return True
    return False