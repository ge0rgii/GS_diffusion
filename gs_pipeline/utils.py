# In gs_pipeline/utils.py
import os
import yaml
from typing import Dict, Any
import sys

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


_temporal_kit_paths_added = False # Флаг, чтобы не добавлять пути многократно

def setup_temporal_kit_path(config: Dict[str, Any]):
    """
    Добавляет путь к папке расширения TemporalKit (из конфига) в sys.path.

    Вызывается один раз в начале основного скрипта для возможности импорта
    модулей TemporalKit (например, Ebsynth_Processing, berry_utility)
    из других частей проекта.

    Args:
        config (Dict[str, Any]): Загруженный словарь конфигурации,
                                 должен содержать ключ 'paths.a1111_extensions_dir'.
    """
    global _temporal_kit_paths_added
    if _temporal_kit_paths_added:
        print("INFO: Пути TemporalKit уже были добавлены в sys.path.")
        return # Уже настроено

    # Безопасно получаем путь из вложенного словаря
    a1111_ext_dir = config.get('paths', {}).get('a1111_extensions_dir')

    if not a1111_ext_dir:
        print("ПРЕДУПРЕЖДЕНИЕ: Ключ 'paths.a1111_extensions_dir' отсутствует или пуст в config.yaml.")
        print("                 Импорт модулей TemporalKit НЕ будет настроен.")
        _temporal_kit_paths_added = True # Отмечаем, что пытались
        return

    # Нормализуем и проверяем путь к папке extensions
    a1111_ext_dir_abs = os.path.abspath(a1111_ext_dir)
    if not os.path.isdir(a1111_ext_dir_abs):
        print(f"ОШИБКА: Указанный путь 'paths.a1111_extensions_dir' не существует или не является папкой:")
        print(f"         '{a1111_ext_dir_abs}'")
        print("         Проверьте config.yaml. Импорт TemporalKit невозможен.")
        _temporal_kit_paths_added = True # Отмечаем
        # Можно здесь пробросить исключение, если это критично для работы:
        # raise FileNotFoundError(f"Папка расширений A1111 не найдена: {a1111_ext_dir_abs}")
        return

    # Формируем ожидаемые пути к TemporalKit
    tk_path = os.path.join(a1111_ext_dir_abs, "TemporalKit")
    tk_scripts_path = os.path.join(tk_path, "scripts")

    # Проверяем наличие папки TemporalKit
    if not os.path.isdir(tk_path):
        print(f"ОШИБКА: Директория 'TemporalKit' не найдена по ожидаемому пути:")
        print(f"         '{tk_path}'")
        print("         Убедитесь, что расширение TemporalKit установлено в A1111 и путь в config.yaml верный.")
        _temporal_kit_paths_added = True # Отмечаем
        # Можно пробросить исключение:
        # raise FileNotFoundError(f"Папка TemporalKit не найдена: {tk_path}")
        return

    # Добавляем пути в начало sys.path (более высокий приоритет)
    paths_added_count = 0
    # Сначала добавляем папку со скриптами, если она есть
    if os.path.isdir(tk_scripts_path):
        if tk_scripts_path not in sys.path:
            sys.path.insert(0, tk_scripts_path)
            print(f"INFO: Добавлен путь TemporalKit/scripts в sys.path: {tk_scripts_path}")
            paths_added_count += 1
    else:
         print(f"ПРЕДУПРЕЖДЕНИЕ: Папка 'scripts' не найдена внутри TemporalKit: {tk_scripts_path}")

    # Потом основную папку TemporalKit
    if tk_path not in sys.path:
        sys.path.insert(0, tk_path)
        print(f"INFO: Добавлен путь TemporalKit в sys.path: {tk_path}")
        paths_added_count += 1

    if paths_added_count == 0:
        print("INFO: Пути TemporalKit уже присутствовали в sys.path.")

    _temporal_kit_paths_added = True # Отмечаем, что настройка выполнена (или была попытка)