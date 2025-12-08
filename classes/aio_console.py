import asyncio
import sys
from pyrogram.errors import FloodWait
from functions_ import search_chats_raw
from cache import TelegramCache
from data.log import logger
import random
import time

def clear_line():
    sys.stdout.write('\r\033[K')
    sys.stdout.flush()

def print_clear(*args, **kwargs):
    clear_line()
    print(*args, **kwargs)

class AsyncConsoleManager:
    def __init__(self, session_switcher):
        self.session_switcher = session_switcher
        self.is_running = False
        self.cache_manager = TelegramCache()

    async def start(self):
        self.is_running = True
        print_clear("💬 Консольный менеджер запущен. Введите 'help' для списка команд")
        await self.console_input()

    async def console_input(self):
        while self.is_running and self.session_switcher.is_running:
            try:
                # ИСПОЛЬЗУЕМ asyncio.to_thread для неблокирующего ввода
                data = await asyncio.to_thread(sys.stdin.readline)
                if not data:
                    break

                data = data.strip()
                if data:
                    clear_line()
                    await self.process_command(data)

            except (KeyboardInterrupt, EOFError):
                logger.info("Завершение работы...")
                await self.graceful_shutdown()
                break
            except Exception as e:
                logger.error(f"Ошибка ввода: {e}")

    async def process_command(self, command):
        if not command or not self.session_switcher.is_running:
            return

        parts = command.split()
        cmd = parts[0].lower()

        # Проверка активной сессии для команд
        if cmd in ['start_mailing', 'stop', 'search', 'me', 'status', 'next', 'leave_chats', 'get_cache']:
            if not self.session_switcher.current_session:
                logger.warning("❌ Нет активной сессии")
                return

            if self.session_switcher.is_session_blocked(self.session_switcher.current_session):
                operation_info = self.session_switcher.block_switching_operations.get(
                    self.session_switcher.current_session, {})
                op_type = operation_info.get('type', 'unknown')
                duration = time.time() - operation_info.get('start_time', time.time())
                logger.warning(f"⏳ Команда '{cmd}' временно недоступна. Выполняется операция '{op_type}' ({duration:.1f} сек.)")
                return

        # Обработка команд
        command_handlers = {
            'stop': self.handle_stop,
            'search': lambda: self.handle_search(' '.join(parts[1:]) if len(parts) > 1 else None),
            'search_me': lambda: self.session_switcher.search_me_channels(self.session_switcher.current_session, "mailing"),
            'me': self.handle_me,
            'status': self.handle_status,
            'exit': self.handle_exit,
            'help': self.handle_help,
            'next': self.handle_next,
            'leave_chats': self.handle_leave_chats,
            'start_continuous': lambda: self.handle_start_continuous(parts),
            'start_mailing': lambda: self.session_switcher.start_continuous_mailing_single(parts),
            'status_mailing': self.session_switcher.continuous_monitor,
            'reload_chats': self.handle_reload_chats,
            'show_chats': self.handle_show_chats,
            'show_all_chats': self.handle_show_all_chats,
            'get_cache': self.handle_get_cache,
            'del_cache': lambda: self.session_switcher.del_cache(),
            'show_mailing_file_chats': lambda: self.session_switcher.search_channels_forever(),
            'start_mailing_file': lambda: self.session_switcher.start_continuous_mailing_forever(int(parts[1]) if len(parts) > 1 else 60
)
        }

        handler = command_handlers.get(cmd)
        if handler:
            await handler()
        else:
            await self.handle_unknown()

    async def handle_help(self):
        help_text = (
            '🤖 КОМАНДЫ БОТА:\n'
            '🚀 start_mailing - Запустить рассылку\n'
            '⏹️ stop - Остановить любую рассылку\n'
            '🚀 search [запрос] - Поиск каналов\n'
            '🔜 next - Переключить сессию\n'
            '📊 status - Статус бота\n'
            '👤 me - Информация о сессии\n'
            '🚪 leave_chats - Выйти из чатов\n'
            '🔁 start_continuous [мин] - Непрерывная рассылка для каждой сессии\n'
            '🔁 start_mailing [мин] - Непрерывная рассылка для текущей сессии\n'
            '🔁 start_mailing_file [мин] - Непрерывная рассылка для каждой сессии для чатов из файла\n'
            '📊 show_mailing_file_chats - Показать чаты из файла (если есть)'
            '📊 status_mailing - Статус рассылки\n'
            '🔄 reload_chats - Перезагрузить чаты\n'
            '📋 show_chats - Показать чаты\n'
            '📁 show_all_chats - Все чаты\n'
            '💾 get_cache - Инфо о кэше\n'
            '❓ help - Справка\n'
            '❌ exit - Выход'
        )
        print_clear(help_text)

    async def handle_start_mailing(self):
        if not self.session_switcher.current_session:
            return

        session_name = self.session_switcher.current_session

        if self.session_switcher.clients[session_name]['is_running']:
            logger.info("✅ Бот уже запущен")
        else:
            try:
                logger.info("🤖 Основная функция бота запущена")
                await asyncio.create_task(self.session_switcher.start_bot_function(session_name))
            except Exception as e:
                logger.warning(f"Ошибка запуска: {e}")

    async def handle_stop(self):
        if not self.session_switcher.current_session:
            return

        if self.session_switcher.continuous_mailing:
            try:
                success = await self.session_switcher.stop_continuous_mailing()
                if success:
                    logger.info("⏹️ Непрерывная рассылка остановлена")
                else:
                    logger.info("ℹ️ Непрерывная рассылка не была активна")
            except Exception as e:
                logger.error(f"❌ Ошибка остановки непрерывной рассылки: {e}")


        elif self.session_switcher.single_continuous['active']:
            try:
                success = await self.session_switcher.stop_continuous_mailing_single()
                if success:
                    logger.info("⏹️ Непрерывная рассылка остановлена")
                    logger.info("🔓 Переключение на другие сессии разблокировано")
                else:
                    logger.info("ℹ️ Непрерывная рассылка не была активна")
            except Exception as e:
                logger.error(f"❌ Ошибка остановки непрерывной рассылки: {e}")

        else:
            session_name = self.session_switcher.current_session
            try:
                await self.session_switcher.stop_bot_function(session_name)
                logger.info("🤖 Основная функция бота остановлена")
            except Exception as e:
                logger.warning(f"Ошибка остановки: {e}")

    async def handle_search(self, query=None):
        if not query:
            logger.warning("❌ Укажите запрос для поиска")
            return

        session_name = self.session_switcher.current_session
        client = self.session_switcher.clients[session_name]['client']

        try:
            groups = await search_chats_raw(client, query=query)
            if not groups:
                logger.info("Чатов не найдено")
                return

            await self.session_switcher.block_session_switching(session_name, "console_search")

            print_clear('Присоединится? [y/n]')
            a = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            clear_line()

            # if len(groups) > 5:
            #     groups = random.sample(groups, 5)

            if a.strip().lower() == 'y':
                for chat in groups:
                    if not self.session_switcher.is_running:
                        break
                    try:
                        await client.join_chat(chat_id=chat['id'])
                        logger.info(f"Зашли в {chat['title']}")
                    except FloodWait as e:
                        logger.warning(f"Ждём {e.value} секунд")
                        self.cache_manager.save_chats(session_name=session_name, cache_type="mailing", chats=groups)
                        await asyncio.sleep(e.value)
                        await self.session_switcher.unblock_session_switching(session_name)
                        return
                    except Exception as ex:
                        logger.error(f"Ошибка захода в {chat['title']}: {ex}")
                        await asyncio.sleep(1)
                    await asyncio.sleep(5 + random.uniform(1.5, 10.5))

            self.cache_manager.save_chats(session_name=session_name, cache_type="mailing", chats=groups)
            await self.session_switcher.unblock_session_switching(session_name)

        except Exception as e:
            logger.warning(f"Ошибка поиска: {e}")
            if self.session_switcher.is_session_blocked(session_name):
                await self.session_switcher.unblock_session_switching(session_name)

    async def handle_me(self):
        session_name = self.session_switcher.current_session
        client = self.session_switcher.clients[session_name]['client']
        me = await client.get_me()
        print_clear(f"🤖 ID: {me.id}")
        print_clear(f"📛 Имя: {me.first_name}")
        print_clear(f"🔗 Username: @{me.username}")
        print_clear(f"⭐ Premium: {'Да' if me.is_premium else 'Нет'}")

    async def handle_status(self):
        if self.session_switcher.current_session:
            status_info = await self.session_switcher.get_session_status()
            logger.info(status_info)
        else:
            logger.info("📊 Нет активной сессии")

    async def handle_next(self):
        if not self.session_switcher.current_session:
            return

        await self.session_switcher.switch_next()

    async def handle_leave_chats(self):
        if not self.session_switcher.current_session:
            return

        session_name = self.session_switcher.current_session
        try:
            await self.session_switcher.leave_me_channels(session_name)
        except Exception as e:
            logger.warning(f"Ошибка выхода из чатов: {e}")

    async def handle_start_continuous(self, parts):
        if not self.session_switcher.current_session:
            return

        duration_minutes = 60
        if len(parts) > 1:
            try:
                # УБЕДИТЕСЬ, ЧТО ЭТО ЧИСЛО, А НЕ СПИСОК
                duration_minutes = int(parts[1])
                if duration_minutes <= 0:
                    logger.warning("❌ Время должно быть положительным числом")
                    return
            except ValueError:
                logger.warning("❌ Укажите корректное время в минутах")
                return

        try:
            # ПЕРЕДАВАЙТЕ ЧИСЛО, А НЕ СПИСОК
            success = await self.session_switcher.start_continuous_mailing(duration_minutes)
            if success:
                logger.info(f"🔁 Непрерывная рассылка запущена на {duration_minutes} минут")
                # logger.info("🔒 Переключение на другие сессии заблокировано")
            else:
                logger.warning("❌ Не удалось запустить непрерывную рассылку")
        except Exception as e:
            logger.error(f"❌ Ошибка запуска непрерывной рассылки: {e}")

    async def handle_reload_chats(self):
        if not self.session_switcher.current_session:
            return

        session_name = self.session_switcher.current_session
        try:
            await self.session_switcher.reload_chats(session_name)
            logger.info(f"🔄 Список чатов перезагружен для {session_name}")
        except Exception as e:
            logger.warning(f"Ошибка перезагрузки чатов: {e}")

    async def handle_show_chats(self):
        if not self.session_switcher.current_session:
            return

        session_name = self.session_switcher.current_session
        await self.session_switcher.show_current_chats(session_name)

    async def handle_show_all_chats(self):
        logger.info("📋 Выбранные чаты для всех сессий:")
        has_chats = False

        for session_name in self.session_switcher.clients.keys():
            if (session_name in self.session_switcher.selected_chats and
                    self.session_switcher.selected_chats[session_name]):
                chats = self.session_switcher.selected_chats[session_name]
                logger.info(f"🎯 {session_name} ({len(chats)} чатов):")
                for i, chat in enumerate(chats, 1):
                    logger.info(f"    {i}. {chat.get('title', 'Без названия')}")
                has_chats = True
            else:
                logger.info(f"📭 {session_name}: нет выбранных чатов")

        if not has_chats:
            logger.info("❌ Нет выбранных чатов ни у одной сессии")

    async def handle_get_cache(self):
        await self.session_switcher.get_cache_info()

    async def handle_unknown(self):
        logger.warning("❌ Неизвестная команда. Введите 'help' для справки")

    async def handle_exit(self):
        await self.graceful_shutdown()

    async def graceful_shutdown(self):
        clear_line()
        logger.info("🛑 Завершение работы...")
        self.is_running = False
        await self.session_switcher.stop_all()
        logger.info("👋 До свидания!")