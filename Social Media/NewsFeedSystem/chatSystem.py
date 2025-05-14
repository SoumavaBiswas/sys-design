import time
import threading
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class User:
    user_id: str
    name: str

@dataclass
class Message:
    sender_id: str
    content: str
    timestamp: float = time.time()

    def __str__(self):
        return f"[{time.strftime('%H:%M:%S', time.localtime(self.timestamp))}] {self.sender_id}: {self.content}"

class Chat:
    def __init__(self, user1_id, user2_id):
        self.user1_id = user1_id
        self.user2_id = user2_id
        self.messages: List[Message] = []

    def add_message(self, message: Message):
        self.messages.append(message)

    def get_history(self):
        return self.messages

class GroupChat:
    def __init__(self, group_id: str, member_ids: List[str]):
        self.group_id = group_id
        self.members = set(member_ids)
        self.messages: List[Message] = []

    def add_member(self, user_id):
        self.members.add(user_id)

    def remove_member(self, user_id):
        self.members.discard(user_id)

    def add_message(self, message: Message):
        self.messages.append(message)

    def get_history(self):
        return self.messages

class MessageQueue:
    def __init__(self):
        self.lock = threading.Lock()
        self.queue: Dict[str, List[Message]] = defaultdict(list)

    def enqueue(self, user_id: str, message: Message):
        with self.lock:
            self.queue[user_id].append(message)

    def get_messages(self, user_id: str) -> List[Message]:
        with self.lock:
            messages = self.queue[user_id][:]
            self.queue[user_id].clear()
            return messages

class ChatService:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.chats: Dict[str, Chat] = {}
        self.group_chats: Dict[str, GroupChat] = {}
        self.queue = MessageQueue()

    def register_user(self, user_id: str, name: str):
        self.users[user_id] = User(user_id, name)

    def send_message(self, sender_id: str, receiver_id: str, content: str):
        key = self._chat_key(sender_id, receiver_id)
        if key not in self.chats:
            self.chats[key] = Chat(sender_id, receiver_id)
        message = Message(sender_id, content, time.time())
        self.chats[key].add_message(message)
        self.queue.enqueue(receiver_id, message)

    def create_group(self, group_id: str, member_ids: List[str]):
        self.group_chats[group_id] = GroupChat(group_id, member_ids)

    def send_group_message(self, sender_id: str, group_id: str, content: str):
        if group_id not in self.group_chats:
            raise Exception("Group does not exist")
        group = self.group_chats[group_id]
        if sender_id not in group.members:
            raise Exception("Sender is not in the group")
        message = Message(sender_id, content, time.time())
        group.add_message(message)
        for member_id in group.members:
            if member_id != sender_id:
                self.queue.enqueue(member_id, message)

    def fetch_inbox(self, user_id: str):
        return self.queue.get_messages(user_id)

    def get_chat_history(self, user1_id: str, user2_id: str):
        key = self._chat_key(user1_id, user2_id)
        return self.chats[key].get_history() if key in self.chats else []

    def get_group_history(self, group_id: str):
        return self.group_chats[group_id].get_history() if group_id in self.group_chats else []

    def _chat_key(self, user1, user2):
        return "-".join(sorted([user1, user2]))


if __name__ == "__main__":
    chat_service = ChatService()

    chat_service.register_user("u1", "Alice")
    chat_service.register_user("u2", "Bob")
    chat_service.register_user("u3", "Charlie")

    chat_service.send_message("u1", "u2", "Hey Bob!")
    chat_service.send_message("u2", "u1", "Hey Alice, how are you?")

    print("Inbox for u1:", chat_service.fetch_inbox("u1"))
    print("Inbox for u2:", chat_service.fetch_inbox("u2"))

    chat_service.create_group("g1", ["u1", "u2", "u3"])
    chat_service.send_group_message("u1", "g1", "Hello everyone!")

    print("Group chat history:")
    for msg in chat_service.get_group_history("g1"):
        print(msg)
