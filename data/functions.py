import asyncio
import random
import sys
from typing import Any
from data.log import logger
from pyrogram.errors import FloodWait, RPCError, ChatWriteForbidden, ChannelPrivate, UserBannedInChannel
from pyrogram.raw import functions


async def async_generator(my_list: list) -> Any:
    for item in my_list:
        yield item


def clear_line():
    sys.stdout.write('\r\033[K')
    sys.stdout.flush()


def handle_rcp():
    def decorator(func):
        async def wrapper(*args, **kwargs):
            for attempt in range(3):
                try:
                    return await func(*args, **kwargs)
                except FloodWait as e:
                    logger.error(f"⚠️ FloodWait: Ждем {e.value} секунд")
                    await asyncio.sleep(e.value)
                except RPCError as rpc_error:
                    if "PEER_ID_INVALID" in str(rpc_error) or "400" in str(rpc_error):
                        logger.error(f"⚠️ PEER_ID_INVALID (попытка {attempt + 1}/3)")
                        if attempt < 2:
                            await asyncio.sleep(2 + attempt)
                            continue
                        return False
                    logger.error(f"⚠️ RPCError: {rpc_error}")
                    await asyncio.sleep(2)
                except Exception as e:
                    logger.error(f"❌ Ошибка: {e}")
                    if attempt == 2:
                        return False
                    await asyncio.sleep(2)
            return None

        return wrapper

    return decorator


async def mess_to_chat(message_text: str, client, chats_data, settings=None, session_switcher=None):
    if not chats_data:
        logger.warning("📭 Список чатов пуст")
        return

    if not message_text or not message_text.strip():
        logger.error("❌ Пустое сообщение")
        return

    async for chat_data in async_generator(chats_data):
        clear_line()

        success = await send_single_message(
            message_text, client, chat_data, session_switcher
        )

        if not success:
            chat_id = chat_data['id']
            chat_title = chat_data.get('title', 'Unknown')
            await handle_invalid_chat(chat_id, chat_title, session_switcher, )

        if settings and 'time_per_message' in settings:
            await asyncio.sleep(settings['time_per_message'] + random.uniform(1.5, 8))


@handle_rcp()
async def send_single_message(message_text: str, client, chat_data, session_switcher):
    global chat_title
    try:
        chat_id = chat_data['id']
        chat_title = chat_data.get('title', 'Unknown')

        if not chat_id or not isinstance(chat_id, (int, str)):
            logger.error(f"❌ Неверный chat_id: {chat_id}")
            return False

        try:
            await client.send_message(chat_id=chat_id, text=message_text)
            logger.info(f"✅ Отправлено в -> {chat_title}")
            return True
        except RPCError:
            try:
                peer = await client.resolve_peer(chat_id)
                if not peer:
                    return False

                await client.invoke(
                    functions.messages.SendMessage(
                        peer=peer,
                        message=message_text,
                        random_id=client.rnd_id(),
                        no_webpage=False,
                        silent=False
                    )
                )
                logger.info(f"✅ Отправлено через raw -> {chat_title}")
                return True
            except Exception:
                return False

    except (ChatWriteForbidden, ChannelPrivate, UserBannedInChannel) as e:
        error_type = {
            ChatWriteForbidden: "✋ Запрещено писать",
            ChannelPrivate: "🔒 Приватный канал",
            UserBannedInChannel: "🚫 Заблокирован"
        }.get(type(e), "❌ Недоступен")
        logger.error(f"{error_type}: {chat_title}")
        return False

    except Exception as e:
        logger.error(f"❌ Ошибка отправки в {chat_title}: {e}")
        return False


async def handle_invalid_chat(chat_id, chat_title, session_switcher):
    await asyncio.sleep(1)
    if session_switcher:
        replacement_chat = await session_switcher.replace_invalid_chat(chat_id)
        if replacement_chat:
            logger.info(f"🔄 Чат заменен: {chat_title} -> {replacement_chat.get('title', 'Без названия')}")

    logger.info("Можно выйти из чата чтобы не засорять бота")
    await asyncio.sleep(1 + random.uniform(1, 3))