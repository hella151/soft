import asyncio
import random
from typing import Any
from data.log import logger
from pyrogram import Client, enums
from pyrogram.errors import FloodWait, RPCError, ChatWriteForbidden, ChannelPrivate, UserBannedInChannel


async def async_generator(my_list: list) -> Any:
    if my_list is None:
        yield None

    for item in my_list:
        yield item

async def delete(client: Client, chats_id):
    async for id in async_generator(my_list=chats_id):
        try:
            await client.leave_chat(chat_id=id)
            await asyncio.sleep(5)
        except Exception:
            continue

async def mess_to_chat(message_text: str, client, chats_id):
    async for id in async_generator(chats_id):
        await client.send_chat_action(chat_id=id, action=enums.ChatAction.TYPING, progress=0)
        await asyncio.sleep(1)
        chat = await client.get_chat(id)

        try:
            await client.send_message(chat_id=id, text=message_text)
            logger.info(f"✅ Отправлено сообщение в чат -> {chat.title}")
        except FloodWait as e:
            wait_time = e.value + 5
            logger.warning(f"⏳ FloodWait: ждем {wait_time} секунд")
            await asyncio.sleep(wait_time)
        except RPCError as e:
            logger.error(f"⚠️ RPCError: {e}")
            continue
        except ChatWriteForbidden:
            logger.error(f"Администратор ограничил вам доступ писать в чат -> {chat.title}")
            continue
        except ChannelPrivate:
            logger.error(f"🔒 Приватный канал {chat.title}")
            continue
        except UserBannedInChannel:
            logger.error(f"🚫 Заблокирован в чате {chat.title}")
            continue
        except Exception as e:
            logger.error(f"❌ Неожиданная ошибка: {e} в чате: {chat.title}")
            continue
        await asyncio.sleep(10 + random.randint(1, 5))