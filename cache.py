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

    def load_chats(self, session_name, cache_type, max_age_hours=1):
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

            if cache_age < timedelta(hours=max_age_hours):
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

    def get_chat_title(self, session_name, cache_type, chat_id):
        """Получить название чата из кэша"""
        chats_dict = self.load_chats(session_name, cache_type)
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