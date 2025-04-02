# GS_diffusion: Project Context for AI Assistants

## 1. Project Overview & Goals

* **Core Goal:** Implement and refine a pipeline transforming an input 3D model (represented as a 360-degree video render) into a stylized 3D Gaussian Splatting representation.
* **Methodology:**
    1.  Preprocess input video using TemporalKit (extract keyframes, potentially create collages).
    2.  Stylize keyframes using Stable Diffusion img2img via A1111 API (leveraging ControlNet for structure, Refiner for detail).
    3.  Prepare data for EbSynth using TemporalKit.
    4.  **[MANUAL STEP]** Run EbSynth GUI to propagate style changes to all frames.
    5.  Recombine EbSynth results using TemporalKit.
    6.  Prepare the stylized frame sequence for Gaussian Splatting (split train/test/val, create `transforms.json` files, potentially copy alpha channel).
    7.  Train a Gaussian Splatting model on the stylized frames.
    8.  Render the final 360-degree video from the trained GS model.
    9.  (Iterative Enhancement): The entire process can be looped, using the output video of one iteration as the input for the next.
* **Target Outcome:** A robust, reproducible, well-documented Python project suitable for a developer portfolio, demonstrating skills in pipeline orchestration, API integration, file manipulation, and working with ML/graphics tools.

## 2. Architecture & Structure (Target)

* **Root Directory (`gs_diffusion/`):** Contains config, readme, requirements, git files.
* **`config.yaml`:** Central configuration for ALL parameters and external paths (`a1111_extensions_dir`, `gaussian_splatting_dir`, `sd_api_url`, `fps`, `resolution`, SD params, etc.). **Crucial for reproducibility and AI context.**
* **`scripts/run_pipeline.py`:** Main entry point. Orchestrates the entire workflow by calling functions from the `gs_pipeline` package. Handles iteration logic. Loads config and sets up paths (including TemporalKit via `utils.setup_temporal_kit_path`).
* **`gs_pipeline/` (Package):** Houses the core logic, broken down by pipeline stage.
    * `utils.py`: Shared utilities - config loading, `subprocess` execution wrapper, `sys.path` setup for TemporalKit, file operations.
    * `preprocessing.py`: Handles initial video processing, calls `TemporalKit.generate_squares_to_folder`.
    * `stable_diffusion.py`: Handles interaction with A1111 img2img API, including ControlNet and Refiner payload construction.
    * `ebsynth_prep.py`: Prepares data structures/folders required by EbSynth, likely calling `TemporalKit.sort_into_folders`.
    * `ebsynth_recombine.py`: Processes output from EbSynth, calls `TemporalKit.crossfade_folder_of_folders` or `sd_utility.crossfade_videos`.
    * `gs_preparation.py`: Splits video into frames (ffmpeg via subprocess), handles alpha channel logic, splits data, generates `transforms_*.json`.
    * `gaussian_splatting.py`: Executes GS `train.py` and `render.py` via `subprocess`, manages `transforms_test.json` backup/restore. Replaces `gs.bat`.
    * `video_joiner.py`: Combines final rendered frames (from GS) into output video (ffmpeg via subprocess).
* **`output/`:** Directory for all generated data, structured by iteration (e.g., `output/iter1/`, `output/iter2/`). Ignored by Git.
* **`ai_meta/`:** This file, prompt templates.

## 3. Key Dependencies & Setup Notes

* **Python Environment:** Managed via `requirements.txt` (standard packages).
* **A1111 + TemporalKit:** Requires separate installation. Path to `extensions` folder must be set in `config.yaml`. `TemporalKit` functions are called via dynamic `sys.path` modification in `utils.setup_temporal_kit_path`.
* **Gaussian Splatting:** Requires separate installation/compilation (CUDA). Path to its root directory must be set in `config.yaml`. Executed via `subprocess`.
* **EbSynth:** Requires manual execution via GUI. The pipeline script (`run_pipeline.py`) should pause and prompt the user at the appropriate step.
* **ffmpeg:** Must be installed and in the system PATH or path provided in config.

## 4. Current Refactoring Plan & Priorities

1.  **Setup:** Initialize Git, create folder structure, setup basic files (`.gitignore`, `config.yaml`, `requirements.txt`, `README.md`, `ai_meta/PROJECT_CONTEXT.md`).
2.  **Configuration:** Populate `config.yaml` with all necessary paths and parameters. Implement config loading in `utils.py`.
3.  **Utilities:** Implement `utils.run_subprocess` and `utils.setup_temporal_kit_path`.
4.  **Orchestrator:** Create `scripts/run_pipeline.py`, implement argument parsing, config loading, path setup, iteration loop, and calls to (initially empty) functions for each pipeline step. Implement user prompt for EbSynth pause.
5.  **Module Refactoring (Iterative):**
    * Migrate logic from old scripts into corresponding `gs_pipeline/*.py` modules, creating functions that accept a `config` dictionary.
    * Replace hardcoded paths/params with values read from the `config` object.
    * Replace direct `sys.path.append` with reliance on `utils.setup_temporal_kit_path`.
    * Replace `gs.bat` logic with Python `subprocess` calls in `gaussian_splatting.py`.
    * Add basic error handling (`try...except`) around external calls (API, subprocess).
    * Add logging (using `logging` module) instead of just `print`.
    * Add docstrings and type hints.
6.  **Documentation:** Flesh out `README.md` with detailed installation and usage instructions.
7.  **(Future):** Add tests, more robust error handling, CI/CD, Docker.

## 5. AI Collaboration Workflow

* Use **Cursor IDE** for inline code generation, refactoring, debugging within files (`@File`, `@Symbol`).
* Use **ChatGPT** (with Custom Instructions and this context file) for architectural discussions, complex problem-solving, code reviews, strategic planning.
* Use **Gemini** (this chat) for interactive guidance, specific persona requests, cross-checking other AI suggestions.
* Break down tasks into small, specific requests for AI. Provide relevant code snippets and configuration context.
* Commit changes frequently using Git. Review and test all AI suggestions.