# GS_diffusion: Project File Structure (v0.1 - Initial Setup)

This file describes the current file and directory structure of the `gs_diffusion` project to provide context for AI assistants.

```plaintext
gs_diffusion/
│
├── .git/                   # Git repository data
├── .gitignore              # Files and patterns ignored by Git
├── README.md               # Main documentation (user-facing)
├── requirements.txt        # Python package dependencies
├── config.yaml             # Project configuration (paths, parameters)
│
├── scripts/                # Entry point scripts
│   └── run_pipeline.py     # Main pipeline orchestrator script (initially basic)
│
├── gs_pipeline/            # Core project logic as a Python package
│   ├── __init__.py         # Makes gs_pipeline an importable package
│   └── utils.py            # Utility functions (config loading, etc. - initially basic)
│   # (Other module files like preprocessing.py will be added here during refactoring)
│
├── notebooks/              # (Optional) Jupyter notebooks
│   └── (empty or example .ipynb)
│
├── docs/                   # (Optional) Extended documentation
│   └── (empty or example .md, .png)
│
├── ai_meta/                # AI assistant metadata
│   ├── PROJECT_CONTEXT.md  # Detailed project context for AI
│   ├── REFACTORING_PLAN.md # Step-by-step refactoring plan
│   └── PROJECT_STRUCTURE.md # This file
│
└── output/                 # Directory for generated output (ignored by Git)
    └── (empty initially)