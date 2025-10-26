import asyncio
import random
from pyrogram import Client
from data.log import logger
from data.functions import mess_to_chat
import sys


def clear_line():
    """Очистка текущей строки"""
    sys.stdout.write('\r\033[K')
    sys.stdout.flush()


async def main_bot_function(client: Client, chats: list, cache_manager=None, session_name=None, settings=None):
    """Основная функция работы бота с поддержкой кэша"""
    try:
        with open('text.txt', 'r', encoding='utf-8') as file:
            messages = [line.strip().replace('\\n', '\n') for line in file if line.strip()]

        # Фильтруем пустые сообщения
        messages = [msg for msg in messages if msg and msg.strip()]

        if not messages:
            logger.error("❌ Нет валидных сообщений в text.txt")
            return

        n = 0
        while n < settings['messages_per_cycle']:
            message = random.choice(messages)

            # Проверяем, что сообщение не пустое
            if not message or not message.strip():
                logger.warning("⚠️ Пропущено пустое сообщение")
                continue

            # ОБНОВЛЕННЫЙ ВЫЗОВ с поддержкой кэша
            await mess_to_chat(
                message_text=message,
                client=client,
                chats_data=chats,
                cache_manager=cache_manager,
                session_name=session_name,
                settings=settings
            )

            await asyncio.sleep(settings['delay_between_messages'] + random.randint(1, 3))

            logger.info(f"📊 цикл: {n + 1}")
            n += 1

    except asyncio.CancelledError:
        clear_line()
        logger.info("🛑 Бот остановлен по команде")

    except Exception as e:
        clear_line()
        logger.error(f"❌ Критическая ошибка в функции рассылки: {e}")