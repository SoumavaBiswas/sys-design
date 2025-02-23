import uuid

class Answer:
    def __init__(self, body, uid, qid):
        self.body = body
        self.uid = uid
        self.qid = qid
        self.aid = str(uuid.uuid4())
        self.vote = 0
        self.comments = []
    
    def upvote(self):
        self.vote += 1
        return f"Answer upvoted successfully."
    
    def add_comment(self, comment):
        self.comments.append(comment)
        return f"Comment added successfully."

    def __str__(self):
        return f"Answer(body={self.body}, answer_vote={self.vote}, comments={self.comments})"