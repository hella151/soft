import asyncio
from pyrogram import Client
from pyrogram.enums import ChatType
from pyrogram.types import Update, User, Chat
from pyrogram.handlers import RawUpdateHandler
from pyrogram.raw import functions, types


app = Client(api_hash='54b8ea23241abdef8044090c3c9a2add', api_id='28982778', name="hella", skip_updates=True)

async def get_dialogs(client: Client, chat_list):
    chats = []
    processed_chats = set()

    async for dialog in client.get_dialogs(chat_list=chat_list):
        chat = dialog.chat

        if chat.id in processed_chats:
            print(".")
            break

        # Правильные значения для типов чатов:
        if chat.type in [ChatType.CHANNEL, ChatType.SUPERGROUP, ChatType.GROUP]:
            try:
                # Проверяем, можем ли мы выйти из этого чата
                if str(chat.id).startswith('-100'):

                    chats.append(chat.id)
                    # await client.leave_chat(chat.id)
                    # print(f"✅ Успешно вышли из: {chat.id}")
                # else:
                #     await client.invoke(functions.messages.DeleteHistory(peer=await client.resolve_peer(chat.id), max_id=0, revoke=True))
                #     print(f"✅ Успешно вышли из: {chat.id}")

                await asyncio.sleep(1)  # Увеличиваем паузу против floodwait

            except Exception as ex:
                print(f'❌ Ошибка {ex}')
                # Продолжаем работу несмотря на ошибку

        processed_chats.add(chat.id)
        # try:
        #     if chats[-1] == chats[-2]:
        #         print(".")
        #         break
        # except IndexError:
        #     continue
    return chats


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