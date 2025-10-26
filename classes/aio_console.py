import asyncio
import sys
from pyrogram.errors import FloodWait
from functions_ import search_chats_raw, is_member
from data.log import logger
import random
import time

def clear_line():
    """Очистка текущей строки"""
    sys.stdout.write('\r\033[K')
    sys.stdout.flush()


def print_clear(*args, **kwargs):
    """Печать с очисткой строки БЕЗ восстановления приглашения"""
    clear_line()
    print(*args, **kwargs)


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
        while self.is_running and self.session_switcher.is_running:
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
        if not command or not self.session_switcher.is_running:
            return

        cmd = command.split()[0].lower()

        # Проверяем блокировку для команд, которые требуют активной сессии
        if cmd in ['start_mailing', 'stop', 'search', 'me', 'status', 'next', 'leave_chats', 'get_cache']:
            if not self.session_switcher.current_session:
                logger.warning("❌ Нет активной сессии")
                return

            # Проверяем блокировку для команд, которые могут конфликтовать с текущими операциями
            if self.session_switcher.is_session_blocked(self.session_switcher.current_session):
                operation_info = self.session_switcher.block_switching_operations.get(
                    self.session_switcher.current_session, {})
                op_type = operation_info.get('type', 'unknown')
                duration = time.time() - operation_info.get('start_time', time.time())
                logger.warning(
                    f"⏳ Команда '{cmd}' временно недоступна. Выполняется операция '{op_type}' ({duration:.1f} сек.)")
                return

        if cmd == 'start_mailing':
            await self.handle_start_mailing()
        elif cmd == 'force_stop':
            await self.session_switcher.force_stop_bot(session_name=self.session_switcher.current_session)
        elif cmd == 'force_switch':
            await self.session_switcher.force_switch_next()
        elif cmd == 'stop':
            await self.handle_stop()
        elif cmd == 'search':
            await self.handle_search()
        elif cmd == 'search_me':
            await self.session_switcher.search_me_channels(session_name=self.session_switcher.current_session, type="mailing")
        elif cmd == 'me':
            await self.handle_me()
        elif cmd == 'status':
            await self.handle_status()
        elif cmd == 'exit':
            await self.handle_exit()
        elif cmd == 'help':
            await self.handle_help()
        elif cmd == 'next':
            await self.handle_next()
        elif cmd == 'leave_chats':
            await self.handle_leave_chats()
        elif cmd == "get_cache":
            await self.handle_get_cache()
        else:
            await self.handle_unknown()

    async def handle_start_mailing(self):
        """Обработка команды start_mailing"""
        if not self.session_switcher.current_session or not self.session_switcher.is_running:
            logger.warning("❌ Нет активной сессии")
            return

        session_name = self.session_switcher.current_session

        # Дополнительная проверка блокировки
        if self.session_switcher.is_session_blocked(session_name):
            logger.warning("❌ Сессия заблокирована, невозможно запустить бота")
            return

        if self.session_switcher.clients[session_name]['is_running']:
            logger.info("✅ Бот уже запущен")
        else:
            try:
                logger.info("🤖 Основная функция бота запущена")
                await asyncio.create_task(self.session_switcher.start_bot_function(session_name))
            except Exception as e:
                logger.warning(f"Ошибка запуска: {e}")

    async def handle_leave_chats(self):
        """Обработка команды leave_chats"""
        if not self.session_switcher.current_session or not self.session_switcher.is_running:
            logger.warning("❌ Нет активной сессии")
            return

        session_name = self.session_switcher.current_session
        try:
            await self.session_switcher.leave_me_channels(session_name)
        except Exception as e:
            logger.warning(f"Ошибка выхода из чатов: {e}")

    async def handle_stop(self):
        """Обработка команды stop"""
        if not self.session_switcher.current_session or not self.session_switcher.is_running:
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
        if not self.session_switcher.current_session or not self.session_switcher.is_running:
            logger.warning("❌ Нет активной сессии")
            return

        session_name = self.session_switcher.current_session
        client = self.session_switcher.clients[session_name]['client']

        try:
            # Блокируем переключение на время поиска и вступления в группы
            await self.session_switcher.block_session_switching(session_name, "console_search")

            groups = await search_chats_raw(client, query="Взаимные подписки")
            print_clear('Присоединится? [y/n]')
            a = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            clear_line()

            if len(groups) > 5:
                groups = random.sample(groups, 5)

            if a.strip().lower() == 'y':
                for chat in groups:
                    if not self.session_switcher.is_running:
                        break
                    if await is_member(client, chat_id=chat['id']):
                        continue
                    try:
                        await client.join_chat(chat_id=chat['id'])
                        logger.info(f"Зашли в {chat['title']}")
                    except FloodWait as e:
                        logger.warning(
                            f"Подождите {e.value} секунд, перед тем как снова вступать в группы, есть риск получить бан")
                        await self.session_switcher.unblock_session_switching(session_name)
                        return
                    except Exception as ex:
                        logger.error(f"Ошибка захода в {chat['title']} {ex}")
                        continue
                    await asyncio.sleep(5)

            await self.session_switcher.unblock_session_switching(session_name)

        except Exception as e:
            logger.warning(f"Ошибка поиска: {e}")
            # Обязательно разблокируем при ошибке
            if self.session_switcher.is_session_blocked(session_name):
                await self.session_switcher.unblock_session_switching(session_name)

    async def handle_me(self):
        """Обработка команды me"""
        if not self.session_switcher.current_session or not self.session_switcher.is_running:
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
        if self.session_switcher.current_session and self.session_switcher.is_running:
            session_name = self.session_switcher.current_session
            bot_status = "🟢 Запущен" if self.session_switcher.clients[session_name]['is_running'] else "🔴 Остановлен"

            # Получаем расширенный статус из SessionSwitcher
            status_info = await self.session_switcher.get_session_status()
            logger.info(status_info)
        else:
            logger.info("📊 Нет активной сессии")

    async def handle_next(self):
        """Обработка команды next"""
        if not self.session_switcher.current_session:
            logger.warning("❌ Нет активной сессии")
            return

        # Проверяем блокировку для команды next
        if self.session_switcher.is_session_blocked(self.session_switcher.current_session):
            operation_info = self.session_switcher.block_switching_operations.get(self.session_switcher.current_session,
                                                                                  {})
            op_type = operation_info.get('type', 'unknown')
            logger.warning(f"⏳ Невозможно переключить сессию. Выполняется операция: {op_type}")
            return

        await self.session_switcher.switch_next()

    async def handle_get_cache(self):
        """Обработка команды get_cache"""
        await self.session_switcher.get_cache_info()

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
            '🚪 leave_chats - Выйти из чатов для активной сессии\n'
            '💾 get_cache - Показать информацию о кэше\n'
            '❓ help    - Показать справку\n'
            '❌ exit    - Завершить работу'
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