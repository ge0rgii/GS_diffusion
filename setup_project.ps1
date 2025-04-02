# setup_project.ps1

# --- Создание основных директорий ---
Write-Host "Creating directories..."
New-Item -ItemType Directory -Path "scripts" -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path "gs_pipeline" -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path "ai_meta" -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path "output" -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path "docs" -ErrorAction SilentlyContinue      # Опционально, но полезно
New-Item -ItemType Directory -Path "notebooks" -ErrorAction SilentlyContinue # Опционально
Write-Host "Directories created."

# --- Создание базовых файлов в корне проекта ---
Write-Host "Creating root files..."
New-Item -ItemType File -Path "config.yaml" -ErrorAction SilentlyContinue
New-Item -ItemType File -Path "requirements.txt" -ErrorAction SilentlyContinue
New-Item -ItemType File -Path ".gitignore" -ErrorAction SilentlyContinue
# Если у тебя уже есть README.md со старым описанием, можно его переименовать:
# Move-Item -Path "README.md" -Destination "README_OLD.md" -ErrorAction SilentlyContinue
New-Item -ItemType File -Path "README.md" -ErrorAction SilentlyContinue # Создаем новый пустой README
Write-Host "Root files created."

# --- Создание файлов внутри директорий ---
Write-Host "Creating files inside directories..."
New-Item -ItemType File -Path "scripts/run_pipeline.py" -ErrorAction SilentlyContinue
New-Item -ItemType File -Path "gs_pipeline/__init__.py" -ErrorAction SilentlyContinue
New-Item -ItemType File -Path "gs_pipeline/utils.py" -ErrorAction SilentlyContinue
New-Item -ItemType File -Path "ai_meta/PROJECT_CONTEXT.md" -ErrorAction SilentlyContinue
New-Item -ItemType File -Path "ai_meta/REFACTORING_PLAN.md" -ErrorAction SilentlyContinue
New-Item -ItemType File -Path "ai_meta/PROJECT_STRUCTURE.md" -ErrorAction SilentlyContinue
Write-Host "Internal files created."

# --- Добавление базового содержимого в .gitignore ---
Write-Host "Adding content to .gitignore..."
# Используем Set-Content, чтобы перезаписать файл, если он уже существует и содержит что-то
# Если нужно именно добавлять, используй Add-Content
Set-Content -Path ".gitignore" -Value @"
# Python
__pycache__/
*.py[cod]
*$py.class

# Virtual environment
venv/
*.env
.env.*

# Output directory
output/

# OS generated files
.DS_Store
Thumbs.db

# IDE files
.vscode/
.idea/

# Temporary files
*.bak
batch_settings.txt
transition_data.txt
"@
Write-Host ".gitignore populated."

# --- Инициализация Git репозитория (раскомментируй, если нужно) ---
# Write-Host "Initializing Git repository..."
# git init
# Write-Host "Git repository initialized."

Write-Host "---------------------------------------------------------"
Write-Host "Project structure setup complete in the current directory!"
Write-Host "Remember to populate the files in ai_meta and config.yaml."
Write-Host "---------------------------------------------------------"