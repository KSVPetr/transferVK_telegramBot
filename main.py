import vk_api, datetime, asyncio

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from config import token, my_id, TOKEN_BOT

session = vk_api.VkApi(token=token)
bot=Bot(token=TOKEN_BOT, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

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

def check_attachments( event ):
    if event.attachments:
        return True
    return False

@dp.message(CommandStart())
async def start_bot(message: types.Message):
    await message.answer(f'Successfully loginned in VKontakte!')
    
    for event in VkLongPoll(session).listen():

        currTime = get_current_time()

        if event.type == VkEventType.MESSAGE_NEW and event.to_me:

            # We send a text message to the user’s telegram if available
            await message.answer(f'<b>[{currTime}] от {get_username(event.user_id)}</b> : {event.message}')

            # if the message has attachments ( photo or audio-message, ... )
            if check_attachments(event):

                # Photo
                if (event.attachments.get('attach1_type') == 'photo'): 
                    out = session.method('messages.getHistory', {'user_id' : event.user_id, 'count' : 1, 'extended' : 1})
                    for count in range (0,len((out['items'])[0]['attachments'])):
                        await message.answer_photo(f'{((((out['items'])[0]['attachments'])[count]['photo'])['sizes'])[-1]['url']}')

                # Audio - message. # TO DO::
                elif (event.attachments.get('attach1_type') == 'doc'):
                    out = session.method('messages.getHistory', {'user_id' : event.user_id, 'count' : 1, 'extended' : 1})
                    await message.answer_audio(f'{(((out['items'])[0]['attachments'])[0]['audio_message'])['link_mp3']}')

                # Sticker # TO DO::
                elif (event.attachments.get('attach1_type') == 'sticker'):
                    await message.answer(f'Стикер')

        elif event.type == VkEventType.MESSAGE_NEW and event.from_me:

            await message.answer(f'<i>[{currTime}] Для {get_username(event.user_id)}</i> : {event.message}')
            
            # if the message has attachments ( photo or audio-message, ... )
            if check_attachments:

                # Photo
                if (event.attachments.get('attach1_type') == 'photo'):
                    out = session.method('messages.getHistory', {'user_id' : event.user_id, 'count' : 1, 'extended' : 1})
                    for count in range (0,len((out['items'])[0]['attachments'])):
                        await message.answer_photo(f'{((((out['items'])[0]['attachments'])[count]['photo'])['sizes'])[-1]['url']}')

                # Audio - message.
                elif (event.attachments.get('attach1_type') == 'doc'):
                    out = session.method('messages.getHistory', {'user_id' : event.user_id, 'count' : 1, 'extended' : 1})
                    await message.answer_audio(f'{(((out['items'])[0]['attachments'])[0]['audio_message'])['link_mp3']}')
            
                # Sticker # TO DO::
                elif (event.attachments.get('attach1_type') == 'sticker'):
                    await message.answer('Стикер')
            

        # A user is typing a text message to you
        elif event.type == VkEventType.USER_TYPING:
            await message.answer(f'[{currTime}] {get_username(event.user_id)} печатает...')

        # The user records an audio recording
        elif event.type == VkEventType.USER_RECORDING_VOICE:
            await message.answer(f'[{currTime}] {get_username(event.user_id)} записывает аудио...')

async def main():

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())