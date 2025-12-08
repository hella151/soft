import asyncio
from data.log import logger
from pyrogram import Client
from pyrogram import filters
import random
from pyrogram.types import Message
import sys
from pyrogram.errors import FloodWait

# Глобальная переменная для хранения времени FloodWait
flood_wait_until = 0


def clear_line():
    """Очистка текущей строки"""
    sys.stdout.write('\r\033[K')
    sys.stdout.flush()


async def catch_callback_urls(client: Client, message: Message):
    """Ловим URL в callback-данных"""
    global flood_wait_until

    # Проверяем, не находимся ли мы в режиме ожидания FloodWait
    current_time = asyncio.get_event_loop().time()
    if flood_wait_until > current_time:
        wait_time = flood_wait_until - current_time
        logger.warning(f"⏳ Ожидаем окончания FloodWait: {wait_time:.1f} секунд")
        await asyncio.sleep(wait_time)
        # Сбрасываем время ожидания после сна
        flood_wait_until = 0

    if not message.reply_markup:
        return

    # Однострочник для извлечения всех URL
    urls = []  # Создаем пустой список

    # Перебираем все ряды кнопок
    for row in message.reply_markup.inline_keyboard:
        # Перебираем все кнопки в ряду
        for button in row:
            # Проверяем, есть ли у кнопки URL
            if hasattr(button, 'url') and button.url:  # hasattr оно проверяет если ли объект
                # Добавляем URL в список
                urls.append(button.url)

    if urls:
        for url in urls:
            try:
                await client.join_chat(chat_id=(url))
                await asyncio.sleep(10 + random.uniform(1.5, 10.5))
                logger.info(f"зашли в {url}")

            except FloodWait as e:
                wait_time = e.value
                flood_wait_until = asyncio.get_event_loop().time() + wait_time
                logger.warning(f"⏳ FloodWait: Ждем {wait_time} секунд перед вступлением в следующие группы")
                # НЕ спим здесь, просто устанавливаем время ожидания для следующих вызовов
                break  # Прерываем обработку текущих URL

            except Exception as ex:
                # Игнорируем ошибку INVITE_REQUEST_SENT - это успешная отправка заявки
                if "INVITE_REQUEST_SENT" in str(ex):
                    logger.info(f"✅ Заявка на вступление отправлена: {url}")
                    continue
                # Игнорируем ошибку USERNAME_NOT_OCCUPIED - username не существует
                elif "USERNAME_NOT_OCCUPIED" in str(ex):
                    logger.warning(f"⚠️ Username не существует: {url}")
                    continue
                else:
                    logger.error(f"не получилось присоединится: {ex}")
                    continue


inline_handler = [(catch_callback_urls, filters.mentioned)]