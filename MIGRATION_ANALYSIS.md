# Migration Plan: Make quantum_image_shield/ the Root

## 🎯 Goal
Move everything FROM `quantum_image_shield/` subfolder TO root, making it the main project.

## 📋 Current Structure
```
quantum-image-shield/              ← Current root
├── quantum_image_shield/          ← Package (what we want as root)
│   ├── __init__.py
│   ├── cli.py
│   ├── encryption.py
│   ├── decryption.py
│   ├── quantum_key_generator.py
│   ├── security.py
│   ├── validators.py
│   └── __pycache__/
├── examples/
├── tests/
├── scripts/
├── samples/
├── docs/
├── requirements.txt
├── README.md
├── setup.py
└── ... (other files)
```

## 🎯 Target Structure
```
quantum-image-shield/              ← New root
├── __init__.py                    ← From quantum_image_shield/
├── cli.py                         ← From quantum_image_shield/
├── encryption.py                  ← From quantum_image_shield/
├── decryption.py                  ← From quantum_image_shield/
├── quantum_key_generator.py       ← From quantum_image_shield/
├── security.py                    ← From quantum_image_shield/
├── validators.py                  ← From quantum_image_shield/
├── examples/                      ← Keep
├── tests/                         ← Keep & update imports
├── scripts/                       ← Keep
├── samples/                       ← Keep
├── docs/                          ← Keep
├── requirements.txt               ← Keep
├── README.md                      ← Keep
├── setup.py                       ← Keep & update
└── .gitignore                     ← Keep
```

## ✅ Files to KEEP from Root
- requirements.txt
- requirements-dev.txt
- README.md
- LICENSE
- .gitignore
- setup.py (needs update)
- pyproject.toml (needs update)

## ❌ Files to DELETE from Root
- batch_encrypt.py (utility script - move to scripts/)
- verify.py (utility script - move to scripts/)
- verify_test.py (test - move to tests/)
- .prompts (editor config - not needed)
- All duplicate .md files (already in docs/)

## 🔄 Migration Steps

### Step 1: Move quantum_image_shield/* to root
```powershell
# Move all Python files from quantum_image_shield/ to root
Move-Item quantum_image_shield/*.py .
Move-Item quantum_image_shield/__pycache__ . -ErrorAction SilentlyContinue
```

### Step 2: Update imports everywhere
Since files are now in root, change:
```python
# OLD
from quantum_image_shield import ImageEncryptor
from quantum_image_shield.security import SecureKeyStorage

# NEW  
from encryption import ImageEncryptor
from security import SecureKeyStorage
```

Files needing import updates:
- `tests/test_*.py` (all test files)
- `examples/*.py` (all example files)
- `cli.py` itself (internal imports change from `.xxx` to `xxx`)
- `__init__.py` (exports change)

### Step 3: Update setup.py
Change:
```python
# OLD
packages=find_packages()  # Would find quantum_image_shield/

# NEW
py_modules=[
    'cli',
    'encryption',
    'decryption',
    'quantum_key_generator',
    'security',
    'validators',
]
```

### Step 4: Clean up
```powershell
# Remove now-empty quantum_image_shield/ directory
Remove-Item quantum_image_shield -Recurse -Force

# Move utility scripts
Move-Item batch_encrypt.py scripts/
Move-Item verify.py scripts/
Move-Item verify_test.py tests/
```

## ⚠️ Breaking Changes

### Import statements change EVERYWHERE:
```python
# Before
from quantum_image_shield import ImageEncryptor, ImageDecryptor
from quantum_image_shield.security import SecureKeyStorage

# After
from encryption import ImageEncryptor
from decryption import ImageDecryptor
from security import SecureKeyStorage
```

### CLI usage changes:
```bash
# Before
python -m quantum_image_shield.cli encrypt input.png output.png

# After
python -m cli encrypt input.png output.png
# OR
python cli.py encrypt input.png output.png
```

## 🤔 Alternative: Keep as Package (RECOMMENDED)

Actually, the current structure IS the correct Python package structure! 
The `quantum_image_shield/` folder SHOULD be a subfolder.

**Why?**
- ✅ Follows Python packaging best practices
- ✅ Allows `pip install` to work properly
- ✅ Prevents name conflicts
- ✅ Clear separation of code vs documentation/tests
- ✅ Can be published to PyPI

**The REAL problem** is missing files (`analysis.py`) and broken imports in examples!

## 💡 Better Solution: FIX the Package (Don't Restructure)

Instead of moving everything to root, we should:
1. ✅ Keep `quantum_image_shield/` as the package
2. ✅ Create missing `analysis.py` module
3. ✅ Fix imports in examples/streamlit_app.py
4. ✅ Clean up unnecessary root files
5. ✅ Update documentation

This is the CORRECT Python project structure:
```
project-root/
├── package_name/          ← Your code
│   ├── __init__.py
│   └── modules.py
├── tests/                 ← Tests
├── examples/              ← Examples
├── docs/                  ← Documentation
├── setup.py               ← Package metadata
├── requirements.txt       ← Dependencies
└── README.md              ← Main docs
```

## 🎯 Recommendation

**DON'T** flatten the structure. **Instead**:
1. Create `quantum_image_shield/analysis.py`
2. Fix `examples/streamlit_app.py` imports
3. Clean up unnecessary root files
4. Keep the professional package structure

This is the industry standard and will make your project:
- ✅ Pip-installable
- ✅ PyPI-publishable
- ✅ Professional
- ✅ Maintainable

---

**Which approach do you want?**
- Option A: Flatten (move quantum_image_shield/* to root) - quick but unprofessional
- Option B: Fix the package (recommended) - proper Python structure
