# def debug_decorator(func):
#     def wrapper(*args, **kwargs):  # Принимаем любые аргументы
#         print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
#         result = func(*args, **kwargs)  # Передаем аргументы дальше
#         print(f"Result: {result}")
#         return result
#     return wrapper
#
# @debug_decorator
# def multiply(x, y):
#     return x * y
#
# # Все работает прозрачно
# multiply(5, 6)        # args=(5, 6), kwargs={}
# multiply(x=5, y=6)    # args=(), kwargs={'x':5, 'y':6}
# class Base:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
# class Person(Base):
#     def __init__(self, occupation, *args, **kwargs):
#         super().__init__(*args, **kwargs)  # Передаем аргументы в родительский класс
#         self.occupation = occupation
#
# # Создаем объект
# person = Person("developer", "Alice", 25)
# print(person.name, person.age, person.occupation)  # Alice 25 developer
# import asyncio
#
#
# def with_retry(max_attempts=3):
#     def decorator(func):
#         async def wrapper(*args, **kwargs):  # Принимаем аргументы
#             for attempt in range(max_attempts):
#                 try:
#                     return await func(*args, **kwargs)  # Передаем аргументы
#                 except Exception as e:
#                     print(f"Attempt {attempt+1} failed: {e}")
#                     if attempt == max_attempts - 1:
#                         raise
#                     await asyncio.sleep(1)
#         return wrapper
#     return decorator
#
# @with_retry(max_attempts=3)
# async def api_call(url, params=None, timeout=30):
#     # params и timeout будут корректно переданы
#