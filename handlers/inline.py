import asyncio
from data.log import logger
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message

chats_vz = [-1002029765485]

# @app.on_message(filters.chat(chats_vz) & filters.mentioned)
async def catch_callback_urls(client: Client, message: Message):
    """Ловим URL в callback-данных"""
    if not message.reply_markup:
        return

    # Однострочник для извлечения всех URL
    urls = []  # Создаем пустой список

    # Перебираем все ряды кнопок
    for row in message.reply_markup.inline_keyboard:
        # Перебираем все кнопки в ряду
        for button in row:
            # Проверяем, есть ли у кнопки URL
            if hasattr(button, 'url') and button.url: #hasattr оно проверяет если ли объект
                # Добавляем URL в список
                urls.append(button.url)

    if urls:
        for url in urls:
            try:
                await client.join_chat(chat_id=(url))
                await asyncio.sleep(3)
                logger.info(f"зашли в {url}")
            except Exception as ex:
                logger.error(f"не получилось присоединится: {ex}")

inline_handler =[(catch_callback_urls, filters.chat(chats_vz) & filters.mentioned)]