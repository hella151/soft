import asyncio
import random
from typing import Any

from pyrogram import Client, enums

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
    async for item in async_generator(chats_id):
        await client.send_chat_action(chat_id=item, action=enums.ChatAction.TYPING, progress=0)
        await asyncio.sleep(1)
        await client.send_message(chat_id=item, text=message_text)
        await asyncio.sleep(15 + random.randint(1, 5))