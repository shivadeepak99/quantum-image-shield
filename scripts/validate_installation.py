"""
Installation and Feature Validation Script

This script verifies that all components are properly installed
and functional.
"""

import sys
import importlib


def check_imports():
    """Check that all required modules can be imported."""
    print("="*60)
    print("1. Checking Dependencies")
    print("="*60)
    
    required_modules = [
        ('qiskit', 'Qiskit'),
        ('qiskit_aer', 'Qiskit Aer'),
        ('numpy', 'NumPy'),
        ('PIL', 'Pillow'),
        ('matplotlib', 'Matplotlib'),
        ('streamlit', 'Streamlit'),
        ('scipy', 'SciPy'),
    ]
    
    all_ok = True
    for module_name, display_name in required_modules:
        try:
            module = importlib.import_module(module_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"  ✓ {display_name:20} {version}")
        except ImportError as e:
            print(f"  ✗ {display_name:20} NOT FOUND")
            all_ok = False
    
    return all_ok


def check_project_modules():
    """Check that all project modules can be imported."""
    print("\n" + "="*60)
    print("2. Checking Project Modules")
    print("="*60)
    
    project_modules = [
        'quantum_key_generator',
        'image_encryptor',
        'image_analysis',
    ]
    
    all_ok = True
    for module_name in project_modules:
        try:
            importlib.import_module(module_name)
            print(f"  ✓ {module_name}")
        except ImportError as e:
            print(f"  ✗ {module_name}: {e}")
            all_ok = False
    
    return all_ok


def check_files():
    """Check that all required files exist."""
    print("\n" + "="*60)
    print("3. Checking Project Files")
    print("="*60)
    
    import os
    
    required_files = [
        'quantum_key_generator.py',
        'image_encryptor.py',
        'image_analysis.py',
        'app.py',
        'test_encryption.py',
        'example_usage.py',
        'generate_sample_image.py',
        'requirements.txt',
        'README.md',
        'USAGE.md',
        'PROJECT_SUMMARY.md',
        'LICENSE',
    ]
    
    all_ok = True
    for filename in required_files:
        if os.path.exists(filename):
            print(f"  ✓ {filename}")
        else:
            print(f"  ✗ {filename} NOT FOUND")
            all_ok = False
    
    return all_ok


def check_sample_directory():
    """Check samples directory."""
    print("\n" + "="*60)
    print("4. Checking Samples Directory")
    print("="*60)
    
    import os
    
    if os.path.exists('samples'):
        print("  ✓ samples/ directory exists")
        
        # Check for sample image
        if os.path.exists('samples/sample_image.png'):
            print("  ✓ samples/sample_image.png exists")
        else:
            print("  ℹ samples/sample_image.png not found (will be generated)")
        
        return True
    else:
        print("  ✗ samples/ directory not found")
        return False


def quick_functional_test():
    """Run a quick functional test."""
    print("\n" + "="*60)
    print("5. Quick Functional Test")
    print("="*60)
    
    try:
        from quantum_key_generator import QuantumKeyGenerator
        from image_encryptor import ImageEncryptor
        from image_analysis import calculate_entropy
        import numpy as np
        
        # Test quantum key generator
        print("  Testing quantum key generator...")
        generator = QuantumKeyGenerator(seed=42)
        bits = generator.generate_random_bits(16)
        assert len(bits) == 16
        print("    ✓ Generated 16 random bits")
        
        # Test image encryptor
        print("  Testing image encryptor...")
        test_image = np.random.randint(0, 256, (32, 32), dtype=np.uint8)
        keystream = generator.generate_keystream(test_image.size)
        seed = generator.generate_permutation_seed()
        encryptor = ImageEncryptor(keystream, seed)
        
        encrypted = encryptor.encrypt_image(test_image)
        decrypted = encryptor.decrypt_image(encrypted)
        assert np.array_equal(test_image, decrypted)
        print("    ✓ Encryption/decryption works correctly")
        
        # Test analysis
        print("  Testing analysis functions...")
        entropy = calculate_entropy(test_image)
        assert 0 <= entropy <= 8
        print(f"    ✓ Entropy calculation works (entropy={entropy:.2f} bits)")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Functional test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all validation checks."""
    print("\n" + "="*60)
    print("Quantum-Seed ImageShield - Installation Validator")
    print("="*60 + "\n")
    
    results = []
    
    results.append(("Dependencies", check_imports()))
    results.append(("Project Modules", check_project_modules()))
    results.append(("Project Files", check_files()))
    results.append(("Samples Directory", check_sample_directory()))
    results.append(("Functional Test", quick_functional_test()))
    
    # Summary
    print("\n" + "="*60)
    print("Validation Summary")
    print("="*60)
    
    for check_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status:10} {check_name}")
    
    all_passed = all(passed for _, passed in results)
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ All checks passed! Installation is complete.")
        print("\nNext steps:")
        print("  1. Run: python test_encryption.py")
        print("  2. Run: streamlit run app.py")
        print("  3. See USAGE.md for more information")
    else:
        print("⚠ Some checks failed. Please review the errors above.")
        print("\nTroubleshooting:")
        print("  - Run: pip install -r requirements.txt")
        print("  - Ensure all project files are present")
        print("  - Check that Python 3.8+ is installed")
    print("="*60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit(main())
