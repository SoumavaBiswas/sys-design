import uuid

class Question:
    def __init__(self, title, body, user, tags):
        self.title = title
        self.body = body
        self.uid = user
        self.qid = str(uuid.uuid4())
        self.tags = tags
        self.answers = []
        self.qsn_vote = 0

    
    def add_answer(self, answer):
        self.answers.append(answer.id)
        return f"Answer added successfully."
    
    def upvote(self):
        self.qsn_vote += 1
        return f"Question upvoted successfully."
    
    def __str__(self):
        return f'Question(title={self.title}, body={self.body}, tags={self.tags}, answers={self.answers} question_vote={self.qsn_vote})'
    