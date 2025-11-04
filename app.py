import json
import asyncio
import sys
from data.log import logger, disable_pyrogram_logs
from classes import SessionSwitcher

def clear_line():
    """Очистка текущей строки"""
    sys.stdout.write('\r\033[K')
    sys.stdout.flush()


def print_clear(*args, **kwargs):
    """Печать с очисткой строки БЕЗ восстановления приглашения"""
    clear_line()
    print(*args, **kwargs)


def get_sessions(filename="data/sessions/sessions.json"):
    with open(filename, 'r', encoding='utf-8') as file:
        return [session for session in json.load(file)]

async def main():
    disable_pyrogram_logs()
    try:
        sessions = get_sessions()
        print_clear(f"📁 Загружено {len(sessions)} сессий")
    except Exception as e:
        print_clear(f"❌ Ошибка загрузки: {e}")
        return

    if not sessions:
        print_clear("❌ Нет сессий!")
        return

    switcher = SessionSwitcher()
    for session in sessions:
        await switcher.setup_session(f"{session['first_name']}", session['session_string'], switcher.config['delay_between_sessions'])

    print_clear("💬 Команды: help - показать все команды")
    print_clear("Доступные команды для набора в личные сообщения аккаунта: /time, /next, /status, /list, /force_stop, /force_switch")
    print_clear("-" * 40)

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