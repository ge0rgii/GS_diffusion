# GS_diffusion: Refactoring Plan (v0.2 - Initial files created)

**Goal:** Refactor the initial script collection into a structured, reproducible Python project using AI assistance.

**High-Level Steps:**

1.  [X] **Step 0: Project Initialization** (Git, Folders, Basic Files) - *Выполнено командами PowerShell*
2.  [ ] **Step 1: Configuration & Core Utilities** (`config.yaml`, `utils.py`)
3.  [ ] **Step 2: Pipeline Orchestrator** (`scripts/run_pipeline.py`)
4.  [ ] **Step 3: Module Refactoring (Iterative)**
    * [ ] 3.1: `gs_pipeline/preprocessing.py`
    * # ... (остальные подшаги) ...
5.  [ ] **Step 4: Documentation & Polishing** (`README.md`, Docstrings)
6.  [ ] **Step 5 (Future):** Testing, Advanced Error Handling, etc.

---

## Current Focus: Step 1 - Configuration & Core Utilities

**Overall Goal for Step 1:** Centralize configuration and create essential helper functions.

**Micro-Tasks for Step 1:**

* **Task 1.1: Populate `config.yaml`**
    * **Current State:** Empty `config.yaml` created. Old scripts exist in root.
    * **Target State:** `config.yaml` populated with parameters extracted from old scripts/bat, paths adjusted by user.
    * **Status:** [X] Done # <-- Отмечаем выполненным (после того как ты скопируешь YAML выше)

* **Task 1.2: Implement Config Loading (`utils.py`)**
    * **Current State:** Empty `gs_pipeline/utils.py`. File `config.yaml` exists and is populated.
    * **Target State:** `gs_pipeline/utils.py` contains a function `load_config(config_path="../config.yaml")` using `PyYAML` that reads the specified YAML file, handles potential `FileNotFoundError`, and returns the configuration as a Python dictionary. `PyYAML` added to `requirements.txt`.
    * **Status:** [ ] To Do # <-- Следующая задача

* **Task 1.3: Implement TemporalKit Path Setup (`utils.py`)**
    * ... (остальные задачи пока To Do) ...
* **Task 1.4: Implement Subprocess Utility (`utils.py`)**
    * ...