"""
Message Queue

FIFO queue for message processing using asyncio.
"""

import asyncio
from collections import deque
from typing import Callable

from sinricpro.core.types import WEBSOCKET_ORIGIN, MessageOrigin, QueuedMessage
from sinricpro.utils.logger import SinricProLogger


class MessageQueue:
    """
    Thread-safe FIFO message queue.

    Entries are :class:`QueuedMessage` - the serialized message plus the origin
    it arrived on, so a response knows which transport and peer to go back to.
    Plain strings are accepted and default to the websocket origin.

    Uses a deque for efficient push/pop operations.
    """

    def __init__(self, max_size: int = 0) -> None:
        """
        Initialize an empty message queue.

        Args:
            max_size: Drop the oldest entry once the queue grows past this.
                0 (default) means unbounded.
        """
        self._queue: deque[QueuedMessage] = deque()
        self._lock = asyncio.Lock()
        self._max_size = max_size

    @staticmethod
    def _coerce(
        message: str | QueuedMessage, origin: MessageOrigin | None
    ) -> QueuedMessage:
        if isinstance(message, QueuedMessage):
            return message
        return QueuedMessage(message, origin or WEBSOCKET_ORIGIN)

    def _trim(self) -> None:
        while self._max_size and len(self._queue) > self._max_size:
            dropped = self._queue.popleft()
            SinricProLogger.warn(
                f"Send queue full ({self._max_size}), dropping oldest "
                f"{dropped.origin.transport.value} message"
            )

    async def push(
        self, message: str | QueuedMessage, origin: MessageOrigin | None = None
    ) -> None:
        """
        Add a message to the queue.

        Args:
            message: The message string (or ready-made QueuedMessage) to add
            origin: Transport and peer the message belongs to

        Example:
            >>> queue = MessageQueue()
            >>> await queue.push('{"type": "request"}')
        """
        async with self._lock:
            self._queue.append(self._coerce(message, origin))
            self._trim()

    def push_sync(
        self, message: str | QueuedMessage, origin: MessageOrigin | None = None
    ) -> None:
        """
        Add a message to the queue synchronously.

        Args:
            message: The message string (or ready-made QueuedMessage) to add
            origin: Transport and peer the message belongs to

        Note:
            This is a synchronous version for use in callbacks.
        """
        self._queue.append(self._coerce(message, origin))
        self._trim()

    def push_front_sync(
        self, message: str | QueuedMessage, origin: MessageOrigin | None = None
    ) -> None:
        """
        Put a message back at the head of the queue, preserving order.

        Args:
            message: The message to requeue
            origin: Transport and peer the message belongs to
        """
        self._queue.appendleft(self._coerce(message, origin))

    async def pop(
        self, predicate: Callable[[QueuedMessage], bool] | None = None
    ) -> QueuedMessage | None:
        """
        Remove and return the first message from the queue.

        Args:
            predicate: Optional filter; the first entry it accepts is removed.

        Returns:
            The first matching message in the queue, or None if there is none

        Example:
            >>> queue = MessageQueue()
            >>> await queue.push("message1")
            >>> (await queue.pop()).message
            'message1'
        """
        async with self._lock:
            return self._pop_locked(predicate)

    def pop_sync(
        self, predicate: Callable[[QueuedMessage], bool] | None = None
    ) -> QueuedMessage | None:
        """
        Remove and return the first message from the queue synchronously.

        Args:
            predicate: Optional filter; the first entry it accepts is removed.

        Returns:
            The first matching message in the queue, or None if there is none

        Note:
            This is a synchronous version for use in non-async contexts.
        """
        return self._pop_locked(predicate)

    def _pop_locked(
        self, predicate: Callable[[QueuedMessage], bool] | None
    ) -> QueuedMessage | None:
        if not self._queue:
            return None
        if predicate is None:
            return self._queue.popleft()
        # Skipping over a message that cannot be delivered yet keeps the gate
        # per message: a held cloud message must not block a LAN reply behind it.
        for index, entry in enumerate(self._queue):
            if predicate(entry):
                del self._queue[index]
                return entry
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
