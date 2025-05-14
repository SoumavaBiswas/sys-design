from collections import defaultdict, OrderedDict

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.key_to_val_freq = {}  # key -> (val, freq)
        self.freq_to_keys = defaultdict(OrderedDict)  # freq -> OrderedDict of keys
        self.min_freq = 0

    def _update_freq(self, key):
        val, freq = self.key_to_val_freq[key]
        # Remove key from current frequency list
        del self.freq_to_keys[freq][key]
        if not self.freq_to_keys[freq]:
            del self.freq_to_keys[freq]
            if freq == self.min_freq:
                self.min_freq += 1

        # Add key to next frequency list
        self.freq_to_keys[freq + 1][key] = None
        self.key_to_val_freq[key] = (val, freq + 1)

    def get(self, key: int) -> int:
        if key not in self.key_to_val_freq:
            return -1
        self._update_freq(key)
        return self.key_to_val_freq[key][0]

    def put(self, key: int, value: int) -> None:
        print(self.freq_to_keys)
        if self.capacity == 0:
            return

        if key in self.key_to_val_freq:
            self.key_to_val_freq[key] = (value, self.key_to_val_freq[key][1])
            self._update_freq(key)
            return

        # Evict if needed
        if len(self.key_to_val_freq) >= self.capacity:
            # Evict the least frequently used and least recently used key
            lfu_keys = self.freq_to_keys[self.min_freq]
            evict_key, _ = lfu_keys.popitem(last=False)
            if not lfu_keys:
                del self.freq_to_keys[self.min_freq]
            del self.key_to_val_freq[evict_key]

        # Insert new key
        self.key_to_val_freq[key] = (value, 1)
        self.freq_to_keys[1][key] = None
        self.min_freq = 1



lfu = LFUCache(2)
lfu.put(1, 1)
lfu.put(2, 2)
print(lfu.get(1))  # 1 (frequency of 1 becomes 2)
lfu.put(3, 3)      # evicts key 2 (least freq = 1, key 2 < key 1 in freq count)
print(lfu.get(2))  # -1
print(lfu.get(3))  # 3
