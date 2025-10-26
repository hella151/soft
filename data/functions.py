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


def handle_rcp():
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


@handle_rcp()
async def mess_to_chat(message_text: str, client, chats_data, cache_manager=None, session_name=None, settings=None):
    """Отправка сообщения в чат с поддержкой кэша"""
    if not chats_data:
        logger.warning("📭 Список чатов пуст")
        return

    # Проверяем, что сообщение не пустое
    if not message_text or not message_text.strip():
        logger.error("❌ Пустое сообщение, пропускаем отправку")
        return

    async for chat_data in async_generator(chats_data):
        clear_line()
        try:
            # Получаем данные чата из переданной структуры
            chat_id = chat_data['id']
            chat_title = chat_data.get('title', 'Unknown')

            # Проверяем валидность chat_id
            if not chat_id or not isinstance(chat_id, (int, str)):
                logger.error(f"❌ Неверный chat_id: {chat_id}")
                continue

            # Проверяем валидность peer
            try:
                peer = await client.resolve_peer(chat_id)
                if not peer:
                    logger.error(f"❌ Не удалось разрешить peer для чата: {chat_title}")
                    continue
            except Exception as e:
                logger.error(f"❌ Ошибка разрешения peer для {chat_title}: {e}")
                continue

            # Проверяем действие перед отправкой
            await client.send_chat_action(
                chat_id=chat_id,
                action=enums.ChatAction.TYPING
            )
            await asyncio.sleep(1)

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
            logger.error(f"❌ Неверный аргумент: {e}")
            continue

        except RPCError as e:
            logger.error(f"⚠️ RPCError: {e}")
            continue

        except Exception as e:
            logger.error(f"❌ Неожиданная ошибка: {e}")
            continue

        # Случайная задержка между сообщениями
        await asyncio.sleep(settings['time_per_message'] + random.randint(1, 5))