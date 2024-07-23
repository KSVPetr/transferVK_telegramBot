import vk_api, asyncio

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from vk_api.longpoll import VkLongPoll, VkEventType
from config import my_id, TOKEN_BOT

from data_vk.authorization import TOKEN
import data_vk.vk_functions as vfunc

session = vk_api.VkApi(token=TOKEN)
bot=Bot(token='', default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(CommandStart())
async def start_bot(message: types.Message):
    await message.answer(f'Successfully loginned in VKontakte!')
    
    try:
        for event in VkLongPoll(session).listen():

            currTime = vfunc.get_current_time()

            if event.type == VkEventType.MESSAGE_NEW and event.to_me:

                await message.answer(f'<b>[{currTime}] от {vfunc.get_username(event.user_id)}</b> : {event.message}')

                if vfunc.check_attachments(event):

                    if (event.attachments.get('attach1_type') == 'photo'): 
                        out = session.method('messages.getHistory', {'user_id' : event.user_id, 'count' : 1, 'extended' : 1})
                        for count in range (0,len((out['items'])[0]['attachments'])):
                            await message.answer_photo(f'{(out['items'])[0]['attachments'][count]['photo']['sizes'][-1]['url']}')

                    elif (event.attachments.get('attach1_type') == 'doc'):
                        out = session.method('messages.getHistory', {'user_id' : event.user_id, 'count' : 1, 'extended' : 1})
                        await message.answer_audio(f'{out['items'][0]['attachments'][0]['audio_message']['link_mp3']}')

                    # Sticker # TO DO::
                    elif (event.attachments.get('attach1_type') == 'sticker'):
                        out = session.method('messages.getHistory', {'user_id' : event.user_id, 'count' : 1, 'extended' : 1})
                        await message.answer_photo(f'{out['items'][0]['attachments'][0]['sticker']['images'][-1]['url']}')

            elif event.type == VkEventType.MESSAGE_NEW and event.from_me:

                await message.answer(f'<i>[{currTime}] Для {vfunc.get_username(event.user_id)}</i> : {event.message}')
                
                if vfunc.check_attachments:

                    if (event.attachments.get('attach1_type') == 'photo'):
                        out = session.method('messages.getHistory', {'user_id' : event.user_id, 'count' : 1, 'extended' : 1})
                        for count in range (0,len((out['items'])[0]['attachments'])):
                            await message.answer_photo(f'{out['items'][0]['attachments'][count]['photo']['sizes'][-1]['url']}')

                    elif (event.attachments.get('attach1_type') == 'doc'):
                        out = session.method('messages.getHistory', {'user_id' : event.user_id, 'count' : 1, 'extended' : 1})
                        await message.answer_audio(f'{out['items'][0]['attachments'][0]['audio_message']['link_mp3']}')
                
                    elif (event.attachments.get('attach1_type') == 'sticker'):
                        out = session.method('messages.getHistory', {'user_id' : event.user_id, 'count' : 1, 'extended' : 1})
                        await message.answer_photo(f'{out['items'][0]['attachments'][0]['sticker']['images'][-1]['url']}')
                
            elif event.type == VkEventType.USER_TYPING:
                await message.answer(f'[{currTime}] {vfunc.get_username(event.user_id)} печатает...')

            elif event.type == VkEventType.USER_RECORDING_VOICE:
                await message.answer(f'[{currTime}] {vfunc.get_username(event.user_id)} записывает аудио...')
    except BaseException as error_message:
        print(error_message)
        start_bot()

async def main():

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())