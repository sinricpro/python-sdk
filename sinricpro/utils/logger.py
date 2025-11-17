"""
SinricPro Logger

Configurable logging utility for the SinricPro SDK.
"""

import logging
from enum import IntEnum


class LogLevel(IntEnum):
    """Log levels for SinricPro SDK."""

    DEBUG = logging.DEBUG  # 10
    INFO = logging.INFO  # 20
    WARN = logging.WARNING  # 30
    ERROR = logging.ERROR  # 40
    NONE = logging.CRITICAL + 10  # 60 (effectively disables logging)


class SinricProLogger:
    """
    Centralized logger for SinricPro SDK.

    Provides consistent logging across the SDK with configurable log levels.
    """

    _logger: logging.Logger = logging.getLogger("sinricpro")
    _initialized: bool = False

    @classmethod
    def _init(cls) -> None:
        """Initialize the logger if not already initialized."""
        if not cls._initialized:
            # Create console handler
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)

            # Create formatter
            formatter = logging.Formatter(
                "[SinricPro:%(levelname)s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            handler.setFormatter(formatter)

            # Add handler to logger
            cls._logger.addHandler(handler)
            cls._logger.setLevel(LogLevel.INFO)
            cls._logger.propagate = False
            cls._initialized = True

    @classmethod
    def set_level(cls, level: LogLevel) -> None:
        """
        Set the logging level.

        Args:
            level: The log level to set (DEBUG, INFO, WARN, ERROR, NONE)

        Example:
            >>> SinricProLogger.set_level(LogLevel.DEBUG)
        """
        cls._init()
        cls._logger.setLevel(level)

    @classmethod
    def debug(cls, message: str, *args: object) -> None:
        """
        Log a debug message.

        Args:
            message: The message to log
            *args: Additional arguments for string formatting
        """
        cls._init()
        cls._logger.debug(message, *args)

    @classmethod
    def info(cls, message: str, *args: object) -> None:
        """
        Log an info message.

        Args:
            message: The message to log
            *args: Additional arguments for string formatting
        """
        cls._init()
        cls._logger.info(message, *args)

    @classmethod
    def warn(cls, message: str, *args: object) -> None:
        """
        Log a warning message.

        Args:
            message: The message to log
            *args: Additional arguments for string formatting
        """
        cls._init()
        cls._logger.warning(message, *args)

    @classmethod
    def error(cls, message: str, *args: object) -> None:
        """
        Log an error message.

        Args:
            message: The message to log
            *args: Additional arguments for string formatting
        """
        cls._init()
        cls._logger.error(message, *args)
