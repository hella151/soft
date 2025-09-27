import asyncio
from pyrogram import Client
import json
from datetime import datetime
import os

api_id = '28982778'
api_hash = '54b8ea23241abdef8044090c3c9a2add'


async def get_session_string():
    print("введите имя для ссессии(любое)")
    session_name = input("> ")
    async with Client(name=session_name, api_id=api_id, api_hash=api_hash) as app:
        session = await app.export_session_string()

        # Получаем информацию об аккаунте для идентификации
        me = await app.get_me()
        user_info = {
            "user_id": me.id,
            "username": me.username,
            "first_name": me.first_name,
            "phone_number": me.phone_number,
            "session_string": session,
            "created_at": datetime.now().isoformat()
        }

        # Читаем существующие сессии
        sessions_data = []
        if os.path.exists("sessions.json"):
            with open("sessions.json", 'r', encoding='utf-8') as file:
                try:
                    sessions_data = json.load(file)
                except json.JSONDecodeError:
                    sessions_data = []

        # Проверяем на уникальность по user_id
        if any(session['user_id'] == user_info['user_id'] for session in sessions_data):
            print(f"Сессия для пользователя {me.first_name} уже существует!")
            return

        # Добавляем новую сессию
        sessions_data.append(user_info)

        # Записываем обратно в файл
        with open("sessions.json", 'w', encoding='utf-8') as file:
            json.dump(sessions_data, file, ensure_ascii=False, indent=2)

        print(f"Сессия для {me.first_name} успешно сохранена!")


asyncio.run(get_session_string())