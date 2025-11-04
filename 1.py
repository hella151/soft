# import asyncio
# from pyrogram import Client
#
# app = Client(api_hash='54b8ea23241abdef8044090c3c9a2add', api_id='28982778', name="karina")
#
#
# from pyrogram.raw import functions, types
#
# async def create_folder_raw():
#     async with app:
#         try:
#             # Создаем папку через raw API
#             result = await app.invoke(
#                 functions.folders.edit_peer_folders(
#                     title="Моя папка",
#                     # Необязательно: указать эмоджи для папки
#                     # emoticon="📁"
#                 )
#             )
#             print(f"Папка создана: {result}")
#             return result
#
#         except Exception as e:
#             print(f"Ошибка создания папки: {e}")
#             return None
#
#
# app.run(create_folder_raw)
#
#
# {
#     "user_id": 8165394439,
#     "username": "xxx_xxx_xyz_xxx",
#     "first_name": ".",
#     "phone_number": "79226050395",
#     "session_string": "AgG6PfoAqgGKq8PzT05VyKj9yF_l6Jnlty9Pq75LRyn9IMIQzLiNqMWnpvJJ1IEpPIdWrdQYyIAgYq0uHW3cC6gGo3SNWnbrLZLz7kvw58q2T6foz0myroer6-0BzANsZAvgrYrhcqdFr6cfxG2HC3z13Jd4OfqLZdKaOnPnG3kqCTc6FlEC3H3Lerv18vIn_ZJcj2gXSk9wJjhhqgcbY8kErt8biuLJ7J4ZsXJJSMrniFRaUpbKEspvutOnJA_LVL-WzeGZ_kcD-83n-MJND8LTVZvXX76QUMMtOLbTcaqwKB_8urWdp61taXyf4yg13YDZxXfToFxE-5DqwDC_3l6YugIQDAAAAAHmsggHAA",
#     "created_at": "2025-09-27T12:22:03.336728"
#   },
#   {
#     "user_id": 1228992044,
#     "username": "hella777",
#     "first_name": "𝙝𝙚𝙡𝙡𝙖...",
#     "phone_number": "79923472259",
#     "session_string": "AgG6PfoAVkQ8ZWmLreza1Qp8uNL3y5u1vStrK-JcSeS8rg19lKTsepe0c90Y3XnikZ847yZZiRejLZTwHdW63bzGfkBM94ZQvtyK-uq7QGpfiSAV-zXUeEhoZlR0sRrLkWfUNxaIP3Ve19IV2FFaaC3ERwD0tceV3mdM-3lbBt4HsnwUVwL6aJK96ze_OqYq3liL2lifBoSKjBtp36Ao4i2fEmJfBbBh-mBC3J9pZ0tRcE-ZAV4Qkac_xjpHxuo1whHAAon_JWWj4oyoB1FN9T0K6-u3-0rH2sgH6BcjpBpGLyGT3aYdCcH2GNYGAxbwhyOLOYzsr7YFjBBYVZH4eZTC3ITkagAAAABJQO4sAA",
#     "created_at": "2025-10-03T14:39:14.720459"
#   },
# Если пользователь ввел: "search взаимные подписки python"
command = "search взаимные подписки python"
parts = command.split()  # ['search', 'взаимные', 'подписки', 'python']
print(parts)

cmd = parts[0]  # 'search'
query = ' '.join(parts[1:])  # 'взаимные подписки python' ОБьДЕНИЕТ ЧЕРЕЗ ПРОБЕЛ
print(query)