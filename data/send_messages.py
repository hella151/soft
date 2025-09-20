import asyncio
import random
from pyrogram import Client
from pyrogram.errors import FloodWait, RPCError

# Импортируем логгер из единого файла
from data.log import logger

# Импортируем функцию после логгера
from data.functions import mess_to_chat

chats_vz = [-1002029765485]


async def main_bot_function(client: Client):
    """Основная функция работы бота"""
    try:
        with open('text.txt', 'r', encoding='utf-8') as file:
            messages = [line.strip().replace('\\n', '\n') for line in file]


        # Тестовое сообщение для проверки логгера
        k = 0
        while k < 15:
            n = 0
            while n < 5 + random.randint(1, 2):
                try:
                    # Сначала проверим работу логгера
                    test_message = random.choice(messages)

                    await mess_to_chat(
                        chats_id=chats_vz,
                        message_text=test_message,
                        client=client
                    )
                    n += 1
                    logger.info(f"✅ Отправлено сообщение {n}")

                    await asyncio.sleep(60 + random.randint(1, 3))

                except FloodWait as e:
                    wait_time = e.value + 5
                    logger.warning(f"⏳ FloodWait: ждем {wait_time} секунд")
                    await asyncio.sleep(wait_time)
                except RPCError as e:
                    logger.error(f"⚠️ RPCError: {e}")
                    continue
                except Exception as e:
                    logger.error(f"❌ Неожиданная ошибка: {e}")
                    continue

            logger.info(f"📊 session: {k + 1}")
            k += 1
            await asyncio.sleep(120)

    except asyncio.CancelledError:
        logger.info("🛑 Бот остановлен по команде")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка в main: {e}")
        raise

