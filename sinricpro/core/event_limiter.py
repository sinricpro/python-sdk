"""
Event Rate Limiter

Prevents excessive event sending with adaptive backoff.
"""

import time
from sinricpro.utils.logger import SinricProLogger


class EventLimiter:
    """
    Rate limiter to prevent excessive event sending.

    Uses adaptive backoff to handle repeated rate limit violations.
    """

    def __init__(self, minimum_distance: int = 1000) -> None:
        """
        Initialize the EventLimiter.

        Args:
            minimum_distance: Minimum time between events in milliseconds (default: 1000ms)
        """
        self.minimum_distance = minimum_distance
        self.next_event: int = 0
        self.extra_distance: int = 0
        self.fail_counter: int = 0

    def is_limited(self) -> bool:
        """
        Check if the event should be rate limited.

        Returns:
            True if event should be blocked, False if allowed

        Example:
            >>> limiter = EventLimiter(1000)
            >>> limiter.is_limited()  # First call: False (allowed)
            False
            >>> limiter.is_limited()  # Immediate second call: True (blocked)
            True
        """
        current_time = int(time.time() * 1000)  # milliseconds
        fail_threshold = self.minimum_distance // 4

        if current_time >= self.next_event:
            # Event is allowed
            if self.fail_counter > fail_threshold:
                # Too many failed attempts, add extra delay
                self.extra_distance += self.minimum_distance
                self.fail_counter = 0
                SinricProLogger.warn(
                    f"Event limiter: Too many events detected. "
                    f"Adding {self.extra_distance}ms delay."
                )
            else:
                # Reset extra distance
                self.extra_distance = 0

            self.next_event = current_time + self.minimum_distance + self.extra_distance
            return False

        # Event is blocked
        self.fail_counter += 1

        if self.fail_counter == fail_threshold:
            SinricProLogger.warn(
                f"WARNING: YOUR CODE SENDS EXCESSIVE EVENTS! "
                f"Events will be limited by an additional {self.extra_distance / 1000}s delay. "
                f"Please check your code!"
            )

        return True

    def can_send_event(self) -> bool:
        """
        Check if an event can be sent (inverse of is_limited).

        Returns:
            True if event is allowed, False if rate limited

        Example:
            >>> limiter = EventLimiter(1000)
            >>> limiter.can_send_event()  # First call: True (allowed)
            True
        """
        return not self.is_limited()

    def event_sent(self) -> None:
        """
        Mark that an event was successfully sent.

        This is called after a successful event send to update the limiter state.
        Note: is_limited() or can_send_event() already updates the state, so this
        is mainly for API compatibility.
        """
        pass

    def reset(self) -> None:
        """
        Reset the limiter state.

        Clears all counters and allows the next event immediately.
        """
        self.next_event = 0
        self.extra_distance = 0
        self.fail_counter = 0
