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


def get_session_strings(filename="data/sessions/sessions.json"):
    with open(filename, 'r') as file:
        return [session['session_string'] for session in json.load(file)]

async def main():
    disable_pyrogram_logs()
    try:
        session_strings = get_session_strings()
        print_clear(f"📁 Загружено {len(session_strings)} сессий")
    except Exception as e:
        print_clear(f"❌ Ошибка загрузки: {e}")
        return

    if not session_strings:
        print_clear("❌ Нет сессий!")
        return

    switcher = SessionSwitcher()

    for i, session_string in enumerate(session_strings, 1):
        await switcher.setup_session(f"account_{i}", session_string, 180)

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