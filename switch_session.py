import json
from pyrogram import Client, filters
import asyncio
import time


def get_session_strings(filename="sessions.json"):
    with open(filename, 'r') as file:
        return [session['session_string'] for session in json.load(file)]


class SessionSwitcher:
    def __init__(self):
        self.clients = {}
        self.current_session = None
        self.start_time = None
        self.is_switching = False
        self.lock = asyncio.Lock()  # Добавляем блокировку

    async def setup_session(self, name, session_string, work_time=300):
        """Создаем и настраиваем сессию"""
        pyro_client = Client(
            name=f"session_{name}",
            api_id="28982778",
            api_hash="54b8ea23241abdef8044090c3c9a2add",
            session_string=session_string
        )

        session_name = name

        # Добавляем хендлер
        @pyro_client.on_message(filters.private & filters.text)
        async def handler(_client, message):
            # Строгая проверка - только активная сессия и не во время переключения
            async with self.lock:
                if (self.is_switching or
                    not self.clients[session_name]['active'] or
                    self.current_session != session_name):
                    return

                # Логируем для отладки
                print(f"Обработка сообщения в сессии: {session_name}, Активна: {self.current_session}")

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

        self.clients[name] = {
            'client': pyro_client,
            'work_time': work_time,
            'active': False
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
            print(f"🔄 Переключаем на: {session_name}")

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
                print(f"✅ Активна: {session_name} - {me.first_name}")
                print(f"⏱️ Время: {self.clients[session_name]['work_time']} сек.")
                await current_client.send_message(
                    chat_id='me',
                    text=f'✅ Сессия {session_name} активирована!\nДоступны команды: /time, /next, /status, /list'
                )
                print("-" * 40)

            except Exception as e:
                print(f"❌ Ошибка при активации сессии {session_name}: {e}")
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
            except ValueError:
                next_session = sessions[0]

        await asyncio.sleep(2)  # Увеличиваем задержку

        await self.switch_to(next_session)

    async def start_all(self):
        """Запускаем все сессии"""
        print(f"🚀 Запускаем {len(self.clients)} сессий...")

        if len(self.clients) == 0:
            print("добавте хотябы одну сессию")
            raise SystemError

        for name, data in self.clients.items():
            try:
                await data['client'].start()
                data['active'] = False  # Все сессии изначально неактивны
                me = await data['client'].get_me()
                print(f"✅ {name}: {me.first_name}")
                await asyncio.sleep(1)
            except Exception as e:
                print(f"❌ Ошибка {name}: {e}")

        # Начинаем с первой сессии
        if self.clients:
            first_session = list(self.clients.keys())[0]
            await self.switch_to(first_session)

        await self.main_loop()

    async def main_loop(self):
        """Главный цикл переключения"""
        print("🔛 Начинаем циклическое переключение...")

        while True:
            try:
                await asyncio.sleep(1)

                if self.is_switching:
                    continue

                remaining = self.get_remaining_time()

                if remaining <= 0:
                    print("⏰ Время вышло, переключаемся...")
                    await self.switch_next()
                else:
                    if remaining % 30 == 0:
                        print(f"⏱️ До переключения: {remaining} сек.")

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Ошибка: {e}")
                await asyncio.sleep(5)

    async def stop_all(self):
        """Останавливаем все сессии"""
        print("\n⏹️ Останавливаем сессии...")
        for name, data in self.clients.items():
            try:
                await data['client'].stop()
                print(f"✅ Остановлена: {name}")
                await asyncio.sleep(1)
            except Exception as e:
                print(f"❌ Ошибка остановки {name}: {e}")


async def main():
    try:
        session_strings = get_session_strings("sessions.json")
        print(f"📁 Загружено {len(session_strings)} сессий")
    except Exception as e:
        print(f"❌ Ошибка загрузки: {e}")
        return

    if not session_strings:
        print("❌ Нет сессий!")
        return

    switcher = SessionSwitcher()

    for i, session_string in enumerate(session_strings, 1):
        await switcher.setup_session(f"account_{i}", session_string, 60)

    print("💬 Команды: /time, /next, /status, /list")
    print("=" * 50)

    try:
        await switcher.start_all()
    except KeyboardInterrupt:
        print("\n🛑 Завершение...")
    finally:
        await switcher.stop_all()
        print("✅ Работа завершена")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Завершение...")