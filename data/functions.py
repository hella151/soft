import asyncio
import random
import sys
from typing import Any
from data.log import logger
from pyrogram import enums
from pyrogram.errors import FloodWait, RPCError, ChatWriteForbidden, ChannelPrivate, UserBannedInChannel
from pyrogram.raw import functions


async def async_generator(my_list: list) -> Any:
    if not my_list:
        return

    for item in my_list:
        yield item


def clear_line():
    """Очистка текущей строки"""
    sys.stdout.write('\r\033[K')
    sys.stdout.flush()
def handle_flood_wait():
    def decorator(func):
        async def wrapper(*args, **kwargs):
            for attempt in range(3):
                try:
                    return await func(*args, **kwargs)
                except RPCError as rpc_error:
                    logger.error(f"⚠️ RPCError:  {rpc_error} (попытка {attempt + 1}/{3}) ждём пару секунд")
                    await asyncio.sleep(2)
                except FloodWait as e:
                    wait_time = e.value
                    logger.error(f"⚠️ FloodWait: Ждем {wait_time} секунд (попытка {attempt + 1}/{3})")
                    await asyncio.sleep(wait_time)
                except Exception as e:
                    logger.error(f"❌ Другая ошибка: {e}")
                    break
            return None
        return wrapper
    return decorator

@handle_flood_wait()
async def mess_to_chat(message_text: str, client, chats_id, cache_manager=None, session_name=None):
    global chat, chat_title
    if not chats_id:
        logger.warning("📭 Список чатов пуст")
        return

    async for chat_id in async_generator(chats_id):
        clear_line()
        try:
            # Проверяем валидность chat_id
            if not chat_id or not isinstance(chat_id, (int, str)):
                logger.error(f"❌ Неверный chat_id: {chat_id}")
                continue

            # Пытаемся получить название из кэша
            chat_title = None
            if cache_manager and session_name:
                chat_title = cache_manager.get_chat_title(session_name, "mailing", chat_id)

            # Если нет в кэше, делаем запрос к API
            if not chat_title:
                try:
                    chat = await client.get_chat(chat_id)
                    chat_title = getattr(chat, 'title', 'Unknown')
                except Exception as e:
                    logger.error(f"❌ Ошибка получения информации о чате {chat_id}: {e}")
                    chat_title = "Unknown"

            # Проверяем действие перед отправкой
            await client.send_chat_action(
                chat_id=chat_id,
                action=enums.ChatAction.TYPING
            )
            await asyncio.sleep(1)

            # Отправляем сообщение
            peer = await client.resolve_peer(chat_id)

            # Отправляем сообщение через raw метод
            await client.invoke(
                functions.messages.SendMessage(
                    peer=peer,
                    message=message_text,
                    random_id=client.rnd_id(),
                    no_webpage=False,
                    silent=False
                )
            )
            logger.info(f"✅ Отправлено сообщение в чат -> {chat_title}")

        except FloodWait as e:
            wait_time = e.value + 5
            logger.warning(f"⏳ FloodWait: ждем {wait_time} секунд")
            await asyncio.sleep(wait_time)

        except ChatWriteForbidden:
            logger.error(f"✋ Запрещено писать в чат: {chat_title}")
            continue

        except ChannelPrivate:
            logger.error(f"🔒 Приватный канал: {chat_title}")
            continue

        except UserBannedInChannel:
            logger.error(f"🚫 Заблокирован в чате: {chat_title}")
            continue

        except ValueError as e:
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