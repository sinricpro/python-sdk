# GitHub Workflows

This directory contains GitHub Actions workflows for the SinricPro Python SDK.

## Workflows

### 1. PR Validation (`pr-validation.yml`)

**Trigger:** Automatically runs on pull requests to main branches

**Purpose:** Validates code quality and ensures all examples compile correctly

**Jobs:**
- **validate-examples**: Tests all example files across Python 3.10, 3.11, and 3.12
  - Uses `.github/scripts/validate_examples.py` to validate syntax and imports
  - Validates Python syntax using AST parsing
  - Tests that all sinricpro imports work correctly

- **lint-check**: Runs code quality checks
  - Ruff for code linting
  - MyPy for type checking

- **package-build**: Tests package building
  - Builds wheel and source distribution
  - Validates with `twine check`

**What it validates:**
- ✅ All example files have valid Python syntax
- ✅ All imports in examples are correct
- ✅ Package can be built successfully
- ✅ Code passes linting checks (non-blocking)
- ✅ Type hints are correct (non-blocking)

### 2. Publish Release (`publish-release.yml`)

**Trigger:** Manual workflow dispatch

**Purpose:** Publishes a new version to PyPI and creates a GitHub release

**Required Secrets:**
- `PYPI_API_TOKEN`: PyPI API token for publishing packages
  - Get from: https://pypi.org/manage/account/token/
  - Add to: Repository Settings → Secrets and variables → Actions → New repository secret

**Input Parameters:**
- `version`: Version number (e.g., `3.0.0` or `3.0.0-beta.1`)
- `branch`: Branch or tag to publish from (default: `main`)
- `prerelease`: Mark as pre-release (checkbox)

**Jobs:**

1. **validate-version**
   - Validates version format (X.Y.Z or X.Y.Z-suffix)
   - Checks that git tag doesn't already exist

2. **build-and-test**
   - Updates version in `sinricpro/__init__.py`
   - Builds package (wheel + source distribution)
   - Validates with `twine check`
   - Tests local installation
   - Uploads artifacts for next jobs

3. **publish-to-pypi**
   - Downloads build artifacts
   - Publishes to PyPI using official PyPI publish action
   - Waits for propagation
   - Verifies package is available on PyPI

4. **create-github-release**
   - Creates and pushes git tag (`vX.Y.Z`)
   - Generates changelog from git commits
   - Creates GitHub release with:
     - Release notes
     - Attached wheel and source files
     - Links to PyPI package

**Workflow Summary:**
After successful completion, the workflow creates a summary with:
- Version number
- PyPI package link
- GitHub release link
- Installation command

## How to Use

### Setting up PyPI Publishing

1. **Create PyPI API Token:**
   ```bash
   # Go to https://pypi.org/manage/account/token/
   # Create a new API token with scope: "Entire account" or specific to "sinricpro"
   # Copy the token (starts with pypi-...)
   ```

2. **Add Token to GitHub Secrets:**
   - Go to repository Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `PYPI_API_TOKEN`
   - Value: Paste your PyPI token
   - Click "Add secret"

### Publishing a Release

1. **Go to Actions tab** in your repository

2. **Select "Publish Release to PyPI"** from the workflows list

3. **Click "Run workflow"** button

4. **Fill in the parameters:**
   - **Version**: Enter version number (e.g., `3.0.1`)
   - **Branch**: Select branch to publish from (usually `main`)
   - **Prerelease**: Check if this is a pre-release version

5. **Click "Run workflow"**

6. **Monitor the workflow:**
   - Watch each job complete
   - Check for any errors
   - View the summary for installation instructions

### Version Numbering Guidelines

**Stable releases:**
- `3.0.0` - Major version
- `3.0.1` - Patch version
- `3.1.0` - Minor version

**Pre-releases:**
- `3.0.0-alpha.1` - Alpha release
- `3.0.0-beta.1` - Beta release
- `3.0.0-rc.1` - Release candidate

### Testing Before Release

Before publishing a release:

1. **Test locally:**
   ```bash
   # Build the package
   python -m build

   # Check with twine
   twine check dist/*

   # Install locally
   pip install dist/*.whl

   # Test import
   python -c "import sinricpro; print(sinricpro.__version__)"
   ```

2. **Test examples:**
   ```bash
   # Validate all examples
   python -m compileall examples/
   ```

3. **Run tests (if available):**
   ```bash
   pytest tests/
   ```

### Troubleshooting

**"Tag already exists" error:**
- The version tag already exists in git
- Choose a different version number or delete the existing tag

**"PyPI upload failed" error:**
- Check that `PYPI_API_TOKEN` secret is set correctly
- Verify token has correct permissions
- Ensure version doesn't already exist on PyPI

**"Package build failed" error:**
- Check `pyproject.toml` for syntax errors
- Verify all dependencies are listed correctly
- Check that version number is valid

**"Import error in examples" (PR validation):**
- Missing import in example file
- Typo in module name
- New module not exported in `__init__.py`

## Workflow Permissions

The workflows require the following permissions:

- `contents: write` - For creating tags and releases
- `packages: write` - For publishing to PyPI (via PYPI_API_TOKEN)

These are automatically granted in the workflow files.

## Best Practices

1. **Always test locally before publishing**
2. **Use semantic versioning (semver.org)**
3. **Write meaningful release notes**
4. **Test examples after each change**
5. **Keep dependencies up to date**
6. **Tag releases consistently (vX.Y.Z format)**

## Scripts

The `.github/scripts/` directory contains helper scripts used by the workflows:

### validate_examples.py

Validates all Python example files in the `examples/` directory:
- Checks Python syntax using AST parsing
- Verifies that all `sinricpro` imports are valid
- Provides detailed output for debugging
- Returns exit code 0 on success, 1 on failure

**Usage:**
```bash
python .github/scripts/validate_examples.py
```

**Output:**
```
Found 16 Python example files

============================================================
Validating Python syntax...
============================================================
  ✓ Syntax valid: examples/switch/switch_example.py
  ✓ Syntax valid: examples/light/light_example.py
  ...

============================================================
Validating sinricpro imports...
============================================================
Checking: examples/switch/switch_example.py
  ✓ Import OK: sinricpro
  ...

============================================================
✅ All examples validated successfully!
```

## Support

If you encounter issues with the workflows:
- Check the workflow run logs in GitHub Actions
- Review the troubleshooting section above
- Open an issue in the repository
