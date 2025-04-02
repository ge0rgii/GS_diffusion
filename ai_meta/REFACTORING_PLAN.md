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
    * **Current State:** Empty `gs_pipeline/utils.py`. `config.yaml` populated. Dedicated venv exists and is activated.
    * **Target State:** `gs_pipeline/utils.py` contains a function `load_config(...)` using `PyYAML` that reads the specified YAML file, handles potential `FileNotFoundError` and `yaml.YAMLError`, and returns the configuration as a Python dictionary. `PyYAML` installed in the dedicated venv and added to `requirements.txt`.
    * **Status:** [X] Done # <-- Отмечаем!

* **Task 1.3: Implement TemporalKit Path Setup (`utils.py`)**
    * **Current State:** `gs_pipeline/utils.py` содержит функцию `load_config`.
    * **Target State:** `gs_pipeline/utils.py` содержит функцию `setup_temporal_kit_path(config)`, которая читает `paths.a1111_extensions_dir` из словаря `config`, проверяет существование путей к `TemporalKit` и `TemporalKit/scripts`, добавляет их в `sys.path` через `sys.path.insert(0, ...)`. Функция использует глобальный флаг `_temporal_kit_paths_added`, чтобы выполняться только один раз, и выводит информационные сообщения или ошибки. Добавлен `import sys`.
    * **Status:** [X] To Do # <-- Начинаем этот таск

* **Task 1.4: Implement Subprocess Utility (`utils.py`)**
    * (...) Status: [ ] To Do