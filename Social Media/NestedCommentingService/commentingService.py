import time
from typing import Optional, List, Dict
from collections import defaultdict

class Comment:
    def __init__(self, comment_id: int, user_id: str, content: str, parent_id: Optional[int] = None):
        self.comment_id = comment_id
        self.user_id = user_id
        self.content = content
        self.parent_id = parent_id  # None if top-level comment
        self.timestamp = time.time()
        self.children: List['Comment'] = []

    def add_child(self, comment: 'Comment'):
        self.children.append(comment)

    def to_dict(self) -> Dict:
        return {
            "id": self.comment_id,
            "user": self.user_id,
            "content": self.content,
            "timestamp": self.timestamp,
            "children": [child.to_dict() for child in sorted(self.children, key=lambda c: c.timestamp)]
        }

class CommentService:
    def __init__(self):
        self.id_counter = 0
        self.comments_by_id: Dict[int, Comment] = {}
        self.comments_by_post: Dict[str, List[Comment]] = defaultdict(list)

    def _get_next_id(self) -> int:
        self.id_counter += 1
        return self.id_counter

    def add_comment(self, post_id: str, user_id: str, content: str, parent_id: Optional[int] = None) -> int:
        comment_id = self._get_next_id()
        comment = Comment(comment_id, user_id, content, parent_id)
        self.comments_by_id[comment_id] = comment

        if parent_id is None:
            self.comments_by_post[post_id].append(comment)
        else:
            parent_comment = self.comments_by_id.get(parent_id)
            if not parent_comment:
                raise Exception("Parent comment not found")
            parent_comment.add_child(comment)

        return comment_id

    def get_comments_for_post(self, post_id: str) -> List[Dict]:
        top_level_comments = self.comments_by_post.get(post_id, [])
        return [comment.to_dict() for comment in sorted(top_level_comments, key=lambda c: c.timestamp)]


if __name__ == "__main__":
    service = CommentService()

    post_id = "post_123"

    c1 = service.add_comment(post_id, "u1", "This is a great article!")
    c2 = service.add_comment(post_id, "u2", "I agree with @u1", parent_id=c1)
    c3 = service.add_comment(post_id, "u3", "But it missed a key point", parent_id=c1)
    c4 = service.add_comment(post_id, "u1", "What point did it miss?", parent_id=c3)
    c5 = service.add_comment(post_id, "u4", "Thanks everyone!")

    from pprint import pprint
    pprint(service.get_comments_for_post(post_id))
