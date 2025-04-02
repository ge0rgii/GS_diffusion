# In gs_pipeline/utils.py
import os
import yaml
from typing import Dict, Any

_DEFAULT_CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../config.yaml"))

def load_config(config_path: str = _DEFAULT_CONFIG_PATH) -> Dict[str, Any]:
    """
    Загружает конфигурацию из YAML-файла.
    Args: ... Returns: ... (Возвращает {} при ЛЮБОЙ ошибке)
    """
    abs_config_path = os.path.abspath(config_path)
    if not os.path.exists(abs_config_path):
        print(f"ОШИБКА: файл конфигурации не найден: {abs_config_path}")
        return {}

    config_data: Dict[str, Any] = {}
    try:
        with open(abs_config_path, "r", encoding="utf-8") as f:
            loaded_data = yaml.safe_load(f)
            if isinstance(loaded_data, dict): # <--- Явная проверка типа dict
                 config_data = loaded_data
            elif loaded_data is None:
                 pass # Пустой файл - ок, вернем {}
            else:
                 # Загрузилось что-то валидное, но не словарь
                 print(f"ПРЕДУПРЕЖДЕНИЕ: Содержимое '{abs_config_path}' не является словарем.")
                 # Вернем {}, т.к. ожидаем словарь

    except yaml.YAMLError as e:
        print(f"ОШИБКА парсинга YAML...: {e}")
        return {}
    except IOError as e: # <--- Явный отлов ошибки чтения файла
        print(f"ОШИБКА чтения файла...: {e}")
        return {}
    except Exception as e: # Ловим все остальное
        print(f"НЕИЗВЕСТНАЯ ОШИБКА при загрузке...: {e}")
        return {}

    return config_data