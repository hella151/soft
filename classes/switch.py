from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from cache import TelegramCache
from data import main_bot_function
from pyrogram.enums import ChatType
from . import AsyncConsoleManager
from settings import Settings
from pyrogram.raw import functions, types
from pyrogram.errors import FloodWait, RPCError
from handlers import all_handlers
from data.log import logger
import asyncio
import random
import sys
import time


def clear_line():
    """Очистка текущей строки"""
    sys.stdout.write('\r\033[K')
    sys.stdout.flush()


def print_clear(*args, **kwargs):
    """Печать с очисткой строки БЕЗ восстановления приглашения"""
    clear_line()
    print(*args, **kwargs)


class SessionSwitcher:
    def __init__(self):
        self.clients = {}
        self.current_session = None
        self.start_time = None
        self.is_switching = False
        self.lock = asyncio.Lock()
        self.console_manager = AsyncConsoleManager(self)
        self.cache_manager = TelegramCache()
        self.bot_tasks = {}
        self.main_loop_task = None
        self.is_running = True  # Главный флаг работы
        self._is_stopping = False  # Флаг защиты от повторной остановки
        # Новые флаги для блокировки переключения
        self.block_switching_sessions = set()  # Сессии, которые блокируют переключение
        self.block_switching_operations = {}  # Информация о блокирующих операциях
        self.settings = Settings()
        self.settings.load_config()  # Загружаем конфигурацию
        self.config = self.settings.config

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
            if not self.is_running or self.is_switching:
                return

            async with self.lock:
                if (not self.clients[session_name]['active'] or
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
                    status_info = await self.get_session_status()
                    await message.reply(status_info)
                elif message.text == "/list":
                    sessions = "\n".join([f"• {name_}" for name_ in self.clients.keys()])
                    await message.reply(f"📋 Сессии:\n{sessions}")

        # Регистрируем хендлеры бота
        for handler, filter_ in all_handlers:
            pyro_client.add_handler(MessageHandler(handler, filter_))

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
        if self.is_switching or not self.is_running:
            return False

        # Проверяем, не заблокирована ли текущая сессия для переключения
        if session_name in self.block_switching_sessions:
            logger.warning(f"⏳ Сессия {session_name} заблокирована для переключения (выполняется операция)")
            return False

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
                    text=f'✅ Сессия {session_name} активирована!\nДоступны команды: /time, /next, /status, /list, /force_stop, /force_switch'
                )
                print_clear("-" * 40)

                # ⛔️ УБРАН автоматический запуск бота!
                # Теперь бот запускается только вручную через команды

                self.is_switching = False
                return True

            except Exception as e:
                print_clear(f"❌ Ошибка при активации сессии {session_name}: {e}")
                self.is_switching = False
                return False

    async def switch_next(self):
        """Переключаем на следующую сессию"""
        if self.is_switching or not self.is_running:
            return False

        sessions = list(self.clients.keys())
        if not sessions:
            return False

        # Ищем следующую незаблокированную сессию
        next_session = None
        attempts = 0

        while attempts < len(sessions):
            if not self.current_session:
                next_session = sessions[0]
            else:
                try:
                    current_index = sessions.index(self.current_session)
                    next_index = (current_index + 1) % len(sessions)
                    next_session = sessions[next_index]
                except ValueError:
                    next_session = sessions[0]

            # Проверяем, не заблокирована ли сессия
            if next_session not in self.block_switching_sessions:
                break

            logger.warning(f"⏳ Сессия {next_session} заблокирована, пробуем следующую...")
            # Если сессия заблокирована, временно убираем ее из списка для этой итерации
            sessions.remove(next_session)
            attempts += 1

        if next_session is None:
            logger.error("❌ Все сессии заблокированы, переключение невозможно")
            return False

        print_clear(f"🔀 Следующая сессия: {next_session}")
        await asyncio.sleep(2)
        return await self.switch_to(next_session)

    # Новые методы для управления блокировкой переключения
    async def block_session_switching(self, session_name, operation_type="unknown"):
        """Блокирует переключение сессии"""
        self.block_switching_sessions.add(session_name)
        self.block_switching_operations[session_name] = {
            'type': operation_type,
            'start_time': time.time(),
            'session': session_name
        }
        logger.info(f"🔒 Блокировка переключения для {session_name} (операция: {operation_type})")

    async def unblock_session_switching(self, session_name):
        """Разблокирует переключение сессии"""
        if session_name in self.block_switching_sessions:
            self.block_switching_sessions.remove(session_name)
            if session_name in self.block_switching_operations:
                operation_info = self.block_switching_operations.pop(session_name)
                duration = time.time() - operation_info['start_time']
                logger.info(f"🔓 Разблокировка переключения для {session_name} (операция длилась: {duration:.1f} сек.)")

    def is_session_blocked(self, session_name):
        """Проверяет, заблокирована ли сессия для переключения"""
        return session_name in self.block_switching_sessions

    async def get_session_status(self):
        """Возвращает статус сессии с информацией о блокировках"""
        if not self.current_session:
            return "❌ Нет активной сессии"

        status_lines = [f"✅ Активная сессия: {self.current_session}"]

        # Время работы
        remaining = self.get_remaining_time()
        status_lines.append(f"⏰ Осталось времени: {remaining} сек.")

        # Статус бота
        bot_status = "запущен" if self.clients[self.current_session]['is_running'] else "остановлен"
        status_lines.append(f"🤖 Бот: {bot_status}")

        # Статус блокировки
        if self.is_session_blocked(self.current_session):
            operation_info = self.block_switching_operations.get(self.current_session, {})
            op_type = operation_info.get('type', 'unknown')
            duration = time.time() - operation_info.get('start_time', time.time())
            status_lines.append(f"🔒 Заблокирована (операция: {op_type}, длится: {duration:.1f} сек.)")
        else:
            status_lines.append("🔓 Готова к переключению")

        return "\n".join(status_lines)

    async def start_bot_function(self, session_name):
        """Запуск основной функции бота для конкретной сессии"""
        if not self.is_running:
            return

        try:
            if not self.clients[session_name]['chats']:
                # Теперь получаем полные данные чатов (с id и title)
                self.clients[session_name]['chats'] = await self.search_me_channels(session_name, type="mailing")

            all_chats = self.clients[session_name]['chats']
            if len(all_chats) > 5:
                random_chats = random.sample(all_chats, 5)
                logger.info(f"🎲 Выбрано 5 случайных чатов из {len(all_chats)}")
            else:
                random_chats = all_chats
                logger.info(f"📊 Используются все {len(all_chats)} чатов")

            logger.info(f"🤖 Запуск основной функции бота для {session_name}...")
            self.clients[session_name]['is_running'] = True

            # Создаем задачу с проверкой флага
            async def bot_task_wrapper():
                while self.is_running and self.clients[session_name]['is_running']:
                    try:
                        # Передаем cache_manager и session_name в функцию
                        await main_bot_function(
                            self.clients[session_name]['client'],
                            random_chats,  # Теперь передаем полные данные чатов
                            cache_manager=self.cache_manager,
                            session_name=session_name,
                            settings=self.config
                        )
                        await asyncio.sleep(1)
                    except asyncio.CancelledError:
                        logger.info(f"⏹️ Задача бота отменена для {session_name}")
                        break
                    except Exception as e:
                        logger.error(f"❌ Ошибка в основной функции бота для {session_name}: {e}")
                        await asyncio.sleep(5)

            task = asyncio.create_task(bot_task_wrapper())
            self.bot_tasks[session_name] = task

        except asyncio.CancelledError:
            logger.info(f"⏹️ Основная функция бота остановлена для {session_name}")
        except Exception as e:
            logger.error(f"❌ Ошибка в основной функции бота для {session_name}: {e}")
            self.clients[session_name]['is_running'] = False

    async def stop_bot_function(self, session_name):
        """Остановка основной функции бота для конкретной сессии"""
        self.clients[session_name]['is_running'] = False

        if session_name in self.bot_tasks:
            task = self.bot_tasks[session_name]
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            del self.bot_tasks[session_name]
            logger.info(f"⏹️ Основная функция бота остановлена для {session_name}")

    @staticmethod
    def handle_rcp():
        def decorator(func):
            async def wrapper(*args, **kwargs):
                for attempt in range(3):
                    try:
                        return await func(*args, **kwargs)
                    except RPCError as rpc_error:
                        logger.error(f"⚠️ RPCError:  {rpc_error} (попытка {attempt + 1}/{3}) ждём пару секунд")
                        await asyncio.sleep(2)
                    except FloodWait as e:
                        wait_time = e.value
                        logger.error(f"⚠️ FloodWait: Ждем {wait_time} секунд (попытка {attempt + 1}/{3})")
                        await asyncio.sleep(wait_time)
                    except Exception as e:
                        logger.error(f"❌ Другая ошибка: {e}")
                        break
                return None
            return wrapper
        return decorator

    @handle_rcp()
    async def leave_me_channels(self, session_name):
        """Выход из чатов для конкретной сессии"""
        global chat_title
        if not self.clients[session_name]['active'] or not self.is_running:
            logger.warning("❌ Сессия не активна")
            return

        # Блокируем переключение на время операции выхода
        await self.block_session_switching(session_name, "leave_channels")
        try:
            client = self.clients[session_name]['client']

            # Получаем список чатов для выхода
            if not self.clients[session_name]['chats']:
                self.clients[session_name]['chats'] = await self.search_me_channels(session_name, type="leave")

            if not self.clients[session_name]['chats']:
                logger.warning("❌ Нет чатов для выхода")
                return

            logger.warning("ДОБАВЬТЕ НУЖНЫЕ ЧАТЫ В АРХИВ ЧТОБЫ ИЗ НИХ НЕ ВЫХОДИТЬ")

            await asyncio.sleep(1)
            print_clear('Выйти? [y/n]')
            a = await asyncio.get_event_loop().run_in_executor(executor=None, func=sys.stdin.readline)
            clear_line()

            if a.strip().lower() == 'y':
                for chat_id in self.clients[session_name]['chats']:
                    try:
                        chat_title = self.cache_manager.get_chat_title(session_name, "leave", chat_id)
                        if str(chat_id).startswith('-100'):
                            await client.leave_chat(chat_id)
                            logger.info(f"✅ Успешно вышли из: {chat_title}")
                        else:
                            await client.invoke(
                                functions.messages.DeleteHistory(peer=await client.resolve_peer(chat_id), max_id=0,
                                                                 revoke=True))
                            logger.info(f"✅ Успешно удалили чат: {chat_title}")
                        await asyncio.sleep(3)

                    except Exception as ex:
                        logger.error(f"❌ Ошибка выхода из {chat_title, chat_id}: {ex}")
                        continue
                self.cache_manager.clear_cache(session_name=session_name, cache_type="leave")
                self.cache_manager.clear_cache(session_name=session_name, cache_type="mailing")
            else:
                logger.info("❌ Выход отменен")
        finally:
            await self.unblock_session_switching(session_name)

    # В методе search_me_channels замените:
    async def search_me_channels(self, session_name, type: str):
        """Поиск каналов для сессии"""
        if not self.clients[session_name]['active'] or not self.is_running:
            logger.warning("❌ Сессия не активна")
            return None

        # Блокируем переключение на время поиска
        await self.block_session_switching(session_name, f"search_{type}")
        try:
            cached_chats = self.cache_manager.load_chats(session_name=session_name, cache_type=type)
            if cached_chats is None:
                chats = []
                processed_chats = set()
                client = self.clients[session_name]['client']
                try:
                    if type == "mailing":
                        logger.info(f"Найденные чаты для рассылки ({session_name}):")

                        async for dialog in client.get_dialogs(chat_list=0):
                            if not self.is_running:
                                break
                            chat = dialog.chat
                            if chat.id in processed_chats:
                                break

                            if chat.type == ChatType.SUPERGROUP:
                                try:
                                    if str(chat.id).startswith('-100'):
                                        # Сохраняем как объект с id и title
                                        chats.append({
                                            'id': chat.id,
                                            'title': chat.title
                                        })
                                        logger.info(chat.title)
                                    await asyncio.sleep(1)
                                except Exception as ex:
                                    print_clear(f'❌ Ошибка {ex}')
                            processed_chats.add(chat.id)

                    elif type == "leave":
                        logger.info(f"Найденные чаты для({session_name}):")

                        async for dialog in client.get_dialogs(chat_list=0):
                            if not self.is_running:
                                break
                            chat = dialog.chat
                            if chat.id in processed_chats:
                                break

                            if chat.type:
                                try:
                                    # Сохраняем как объект с id и title
                                    chat_data = {'id': chat.id}
                                    if chat.title:
                                        chat_data['title'] = chat.title
                                        logger.info(chat.title)
                                    else:
                                        chat_data['title'] = chat.first_name
                                        logger.info(chat.first_name)
                                    chats.append(chat_data)
                                    await asyncio.sleep(1)
                                except Exception as ex:
                                    print_clear(f'❌ Ошибка {ex}')
                            processed_chats.add(chat.id)

                    self.cache_manager.save_chats(session_name=session_name, cache_type=type, chats=chats)
                    # ВОЗВРАЩАЕМ ПОЛНЫЕ ДАННЫЕ, А НЕ ТОЛЬКО ID
                    return chats
                except Exception as e:
                    logger.warning(f"Ошибка поиска каналов для {session_name}: {e}")
                    return []
            else:
                # cached_chats теперь словарь {id: title}, преобразуем в список словарей
                chat_list = [{'id': chat_id, 'title': title} for chat_id, title in cached_chats.items()]
                for chat_id, title in cached_chats.items():
                    print(f"{chat_id}: {title}")
                return chat_list
        finally:
            await self.unblock_session_switching(session_name)

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
        """Главный цикл переключения с проверкой блокировок"""
        print_clear("🔛 Начинаем циклическое переключение...")

        while self.is_running:
            try:
                await asyncio.sleep(1)

                if self.is_switching or not self.is_running:
                    continue

                # Проверяем, не заблокирована ли текущая сессия
                if self.current_session and self.is_session_blocked(self.current_session):
                    operation_info = self.block_switching_operations.get(self.current_session, {})
                    op_type = operation_info.get('type', 'unknown')
                    duration = time.time() - operation_info.get('start_time', time.time())
                    # Выводим сообщение только раз в 30 секунд, чтобы не засорять лог
                    if int(duration) % 30 == 0:
                        logger.info(
                            f"⏳ Ожидание завершения операции '{op_type}' в сессии {self.current_session} ({duration:.1f} сек.)")
                    continue

                remaining = self.get_remaining_time()

                if remaining <= 0:
                    print_clear("⏰ Время вышло, переключаемся...")
                    await self.switch_next()

            except KeyboardInterrupt:
                await self.stop_all()
                break
            except Exception as e:
                print_clear(f"❌ Ошибка в main_loop: {e}")
                await asyncio.sleep(5)

    async def stop_all(self):
        """Останавливаем все сессии с защитой от повторного вызова"""
        if self._is_stopping:
            return

        self._is_stopping = True
        self.is_running = False

        print_clear("\n⏹️ Останавливаем сессии...")

        # Останавливаем консольный менеджер
        if hasattr(self.console_manager, 'is_running'):
            self.console_manager.is_running = False

        # Останавливаем все задачи бота
        for session_name in list(self.bot_tasks.keys()):
            await self.stop_bot_function(session_name)
            await asyncio.sleep(0.5)

        # Останавливаем главный цикл
        if self.main_loop_task and not self.main_loop_task.done():
            self.main_loop_task.cancel()
            try:
                await self.main_loop_task
            except asyncio.CancelledError:
                pass

        # Даем время для завершения операций
        await asyncio.sleep(2)

        # Останавливаем все клиенты с обработкой исключений
        for name, data in self.clients.items():
            try:
                if hasattr(data['client'], 'is_connected') and data['client'].is_connected:
                    await data['client'].stop()
                    print_clear(f"✅ Остановлена: {name}")
                else:
                    print_clear(f"✅ Сессия уже остановлена: {name}")
            except Exception as e:
                if "closed database" not in str(e) and "already terminated" not in str(e):
                    print_clear(f"❌ Ошибка остановки {name}: {e}")
                else:
                    print_clear(f"✅ Остановлена: {name}")

    async def get_cache_info(self):
        cache_info = self.cache_manager.get_cache_info(session_name=self.current_session)

        if not cache_info:
            logger.info("📁 Кэш-файлы не найдены")
            return

        logger.info(f"📊 Информация о кэше ({len(cache_info)} файлов):")
        for cache_file in cache_info:
            status = "🟢 Свежий" if cache_file['age_minutes'] < 60 else "🟡 Старый"
            logger.info(f"  📄 {cache_file['file']}")
            logger.info(f"    Сессия: {cache_file['session']}, Тип: {cache_file['type']}")
            logger.info(f"    Чатов: {cache_file['chats_count']}, Возраст: {cache_file['age_minutes']} мин. {status}")