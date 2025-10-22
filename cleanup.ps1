# 🧹 AUTOMATED CLEANUP SCRIPT
# Removes duplicate, obsolete, and test files
# Organizes project for Phase 2

Write-Host "`n=== Quantum-Seed ImageShield - Project Cleanup ===" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "`nThis will remove:" -ForegroundColor Yellow
Write-Host "  [X] Test output files (*.png, *.npz in root)" -ForegroundColor Gray
Write-Host "  [X] Python cache folders (__pycache__)" -ForegroundColor Gray
Write-Host "  [X] Duplicate test folder" -ForegroundColor Gray
Write-Host "  [X] Duplicate documentation" -ForegroundColor Gray
Write-Host "  [X] Old/obsolete files" -ForegroundColor Gray
Write-Host "`nWARNING: This action CANNOT be undone!" -ForegroundColor Red

$confirm = Read-Host "`nProceed with cleanup? (yes/no)"

if ($confirm -ne "yes") {
    Write-Host "`n[X] Cleanup cancelled." -ForegroundColor Red
    exit
}

Write-Host "`n>>> Starting cleanup...`n" -ForegroundColor Green

# Phase 1: Remove test outputs in root
Write-Host "[Phase 1] Removing test outputs..." -ForegroundColor Cyan
$testFiles = @(
    "decrypted_output.png",
    "encrypted_output.png",
    "encrypted_fast.png",
    "encrypted_output_keys.npz",
    "encrypted_fast_keys.npz"
)

foreach ($file in $testFiles) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-Host "  [OK] Removed: $file" -ForegroundColor Green
    }
}

# Phase 2: Remove __pycache__ folders
Write-Host "`n[Phase 2] Removing Python cache..." -ForegroundColor Cyan
$cacheDirs = @(
    "__pycache__",
    "quantum_image_shield\__pycache__",
    "tests\__pycache__"
)

foreach ($dir in $cacheDirs) {
    if (Test-Path $dir) {
        Remove-Item $dir -Recurse -Force
        Write-Host "  [OK] Removed: $dir" -ForegroundColor Green
    }
}

# Phase 3: Remove duplicate docs
Write-Host "`n[Phase 3] Removing duplicate documentation..." -ForegroundColor Cyan
if (Test-Path "QUICK_START.md") {
    Remove-Item "QUICK_START.md" -Force
    Write-Host "  [OK] Removed: QUICK_START.md (use HOW_TO_TEST.md)" -ForegroundColor Green
}

# Phase 4: Remove old tests folder (keep quantum_image_shield/tests/)
Write-Host "`n[Phase 4] Removing duplicate tests folder..." -ForegroundColor Cyan
if (Test-Path "tests") {
    Remove-Item "tests" -Recurse -Force
    Write-Host "  [OK] Removed: tests/ (keeping quantum_image_shield/tests/)" -ForegroundColor Green
}

# Phase 5: Clean quantum_image_shield internals
Write-Host "`n[Phase 5] Cleaning package internals..." -ForegroundColor Cyan
$packageCleanup = @(
    "quantum_image_shield\README.md",
    "quantum_image_shield\requirements.txt"
)

foreach ($file in $packageCleanup) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-Host "  [OK] Removed: $file" -ForegroundColor Green
    }
}

# Phase 6: Clean examples folder
Write-Host "`n[Phase 6] Cleaning examples folder..." -ForegroundColor Cyan
$exampleCleanup = @(
    "examples\example_usage_old.py",
    "examples\demo_screenshots.py",
    "examples\streamlit_app.py",
    "examples\encrypted_image.png",
    "examples\encryption_keys.npz",
    "examples\decrypted_image.png",
    "examples\sample_image.png"
)

foreach ($file in $exampleCleanup) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-Host "  [OK] Removed: $file" -ForegroundColor Green
    }
}

# Phase 7: Clean docs folder
Write-Host "`n[Phase 7] Cleaning docs folder..." -ForegroundColor Cyan
$docsCleanup = @(
    "docs\IMPLEMENTATION_SUMMARY.md",
    "docs\MERGE_PLAN.md",
    "docs\PROJECT_SUMMARY.md",
    "docs\USAGE.md"
)

foreach ($file in $docsCleanup) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-Host "  [OK] Removed: $file" -ForegroundColor Green
    }
}

# Phase 8: Update .gitignore
Write-Host "`n[Phase 8] Updating .gitignore..." -ForegroundColor Cyan
$gitignoreContent = @"
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Unit test / coverage
.pytest_cache/
.coverage
.coverage.*
htmlcov/
.tox/
.nox/

# Virtual environments
venv/
ENV/
env/
.venv

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# Test outputs (keep samples/)
encrypted*.png
decrypted*.png
*.npz

# OS
.DS_Store
Thumbs.db

# Logs
*.log
"@

Set-Content -Path ".gitignore" -Value $gitignoreContent
Write-Host "  [OK] Updated: .gitignore" -ForegroundColor Green

# Summary
Write-Host "`n" + "=" * 60 -ForegroundColor Cyan
Write-Host "[SUCCESS] CLEANUP COMPLETE!" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan

Write-Host "`nSummary:" -ForegroundColor Cyan
Write-Host "  [OK] Removed test outputs" -ForegroundColor White
Write-Host "  [OK] Removed Python cache" -ForegroundColor White
Write-Host "  [OK] Removed duplicate files" -ForegroundColor White
Write-Host "  [OK] Cleaned package structure" -ForegroundColor White
Write-Host "  [OK] Updated .gitignore" -ForegroundColor White

Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "  1. Review CLEANUP_AUDIT.md for details" -ForegroundColor White
Write-Host "  2. Test encryption still works:" -ForegroundColor White
Write-Host "     python -m quantum_image_shield.cli encrypt samples/sample_image.png test.png" -ForegroundColor Gray
Write-Host "  3. Commit changes to git" -ForegroundColor White
Write-Host "  4. Proceed to Phase 2 (Golang backend)" -ForegroundColor White

Write-Host "`nYour project is now clean and ready for Phase 2!`n" -ForegroundColor Magenta
