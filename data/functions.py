import asyncio
import random
import sys
from typing import Any
from data.log import logger
from pyrogram import enums
from pyrogram.errors import FloodWait, RPCError, ChatWriteForbidden, ChannelPrivate, UserBannedInChannel
from pyrogram.raw import functions

async def async_generator(my_list: list) -> Any:
    if not my_list:  # Проверяем пустой список/None
        return  # Просто выходим

    for item in my_list:
        yield item

def clear_line():
    """Очистка текущей строки"""
    sys.stdout.write('\r\033[K')
    sys.stdout.flush()

# УЛУЧШЕННАЯ ВЕРСИЯ ФУНКЦИИ mess_to_chat
async def mess_to_chat(message_text: str, client, chats_id):
    global chat
    if not chats_id:  # Проверка на пустой список
        logger.warning("📭 Список чатов пуст")
        return


    async for chat_id in async_generator(chats_id):
        clear_line()
        try:
            # Проверяем валидность chat_id
            if not chat_id or not isinstance(chat_id, (int, str)):
                logger.error(f"❌ Неверный chat_id: {chat_id}")
                continue

            # Получаем информацию о чате
            chat = await client.get_chat(chat_id)

            # Проверяем действие перед отправкой
            await client.send_chat_action(
                chat_id=chat_id,
                action=enums.ChatAction.TYPING
            )
            await asyncio.sleep(1)

            # Отправляем сообщение
            peer = await client.resolve_peer(chat_id)
            print(peer)
            # Отправляем сообщение через raw метод
            await client.invoke(
                functions.messages.SendMessage(
                    peer=peer,
                    message="Тестовое сообщение через raw",
                    random_id=client.rnd_id(),
                    no_webpage=False,
                    silent=False
                )
            )
            logger.info(f"✅ Отправлено сообщение в чат -> {chat.title}")

        except FloodWait as e:
            wait_time = e.value + 5
            logger.warning(f"⏳ FloodWait: ждем {wait_time} секунд")
            await asyncio.sleep(wait_time)

        except ChatWriteForbidden:
            logger.error(f"✋ Запрещено писать в чат: {getattr(chat, 'title', 'Unknown')}")
            continue

        except ChannelPrivate:
            logger.error(f"🔒 Приватный канал: {getattr(chat, 'title', 'Unknown')}")
            continue

        except UserBannedInChannel:
            logger.error(f"🚫 Заблокирован в чате: {getattr(chat, 'title', 'Unknown')}")
            continue

        except ValueError as e:
            print(chat_id)
            logger.error(f"❌ Неверный аргумент: {e.args, e}")
            continue

        except RPCError as e:
            logger.error(f"⚠️ RPCError: {e}")
            continue

        except Exception as e:
            logger.error(f"❌ Неожиданная ошибка: {e}")
            continue

        # Случайная задержка между сообщениями
        await asyncio.sleep(10 + random.randint(1, 5))