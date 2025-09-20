import configparser
import os

# Получаем путь к корневой директории проекта
project_root = os.path.dirname(os.path.abspath(__file__))  # Директория текущего файла входит в дирикторю
# Поднимаемся на уровень выше (из functions_ в корень) выходит из дириктории и попадает в корень
project_root = os.path.dirname(project_root)

# Правильный путь к config.json
config_full_path = os.path.join(project_root, "config.cfg")


def load_config(config_path=config_full_path):
    """Создание клиента Pyrogram из конфига"""
    config = configparser.ConfigParser()

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file {config_path} not found")

    config.read(config_path, encoding='utf-8')

    return config

# Использование
config = load_config()
for i in config.sections():
    print(i)
# Получение значений
api_id = config.getint('Telegram', 'api_id')
api_hash = config.get('Telegram', 'api_hash')
debug_mode = config.getboolean('Settings', 'debug_mode')
admin_ids = [int(x.strip()) for x in config.get('Settings', 'admin_ids').split(',')]

print(f"API ID: {api_id}")
print(f"Debug mode: {debug_mode}")
print(f"Admin IDs: {admin_ids}")