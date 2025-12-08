import json
import os
import sys
from datetime import datetime, timedelta


def print_clear(*args, **kwargs):
    """Печать с очисткой строки БЕЗ восстановления приглашения"""
    sys.stdout.write('\r\033[K')
    sys.stdout.flush()
    print(*args, **kwargs)


class TelegramCache:
    def __init__(self, cache_dir="telegram_cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def _get_cache_path(self, session_name, cache_type):
        return os.path.join(self.cache_dir, f"{session_name}_{cache_type}.json")

    def save_chats(self, session_name, cache_type, chats):
        """Сохранить чаты в кэш с названиями"""
        # Преобразуем чаты в формат {id: title} для быстрого доступа
        chats_dict = {}
        for chat in chats:
            if isinstance(chat, dict) and 'id' in chat and 'title' in chat:
                chats_dict[chat['id']] = chat['title']
            elif hasattr(chat, 'id') and hasattr(chat, 'title'):
                chats_dict[chat.id] = chat.title

        cache_data = {
            'session_name': session_name,
            'cache_type': cache_type,
            'timestamp': datetime.now().isoformat(),
            'chats': chats_dict  # Сохраняем как словарь {id: title}
        }

        cache_file = self._get_cache_path(session_name, cache_type)
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            print_clear(f"💾 Кэш сохранен: {len(chats_dict)} чатов с названиями")
        except Exception as e:
            print_clear(f"❌ Ошибка сохранения кэша: {e}")

    def save_chats_forever(self, session_name, cache_type, chats):
        """Сохранить чаты в кэш с названиями"""
        # Преобразуем список чатов в формат для сохранения
        chats_dict = {}
        for chat in chats:
            if isinstance(chat, dict) and 'id' in chat:
                # Сохраняем как [title, username, http]
                chats_dict[str(chat['id'])] = [
                    chat.get('title', 'Без названия'),
                    chat.get('username', ''),
                    chat.get('http', '')
                ]

        cache_data = {
            'session_name': session_name,
            'cache_type': cache_type,
            'timestamp': datetime.now().isoformat(),
            'chats': chats_dict
        }

        cache_file = self._get_cache_path(session_name, cache_type)
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            print_clear(f"💾 Кэш сохранен: {len(chats_dict)} чатов с названиями")
        except Exception as e:
            print_clear(f"❌ Ошибка сохранения кэша: {e}")


    def load_chats(self, session_name, cache_type, type_):
        """Загрузить чаты из кэша"""
        cache_file = self._get_cache_path(session_name, cache_type)

        if not os.path.exists(cache_file):
            return None

        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)

            # Проверяем свежесть кэша
            cache_time = datetime.fromisoformat(cache_data['timestamp'])
            cache_age = datetime.now() - cache_time

            if type_ == "default":
                if cache_age < timedelta(hours=3):
                    chats_dict = cache_data.get('chats', {})
                    print_clear(f"📁 Загружено из кэша: {len(chats_dict)} чатов с названиями")
                    return chats_dict
                else:
                    print_clear("🗑 Кэш устарел")
                    os.remove(cache_file)
                    return None

            elif type_ == 'forever':
                if cache_age < timedelta(hours=24):
                    chats_dict = cache_data.get('chats', {})
                    print_clear(f"📁 Загружено из кэша: {len(chats_dict)} чатов с названиями")
                    return chats_dict
                else:
                    print_clear("🗑 Кэш устарел")
                    os.remove(cache_file)
                    return None

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print_clear(f"❌ Ошибка загрузки кэша (поврежденный файл): {e}")
            try:
                os.remove(cache_file)
            except:
                pass
            return None
        except Exception as e:
            print_clear(f"❌ Ошибка загрузки кэша: {e}")
            return None

    def get_chat_title(self, session_name, cache_type, chat_id, type_):
        """Получить название чата из кэша"""
        chats_dict = self.load_chats(session_name, cache_type, type_ = type_)
        if chats_dict and str(chat_id) in chats_dict:
            return chats_dict[str(chat_id)]
        return None

    def main(self, session_name, cache_type):
        """Основной метод для получения чатов"""
        try:
            chats = self.load_chats(session_name=session_name, cache_type=cache_type)
            if chats:
                return chats
            return "кэша нет"
        except Exception as e:
            return f"ошибка: {e}"

    def get_cache_info(self, session_name=None):
        """Получить информацию о кэше"""
        cache_files = []
        for file in os.listdir(self.cache_dir):
            if file.endswith('.json'):
                file_path = os.path.join(self.cache_dir, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    cache_time = datetime.fromisoformat(data['timestamp'])
                    cache_age = datetime.now() - cache_time

                    chats_dict = data.get('chats', {})
                    chats_count = len(chats_dict)

                    cache_files.append({
                        'file': file,
                        'session': data.get('session_name'),
                        'type': data.get('cache_type'),
                        'chats_count': chats_count,
                        'age_minutes': int(cache_age.total_seconds() // 60),
                        'timestamp': data['timestamp']
                    })
                except:
                    continue

        if session_name:
            cache_files = [f for f in cache_files if f['session'] == session_name]

        return cache_files

    def clear_cache(self, session_name=None, cache_type=None):
        """Очистить кэш"""
        for file in os.listdir(self.cache_dir):
            if file.endswith('.json'):
                file_path = os.path.join(self.cache_dir, file)

                # Проверяем условия удаления
                should_delete = True
                if session_name and session_name not in file:
                    should_delete = False
                if cache_type and cache_type not in file:
                    should_delete = False

                if should_delete:
                    try:
                        os.remove(file_path)
                        print_clear(f"🗑 Удален: {file}")
                    except Exception as e:
                        print_clear(f"❌ Ошибка удаления {file}: {e}")

        print_clear(f"✅ Кэш удалён для {session_name, cache_type}")

    def remove_chat_from_cache(self, session_name, cache_type, chat_id):
        """Удаляет конкретный чат из кэша"""
        cache_file = self._get_cache_path(session_name, cache_type)

        if not os.path.exists(cache_file):
            return False

        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)

            chats_dict = cache_data.get('chats', {})

            # Удаляем чат из словаря
            chat_id_str = str(chat_id)
            if chat_id_str in chats_dict:
                removed_title = chats_dict.pop(chat_id_str)

                # Обновляем timestamp
                cache_data['timestamp'] = datetime.now().isoformat()
                cache_data['chats'] = chats_dict

                # Сохраняем обновленный кэш
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(cache_data, f, ensure_ascii=False, indent=2)

                print_clear(f"🗑 Удален из кэша {cache_type}: {removed_title} (ID: {chat_id})")
                return True
            else:
                return False

        except Exception as e:
            print_clear(f"❌ Ошибка удаления чата из кэша: {e}")
            return False

    def remove_chats_from_cache(self, session_name, cache_type, chat_ids):
        """Удаляет несколько чатов из кэша"""
        cache_file = self._get_cache_path(session_name, cache_type)

        if not os.path.exists(cache_file):
            return 0

        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)

            chats_dict = cache_data.get('chats', {})
            removed_count = 0

            # Удаляем чаты из словаря
            for chat_id in chat_ids:
                chat_id_str = str(chat_id)
                if chat_id_str in chats_dict:
                    removed_title = chats_dict.pop(chat_id_str)
                    removed_count += 1
                    print_clear(f"🗑 Удален из кэша {cache_type}: {removed_title} (ID: {chat_id})")

            if removed_count > 0:
                # Обновляем timestamp
                cache_data['timestamp'] = datetime.now().isoformat()
                cache_data['chats'] = chats_dict

                # Сохраняем обновленный кэш
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(cache_data, f, ensure_ascii=False, indent=2)

                print_clear(f"✅ Удалено {removed_count} чатов из кэша {cache_type}")

            return removed_count

        except Exception as e:
            print_clear(f"❌ Ошибка удаления чатов из кэша: {e}")
            return 0