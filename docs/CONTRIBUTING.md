# Contributing to SinricPro Python SDK

Thank you for your interest in contributing to the SinricPro Python SDK! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with:

1. **Clear title** - Summarize the problem
2. **Description** - Detailed description of the issue
3. **Steps to reproduce** - How to recreate the bug
4. **Expected behavior** - What should happen
5. **Actual behavior** - What actually happens
6. **Environment** - Python version, OS, SDK version
7. **Code sample** - Minimal code that reproduces the issue

### Suggesting Features

We love feature suggestions! Please create an issue with:

1. **Clear title** - Summarize the feature
2. **Use case** - Why is this feature needed?
3. **Proposed solution** - How should it work?
4. **Alternatives** - Other approaches you've considered

### Pull Requests

We actively welcome pull requests!

1. **Fork** the repository
2. **Create a branch** from `main` for your changes
3. **Make your changes** following our code style
4. **Add tests** for any new functionality
5. **Update documentation** if needed
6. **Run tests** to ensure everything works
7. **Submit a pull request**

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Git

### Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/python-sdk.git
cd python-sdk

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

## Code Style

We use Python standard tools for code quality:

### Formatting

We use **Black** for code formatting:

```bash
# Format all code
black .

# Check formatting
black --check .
```

Configuration in `pyproject.toml`:
- Line length: 100 characters
- Target: Python 3.10+

### Import Sorting

We use **isort** for import sorting:

```bash
# Sort imports
isort .

# Check import sorting
isort --check .
```

### Type Checking

We use **mypy** for static type checking:

```bash
# Run type checker
mypy sinricpro
```

All code should have type hints. Configuration in `pyproject.toml`.

### Linting

We use **flake8** for linting:

```bash
# Run linter
flake8 sinricpro
```

## Testing

We use **pytest** for testing:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=sinricpro --cov-report=html

# Run specific test file
pytest test/unit/test_signature.py

# Run specific test
pytest test/unit/test_signature.py::test_sign_message
```

### Writing Tests

- Place unit tests in `test/unit/`
- Place integration tests in `test/integration/`
- Use descriptive test names: `test_should_validate_correct_signature`
- Use fixtures for common setup
- Mock external dependencies (WebSocket, etc.)

Example test:

```python
import pytest
from sinricpro import SinricProSwitch

async def test_switch_power_state():
    """Test switch power state callback."""
    switch = SinricProSwitch("5dc1564130xxxxxxxxxxxxxx")

    power_state = None

    async def on_power_state(state: bool) -> bool:
        nonlocal power_state
        power_state = state
        return True

    switch.on_power_state(on_power_state)

    # Simulate request
    from sinricpro.core.types import SinricProRequest
    request = SinricProRequest(
        action="setPowerState",
        request_value={"state": "On"}
    )

    success = await switch.handle_request(request)

    assert success is True
    assert power_state is True
```

## Code Guidelines

### Python Style

- Follow [PEP 8](https://pep8.org/)
- Use type hints for all functions
- Write docstrings for all public methods (Google style)
- Use descriptive variable names
- Keep functions focused and small

### Naming Conventions

- **Classes**: PascalCase (e.g., `SinricProSwitch`)
- **Functions/Methods**: snake_case (e.g., `send_power_state_event`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `WEBSOCKET_PING_INTERVAL`)
- **Private members**: prefix with underscore (e.g., `_process_queue`)

### Documentation

Use Google-style docstrings:

```python
async def send_event(
    self,
    action: str,
    value: dict[str, Any],
    cause: str = "PHYSICAL_INTERACTION",
) -> bool:
    """
    Send an event to SinricPro.

    Args:
        action: The action type (e.g., "setPowerState")
        value: Event data
        cause: Cause of the event (PHYSICAL_INTERACTION or APP_INTERACTION)

    Returns:
        True if event was sent successfully, False if rate limited

    Raises:
        SinricProConnectionError: If not connected to server

    Example:
        >>> await device.send_event("setPowerState", {"state": "On"})
        True
    """
```

## Adding New Devices

To add a new device type:

1. **Create capability controllers** in `sinricpro/capabilities/`
2. **Create device class** in `sinricpro/devices/`
3. **Export in __init__.py** files
4. **Add tests** in `test/unit/`
5. **Create example** in `examples/`
6. **Update README.md** with new device

Example device structure:

```python
from sinricpro.capabilities.power_state_controller import PowerStateController
from sinricpro.core.sinric_pro_device import SinricProDevice

class SinricProMyDevice(SinricProDevice, PowerStateController):
    """My new device type."""

    def __init__(self, device_id: str) -> None:
        super().__init__(device_id=device_id, product_type="MY_DEVICE")

    async def handle_request(self, request: SinricProRequest) -> bool:
        # Handle requests
        pass
```

## Adding New Capabilities

To add a new capability:

1. **Create capability controller** in `sinricpro/capabilities/`
2. **Follow mixin pattern** (see existing capabilities)
3. **Add rate limiting** for events
4. **Add type hints** and docstrings
5. **Create tests**
6. **Update documentation**

## Commit Messages

Write clear, descriptive commit messages:

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and PRs when relevant

Examples:
```
Add support for thermostat device

- Implement ThermostatController capability
- Add SinricProThermostat device class
- Create thermostat example
- Add tests for thermostat functionality

Fixes #123
```

## Release Process

Releases are handled by maintainers:

1. Update version in `sinricpro/__init__.py`
2. Update `CHANGELOG.md`
3. Create git tag
4. Push to PyPI

## Questions?

If you have questions about contributing:

- Check existing issues and PRs
- Ask in our [Discord community](https://discord.gg/sinricpro)
- Create a discussion on GitHub

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help newcomers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to SinricPro Python SDK! 🎉
