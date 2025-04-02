# Final correct code for: gs_pipeline/utils.py

import os
import yaml
from typing import Dict, Any, List, Optional, Tuple
import sys
import shlex
import subprocess
import logging

# --- Configuration Loading ---

# Определяем путь к конфигу относительно папки gs_pipeline
_DEFAULT_CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../config.yaml"))

def load_config(config_path: str = _DEFAULT_CONFIG_PATH) -> Dict[str, Any]:
    """
    Загружает конфигурацию из YAML-файла.

    Args:
        config_path (str): Путь к файлу конфигурации.
                           По умолчанию используется 'config.yaml' в корне проекта.

    Returns:
        Dict[str, Any]: Словарь с загруженной конфигурацией.
                        Возвращает пустой словарь {} в случае ЛЮБОЙ ошибки при чтении или парсинге.
    """
    # Используем абсолютный путь для надежности и понятных сообщений об ошибках
    abs_config_path = os.path.abspath(config_path)

    if not os.path.exists(abs_config_path):
        # Используем logging вместо print для ошибок в библиотечных функциях
        logging.error(f"Файл конфигурации не найден: {abs_config_path}")
        return {}

    config_data: Dict[str, Any] = {}
    try:
        with open(abs_config_path, "r", encoding="utf-8") as f:
            # yaml.safe_load может вернуть None для пустого файла или файла с 'null'
            loaded_data = yaml.safe_load(f)
            if isinstance(loaded_data, dict): # Убедимся, что загружен именно словарь
                config_data = loaded_data
            elif loaded_data is None:
                logging.warning(f"Файл конфигурации '{abs_config_path}' пуст или содержит только null.")
                # Пустой файл - это нормально, возвращаем пустой словарь
                pass # config_data уже {}
            else:
                # Если YAML валидный, но не является словарем (напр., просто число или строка)
                logging.warning(f"Содержимое '{abs_config_path}' не является словарем (dict). Возвращен пустой конфиг.")
                # Возвращаем пустой словарь, т.к. ожидаем словарь конфигурации

    except yaml.YAMLError as e:
        logging.error(f"Ошибка парсинга YAML в файле '{abs_config_path}': {e}")
        return {}
    except IOError as e: # Явно ловим ошибки чтения/записи
        logging.error(f"Ошибка чтения файла '{abs_config_path}': {e}")
        return {}
    except Exception as e: # Ловим все остальные непредвиденные ошибки
        # Используем logger.exception для вывода traceback'а
        logging.exception(f"Неизвестная ошибка при загрузке '{abs_config_path}': {e}")
        return {}

    return config_data

# --- Path Setup ---

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
        logging.info("Пути TemporalKit уже были добавлены в sys.path.")
        return # Уже настроено

    # Безопасно получаем путь из вложенного словаря
    a1111_ext_dir = config.get('paths', {}).get('a1111_extensions_dir')

    if not a1111_ext_dir:
        logging.warning("Ключ 'paths.a1111_extensions_dir' отсутствует или пуст в config.yaml.")
        logging.warning("Импорт модулей TemporalKit НЕ будет настроен.")
        _temporal_kit_paths_added = True # Отмечаем, что пытались
        return

    # Нормализуем и проверяем путь к папке extensions
    a1111_ext_dir_abs = os.path.abspath(a1111_ext_dir)
    if not os.path.isdir(a1111_ext_dir_abs):
        logging.error(f"Указанный путь 'paths.a1111_extensions_dir' не существует или не папка:")
        logging.error(f"  '{a1111_ext_dir_abs}'")
        logging.error("Проверьте config.yaml. Импорт TemporalKit невозможен.")
        _temporal_kit_paths_added = True # Отмечаем
        # Можно пробросить исключение: raise FileNotFoundError(...)
        return

    # Формируем ожидаемые пути к TemporalKit
    tk_path = os.path.join(a1111_ext_dir_abs, "TemporalKit")
    tk_scripts_path = os.path.join(tk_path, "scripts")

    # Проверяем наличие папки TemporalKit
    if not os.path.isdir(tk_path):
        logging.error(f"Директория 'TemporalKit' не найдена по ожидаемому пути:")
        logging.error(f"  '{tk_path}'")
        logging.error("Убедитесь, что расширение TemporalKit установлено в A1111.")
        _temporal_kit_paths_added = True # Отмечаем
        # Можно пробросить исключение: raise FileNotFoundError(...)
        return

    # Добавляем пути в начало sys.path (более высокий приоритет)
    paths_added_count = 0
    # Сначала добавляем папку со скриптами, если она есть
    if os.path.isdir(tk_scripts_path):
        if tk_scripts_path not in sys.path:
            sys.path.insert(0, tk_scripts_path)
            logging.info(f"Добавлен путь TemporalKit/scripts в sys.path: {tk_scripts_path}")
            paths_added_count += 1
    else:
         logging.warning(f"Папка 'scripts' не найдена внутри TemporalKit: {tk_scripts_path}")

    # Потом основную папку TemporalKit
    if tk_path not in sys.path:
        sys.path.insert(0, tk_path)
        logging.info(f"Добавлен путь TemporalKit в sys.path: {tk_path}")
        paths_added_count += 1

    if paths_added_count == 0 and _temporal_kit_paths_added == False : # Проверяем флаг еще раз
         logging.info("Пути TemporalKit уже присутствовали в sys.path.")

    _temporal_kit_paths_added = True # Отмечаем, что настройка выполнена (или была попытка)


# --- Subprocess Execution ---

logger = logging.getLogger(__name__) # Logger для этого модуля

def run_subprocess(
    command_args: List[str],
    cwd: Optional[str] = None,
    env: Optional[dict] = None,
    capture_output: bool = False,
    check: bool = True
) -> Tuple[int, str, str]:
    """
    Запускает внешнюю команду (скрипт/программу) через subprocess.run и возвращает кортеж
    (return_code, stdout_str, stderr_str).
    (Полный docstring как в версии o1...)
    """
    # Логирование команды
    # Используем sys.executable для команд 'python', чтобы точно вызвать из venv
    cmd_to_log = list(command_args) # Копируем, чтобы не изменять оригинал
    if cmd_to_log[0] == 'python' and sys.executable:
         cmd_to_log[0] = sys.executable

    cmd_str = shlex.join(cmd_to_log) # Используем копию для лога
    log_prefix = f"(cwd='{cwd}')" if cwd else ""
    logger.info(f"Запуск команды: {cmd_str} {log_prefix}")

    # Подготавливаем окружение
    merged_env = None
    if env is not None:
        merged_env = os.environ.copy()
        merged_env.update(env)

    # Настраиваем параметры для subprocess.run
    run_kwargs = {
        "cwd": cwd,
        "env": merged_env,
        "check": False, # <--- Важно: ВСЕГДА check=False здесь, мы сами проверим код возврата
        "capture_output": capture_output,
        "text": capture_output # text=True имеет смысл только если capture_output=True
        # Добавляем кодировку для Windows на всякий случай
        # "encoding": 'utf-8' if capture_output else None, # Может вызвать проблемы на некоторых системах
        # "errors": 'replace' if capture_output else None
    }
    # Если не захватываем вывод, он пойдет в консоль родителя
    # stdout=None (по умолч.), stderr=None (по умолч.)

    stdout_str = ""
    stderr_str = ""
    return_code = 1 # По умолчанию считаем, что ошибка

    try:
        result = subprocess.run(command_args, **run_kwargs) # Запускаем с check=False
        return_code = result.returncode
        if capture_output:
            stdout_str = result.stdout or ""
            stderr_str = result.stderr or ""

        if return_code == 0:
             logger.info(f"Команда успешно завершена (код {return_code}): {cmd_str}")
        else:
             # Логируем ошибку, даже если check=False
             logger.error(f"Команда завершилась с ошибкой (код {return_code}): {cmd_str}")
             if capture_output and stderr_str:
                  logger.error(f"Stderr:\n{stderr_str.strip()}")
             # Если check=True в аргументах функции, возбуждаем исключение
             if check:
                  raise subprocess.CalledProcessError(return_code, command_args, output=stdout_str, stderr=stderr_str)

    except FileNotFoundError as e:
         # Если сама команда не найдена
         logger.error(f"Ошибка выполнения: Команда или файл не найдены: '{command_args[0]}'")
         logger.debug(e) # Выводим детали ошибки в debug
         stderr_str = f"FileNotFoundError: {e}"
         return_code = 1 # Стандартный код ошибки для FileNotFoundError
         if check: raise # Перевыбрасываем, если check=True

    except subprocess.CalledProcessError as e:
         # Этот блок сработает только если мы вызвали raise выше при check=True
         # Мы уже залогировали ошибку перед raise, просто перевыбрасываем
         logger.error(f"Перехвачено CalledProcessError (код {e.returncode}) для команды: {cmd_str}")
         # Возвращаем значения из исключения
         return e.returncode, (e.stdout or ""), (e.stderr or "")

    except Exception as e: # Ловим все остальные ошибки (например, PermissionError)
        logger.exception(f"Неожиданная ошибка при выполнении команды: {cmd_str}")
        stderr_str = f"{type(e).__name__}: {str(e)}"
        return_code = 1 # Общий код ошибки
        if check: raise # Перевыбрасываем, если check=True

    return return_code, stdout_str, stderr_str


# --- Basic Testing Block ---

if __name__ == "__main__":
    print("\n--- Запуск тестов для utils.py ---")
    # Настроим базовое логирование СРАЗУ
    logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')

    # --- Тест load_config ---
    print("\n[Тест 1] Загрузка реального config.yaml...")
    actual_config_path = _DEFAULT_CONFIG_PATH
    config = load_config(actual_config_path)
    if isinstance(config, dict) and config:
        print("  УСПЕХ: config.yaml загружен.")
        print(f"    Путь к A1111 extensions: {config.get('paths', {}).get('a1111_extensions_dir', 'НЕ НАЙДЕНО')}")
        print(f"    FPS: {config.get('pipeline_settings', {}).get('fps', 'НЕ НАЙДЕНО')}")
    elif config == {}:
         logging.warning("load_config вернул пустой словарь. Проверьте путь и содержимое config.yaml.")
         print("  ПРОВЕРКА: load_config вернул {}. Проверьте логи.")
    else:
        logging.error(f"load_config вернул НЕ словарь: {type(config)}")
        print(f"  !!! ОШИБКА: load_config вернул НЕ словарь: {type(config)}")

    print("\n[Тест 2] Загрузка несуществующего файла...")
    non_existent_config = load_config("invalid_path/non_existent_config.yaml")
    if non_existent_config == {}:
        print("  УСПЕХ: Корректно вернулся пустой словарь для несуществующего файла.")
    else:
        print("  !!! ОШИБКА: Не вернулся пустой словарь для несуществующего файла.")

    # --- Тест setup_temporal_kit_path ---
    print("\n[Тест 3] Настройка путей TemporalKit...")
    if isinstance(config, dict) and config:
        _temporal_kit_paths_added = False # Сброс флага для теста
        initial_path_len = len(sys.path)
        print(f"  Длина sys.path до вызова: {initial_path_len}")
        setup_temporal_kit_path(config)
        first_call_path_len = len(sys.path)
        print(f"  Длина sys.path после первого вызова: {first_call_path_len}")
        print("  Повторный вызов setup_temporal_kit_path...")
        setup_temporal_kit_path(config) # Флаг должен сработать
        second_call_path_len = len(sys.path)
        print(f"  Длина sys.path после второго вызова: {second_call_path_len}")
        if second_call_path_len == first_call_path_len and first_call_path_len >= initial_path_len :
            print("  УСПЕХ: Повторный вызов не изменил sys.path (флаг работает).")
        else:
             print("  !!! ОШИБКА: Длина sys.path изменилась при повторном вызове или пути не добавились!")
    else:
        print("  Пропуск теста setup_temporal_kit_path, так как конфиг не загружен.")

    # --- Тест run_subprocess ---
    print("\n[Тест 4] Запуск 'python --version' с захватом вывода...")
    # Используем sys.executable, чтобы точно вызвать python из активного venv
    rc4, out4, err4 = run_subprocess([sys.executable, "--version"], capture_output=True)
    print(f"  Код: {rc4}, Вывод: '{out4.strip()}', Ошибка: '{err4.strip()}'")
    if rc4 == 0 and "Python" in out4:
        print("  УСПЕХ: Команда выполнена, версия Python получена.")
    else:
        print("  !!! ОШИБКА: Не удалось получить версию Python.")

    print("\n[Тест 5] Запуск несуществующей команды (check=False)...")
    rc5, out5, err5 = run_subprocess(["несуществующая_команда_123"], capture_output=True, check=False)
    print(f"  Код: {rc5}, Вывод: '{out5.strip()}', Ошибка: '{err5.strip()}'")
    if rc5 != 0 and "FileNotFoundError" in err5: # Проверяем код и тип ошибки в stderr
        print("  УСПЕХ: Корректно обработана ошибка несуществующей команды (код != 0, FileNotFoundError).")
    else:
        print("  !!! ОШИБКА: Неверный код или тип ошибки для несуществующей команды.")

    print("\n[Тест 6] Запуск команды с ошибкой (check=True, capture=True)...")
    # Используем python для генерации ненулевого кода возврата
    cmd_to_fail = [sys.executable, "-c", "import sys; sys.exit(55)"] # Пример кода ошибки 55
    # Ожидаем, что функция поймает CalledProcessError и вернет код/вывод
    rc6, out6, err6 = run_subprocess(cmd_to_fail, capture_output=True, check=True)
    print(f"  Код: {rc6}, Вывод: '{out6.strip()}', Ошибка: '{err6.strip()}'")
    if rc6 == 55:
         print("  УСПЕХ: Ошибка выполнения команды (код 55) поймана и возвращен верный код.")
    else:
         print(f"  !!! ОШИБКА: Ожидался код возврата 55, получен {rc6}.")

    print("\n[Тест 7] Запуск 'python --version' (проверка лога, без захвата)...")
    rc7, _, _ = run_subprocess([sys.executable, "--version"])
    if rc7 == 0:
         print("  УСПЕХ: Команда выполнена (проверь лог INFO).")
    else:
         print("  !!! ОШИБКА: Команда завершилась с ошибкой.")


    print("\n[Тест 8] Запуск команды с ошибкой (check=True, проверка лога ошибки)...")
    # Используем ту же команду, что и в Тесте 6
    rc8, _, _ = run_subprocess(cmd_to_fail, check=True)
    if rc8 == 55:
        print("  УСПЕХ: Команда завершилась с ожидаемым кодом ошибки 55 (проверь лог ERROR).")
    else:
        print(f"  !!! ОШИБКА: Ожидался код возврата 55, получен {rc8}.")

    print("\n--- Тестирование utils.py завершено ---")