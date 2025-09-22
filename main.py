import asyncio
import sys
import time
from pyrogram.handlers import MessageHandler
from data import licensia_check, main_bot_function
from pyrogram import Client
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait
from handlers import all_handlers
from data.log import logger
from functions_ import search_chats_raw, is_member


def clear_line():
    """Очистка текущей строки"""
    sys.stdout.write('\r\033[K')
    sys.stdout.flush()


class AsyncConsoleManager:
    def __init__(self):
        self.app = Client(api_hash='54b8ea23241abdef8044090c3c9a2add', api_id='28982778',
                          name="hella", skip_updates=True)
        self.is_running = False
        self.bot_task = None

    def setup_handlers(self):
        """Регистрация хендлеров"""
        for handler, filter in all_handlers:
            self.app.add_handler(MessageHandler(handler, filter))

    async def console_input(self):
        """Асинхронный ввод с консоли"""
        while True:
            try:
                await asyncio.sleep(0.1)
                data = await asyncio.get_event_loop().run_in_executor(None, input, "> ")
                clear_line()
                await self.process_command(data.strip())
            except (KeyboardInterrupt, EOFError):
                logger.info("Завершение работы...")
                await self.graceful_shutdown()
            except Exception as e:
                logger.error(f"Ошибка ввода: {e}")

    async def process_command(self, command):
        """Обработка команд через словарь-диспетчер"""
        if not command:
            return

        cmd = command.split()[0].lower()
        command_handlers = {
            'start': lambda: self.handle_start(),
            'start_mailing': lambda: self.handle_start_mailing(),
            'stop': lambda: self.handle_stop(),
            'search': lambda: self.handle_search(),
            'me': lambda: self.handle_me(),
            'status': lambda: self.handle_status(),
            'exit': lambda: self.handle_exit(),
            'help': lambda: self.handle_help()
        }

        handler = command_handlers.get(cmd, lambda: self.handle_unknown())
        await handler()  # Вызываем без аргументов

    async def handle_start(self):
        """Обработка команды start"""

        if self.is_running:
            logger.info("✅ Бот уже запущен")
        else:
            await self.app.start()
            self.setup_handlers()
            self.is_running = True
            logger.info("✅ Клиент запущен")
            self.chats = await self.search_me_channels()

    async def handle_start_mailing(self):
        """Обработка команды start_mailing"""
        if not self.is_running:
            logger.warning("❌ Бот не запущен")
            return

        try:
            self.bot_task = asyncio.create_task(self.start_bot_function())
            logger.info("🤖 Основная функция бота запущена")
        except Exception as e:
            logger.warning(f"Перезапустите программу {e}")

    async def handle_stop(self):
        """Обработка команды stop"""
        if not self.is_running:
            logger.warning("❌ Бот не запущен")
            return

        try:
            await self.stop_bot_function()
            logger.info("🤖 Основная функция бота остановлена")
        except Exception as e:
            logger.warning(f"Перезапустите программу {e}")

    async def search_me_channels(self):
        if not self.is_running:
            logger.warning("❌ Бот не запущен")
            return
        try:
            chats = []
            processed_chats = set()

            logger.info(f"Найденные чаты для рассылки:")
            async for dialog in self.app.get_dialogs(chat_list=0):
                chat = dialog.chat

                if chat.id in processed_chats:
                    break

                if chat.type == ChatType.SUPERGROUP:
                    try:
                        if str(chat.id).startswith('-100'):
                            chats.append(chat.id)
                            logger.info(chat.title)
                        await asyncio.sleep(1)  # Увеличиваем паузу против floodwait

                    except Exception as ex:
                        print(f'❌ Ошибка {ex}')

                processed_chats.add(chat.id)

            await asyncio.sleep(0.5)

            async for dialog in self.app.get_dialogs(chat_list=1):
                chat = dialog.chat

                if chat.id in processed_chats:
                    break

                if chat.type == ChatType.SUPERGROUP:
                    try:
                        if str(chat.id).startswith('-100'):
                            chats.append(chat.id)
                            logger.info(chat.title)
                        await asyncio.sleep(1)  # Увеличиваем паузу против floodwait

                    except Exception as ex:
                        print(f'❌ Ошибка {ex}')

                processed_chats.add(chat.id)

            return chats
        except Exception as e:
            logger.warning(f"Перезапустите программу {e}")

    async def handle_search(self):
        """Обработка команды search"""
        if not self.is_running:
            logger.warning("❌ Бот не запущен")
            return

        try:
            groups = await search_chats_raw(self.app, query="Взаимные подписки")
            print('Присоединится? [y/n]')
            await asyncio.sleep(0.5)
            a = input('> ')
            clear_line()
            
            if a == 'y':
                for chat in groups:
                    if await is_member(self.app, chat_id=chat['id']):
                        continue
                    try:
                        await self.app.join_chat(chat_id=chat['id'])
                        logger.info(f"Зашли в {chat['title']}")
                    except FloodWait as e:
                        logger.warning(
                            f"Подождите {e.value} секунд, перед тем как снова вступать в группы, есть риск получить бан")
                        return
                    except Exception as ex:
                        logger.error(f"Ошибка захода в {chat['title']} {ex}")
                    await asyncio.sleep(5)
        except Exception as e:
            logger.warning(f"Перезапустите программу {e}")

    async def handle_me(self):
        """Обработка команды me"""
        if not self.is_running:
            logger.warning("❌ Сначала запустите бота командой 'start'")
            return

        me = await self.app.get_me()
        print(f"🤖 ID: {me.id}")
        print(f"📛 Имя: {me.first_name}")
        print(f"🔗 Username: @{me.username}")
        print(f"⭐ Premium: {'Да' if me.is_premium else 'Нет'}")

    async def handle_status(self):
        """Обработка команды status"""
        status = "🟢 Запущен" if self.is_running else "🔴 Остановлен"
        logger.info(f"📊 Статус: {status}")

    async def handle_exit(self):
        """Обработка команды exit"""
        if self.is_running:
            await self.app.stop()
            logger.info("⏹️ Клиент остановлен")
            self.is_running = False
        await self.graceful_shutdown()

    async def handle_help(self):
        """Обработка команды help"""
        help_text = (
            '🤖 КОМАНДЫ БОТА: \n'
            '🚀 start   - Запустить клиента\n'
            '⏹️ stop    - Остановить клиента\n'
            '🚀 start_mailing - Запустить рассылку\n'
            '🚀 search  - Начать поиск каналов\n'
            '📊 status  - Показать статус бота\n'
            '👤 me      - Информация о боте\n'
            '❓ help    - Показать справку'
        )
        print(help_text)

    async def handle_unknown(self):
        """Обработка неизвестной команды"""
        logger.warning("❌ Неизвестная команда. Введите 'help' для справки")

    async def graceful_shutdown(self):
        """Корректное завершение работы"""
        clear_line()
        logger.info("🛑 Завершение работы...")

        if self.is_running:
            try:
                await self.app.stop()
                self.is_running = False
                logger.info("✅ Клиент корректно остановлен")
            except Exception as e:
                logger.error(f"❌ Ошибка при остановке клиента: {e}")

        logger.info("👋 До свидания!")
        time.sleep(1)
        sys.exit(0)


    async def start_bot_function(self):
        """Запуск основной функции бота"""
        try:
            logger.info("🤖 Запуск основной функции бота...")
            await main_bot_function(self.app, self.chats)
        except asyncio.CancelledError:
            logger.info("⏹️ Основная функция бота остановлена")
        except Exception as e:
            logger.error(f"❌ Ошибка в основной функции бота: {e}")

        finally:
            self.is_running = False

    async def stop_bot_function(self):
        """Остановка основной функции бота"""
        if self.bot_task and not self.bot_task.done():
            self.bot_task.cancel()
            try:
                await self.bot_task
            except asyncio.CancelledError:
                pass
            logger.info("⏹️ Основная функция бота остановлена")
        self.is_running = False


async def main():
    console = AsyncConsoleManager()
    logger.info("🚀 Pyrogram Console Manager запущен!")
    logger.info("📝 Введите 'help' для просмотра команд")

    try:
        await console.console_input()
    except asyncio.CancelledError:
        clear_line()
        logger.info("Задачи отменены")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
    finally:
        if console.is_running:
            await console.app.stop()
            logger.info("✅ Клиент остановлен")


if __name__ == "__main__":
    try:
        # check = licensia_check()

        asyncio.run(main())
        # else:
            # logger.error(check)
    except KeyboardInterrupt:
        logger.info("👋 Программа завершена по Ctrl+C")