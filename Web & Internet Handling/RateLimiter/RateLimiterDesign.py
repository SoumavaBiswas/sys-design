import time
import threading
from collections import defaultdict

class TokenBucket:
    def __init__(self, max_tokens, refill_rate, refill_interval):
        self.max_tokens = max_tokens
        self.refill_rate = refill_rate
        self.refill_interval = refill_interval
        self.tokens = max_tokens
        self.last_refill_time = time.time()
        self.lock = threading.Lock()

    def _refill(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_refill_time
        intervals_passed = int(elapsed_time / self.refill_interval)

        if intervals_passed > 0:
            tokens_to_add = intervals_passed * self.refill_rate
            self.tokens = min(self.max_tokens, self.tokens + tokens_to_add)
            self.last_refill_time += intervals_passed * self.refill_interval

    def consume(self, cost=1):
        with self.lock:
            self._refill()
            if self.tokens >= cost:
                self.tokens -= cost
                return True
            return False

    def get_token_info(self):
        return {
            'tokens': self.tokens,
            'time_since_last_refill': time.time() - self.last_refill_time
        }


class InMemoryRateLimiter:
    def __init__(self, max_tokens, refill_rate, refill_interval):
        self.max_tokens = max_tokens
        self.refill_rate = refill_rate
        self.refill_interval = refill_interval
        self.user_buckets = defaultdict(self._create_bucket)

    def _create_bucket(self):
        return TokenBucket(self.max_tokens, self.refill_rate, self.refill_interval)

    def consume_request(self, user_id, cost=1):
        return self.user_buckets[user_id].consume(cost)

    def debug_user(self, user_id):
        if user_id in self.user_buckets:
            info = self.user_buckets[user_id].get_token_info()
            print(f"  Current tokens: {info['tokens']:.2f}")
            print(f"  Time since last refill: {info['time_since_last_refill']:.2f}s")
        else:
            print("  User bucket does not exist yet.")


# Usage Example
if __name__ == "__main__":
    rate_limiter = InMemoryRateLimiter(max_tokens=10, refill_rate=1, refill_interval=1)
    user_id = "user123"

    for i in range(30):
        result = rate_limiter.consume_request(user_id)
        print(f"Request {i+1}: {'Allowed' if result else 'Denied'}")
        rate_limiter.debug_user(user_id)
        time.sleep(0.5)
