import asyncio
from typing import Any

from data import  delete
from pyrogram import Client, enums

from pyrogram import filters
from pyrogram.types import Message


user_chats = [1228992044]
chats_ids = []

async def reply(client: Client, message: Message) -> Any:
    global url_join, chat_id
    if not message.text:
        return

    url = "https://t.me/vzz_piar_vzz"

    if message.chat.id not in user_chats:
        try:
            user_chats.append(message.chat.id)

            await asyncio.sleep(1)
            await client.send_chat_action(chat_id=message.chat.id, action=enums.ChatAction.TYPING, progress=0)
            await asyncio.sleep(1)
            await client.send_message(chat_id=message.chat.id, text=f'Привет')
            await asyncio.sleep(1)
            await client.send_message(chat_id=message.chat.id, text=f'{url}')


        except Exception:
            pass

    if 'https://t.me/' in message.text:
        words = message.text.split()
        for i in words:
            if i.startswith("http"):
                try:
                    chat_id = await client.get_chat(chat_id=str(i))
                    url_join = str(i)
                    chats_ids.append(chat_id.id)

                    await asyncio.sleep(3)
                    await client.join_chat(chat_id=url_join)
                    await message.reply('готово', quote=True)
                    print(f'{url_join, chat_id.id, message.from_user.username} успешно')
                except Exception:
                    await message.reply('только вз могу делать(', quote=True)
                    print(f'{url_join, chat_id.id, message.from_user.username} провал')
                    # await message.reply('готово', quote=True)

    if '@' in message.text:
        await asyncio.sleep(1)
        await client.send_chat_action(chat_id=message.chat.id, action=enums.ChatAction.TYPING, progress=0)
        await asyncio.sleep(1)
        await message.reply(f'скинь пж полную ссылку, типо вот так \n'
                            f'{url}')

    if message.text.lower() == 'delete':
        try:
            await message.reply('Начинаю выход из чатов...', quote=True)
            # Здесь должна быть функция delete() для выхода из чатов
            await delete(client, chats_id=chats_ids)
            await message.reply('Готово!', quote=True)
        except Exception as e:
            await message.reply(f'Ошибка: {e}', quote=True)

# @app.on_message(filters=filters.private)

reply_handler = [
    (reply, filters.private)
]