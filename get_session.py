import json


def get_all_session_strings(filename="sessions.json"):
    with open(filename, 'r', encoding='utf-8') as file:
        sessions_data = json.load(file)

    session_strings = [session['session_string'] for session in sessions_data]
    return session_strings


# Использование
all_sessions = get_all_session_strings()
print("Все session_string:")
for i, session in enumerate(all_sessions, 1): #enumerate получает порядковый номер начиная с 1
    print(f"{i}. {session}")  # Показываем первые 50 символов