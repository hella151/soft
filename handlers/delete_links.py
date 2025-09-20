from typing import Any

from pyrogram import Client

from pyrogram import filters
from pyrogram.types import Message


# @app.on_message(filters.chat(-1002556012291))  # ID вашего чата
async def delete_links(client: Client, message: Message) -> Any:
    # Удаляем системные сообщения
    if message.service:
        try:
            await message.delete()
            print(f"Удалено системное сообщение")
        except Exception as e:
            print(f"Ошибка удаления системного сообщения: {e}")
        return

    # Проверяем, есть ли текст в сообщении
    if not message.text:
        return

    if "bot?" in message.text.lower():
        try:
            await message.delete()
            await client.send_message(
                chat_id=1228992044,  # ID чата для уведомлений
                text=f'🚫 Удалено сообщение с ссылкой:\n'
                     f'👤 Пользователь: @{message.from_user.username}\n'
                     f'📝 Текст: {message.text[:300]}...'  # Обрезаем длинный текст
            )
            print(f"Удалено сообщение с ссылкой от @{message.from_user.username}")
        except Exception as e:
            print(f"Ошибка при удалении ссылки: {e}")

    # Удаляем сообщения с HTTP-ссылками (кроме t.me)
    if 'http' in message.text.lower() and 't.me' not in message.text.lower():
        try:
            await message.delete()
            await client.send_message(
                chat_id=1228992044,  # ID чата для уведомлений
                text=f'🚫 Удалено сообщение с ссылкой:\n'
                     f'👤 Пользователь: @{message.from_user.username}\n'
                     f'📝 Текст: {message.text[:300]}...'  # Обрезаем длинный текст
            )
            print(f"Удалено сообщение с ссылкой от @{message.from_user.username}")
        except Exception as e:
            print(f"Ошибка при удалении ссылки: {e}")

delete_links_handler = [(delete_links, filters.chat(-1002556012291))]