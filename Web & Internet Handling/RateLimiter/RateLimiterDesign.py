import time
from collections import defaultdict

class InMemoryRateLimiter:
    def __init__(self, max_tokens, refill_rate, refill_interval):
        self.max_tokens = max_tokens  # Max tokens in the bucket
        self.refill_rate = refill_rate  # Tokens refilled per interval
        self.refill_interval = refill_interval  # Interval for refilling (in seconds)
        self.user_tokens = defaultdict(lambda: {'tokens': max_tokens, 'last_refill_time': time.time()})
    
    def get_current_time(self):
        return time.time()
    
    def refill_tokens(self, user_id, tokens, last_refill_time):
        """Refill tokens for the user based on the time elapsed since the last refill."""
        current_time = self.get_current_time()
        elapsed_time = current_time - last_refill_time
        
        # Calculate how many complete intervals have passed
        intervals_passed = int(elapsed_time / self.refill_interval)
        
        if intervals_passed > 0:
            # Add tokens only for complete intervals
            tokens_to_add = intervals_passed * self.refill_rate
            new_tokens = min(tokens + tokens_to_add, self.max_tokens)
            
            # Update the last refill time based on the complete intervals
            # This is the key fix - only move the last_refill_time forward by the amount of
            # complete intervals that have passed
            new_last_refill_time = last_refill_time + (intervals_passed * self.refill_interval)
            
            return new_tokens, new_last_refill_time
        else:
            # No complete intervals have passed, so no tokens to add
            return tokens, last_refill_time
    
    def consume_request(self, user_id):
        """Consume a request and check if it's allowed based on the available tokens."""
        
        # Get the user's current token data
        user_data = self.user_tokens[user_id]
        tokens, last_refill_time = user_data['tokens'], user_data['last_refill_time']
        
        # Refill the tokens if needed
        tokens, last_refill_time = self.refill_tokens(user_id, tokens, last_refill_time)
        
        # Update the user's token bucket in memory
        self.user_tokens[user_id] = {'tokens': tokens, 'last_refill_time': last_refill_time}
        
        # Check if there's a token available for the request
        if tokens > 0:
            # Allow the request, consume one token
            self.user_tokens[user_id]['tokens'] -= 1
            return True  # Request allowed
        else:
            # Deny the request if no tokens are available
            return False  # Request denied

# Usage Example
if __name__ == "__main__":
    # Initialize the rate limiter with:
    # - 10 max tokens
    # - 1 token refilled every second
    # - Refills occur every 1 second
    rate_limiter = InMemoryRateLimiter(max_tokens=10, refill_rate=1, refill_interval=1)
    
    user_id = "user123"
    
    # Simulate 30 requests
    for i in range(30):
        result = rate_limiter.consume_request(user_id)
        print(f"Request {i+1}: {'Allowed' if result else 'Denied'}")
        
        # Print current tokens for debugging
        print(f"  Current tokens: {rate_limiter.user_tokens[user_id]['tokens']}")
        print(f"  Time since last refill: {rate_limiter.get_current_time() - rate_limiter.user_tokens[user_id]['last_refill_time']:.2f}s")
        
        time.sleep(0.5)  # Simulate a small delay between requests (500ms)