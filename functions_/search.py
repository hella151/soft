import asyncio
from typing import List

from pyrogram import Client
from pyrogram.errors import FloodWait
from pyrogram.raw import functions
from pyrogram.errors import UserNotParticipant, ChannelPrivate, ChatAdminRequired
from data.log import logger

async def is_member(client: Client, chat_id):
    """Проверяет, является ли пользователь участником чата"""
    try:
        await client.get_chat_member(chat_id=chat_id, user_id="me")
        return True
    except UserNotParticipant:
        return False  # Не участник
    except ChannelPrivate:
        return False  # Приватный канал, нет доступа
    except ChatAdminRequired:
        return False  # Нет прав администратора
    except Exception as e:
        logger.error(f"❌ Ошибка проверки: {e}")
        return False

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

            chats.append(chat_info)
            logger.info(f"{cnt}: 👥 {type(chat).__name__}: {chat_info['title']}: {chat_info['id']}: {chat_info['username']}: {chat_info['podpischiki']}")

        return chats

    except Exception as e:
        print(f"❌ Ошибка поиска: {e}")
        return []



# if __name__ == "__main__":
#     try:
#         app.run(main())
#     except KeyboardInterrupt:
#         print('\n⏹️ Программа остановлена пользователем')
#
# if await is_member(client, chat_id=str("-100" + f"{chat.id}")):
#     continue
# else:
#     try:
#         await client.join_chat(chat_id=str("-100" + f"{chat.id}"))
#         print(f"Зашли в {getattr(chat, 'title', '')}")
#
#     except Exception as ex:
#         print(f"Ошибка захода в {getattr(chat, 'title', '')} {ex}")
# await asyncio.sleep(3)