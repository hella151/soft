import asyncio
from pyrogram import Client
from pyrogram.enums import ChatType
from pyrogram.types import Update, User, Chat
from pyrogram.handlers import RawUpdateHandler
from pyrogram.raw import functions, types


app = Client(api_hash='54b8ea23241abdef8044090c3c9a2add', api_id='28982778', name="hella", skip_updates=True)
no_del = ['-1002556012291', '-1002287709773', '-1002320647544', '8018984797', '7290713590', '1228992044',
          '-1002181046523', '-1004939159489', '-1001934457510', '-1002675055562', '93372553']

async def get_dialogs(client: Client, chat_list):
    count_chat = await client.get_dialogs_count(chat_list=chat_list)
    cnt = 0
    async for dialog in client.get_dialogs(chat_list=chat_list):
        chat = dialog.chat
        print(cnt, count_chat)

        if cnt == count_chat:
            print(".")
            break

        # Правильные значения для типов чатов:
        if chat.type in [ChatType.BOT, ChatType.PRIVATE, ChatType.CHANNEL, ChatType.SUPERGROUP, ChatType.GROUP] and str(chat.id) not in no_del:
            try:
                # Проверяем, можем ли мы выйти из этого чата
                if str(chat.id).startswith('-100'):

                    await client.leave_chat(chat.id)
                    # print(f"✅ Успешно вышли из: {chat.id}")
                else:
                    await client.invoke(functions.messages.DeleteHistory(peer=await client.resolve_peer(chat.id), max_id=0, revoke=True))
                    print(f"✅ Успешно вышли из: {chat.id}")

                await asyncio.sleep(1)  # Увеличиваем паузу против floodwait

            except Exception as ex:
                print(f'❌ Ошибка выхода из {chat.title}: {ex}')
                # Продолжаем работу несмотря на ошибку
        cnt += 1
async def delete_all(client: Client):
    await get_dialogs(client, chat_list=0)
    # await asyncio.sleep(5)
    # await get_dialogs(client, chat_list=1)


# async def raw_update_handler(client: Client, update: Update, users: User, chats: Chat):
#     """Обрабатывает все raw события"""
#     print(f"📡 Raw update: {update}")
#
# # Регистрируем raw handler
# app.add_handler(RawUpdateHandler(raw_update_handler))

# Использование
async def main():
    async with app:
        print("🚀 Начинаем процесс выхода из чатов...")
        await delete_all(app)
        print("🎉 Процесс завершен!")


if __name__ == "__main__":
    try:
        app.run(main())
    except KeyboardInterrupt:
        print('\n⏹️ Программа остановлена пользователем')