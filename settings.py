import os
from data.log import logger

class Settings:
    """Класс для работы с настройками бота"""

    def __init__(self):
        self.default_config = {
            "time_per_message": 15,
            "messages_per_cycle": 5,
            "delay_between_messages": 60,
            "delay_between_sessions": 120
        }
        self.config = self.default_config.copy()
        self.settings_path = self._get_settings_path()

    @staticmethod
    def _get_settings_path():
        """Находит путь к файлу настроек в той же директории, где находится скрипт"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        settings_path = os.path.join(script_dir, 'settings.txt')
        return settings_path

    def create_default_settings(self):
        """Создает файл с настройками по умолчанию"""
        default_settings = """# Настройки бота для рассылки

# Количество сессий (циклов) работы
messages_per_session=15

# Количества сообщений за один цикл
messages_per_cycle=5

# Задержка в секундах в цикле за один шаг
delay_between_messages=60

# Задержка в секундах между переключением сессий
delay_between_sessions=120
"""
        try:
            with open(self.settings_path, 'w', encoding='utf-8') as file:
                file.write(default_settings)
            logger.info(f"📁 Создан файл настроек: {self.settings_path}")
            logger.info("⚙️ Пожалуйста, настройте параметры в settings.txt и перезапустите бота")
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка создания файла настроек: {e}")
            return False

    def load_config(self):
        """Загрузка конфигурации из TXT файла"""
        try:
            # Проверяем существование файла
            if not os.path.exists(self.settings_path):
                logger.warning(f"📁 Файл настроек не найден: {self.settings_path}")
                if self.create_default_settings():
                    # После создания файла загружаем настройки по умолчанию
                    self.config = self.default_config.copy()
                    logger.info(f"📁 Используем значения по умолчанию")
                return

            # Читаем настройки из файла
            with open(self.settings_path, 'r', encoding='utf-8') as file:
                loaded_config = self.default_config.copy()

                for line in file:
                    line = line.strip()
                    # Пропускаем пустые строки и комментарии
                    if not line or line.startswith('#'):
                        continue

                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()

                        # Преобразуем числовые значения
                        if key in self.default_config:
                            if isinstance(self.default_config[key], int):
                                try:
                                    loaded_config[key] = int(value)
                                except ValueError:
                                    logger.warning(
                                        f"⚠️ Неверное значение для {key}: '{value}', использую значение по умолчанию: {self.default_config[key]}")
                            elif isinstance(self.default_config[key], float):
                                try:
                                    loaded_config[key] = float(value)
                                except ValueError:
                                    logger.warning(
                                        f"⚠️ Неверное значение для {key}: '{value}', использую значение по умолчанию: {self.default_config[key]}")
                            else:
                                loaded_config[key] = value
                        else:
                            logger.warning(f"⚠️ Неизвестный параметр в настройках: {key}")

                self.config = loaded_config

            logger.info(f"✅ Настройки загружены из: {self.settings_path}")

        except Exception as e:
            logger.error(f"❌ Ошибка загрузки настроек из {self.settings_path}: {e}")
            logger.info("🔄 Использую настройки по умолчанию")
            self.config = self.default_config.copy()

    def get(self, key, default=None):
        """Получить значение настройки"""
        return self.config.get(key, default)

    def validate_config(self):
        """Проверка валидности конфигурации"""
        errors = []

        # Проверка числовых значений
        if self.config['min_messages_per_cycle'] > self.config['max_messages_per_cycle']:
            errors.append("min_messages_per_cycle не может быть больше max_messages_per_cycle")

        if self.config['messages_per_session'] <= 0:
            errors.append("messages_per_session должен быть больше 0")


        return errors


