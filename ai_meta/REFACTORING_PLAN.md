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
    * **Target State:** `gs_pipeline/utils.py` contains `load_config(...)`. `PyYAML` installed in the dedicated venv and added to `requirements.txt`.
    * **Status:** [ ] To Do # <-- Фактическая следующая задача ПОСЛЕ создания venv

* **Task 1.3: Implement TemporalKit Path Setup (`utils.py`)**
    * (...) Status: [ ] To Do
* **Task 1.4: Implement Subprocess Utility (`utils.py`)**
    * (...) Status: [ ] To Do