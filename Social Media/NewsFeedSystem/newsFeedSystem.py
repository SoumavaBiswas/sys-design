import heapq
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List

@dataclass(order=True)
class Post:
    timestamp: float
    user_id: str = field(compare=False)
    content: str = field(compare=False)

class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.following = set()
        self.posts = []

    def follow(self, other_user_id):
        self.following.add(other_user_id)

    def unfollow(self, other_user_id):
        self.following.discard(other_user_id)

    def add_post(self, content):
        post = Post(timestamp=time.time(), user_id=self.user_id, content=content)
        self.posts.append(post)

class NewsFeedService:
    def __init__(self):
        self.users = {}

    def get_or_create_user(self, user_id):
        if user_id not in self.users:
            self.users[user_id] = User(user_id)
        return self.users[user_id]

    def post(self, user_id, content):
        user = self.get_or_create_user(user_id)
        user.add_post(content)

    def follow(self, follower_id, followee_id):
        follower = self.get_or_create_user(follower_id)
        self.get_or_create_user(followee_id)  # ensure followee exists
        follower.follow(followee_id)

    def unfollow(self, follower_id, followee_id):
        follower = self.get_or_create_user(follower_id)
        follower.unfollow(followee_id)

    def get_news_feed(self, user_id, limit=10):
        user = self.get_or_create_user(user_id)
        min_heap = []

        # Include user's own posts
        sources = list(user.following) + [user.user_id]
        for uid in sources:
            u = self.get_or_create_user(uid)
            for post in u.posts[-limit:]:  # only consider last 'limit' posts from each user
                heapq.heappush(min_heap, post)
                if len(min_heap) > limit:
                    heapq.heappop(min_heap)

        # Return posts sorted by timestamp (most recent first)
        feed = sorted(min_heap, reverse=True)
        return feed


if __name__ == "__main__":
    service = NewsFeedService()

    service.post("alice", "Alice's first post")
    time.sleep(0.1)
    service.post("bob", "Bob's post")
    service.follow("alice", "bob")

    feed = service.get_news_feed("alice")
    for post in feed:
        print(f"[{post.timestamp}] {post.user_id}: {post.content}")
