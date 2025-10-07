#!/usr/bin/env python3
"""
Windows-compatible verification script for YouTube AI Content Analyzer setup
"""

import sys
import os

def check_imports():
    """Check that all modules can be imported"""
    print("🔍 Checking module imports...")
    
    # Add src to path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    
    modules_to_check = [
        'config',
        'youtube_client', 
        'advanced_analyzer',
        'ensemble_analyzer',
        'content_analyzer',
        'utils',
        'visualizer',
        'dashboard',
        'enhanced_main'
    ]
    
    all_imports_ok = True
    for module_name in modules_to_check:
        try:
            __import__(module_name)
            print(f"  ✅ {module_name}")
        except ImportError as e:
            print(f"  ❌ {module_name}: {e}")
            all_imports_ok = False
    
    return all_imports_ok

def check_files():
    """Check that all required files exist"""
    print("\n📁 Checking required files...")
    
    required_files = [
        'README.md',
        'LICENSE', 
        '.gitignore',
        'CONTRIBUTING.md',
        'CHANGELOG.md',
        'requirements.txt',
        'setup.py',
        '.env.example',
        r'src\__init__.py',
        r'src\config.py',
        r'src\enhanced_main.py',
        r'.github\workflows\python-package.yml'
    ]
    
    all_files_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - MISSING")
            all_files_exist = False
    
    return all_files_exist

def check_directories():
    """Check that all required directories exist"""
    print("\n📂 Checking required directories...")
    
    required_dirs = [
        'src',
        'tests',
        'docs',
        'docs/images',
        '.github',
        '.github/workflows'
    ]
    
    all_dirs_exist = True
    for dir_path in required_dirs:
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            print(f"  ✅ {dir_path}")
        else:
            print(f"  ❌ {dir_path} - MISSING")
            all_dirs_exist = False
    
    return all_dirs_exist

def main():
    print("🚀 YouTube AI Content Analyzer - Windows Setup Verification")
    print("=" * 60)
    
    dirs_ok = check_directories()
    files_ok = check_files()
    imports_ok = check_imports()
    
    print("\n" + "=" * 60)
    if all([dirs_ok, files_ok, imports_ok]):
        print("🎉 All checks passed! Your repository is ready for GitHub.")
        print("\nNext steps:")
        print("1. Create repository on GitHub.com")
        print("2. Run: git remote add origin https://github.com/yourusername/youtube-ai-analyzer.git")
        print("3. Run: git push -u origin main")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()