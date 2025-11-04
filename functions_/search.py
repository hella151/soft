import asyncio
from typing import List

from pyrogram import Client
from pyrogram.errors import FloodWait
from pyrogram.raw import functions
from pyrogram.errors import UserNotParticipant, ChannelPrivate, ChatAdminRequired
from data.log import logger

def handle_flood_wait(retries=3):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return await func(*args, **kwargs)
                except FloodWait as e:
                    wait_time = e.value
                    logger.error(f"⚠️ FloodWait: Ждем {wait_time} секунд (попытка {attempt + 1}/{retries})")
                    await asyncio.sleep(wait_time)
                except Exception as e:
                    logger.error(f"❌ Другая ошибка: {e}")
                    break
            return None
        return wrapper
    return decorator

@handle_flood_wait(retries=3)
async def search_chats_raw(client: Client, query) -> List:
    """Поиск чатов через raw API"""
    cnt = 0
    chats = []
    logger.info("Найденные чаты:")
    try:
        result = await client.invoke(
            functions.contacts.Search(
                q=query,
                limit=10
            )
        )

        # Обрабатываем результаты
        for chat in result.chats:
            cnt += 1
            # if getattr(chat, 'participants_count', '') <= 500:
            #     continue

            chat_info = {
                'id': "-100" + f"{chat.id}",
                'title': getattr(chat, 'title', ''),
                'username': getattr(chat, 'username', ''),
                'type': type(chat).__name__,
                'podpischiki': getattr(chat, 'participants_count', '')
            }

            if chat_info['podpischiki'] >= 2000:
                chats.append(chat_info)
                logger.info(f"{cnt}: 👥 {type(chat).__name__}: {chat_info['title']}: {chat_info['id']}: {chat_info['username']}: {chat_info['podpischiki']}")


        return chats

    except Exception as e:
        print(f"❌ Ошибка поиска: {e}")
        return []