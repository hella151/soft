from pyrogram import Client, filters, enums
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
        self.selected_chats = {}
        self.invalid_chats = {}
        self.main_loop_task = None
        self.is_running = True  # Главный флаг работы
        self._is_stopping = False  # Флаг защиты от повторной остановки
        # Новые флаги для блокировки переключения
        self.block_switching_sessions = set()  # Сессии, которые блокируют переключение
        self.block_switching_operations = {}  # Информация о блокирующих операциях
        self.settings = Settings()
        self.settings.load_config()  # Загружаем конфигурацию
        self.config = self.settings.config
        self.continuous_mailing = False  # Флаг непрерывной рассылки
        self.continuous_mailing_duration = 3600  # Длительность непрерывной работы (по умолчанию 1 час)
        self.continuous_start_time = None

        self.single_continuous = {
            'active': False,
            'duration': 3600,
            'start_time': None,
            'session': None
        }

    async def setup_session(self, name, session_string, work_time=300):
        """Создаем и настраиваем сессию"""
        pyro_client = Client(
            name=f"session_{name}",
            api_id="28982778",
            api_hash="54b8ea23241abdef8044090c3c9a2add",
            session_string=session_string
        )

        session_name = name
        user_chats = []
        # Добавляем хендлер для управления сессиями
        @pyro_client.on_message(filters.private & filters.text)
        async def session_handler(_client, message):
            if not self.is_running or self.is_switching:
                return

            async with self.lock:
                if (not self.clients[session_name]['active'] or
                        self.current_session != session_name):
                    return

                print_clear(f"📨 Получено сообщение: {message.text} в сессии {session_name}")

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

                url = "https://t.me/vzz_piar_vzz"

                if message.chat.id not in user_chats:
                    try:
                        user_chats.append(message.chat.id)

                        await asyncio.sleep(1)
                        await pyro_client.send_chat_action(chat_id=message.chat.id, action=enums.ChatAction.TYPING,
                                                      progress=0)
                        await asyncio.sleep(1)
                        await pyro_client.send_message(chat_id=message.chat.id, text=f'Привет')
                        await asyncio.sleep(1)
                        await pyro_client.send_message(chat_id=message.chat.id, text=f'{url}')


                    except Exception as ex:
                        print(ex)

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

        # БЛОКИРОВКА ПЕРЕКЛЮЧЕНИЯ ПРИ НЕПРЕРЫВНОЙ РАССЫЛКЕ ДЛЯ ОДНОЙ СЕССИИ
        if (self.single_continuous['active'] and
                self.single_continuous['session'] != session_name):
            logger.warning(
                f"⏳ Переключение заблокировано: активна непрерывная рассылка для {self.single_continuous['session']}")
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

                print_clear("-" * 40)
                print_clear(f"✅ Активна: {session_name}")
                print_clear(f"⏱️ Время: {self.clients[session_name]['work_time']} сек.")

                print_clear("-" * 40)

                # 🔄 АВТОМАТИЧЕСКИ ЗАПУСКАЕМ РАССЫЛКУ ПРИ НЕПРЕРЫВНОМ РЕЖИМЕ
                if self.continuous_mailing and not self.clients[session_name]['is_running']:
                    logger.info(f"🤖 Автозапуск рассылки для {session_name} (непрерывный режим)")
                    await self.start_bot_function(session_name)



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

        # БЛОКИРОВКА ПРИ НЕПРЕРЫВНОЙ РАССЫЛКЕ ДЛЯ ОДНОЙ СЕССИИ
        if self.single_continuous['active']:
            logger.warning(
                f"⏳ Переключение заблокировано: активна непрерывная рассылка для {self.single_continuous['session']}")
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
            # Получаем сохраненные чаты ДЛЯ ЭТОЙ СЕССИИ
            selected_chats = await self.get_or_select_chats(session_name)

            if not selected_chats:
                logger.error(f"❌ Нет доступных чатов для рассылки в сессии {session_name}, добавьте чаты")
                return

            logger.info(f"🤖 Запуск основной функции бота для {session_name}...")

            self.clients[session_name]['is_running'] = True

            await asyncio.sleep(1)
            # Создаем задачу с проверкой флага
            async def bot_task_wrapper():
                while self.is_running and self.clients[session_name]['is_running']:
                    try:
                        # Передаем cache_manager и session_name в функцию
                        await main_bot_function(
                            self.clients[session_name]['client'],
                            selected_chats,  # Используем сохраненные чаты ДЛЯ ЭТОЙ СЕССИИ
                            cache_manager=self.cache_manager,
                            session_name=session_name,
                            settings=self.config,
                            session_switcher=self
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

        if (self.single_continuous['active'] and
                self.single_continuous['session'] == session_name):
            await self.stop_continuous_mailing_single()

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
        global chat_title, chat_id
        if not self.clients[session_name]['active'] or not self.is_running:
            logger.warning("❌ Сессия не активна")
            return

        # Блокируем переключение на время операции выхода

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
                await self.block_session_switching(session_name, "leave_channels")
                for chat_data in self.clients[session_name]['chats']:  # Итерируем по словарям
                    try:
                        chat_id = chat_data['id']  # Извлекаем числовой ID
                        chat_title = chat_data.get('title', 'Без названия')

                        if str(chat_id).startswith('-100'):
                            await client.leave_chat(chat_id)  # Теперь передаем число, а не словарь
                            logger.info(f"✅ Успешно вышли из: {chat_title}")
                        else:
                            await client.invoke(
                                functions.messages.DeleteHistory(peer=await client.resolve_peer(chat_id), max_id=0,
                                                                 revoke=True))
                            logger.info(f"✅ Успешно удалили чат: {chat_title}")
                        await asyncio.sleep(3)

                    except Exception as ex:
                        logger.error(f"❌ Ошибка выхода из {chat_title} ({chat_id}): {ex}")
                        continue
                self.cache_manager.clear_cache(session_name=session_name, cache_type="leave")
                self.cache_manager.clear_cache(session_name=session_name, cache_type="mailing")
            else:
                logger.info("❌ Выход отменен")
        finally:
            await self.unblock_session_switching(session_name)


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
                # for chat_id, title in cached_chats.items():
                #     print(f"{chat_id}: {title}")
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
                # me = await data['client'].get_me()
                print_clear(f"✅ {name}")
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

                # ПРОВЕРКА НЕПРЕРЫВНОЙ РАССЫЛКИ ДЛЯ ОДНОЙ СЕССИИ - БЛОКИРОВКА ПЕРЕКЛЮЧЕНИЯ
                if self.single_continuous['active']:
                    # Проверяем время непрерывной рассылки
                    if not await self.check_single_continuous_time():
                        continue
                    # Если непрерывная рассылка активна - пропускаем переключение
                    continue

                # Проверяем, не заблокирована ли текущая сессия
                if self.current_session and self.is_session_blocked(self.current_session):
                    operation_info = self.block_switching_operations.get(self.current_session, {})
                    op_type = operation_info.get('type', 'unknown')
                    duration = time.time() - operation_info.get('start_time', time.time())
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

    async def get_or_select_chats(self, session_name, force_reload=False):
        """Получает или выбирает чаты для рассылки для конкретной сессии"""
        # Если уже есть выбранные чаты для этой сессии и не требуется перезагрузка - возвращаем их
        if session_name in self.selected_chats and not force_reload and self.selected_chats[session_name]:
            logger.info(f"📁 Используются сохраненные чаты для {session_name}")
            for i, chat in enumerate(self.selected_chats[session_name], 1):
                logger.info(f"  {i}. {chat.get('title', 'Без названия')} (ID: {chat['id']})")

            return self.selected_chats[session_name]

        # Получаем все доступные чаты ДЛЯ ЭТОЙ СЕССИИ
        all_chats = await self.search_me_channels(session_name, type="mailing")
        if not all_chats:
            logger.warning(f"❌ Нет доступных чатов для сессии {session_name}")
            return []

        # Выбираем чаты для этой сессии (первые 3 или все, если меньше)
        if len(all_chats) > 3:
            random_chats = random.sample(all_chats, 3)
            selected_chats = random_chats  # Берем первые 3 вместо случайных
            logger.info(f"🎲 Выбрано 3 случайных чатов из {len(all_chats)} Для {session_name}")
        else:
            selected_chats = all_chats
            logger.info(f"📋 Для {session_name} используются все {len(all_chats)} чатов")

        # Сохраняем выбранные чаты ДЛЯ ЭТОЙ СЕССИИ
        self.selected_chats[session_name] = selected_chats

        # Логируем выбранные чаты для этой сессии
        logger.info(f"🎯 Выбранные чаты для {session_name}:")
        for i, chat in enumerate(selected_chats, 1):
            logger.info(f"  {i}. {chat.get('title', 'Без названия')} (ID: {chat['id']})")

        return selected_chats

    async def reload_chats(self, session_name):
        """Перезагружает выбранные чаты для конкретной сессии"""
        if session_name in self.selected_chats:
            del self.selected_chats[session_name]
            logger.info(f"🔄 Перезагружаем список чатов для {session_name}")
        return await self.get_or_select_chats(session_name, force_reload=True)

    async def show_current_chats(self, session_name):
        """Показывает выбранные чаты для конкретной сессии"""
        if session_name in self.selected_chats and self.selected_chats[session_name]:
            chats = self.selected_chats[session_name]
            logger.info(f"🎯 Текущие чаты для {session_name} ({len(chats)}):")
            for i, chat in enumerate(chats, 1):
                logger.info(f"  {i}. {chat.get('title', 'Без названия')} (ID: {chat['id']})")
            return True
        else:
            logger.info(f"📭 Нет выбранных чатов для {session_name}. Запустите рассылку для их выбора.")
            return False

    async def replace_invalid_chat(self, session_name, invalid_chat_id):
        """Заменяет невалидный чат на случайный из доступных и удаляет из кэша"""
        if session_name not in self.invalid_chats:
            self.invalid_chats[session_name] = set()

        # Добавляем чат в список невалидных
        self.invalid_chats[session_name].add(invalid_chat_id)

        # УДАЛЯЕМ ЧАТ ИЗ КЭША
        removed_from_cache = self.cache_manager.remove_chat_from_cache(
            session_name, "mailing", invalid_chat_id
        )
        if removed_from_cache:
            logger.info(f"🗑 Чат удален из кэша рассылки")

        # Получаем все доступные чаты
        all_chats = await self.search_me_channels(session_name, type="mailing")
        if not all_chats:
            logger.warning(f"❌ Нет доступных чатов для замены в сессии {session_name}")
            return None

        # Фильтруем уже используемые и невалидные чаты
        current_chats = self.selected_chats.get(session_name, [])
        current_chat_ids = {chat['id'] for chat in current_chats}
        invalid_chat_ids = self.invalid_chats.get(session_name, set())

        available_chats = [
            chat for chat in all_chats
            if (chat['id'] not in current_chat_ids and
                chat['id'] not in invalid_chat_ids)
        ]

        if not available_chats:
            logger.warning(f"❌ Нет доступных чатов для замены в сессии {session_name}")
            return None

        # Выбираем случайный чат из доступных
        replacement_chat = random.choice(available_chats)
        logger.info(f"🔄 Заменяем недоступный чат на: {replacement_chat.get('title', 'Без названия')}")

        return replacement_chat

    async def cleanup_invalid_chats(self, session_name):
        """Очищает все невалидные чаты из кэша"""
        if session_name not in self.invalid_chats or not self.invalid_chats[session_name]:
            return 0

        invalid_chat_ids = list(self.invalid_chats[session_name])
        removed_count = self.cache_manager.remove_chats_from_cache(
            session_name, "mailing", invalid_chat_ids
        )

        if removed_count > 0:
            logger.info(f"🗑 Очищено {removed_count} невалидных чатов из кэша")
            self.invalid_chats[session_name].clear()

        return removed_count

    async def update_selected_chats(self, session_name, invalid_chat_id, replacement_chat):
        """Обновляет список выбранных чатов"""
        if session_name not in self.selected_chats or not self.selected_chats[session_name]:
            return False

        # Находим и заменяем невалидный чат
        for i, chat in enumerate(self.selected_chats[session_name]):
            if chat['id'] == invalid_chat_id:
                self.selected_chats[session_name][i] = replacement_chat
                logger.info(f"✅ Обновлен список чатов для {session_name}")
                return True

        return False

    async def start_continuous_mailing(self, duration_minutes=60):
        """Запуск непрерывной рассылки на указанное время"""
        if not self.is_running:
            logger.warning("❌ Система не запущена")
            return False

        self.continuous_mailing = True
        self.continuous_mailing_duration = duration_minutes * 60  # Конвертируем в секунды
        self.continuous_start_time = time.time()

        logger.info(f"🔁 Запуск непрерывной рассылки на {duration_minutes} минут")

        # Автоматически запускаем рассылку на текущей сессии
        if self.current_session and not self.clients[self.current_session]['is_running']:
            await self.start_bot_function(self.current_session)

        return True

    async def stop_continuous_mailing(self):
        """Остановка непрерывной рассылки"""
        if not self.continuous_mailing:
            logger.info("❌ Непрерывная рассылка не активна")
            return False

        self.continuous_mailing = False
        logger.info("⏹️ Остановка непрерывной рассылки")

        # Останавливаем рассылку на текущей сессии
        if self.current_session and self.clients[self.current_session]['is_running']:
            await self.stop_bot_function(self.current_session)

        return True

    async def check_continuous_mailing_time(self):
        """Проверяем, не истекло ли время непрерывной рассылки"""
        if not self.continuous_mailing or not self.continuous_start_time:
            return True

        elapsed = time.time() - self.continuous_start_time
        remaining = self.continuous_mailing_duration - elapsed

        if remaining <= 0:
            logger.info("⏰ Время непрерывной рассылки истекло")
            await self.stop_continuous_mailing()
            return False

        # Логируем оставшееся время каждые 5 минут
        if int(elapsed) % 300 == 0:  # Каждые 5 минут
            minutes_left = int(remaining // 60)
            logger.info(f"⏱️ До окончания непрерывной рассылки: {minutes_left} минут")

        return True

    async def del_cache(self):
        self.cache_manager.clear_cache(session_name=self.current_session, cache_type="mailing")

    async def start_continuous_mailing_single(self, duration_minutes=60):
        """Запуск непрерывной рассылки для одной сессии"""
        if not self.is_running or not self.current_session:
            logger.warning("❌ Нет активной сессии")
            return False

        if self.single_continuous['active']:
            logger.warning(f"⚠️ Непрерывная рассылка уже запущена для {self.single_continuous['session']}")
            return False

        self.single_continuous.update({
            'active': True,
            'duration': duration_minutes * 60,
            'start_time': time.time(),
            'session': self.current_session
        })

        logger.info(f"🔁 Запуск непрерывной рассылки для {self.current_session} на {duration_minutes} минут")

        # Автоматически запускаем рассылку если она не запущена
        if not self.clients[self.current_session]['is_running']:
            await self.start_bot_function(self.current_session)

        return True

    async def stop_continuous_mailing_single(self):
        """Остановка непрерывной рассылки для одной сессии"""
        if not self.single_continuous['active']:
            logger.info("❌ Непрерывная рассылка не активна")
            return False

        session_name = self.single_continuous['session']
        self.single_continuous['active'] = False

        logger.info(f"⏹️ Остановка непрерывной рассылки для {session_name}")

        # Останавливаем рассылку если сессия все еще активна
        if session_name and self.clients[session_name]['is_running']:
            await self.stop_bot_function(session_name)

        self.single_continuous['session'] = None
        return True

    async def check_single_continuous_time(self):
        """Проверяем время непрерывной рассылки для одной сессии"""
        if not self.single_continuous['active']:
            return True

        elapsed = time.time() - self.single_continuous['start_time']
        remaining = self.single_continuous['duration'] - elapsed

        if remaining <= 0:
            logger.info("⏰ Время непрерывной рассылки истекло")
            await self.stop_continuous_mailing_single()
            return False

        # Логируем оставшееся время каждые 5 минут
        if int(elapsed) % 300 == 0:
            minutes_left = int(remaining // 60)
            logger.info(f"⏱️ До окончания непрерывной рассылки: {minutes_left} минут")

        return True

    async def get_continuous_mailing_status_single(self):
        """Получение статуса непрерывной рассылки для одной сессии"""
        if not self.single_continuous['active']:
            return "🔁 Непрерывная рассылка не активна"

        elapsed = time.time() - self.single_continuous['start_time']
        remaining = self.single_continuous['duration'] - elapsed
        minutes_left = max(0, int(remaining // 60))
        minutes_elapsed = int(elapsed // 60)
        total_minutes = int(self.single_continuous['duration'] // 60)

        status_lines = [
            f"🔁 Непрерывная рассылка активна для {self.single_continuous['session']}",
            f"⏱️ Прошло: {minutes_elapsed} мин., Осталось: {minutes_left} мин.",
            f"📊 Всего времени: {total_minutes} мин.",
            f"🤖 Статус бота: {'🟢 Запущен' if self.clients[self.single_continuous['session']]['is_running'] else '🔴 Остановлен'}"
        ]

        return "\n".join(status_lines)

