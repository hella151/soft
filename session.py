import asyncio
from pyrogram import Client

client = Client(api_hash='54b8ea23241abdef8044090c3c9a2add', api_id='28982778', name="hell")
# async def main():
#     async with Client("hella") as app:
#         await app.send_message(chat_id="me", text="Greetings from **Pyrogram**!")

client.run()
# asyncio.run(main())





# async def main_bot_function(client: Client):
#     """Основная функция работы бота"""
#     global is_running
#     try:
#         while is_running:
#             message_other = [
#                 "Вз лс 🚀🚀🚀 \nhttps://t.me/vzz_piar_vzz",
#                 "Вз пишите лс у меня бан 🚀🚀🚀 \nhttps://t.me/vzz_piar_vzz",
#                 "Только вз, без ботов пишите лс 🚀🚀🚀\nhttps://t.me/vzz_piar_vzz"
#             ]
#
#             k = 0
#             while k < 15 and is_running:
#                 n = 0
#                 while n < 5 + random.randint(1, 2) and is_running:
#                     try:
#                         await mess_to_chat(
#                             chats_id=chats_vz,
#                             message_text=random.choice(message_other),
#                             client=client
#                         )
#                         n += 1
#                         await asyncio.sleep(60 + random.randint(1, 3))
#
#                     except FloodWait as e:
#                         await asyncio.sleep(e.value + 5)
#                     except RPCError:
#                         continue
#
#                 print(f"session: {k + 1}")
#                 k += 1
#                 await asyncio.sleep(120)
#
#
#     except asyncio.CancelledError:
#         print("Бот остановлен 🛑")
#     except Exception as e:
#         print(f"Ошибка в main: {e}")
#         raise
#     finally:
#         is_running = False