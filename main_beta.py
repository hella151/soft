import json
import asyncio
import random
import sys
import time
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from data import licensia_check, main_bot_function
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait
from handlers import all_handlers
from data.log import logger, disable_pyrogram_logs
from functions_ import search_chats_raw, is_member
from pyrogram.raw import functions, types


def clear_line():
    """Очистка текущей строки"""
    sys.stdout.write('\r\033[K')
    sys.stdout.flush()

def print_clear(*args, **kwargs):
    """Печать с очисткой строки БЕЗ восстановления приглашения"""
    clear_line()
    print(*args, **kwargs)
    # УБРАТЬ: setup_line() - приглашение выводится только в console_input

def get_session_strings(filename="sessions.json"):
    with open(filename, 'r') as file:
        return [session['session_string'] for session in json.load(file)]


class SessionSwitcher:
    def __init__(self):
        self.clients = {}
        self.current_session = None
        self.start_time = None
        self.is_switching = False
        self.lock = asyncio.Lock()
        self.console_manager = AsyncConsoleManager(self)
        self.bot_tasks = {}
        self.main_loop_task = None

    async def setup_session(self, name, session_string, work_time=300):
        """Создаем и настраиваем сессию"""
        pyro_client = Client(
            name=f"session_{name}",
            api_id="28982778",
            api_hash="54b8ea23241abdef8044090c3c9a2add",
            session_string=session_string
        )

        session_name = name

        # Добавляем хендлер для управления сессиями
        @pyro_client.on_message(filters.private & filters.text)
        async def session_handler(_client, message):
            async with self.lock:
                if (self.is_switching or
                        not self.clients[session_name]['active'] or
                        self.current_session != session_name):
                    return

                print_clear(f"📨 Получена команда: {message.text} в сессии {session_name}")

                if message.text == "/time":
                    remaining = self.get_remaining_time()
                    await message.reply(f"⏰ Осталось: {remaining} сек.")
                elif message.text == "/next":
                    await message.reply("🔜 Переключаемся...")
                    await self.switch_next()
                elif message.text == "/status":
                    await message.reply(f"✅ Активная сессия: {self.current_session}")
                elif message.text == "/list":
                    sessions = "\n".join([f"• {name_}" for name_ in self.clients.keys()])
                    await message.reply(f"📋 Сессии:\n{sessions}")

        # Регистрируем хендлеры бота
        for handler, filter in all_handlers:
            pyro_client.add_handler(MessageHandler(handler, filter))

        self.clients[name] = {
            'client': pyro_client,
            'work_time': work_time,
            'active': False,
            'chats': None,
            'is_running': False
        }

    def get_remaining_time(self):
        if not self.current_session or not self.start_time:
            return 0
        elapsed = time.time() - self.start_time
        remaining = self.clients[self.current_session]['work_time'] - elapsed
        return max(0, int(remaining))

    async def switch_to(self, session_name):
        """Переключаем на указанную сессию"""
        if self.is_switching:
            return

        async with self.lock:
            self.is_switching = True
            print_clear(f"🔄 Переключаем на: {session_name}")

            # Останавливаем бота на текущей сессии
            if self.current_session and self.clients[self.current_session]['is_running']:
                await self.stop_bot_function(self.current_session)

            # Деактивируем все сессии
            for name in self.clients:
                self.clients[name]['active'] = False

            # Активируем новую
            self.current_session = session_name
            self.clients[session_name]['active'] = True
            self.start_time = time.time()

            try:
                current_client = self.clients[session_name]['client']
                me = await current_client.get_me()
                print_clear(f"✅ Активна: {session_name} - {me.first_name}")
                print_clear(f"⏱️ Время: {self.clients[session_name]['work_time']} сек.")
                await current_client.send_message(
                    chat_id='me',
                    text=f'✅ Сессия {session_name} активирована!\nДоступны команды: /time, /next, /status, /list'
                )
                print_clear("-" * 40)
            except Exception as e:
                print_clear(f"❌ Ошибка при активации сессии {session_name}: {e}")
            finally:
                self.is_switching = False

    async def switch_next(self):
        """Переключаем на следующую сессию"""
        if self.is_switching:
            return

        sessions = list(self.clients.keys())
        if not sessions:
            return

        if not self.current_session:
            next_session = sessions[0]
        else:
            try:
                current_index = sessions.index(self.current_session)
                next_index = (current_index + 1) % len(sessions)
                next_session = sessions[next_index]
                print_clear(f"🔀 Следующая сессия: {next_session} (индекс {next_index})")
            except ValueError:
                next_session = sessions[0]

        await asyncio.sleep(2)
        await self.switch_to(next_session)



    async def start_bot_function(self, session_name):
        """Запуск основной функции бота для конкретной сессии"""
        try:
            if not self.clients[session_name]['chats']:
                self.clients[session_name]['chats'] = await self.search_me_channels(session_name, type="mailing")

            # Берем только 5 случайных чатов
            all_chats = self.clients[session_name]['chats']
            if len(all_chats) > 5:
                random_chats = random.sample(all_chats, 5)
                logger.info(f"🎲 Выбрано 5 случайных чатов из {len(all_chats)}")
            else:
                random_chats = all_chats
                logger.info(f"📊 Используются все {len(all_chats)} чатов")

            logger.info(f"🤖 Запуск основной функции бота для {session_name}...")
            self.clients[session_name]['is_running'] = True
            task = asyncio.create_task(
                main_bot_function(self.clients[session_name]['client'], random_chats)
            )
            self.bot_tasks[session_name] = task
            await task
        except asyncio.CancelledError:
            logger.info(f"⏹️ Основная функция бота остановлена для {session_name}")
        except Exception as e:
            logger.error(f"❌ Ошибка в основной функции бота для {session_name}: {e}")
        finally:
            self.clients[session_name]['is_running'] = False

    async def stop_bot_function(self, session_name):
        """Остановка основной функции бота для конкретной сессии"""
        if session_name in self.bot_tasks and not self.bot_tasks[session_name].done():
            self.bot_tasks[session_name].cancel()
            try:
                await self.bot_tasks[session_name]
            except asyncio.CancelledError:
                pass
            logger.info(f"⏹️ Основная функция бота остановлена для {session_name}")
        self.clients[session_name]['is_running'] = False

    async def leave_me_channels(self, session_name):
        """Выход из чатов для конкретной сессии"""
        if not self.clients[session_name]['active']:
            logger.warning("❌ Сессия не активна")
            return

        client = self.clients[session_name]['client']

        # Получаем список чатов для выхода
        if not self.clients[session_name]['chats']:
            self.clients[session_name]['chats'] = await self.search_me_channels(session_name, type="leave")

        if not self.clients[session_name]['chats']:
            logger.warning("❌ Нет чатов для выхода")
            return

        logger.warning("ДОБАВЬТЕ НУЖНЫЕ ЧАТЫ В АРХИВ ЧТОБЫ ИЗ НИХ ВЫХОДИТЬ")
        print_clear('Выйти? [y/n]')
        a = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
        clear_line()

        if a.strip().lower() == 'y':
            for chat_id in self.clients[session_name]['chats']:
                try:
                    # Пытаемся выйти из чата
                    # await client.leave_chat(chat_id)
                    # logger.info(f"✅ Успешно вышли из чата: {chat_id}")
                    # await asyncio.sleep(1)  # Пауза против floodwait
                    print(chat_id)

                except FloodWait as e:
                    logger.warning(f"⏳ FloodWait: ждем {e.value} секунд")
                    await asyncio.sleep(e.value)

                except Exception as ex:
                    logger.error(f"❌ Ошибка выхода из {chat_id}: {ex}")
                    # Продолжаем работу несмотря на ошибку
        else:
            logger.info("❌ Выход отменен")

    async def search_me_channels(self, session_name, type: str):
        """Поиск каналов для сессии"""
        if not self.clients[session_name]['active']:
            logger.warning("❌ Сессия не активна")
            return None

        chats = []
        processed_chats = set()
        client = self.clients[session_name]['client']
        try:
            if type == "mailing":

                logger.info(f"Найденные чаты для рассылки ({session_name}):")

                async for dialog in client.get_dialogs(chat_list=0):
                    chat = dialog.chat
                    if chat.id in processed_chats:
                        break

                    if chat.type == ChatType.SUPERGROUP:
                        try:
                            if str(chat.id).startswith('-100'):
                                chats.append(chat.id)
                                logger.info(chat.title)
                            await asyncio.sleep(1)
                        except Exception as ex:
                            print_clear(f'❌ Ошибка {ex}')
                    processed_chats.add(chat.id)
            elif type == "leave":
                logger.info(f"Найденные чаты для({session_name}):")

                async for dialog in client.get_dialogs(chat_list=0):
                    chat = dialog.chat
                    if chat.id in processed_chats:
                        break

                    if chat.type:
                        try:
                            chats.append(chat.id)
                            logger.info(chat.title)
                            await asyncio.sleep(1)
                        except Exception as ex:
                            print_clear(f'❌ Ошибка {ex}')
                    processed_chats.add(chat.id)


            # await asyncio.sleep(0.5)
            #
            # async for dialog in client.get_dialogs(chat_list=1):
            #     chat = dialog.chat
            #     if chat.id in processed_chats:
            #         break
            #     if chat.type == ChatType.SUPERGROUP:
            #         try:
            #             if str(chat.id).startswith('-100'):
            #                 chats.append(chat.id)
            #                 logger.info(chat.title)
            #             await asyncio.sleep(1)
            #         except Exception as ex:
            #             print_clear(f'❌ Ошибка {ex}')
            #     processed_chats.add(chat.id)

            return chats
        except Exception as e:
            logger.warning(f"Ошибка поиска каналов для {session_name}: {e}")

    async def start_all(self):
        """Запускаем все сессии"""
        print_clear(f"🚀 Запускаем {len(self.clients)} сессий...")

        if len(self.clients) == 0:
            print_clear("добавте хотябы одну сессию")
            raise SystemError

        for name, data in self.clients.items():
            try:
                await data['client'].start()
                data['active'] = False
                me = await data['client'].get_me()
                print_clear(f"✅ {name}: {me.first_name}")
                await asyncio.sleep(1)
            except Exception as e:
                print_clear(f"❌ Ошибка {name}: {e}")

        # Начинаем с первой сессии
        if self.clients:
            first_session = list(self.clients.keys())[0]
            await self.switch_to(first_session)

        # Запускаем главный цикл в отдельной задаче
        self.main_loop_task = asyncio.create_task(self.main_loop())

        # Запускаем консольный менеджер
        await self.console_manager.start()

    async def main_loop(self):
        """Главный цикл переключения"""
        print_clear("🔛 Начинаем циклическое переключение...")

        while True:
            try:
                await asyncio.sleep(1)

                if self.is_switching:
                    continue

                remaining = self.get_remaining_time()

                # Показываем статус каждые 10 секунд для отладки
                # if remaining % 90 == 0:
                #     print_clear(f"⏱️ До переключения: {remaining} сек. (Активна: {self.current_session})")

                if remaining <= 0:
                    print_clear("⏰ Время вышло, переключаемся...")
                    await self.switch_next()

            except KeyboardInterrupt:
                break
            except Exception as e:
                print_clear(f"❌ Ошибка в main_loop: {e}")
                await asyncio.sleep(5)

    async def stop_all(self):
        """Останавливаем все сессии"""
        print_clear("\n⏹️ Останавливаем сессии...")

        # Останавливаем главный цикл
        if self.main_loop_task:
            self.main_loop_task.cancel()
            try:
                await self.main_loop_task
            except asyncio.CancelledError:
                pass

        # Останавливаем все задачи бота
        for session_name in list(self.bot_tasks.keys()):
            await self.stop_bot_function(session_name)

        # Останавливаем все клиенты с обработкой исключений
        for name, data in self.clients.items():
            try:
                # Останавливаем клиент и игнорируем ошибки базы данных
                await data['client'].stop()
                print_clear(f"✅ Остановлена: {name}")
                await asyncio.sleep(0.5)  # Уменьшаем задержку
            except Exception as e:
                # Игнорируем ошибки закрытой базы данных
                if "closed database" not in str(e):
                    print_clear(f"❌ Ошибка остановки {name}: {e}")
                else:
                    print_clear(f"✅ Остановлена: {name} (база закрыта)")


class AsyncConsoleManager:
    def __init__(self, session_switcher):
        self.session_switcher = session_switcher
        self.is_running = False

    async def start(self):
        """Запуск консольного менеджера"""
        self.is_running = True
        print_clear("💬 Консольный менеджер запущен. Введите 'help' для списка команд")
        await self.console_input()

    async def console_input(self):
        """Асинхронный ввод с консоли"""
        while self.is_running:
            try:
                # Ждем ввод
                data = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                if not data:  # EOF
                    break

                data = data.strip()
                if data:
                    clear_line()  # Очищаем строку с вводом
                    await self.process_command(data)

            except (KeyboardInterrupt, EOFError):
                logger.info("Завершение работы...")
                await self.graceful_shutdown()
                break
            except Exception as e:
                logger.error(f"Ошибка ввода: {e}")

    async def process_command(self, command):
        """Обработка команд"""
        if not command:
            return

        cmd = command.split()[0].lower()

        if cmd == 'start_mailing':
            await self.handle_start_mailing()
        elif cmd == 'stop':
            await self.handle_stop()
        elif cmd == 'search':
            await self.handle_search()
        elif cmd == 'me':
            await self.handle_me()
        elif cmd == 'status':
            await self.handle_status()
        elif cmd == 'exit':
            await self.handle_exit()
        elif cmd == 'help':
            await self.handle_help()
        elif cmd == 'next':
            await self.session_switcher.switch_next()
        elif cmd == 'leave_chats':
            await self.session_switcher.leave_me_channels(self.session_switcher.current_session)
        else:
            await self.handle_unknown()

    async def handle_start_mailing(self):
        """Обработка команды start_mailing"""
        if not self.session_switcher.current_session:
            logger.warning("❌ Нет активной сессии")
            return

        session_name = self.session_switcher.current_session
        if self.session_switcher.clients[session_name]['is_running']:
            logger.info("✅ Бот уже запущен")
        else:
            try:
                logger.info("🤖 Основная функция бота запущена")
                asyncio.create_task(self.session_switcher.start_bot_function(session_name))
            except Exception as e:
                logger.warning(f"Ошибка запуска: {e}")

    async def handle_leave(self):
        """Обработка команды stop"""
        if not self.session_switcher.current_session:
            logger.warning("❌ Нет активной сессии")
            return

        session_name = self.session_switcher.current_session
        try:
            await self.session_switcher.leave_me_channels(session_name)
        except Exception as e:
            logger.warning(f"Ошибка остановки: {e}")

    async def handle_stop(self):
        """Обработка команды stop"""
        if not self.session_switcher.current_session:
            logger.warning("❌ Нет активной сессии")
            return

        session_name = self.session_switcher.current_session
        try:
            await self.session_switcher.stop_bot_function(session_name)
            logger.info("🤖 Основная функция бота остановлена")
        except Exception as e:
            logger.warning(f"Ошибка остановки: {e}")

    async def handle_search(self):
        """Обработка команды search"""
        if not self.session_switcher.current_session:
            logger.warning("❌ Нет активной сессии")
            return

        session_name = self.session_switcher.current_session
        client = self.session_switcher.clients[session_name]['client']

        try:
            groups = await search_chats_raw(client, query="Взаимные подписки")
            print_clear('Присоединится? [y/n]')
            a = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            clear_line()

            if a.strip().lower() == 'y':
                for chat in groups:
                    if await is_member(client, chat_id=chat['id']):
                        continue
                    try:
                        await client.join_chat(chat_id=chat['id'])
                        logger.info(f"Зашли в {chat['title']}")
                    except FloodWait as e:
                        logger.warning(
                            f"Подождите {e.value} секунд, перед тем как снова вступать в группы, есть риск получить бан")
                        return
                    except Exception as ex:
                        logger.error(f"Ошибка захода в {chat['title']} {ex}")
                    await asyncio.sleep(5)
        except Exception as e:
            logger.warning(f"Ошибка поиска: {e}")

    async def handle_me(self):
        """Обработка команды me"""
        if not self.session_switcher.current_session:
            logger.warning("❌ Нет активной сессии")
            return

        session_name = self.session_switcher.current_session
        client = self.session_switcher.clients[session_name]['client']
        me = await client.get_me()
        print_clear(f"🤖 ID: {me.id}")
        print_clear(f"📛 Имя: {me.first_name}")
        print_clear(f"🔗 Username: @{me.username}")
        print_clear(f"⭐ Premium: {'Да' if me.is_premium else 'Нет'}")

    async def handle_status(self):
        """Обработка команды status"""
        clear_line()
        if self.session_switcher.current_session:
            session_name = self.session_switcher.current_session
            bot_status = "🟢 Запущен" if self.session_switcher.clients[session_name]['is_running'] else "🔴 Остановлен"
            logger.info(f"📊 Активная сессия: {session_name}")
            logger.info(f"📊 Статус бота: {bot_status}")
            remaining = self.session_switcher.get_remaining_time()
            logger.info(f"⏱️ До переключения: {remaining} сек.")
        else:
            logger.info("📊 Нет активной сессии")

    async def handle_exit(self):
        """Обработка команды exit"""
        await self.graceful_shutdown()

    async def handle_help(self):
        """Обработка команды help"""
        help_text = (
            '🤖 КОМАНДЫ БОТА: \n'
            '🚀 start_mailing - Запустить рассылку на активной сессии\n'
            '⏹️ stop    - Остановить рассылку на активной сессии\n'
            '🚀 search  - Начать поиск каналов для активной сессии\n'
            '🔜 next    - Принудительно переключить сессию\n'
            '📊 status  - Показать статус бота и сессии\n'
            '👤 me      - Информация о активной сессии\n'
            '❓ help    - Показать справку'

        )
        print_clear(help_text)

    async def handle_unknown(self):
        """Обработка неизвестной команды"""
        logger.warning("❌ Неизвестная команда. Введите 'help' для справки")

    async def graceful_shutdown(self):
        """Корректное завершение работы"""
        clear_line()
        logger.info("🛑 Завершение работы...")
        self.is_running = False
        await self.session_switcher.stop_all()
        logger.info("👋 До свидания!")
        sys.exit(0)



async def main():
    disable_pyrogram_logs()
    try:
        session_strings = get_session_strings("sessions.json")
        print_clear(f"📁 Загружено {len(session_strings)} сессий")
    except Exception as e:
        print_clear(f"❌ Ошибка загрузки: {e}")
        return

    if not session_strings:
        print_clear("❌ Нет сессий!")
        return

    switcher = SessionSwitcher()

    for i, session_string in enumerate(session_strings, 1):
        await switcher.setup_session(f"account_{i}", session_string, 90)

    print_clear("💬 Команды: help - показать все команды")
    print_clear("=" * 50)

    try:
        await switcher.start_all()
    except KeyboardInterrupt:
        print_clear("\n🛑 Завершение...")
    finally:
        await switcher.stop_all()
        print_clear("✅ Работа завершена")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Программа завершена по Ctrl+C")