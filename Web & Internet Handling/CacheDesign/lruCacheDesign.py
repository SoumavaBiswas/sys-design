# Using Hashmap + Doubly Linked List
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> Node
        # Dummy head and tail to avoid null checks
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    # Internal helper to remove a node from the list
    def _remove(self, node):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    # Internal helper to insert a node right after head (most recently used)
    def _insert_at_front(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            # Move the accessed node to the front
            self._remove(node)
            self._insert_at_front(node)
            return node.value
        return -1

    def put(self, key: int, value: int):
        if key in self.cache:
            # Remove the old node
            self._remove(self.cache[key])

        # Insert new node
        new_node = Node(key, value)
        self._insert_at_front(new_node)
        self.cache[key] = new_node

        # Evict least recently used if over capacity
        if len(self.cache) > self.capacity:
            # Remove from linked list and hash map
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]


# Using OrderedDict
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        # Mark as recently used
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int):
        if key in self.cache:
            # Update and move to end (most recently used)
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            # Pop the least recently used item (first one)
            self.cache.popitem(last=False)



if __name__ == "__main__":
    lru = LRUCache(2)
    lru.put(1, 1)
    lru.put(2, 2)
    print(lru.get(1))    # returns 1
    lru.put(3, 3)        # evicts key 2
    print(lru.get(2))    # returns -1
    lru.put(4, 4)        # evicts key 1
    print(lru.get(1))    # returns -1
    print(lru.get(3))    # returns 3
    print(lru.get(4))    # returns 4
