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


async def main_bot_function(client: Client, chats: list):
    """Основная функция работы бота"""
    try:
        with open('text.txt', 'r', encoding='utf-8') as file:
            messages = [line.strip().replace('\\n', '\n') for line in file]

        k = 0
        while k < 15:
            n = 0
            while n < 5 + random.randint(1, 2):
                test_message = random.choice(messages)

                # ИСПРАВЛЕННЫЙ ВЫЗОВ - параметры в правильном порядке
                await mess_to_chat(
                    message_text=test_message,  # ПЕРВЫЙ параметр
                    client=client,              # ВТОРОЙ параметр
                    chats_id=chats              # ТРЕТИЙ параметр
                )
                n += 1
                await asyncio.sleep(60 + random.randint(1, 3))

            logger.info(f"📊 session: {k + 1}")
            k += 1
            await asyncio.sleep(120)

    except asyncio.CancelledError:
        clear_line()
        logger.info("🛑 Бот остановлен по команде")

    except Exception as e:
        clear_line()
        logger.error(f"❌ Критическая ошибка в функции рассылки: {e}")

