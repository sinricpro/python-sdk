#!/usr/bin/env python3
"""Validate Python example files for syntax and imports."""

import ast
import importlib
import sys
from pathlib import Path


def validate_syntax(file_path: Path) -> bool:
    """Validate Python syntax of a file."""
    try:
        with open(file_path, 'r') as f:
            ast.parse(f.read())
        print(f'  ✓ Syntax valid: {file_path}')
        return True
    except SyntaxError as e:
        print(f'  ✗ Syntax error in {file_path}: {e}')
        return False


def validate_imports(file_path: Path) -> bool:
    """Validate that sinricpro imports work."""
    try:
        with open(file_path, 'r') as f:
            tree = ast.parse(f.read())
    except SyntaxError:
        return False  # Already reported by validate_syntax

    success = True
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module and node.module.startswith('sinricpro'):
                module_name = node.module
                try:
                    importlib.import_module(module_name)
                    print(f'  ✓ Import OK: {module_name}')
                except ImportError as e:
                    print(f'  ✗ Failed to import {module_name}: {e}')
                    success = False
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith('sinricpro'):
                    try:
                        importlib.import_module(alias.name)
                        print(f'  ✓ Import OK: {alias.name}')
                    except ImportError as e:
                        print(f'  ✗ Failed to import {alias.name}: {e}')
                        success = False

    return success


def main():
    """Main validation function."""
    examples_dir = Path('examples')

    if not examples_dir.exists():
        print(f'Error: {examples_dir} directory not found')
        sys.exit(1)

    python_files = sorted(examples_dir.rglob('*.py'))

    if not python_files:
        print('Warning: No Python files found in examples/')
        sys.exit(0)

    print(f'Found {len(python_files)} Python example files\n')

    all_valid = True

    # Check syntax
    print('=' * 60)
    print('Validating Python syntax...')
    print('=' * 60)
    for file_path in python_files:
        if not validate_syntax(file_path):
            all_valid = False

    # Check imports
    print('\n' + '=' * 60)
    print('Validating sinricpro imports...')
    print('=' * 60)
    for file_path in python_files:
        print(f'\nChecking: {file_path}')
        if not validate_imports(file_path):
            all_valid = False

    print('\n' + '=' * 60)
    if all_valid:
        print('✅ All examples validated successfully!')
        sys.exit(0)
    else:
        print('❌ Some examples failed validation')
        sys.exit(1)


if __name__ == '__main__':
    main()
