"""
Message Queue

FIFO queue for message processing using asyncio.
"""

import asyncio
from collections import deque


class MessageQueue:
    """
    Thread-safe FIFO message queue.

    Uses a deque for efficient push/pop operations.
    """

    def __init__(self) -> None:
        """Initialize an empty message queue."""
        self._queue: deque[str] = deque()
        self._lock = asyncio.Lock()

    async def push(self, message: str) -> None:
        """
        Add a message to the queue.

        Args:
            message: The message string to add

        Example:
            >>> queue = MessageQueue()
            >>> await queue.push('{"type": "request"}')
        """
        async with self._lock:
            self._queue.append(message)

    def push_sync(self, message: str) -> None:
        """
        Add a message to the queue synchronously.

        Args:
            message: The message string to add

        Note:
            This is a synchronous version for use in callbacks.
        """
        self._queue.append(message)

    async def pop(self) -> str | None:
        """
        Remove and return the first message from the queue.

        Returns:
            The first message in the queue, or None if empty

        Example:
            >>> queue = MessageQueue()
            >>> await queue.push("message1")
            >>> await queue.pop()
            'message1'
        """
        async with self._lock:
            if self._queue:
                return self._queue.popleft()
            return None

    def pop_sync(self) -> str | None:
        """
        Remove and return the first message from the queue synchronously.

        Returns:
            The first message in the queue, or None if empty

        Note:
            This is a synchronous version for use in non-async contexts.
        """
        if self._queue:
            return self._queue.popleft()
        return None

    def is_empty(self) -> bool:
        """
        Check if the queue is empty.

        Returns:
            True if queue is empty, False otherwise
        """
        return len(self._queue) == 0

    def clear(self) -> None:
        """Clear all messages from the queue."""
        self._queue.clear()

    def __len__(self) -> int:
        """
        Get the number of messages in the queue.

        Returns:
            Number of messages in the queue
        """
        return len(self._queue)
