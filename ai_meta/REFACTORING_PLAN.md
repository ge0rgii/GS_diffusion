# GS_diffusion: Refactoring Plan (v0.3 - Environment Setup Added)

**Goal:** Refactor the initial script collection into a structured, reproducible Python project using AI assistance.

**High-Level Steps:**

1.  [X] **Step 0: Project Initialization** (Git, Folders, Basic Files) - *Done*
2.  [ ] **Step 1: Environment, Configuration & Core Utilities**
    * [ ] **Task 1.0: Setup Dedicated Virtual Environment** # <-- НОВЫЙ ШАГ
    * [X] **Task 1.1: Populate `config.yaml`** - *Done*
    * [ ] **Task 1.2: Implement Config Loading (`utils.py`)** # <-- ТЕКУЩИЙ ШАГ
    * [ ] **Task 1.3: Implement TemporalKit Path Setup (`utils.py`)**
    * [ ] **Task 1.4: Implement Subprocess Utility (`utils.py`)**
3.  [ ] **Step 2: Pipeline Orchestrator** (`scripts/run_pipeline.py`)
4.  [ ] **Step 3: Module Refactoring (Iterative)**
    * # ... (подшаги) ...
5.  [ ] **Step 4: Documentation & Polishing** (`README.md`, Docstrings)
6.  [ ] **Step 5 (Future):** Testing, Advanced Error Handling, etc.

---

## Current Focus: Step 1 - Environment, Configuration & Core Utilities

**Overall Goal for Step 1:** Create isolated environment, centralize configuration, create essential helpers.

* **Task 1.0: Setup Dedicated Virtual Environment**
    * **Current State:** Project folder exists with basic structure. No dedicated venv.
    * **Target State:** A Python virtual environment (e.g., `.venv`) created within the `GS_diffusion` project directory. `.venv` added to `.gitignore`. Environment is activated for subsequent commands.
    * **Status:** [X] To Do

* **Task 1.1: Populate `config.yaml`**
    * (...)
    * **Status:** [X] Done

* **Task 1.2: Implement Config Loading (`utils.py`)**
    * (...)
    * **Status:** [X] Done # <-- Ты только что это сделал (или сейчас сделаешь)

* **Task 1.3: Implement TemporalKit Path Setup (`utils.py`)**
    * **Current State:** `gs_pipeline/utils.py` содержит `load_config`.
    * **Target State:** `gs_pipeline/utils.py` содержит функцию `setup_temporal_kit_path(...)`. Добавлен `import sys`.
    * **Status:** [ ] To Do # <-- СЛЕДУЮЩИЙ ШАГ КОДИНГА

* **Task 1.4: Add Basic Tests for Utils**
    * (...)
    * **Status:** [X] Done # <-- Отмечаем!

* **Task 1.5: Implement Subprocess Utility (`utils.py`)**
    * **Current State:** `utils.py` содержит `load_config`, `setup_temporal_kit_path` и блок тестов. Старая функция `run_script` есть в `combined.txt`.
    * **Target State:** `gs_pipeline/utils.py` содержит новую, более гибкую и надежную функцию `run_subprocess(command_args: list, cwd: Optional[str] = None, env: Optional[dict] = None, capture_output: bool = False) -> tuple[int, str, str]`. Эта функция использует `subprocess.run`, умеет запускать команды в указанной директории (`cwd`), опционально передавать переменные окружения (`env`), захватывать вывод (`capture_output`), логирует команду и результат, обрабатывает `CalledProcessError` и возвращает код возврата, stdout и stderr. Старый `run_script` больше не используется. Добавлены тесты для `run_subprocess` в блок `if __name__ == "__main__":`.
    * **Status:** [ ] To Do # <-- Начинаем этот таск