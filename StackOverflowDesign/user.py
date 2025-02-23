import uuid

class User:
    def __init__(self, name, username):
        self.name = name
        self.username = username
        self.uid = str(uuid.uuid4())
        self.questions = []
        self.reputation = 0
    
    def add_question(self, qid):
        self.questions.append(qid)
    
    def update_reputation(self, inc):
        self.reputation += inc