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
async def mess_to_chat(message_text: str, client, chats_data, cache_manager=None, session_name=None, settings=None,
                       session_switcher=None):
    """Отправка сообщения в чат с автоматической заменой недоступных чатов"""
    global chat_id, chat_title
    if not chats_data:
        logger.warning("📭 Список чатов пуст")
        return

    # Проверяем, что сообщение не пустое
    if not message_text or not message_text.strip():
        logger.error("❌ Пустое сообщение, пропускаем отправку")
        return

    async for chat_data in async_generator(chats_data):
        clear_line()

        # ПЕРЕНЕСЕМ ОСНОВНУЮ ЛОГИКУ В ОТДЕЛЬНУЮ ФУНКЦИЮ С ДЕКОРАТОРОМ
        success = await send_single_message(
            message_text, client, chat_data, session_name, settings, session_switcher
        )

        if not success:
            continue

        # Случайная задержка между сообщениями
        await asyncio.sleep(settings['time_per_message'] + random.randint(1, 5))


# НОВАЯ ФУНКЦИЯ ДЛЯ ОТПРАВКИ ОДНОГО СООБЩЕНИЯ С ПОВТОРАМИ
@handle_rcp()
async def send_single_message(message_text: str, client, chat_data, session_name, settings, session_switcher):
    """Отправка одного сообщения с обработкой ошибок"""
    global chat_id, chat_title
    try:
        chat_id = chat_data['id']
        chat_title = chat_data.get('title', 'Unknown')

        # Проверяем валидность chat_id
        if not chat_id or not isinstance(chat_id, (int, str)):
            logger.error(f"❌ Неверный chat_id: {chat_id}")
            return False

        # Проверяем валидность peer
        peer = await client.resolve_peer(chat_id)
        if not peer:
            logger.error(f"❌ Не удалось разрешить peer для чата: {chat_title}")
            await handle_invalid_chat(chat_id, chat_title, session_name, session_switcher)
            return False

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
        return True

    except FloodWait as e:
        wait_time = e.value + 5
        logger.warning(f"⏳ FloodWait: ждем {wait_time} секунд")
        await asyncio.sleep(wait_time)
        return False  # Не продолжаем для этого чата после FloodWait

    except (ChatWriteForbidden, ChannelPrivate, UserBannedInChannel) as e:
        error_type = {
            ChatWriteForbidden: "✋ Запрещено писать в чат",
            ChannelPrivate: "🔒 Приватный канал",
            UserBannedInChannel: "🚫 Заблокирован в чате"
        }.get(type(e), "❌ Недоступен")

        logger.error(f"{error_type}: {chat_title}")
        await handle_invalid_chat(chat_id, chat_title, session_name, session_switcher)
        return False

    except Exception as e:
        logger.error(f"❌ Ошибка отправки в {chat_title}: {e}")
        await handle_invalid_chat(chat_id, chat_title, session_name, session_switcher)
        return False


# ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ДЛЯ ОБРАБОТКИ НЕВАЛИДНЫХ ЧАТОВ
async def handle_invalid_chat(chat_id, chat_title, session_name, session_switcher):
    """Обработка невалидного чата"""
    if session_switcher:
        replacement_chat = await session_switcher.replace_invalid_chat(session_name, chat_id)
        if replacement_chat:
            await session_switcher.update_selected_chats(session_name, chat_id, replacement_chat)
            logger.info(f"🔄 Чат автоматически заменен: {chat_title} -> {replacement_chat.get('title', 'Без названия')}")

    await asyncio.sleep(1)