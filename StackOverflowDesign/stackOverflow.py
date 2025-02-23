from StackOverflowDesign.user import User
from StackOverflowDesign.question import Question
from StackOverflowDesign.answer import Answer

class StackOverflow:
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(StackOverflow, cls).__new__(cls)
            cls._instance.users = {}
            cls._instance.questions = {}
            cls._instance.answers = {}
        return cls._instance
    

    def add_user(self, user: User):
        self.users[user.uid] = user
        return user

    
    def create_question(self, title, body, uid, tags):
        qsn = Question(title, body, uid, tags)
        self.questions[qsn.qid] = qsn
        user = self.users[uid]
        user.add_question(qsn.qid)
        print("Question added successfully")
        return qsn
    
    def create_answer(self, ans, qid, uid):
        question = self.questions.get(qid)
        if question:
            answer = Answer(ans, uid, qid)
            question.answers.append(answer)
            self.answers[answer.aid] = answer
            print(f"Answer added successfully.")
            return answer
        print("Question not found.")
    
    def upvote_question(self, qid, uid):
        question = self.questions.get(qid)
        author_id = question.uid
        if question and author_id != uid:
            question.upvote()
            user = self.users.get(author_id)
            if user:
                user.update_reputation(5)
            return f"Question upvoted successfully."
        elif author_id == uid:
            return "You can't upvote your own question!"
        return "Question not found."
    
    def add_comment(self, comment, aid, uid):
        answer = self.answers.get(aid)
        if answer:
            answer.add_comment(comment)
            return "Added comment successfully"
        return "Answer not found"

    def upvote_answer(self, aid, uid):
        answer = self.answers.get(aid)
        if answer and answer.uid != uid:
            answer.upvote()
            user = self.users.get(answer.uid)
            if user:
                user.update_reputation(15)
            return "Answer upvoted successfully"
        elif answer.uid == uid:
            return "You can't upvote your own answer!"
        return "Answer not found."

    
    def search_qns_by_tag(self, tag):
        qns = [str(qsn) for qsn in self.questions.values() if tag in qsn.tags]
        return qns
    
    def search_qns_by_user(self, uid):
        qns = [str(qsn) for qsn in self.questions.values() if qsn.uid == uid]
        return qns
    
    def search_answer_by_user(self, uid):
        answers = []
        for qsn in self.questions.values():
            for ans in qsn.answers:
                if ans.uid == uid:
                    answers.append(str(ans))
        return answers