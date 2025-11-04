import asyncio
import sys
from pyrogram.errors import FloodWait
from functions_ import search_chats_raw
from cache import TelegramCache
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
        self.cache_manager = TelegramCache()

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

        parts = command.split()
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
        # Исправлено: правильно извлекаем query из команды
            if len(parts) < 2:
                logger.warning("❌ Укажите запрос для поиска. Пример: search python")
                return
            query = ' '.join(parts[1:])  # Объединяем все части после команды
            await self.handle_search(query=query)
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
        elif cmd == 'start_all_mailing':
            await self.handle_continuous_start(parts)
        elif cmd == 'stop_all_mailing':
            await self.handle_continuous_stop()
        elif cmd == 'status_mailing':
            await self.handle_continuous_status()
        elif cmd == 'start_continuous':
            await self.handle_start_continuous(parts)
        elif cmd == 'stop_continuous':
            await self.handle_stop_continuous()
        elif cmd == 'reload_chats':
            await self.handle_reload_chats()
        elif cmd == 'show_chats':
            await self.handle_show_chats()
        elif cmd == 'show_all_chats':
            await self.handle_show_all_chats()
        elif cmd == "get_cache":
            await self.handle_get_cache()
        elif cmd == "del_cache":
            await self.session_switcher.del_cache()
        else:
            await self.handle_unknown()

    async def handle_cleanup_cache(self):
        """Очистить кэш от невалидных чатов"""
        if not self.session_switcher.current_session or not self.session_switcher.is_running:
            logger.warning("❌ Нет активной сессии")
            return

        session_name = self.session_switcher.current_session
        try:
            removed_count = await self.session_switcher.cleanup_invalid_chats(session_name)
            if removed_count > 0:
                logger.info(f"✅ Очищено {removed_count} невалидных чатов из кэша")
            else:
                logger.info("✅ Нет невалидных чатов для очистки")
        except Exception as e:
            logger.error(f"❌ Ошибка очистки кэша: {e}")

    async def handle_reload_chats(self):
        """Перезагрузить выбранные чаты ДЛЯ ТЕКУЩЕЙ СЕССИИ"""
        if not self.session_switcher.current_session or not self.session_switcher.is_running:
            logger.warning("❌ Нет активной сессии")
            return

        session_name = self.session_switcher.current_session
        try:
            await self.session_switcher.reload_chats(session_name)
            logger.info(f"🔄 Список чатов перезагружен для {session_name}")
        except Exception as e:
            logger.warning(f"Ошибка перезагрузки чатов: {e}")

    async def handle_show_chats(self):
        """Показать выбранные чаты ДЛЯ ТЕКУЩЕЙ СЕССИИ"""
        if not self.session_switcher.current_session or not self.session_switcher.is_running:
            logger.warning("❌ Нет активной сессии")
            return

        session_name = self.session_switcher.current_session
        await self.session_switcher.show_current_chats(session_name)

    async def handle_show_all_chats(self):
        """Показать выбранные чаты ДЛЯ ВСЕХ СЕССИЙ"""
        if not self.session_switcher.is_running:
            logger.warning("❌ Система не запущена")
            return

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

    async def handle_search(self, query: str = None):
        """Обработка команды search"""
        if not self.session_switcher.current_session or not self.session_switcher.is_running:
            logger.warning("❌ Нет активной сессии")
            return

        if query is None:
            logger.warning("❌ Напишите что именно нужно искать")
            return

        session_name = self.session_switcher.current_session
        client = self.session_switcher.clients[session_name]['client']

        try:
            # Блокируем переключение на время поиска и вступления в группы
            groups = await search_chats_raw(client, query=query)
            if len(groups) == 0:
                logger.info("Чатов не найдено")
                return

            await self.session_switcher.block_session_switching(session_name, "console_search")

            print_clear('Присоединится? [y/n]')
            a = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            clear_line()

            if len(groups) > 5:
                groups = random.sample(groups, 5)

            if a.strip().lower() == 'y':
                for chat in groups:
                    if not self.session_switcher.is_running:
                        break
                    try:
                        await client.join_chat(chat_id=chat['id'])
                        logger.info(f"Зашли в {chat['title']}")
                    except FloodWait as e:
                        logger.warning(f"Ждём {e.value} секунд, перед тем как снова что-то делать, есть риск получить бан")
                        self.cache_manager.save_chats(session_name=session_name, cache_type="mailing", chats=groups)
                        await asyncio.sleep(e.value)
                        await self.session_switcher.unblock_session_switching(session_name)
                        return
                    except Exception as ex:
                        logger.error(f"Ошибка захода в {chat['title']} {ex}")
                        await asyncio.sleep(1)
                        continue
                    await asyncio.sleep(5)

            self.cache_manager.save_chats(session_name=session_name, cache_type="mailing", chats=groups)
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
            '🔄 reload_chats - Перезагрузить список чатов ДЛЯ АКТИВНОЙ СЕССИИ\n'
            '📋 show_chats - Показать чаты ДЛЯ АКТИВНОЙ СЕССИИ\n'
            '📁 show_all_chats - Показать чаты ДЛЯ ВСЕХ СЕССИЙ\n'
            '🚫 show_invalid_chats - Показать невалидные чаты\n'
            '🗑 clear_invalid_chats - Очистить список невалидных чатов\n'
            '🧹 cleanup_cache - Очистить кэш от невалидных чатов\n'
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

    async def handle_continuous_start(self, parts):
        """Запуск непрерывной рассылки"""
        if not self.session_switcher.current_session or not self.session_switcher.is_running:
            logger.warning("❌ Нет активной сессии")
            return

        # Получаем время из аргументов (по умолчанию 60 минут)
        duration_minutes = 60
        if len(parts) > 1:
            try:
                duration_minutes = int(parts[1])
                if duration_minutes <= 0:
                    logger.warning("❌ Время должно быть положительным числом")
                    return
            except ValueError:
                logger.warning("❌ Укажите корректное время в минутах. Пример: continuous_start 120")
                return

        try:
            success = await self.session_switcher.start_continuous_mailing(duration_minutes)
            if success:
                logger.info(f"🔁 Непрерывная рассылка запущена на {duration_minutes} минут")
                logger.info("🔄 Сессии будут автоматически переключаться и запускать рассылку")
            else:
                logger.warning("❌ Не удалось запустить непрерывную рассылку")
        except Exception as e:
            logger.error(f"❌ Ошибка запуска непрерывной рассылки: {e}")

    async def handle_continuous_status(self):
        """Статус непрерывной рассылки"""
        if self.session_switcher.continuous_mailing:
            elapsed = time.time() - self.session_switcher.continuous_start_time
            remaining = self.session_switcher.continuous_mailing_duration - elapsed
            minutes_left = max(0, int(remaining // 60))
            minutes_elapsed = int(elapsed // 60)

            logger.info(f"🔁 Непрерывная рассылка активна")
            logger.info(f"⏱️ Прошло: {minutes_elapsed} мин., Осталось: {minutes_left} мин.")
            logger.info(f"📊 Всего времени: {int(self.session_switcher.continuous_mailing_duration // 60)} мин.")
            logger.info(f"🔄 Автопереключение: включено")
            logger.info(f"🤖 Автозапуск рассылки: включено")
        elif self.session_switcher.single_continuous['active'] is True:
            status_info = await self.session_switcher.get_continuous_mailing_status_single()
            logger.info("\n" + status_info)
        else:
            logger.info("🔁 Непрерывная рассылка не активна")

    async def handle_continuous_stop(self):
        """Остановка непрерывной рассылки"""
        try:
            success = await self.session_switcher.stop_continuous_mailing()
            if success:
                logger.info("⏹️ Непрерывная рассылка остановлена")
            else:
                logger.info("ℹ️ Непрерывная рассылка не была активна")
        except Exception as e:
            logger.error(f"❌ Ошибка остановки непрерывной рассылки: {e}")

    async def handle_start_continuous(self, parts):
        """Запуск непрерывной рассылки для текущей сессии"""
        if not self.session_switcher.current_session or not self.session_switcher.is_running:
            logger.warning("❌ Нет активной сессии")
            return

        duration_minutes = 60
        if len(parts) > 1:
            try:
                duration_minutes = int(parts[1])
                if duration_minutes <= 0:
                    logger.warning("❌ Время должно быть положительным числом")
                    return
            except ValueError:
                logger.warning("❌ Укажите корректное время в минутах. Пример: start_continuous 120")
                return

        try:
            success = await self.session_switcher.start_continuous_mailing_single(duration_minutes)
            if success:
                logger.info(
                    f"🔁 Непрерывная рассылка запущена для {self.session_switcher.current_session} на {duration_minutes} минут")
                logger.info("🔒 Переключение на другие сессии заблокировано")
            else:
                logger.warning("❌ Не удалось запустить непрерывную рассылку")
        except Exception as e:
            logger.error(f"❌ Ошибка запуска непрерывной рассылки: {e}")

    async def handle_stop_continuous(self):
        """Остановка непрерывной рассылки для текущей сессии"""
        try:
            success = await self.session_switcher.stop_continuous_mailing_single()
            if success:
                logger.info("⏹️ Непрерывная рассылка остановлена")
                logger.info("🔓 Переключение на другие сессии разблокировано")
            else:
                logger.info("ℹ️ Непрерывная рассылка не была активна")
        except Exception as e:
            logger.error(f"❌ Ошибка остановки непрерывной рассылки: {e}")
