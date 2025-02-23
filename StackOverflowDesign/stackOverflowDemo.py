from StackOverflowDesign.user import User
from StackOverflowDesign.stackOverflow import StackOverflow

class StackOverflowDemo:
    @staticmethod
    def run():
        stackOverflow = StackOverflow()

        user1 = User("Soumava Biswas", "soumavabiswas@gmail.com")
        user2 = User("Sumana Biswas", "sumanabiswas@gmail.com")
        user3 = User("Indranil Biswas", "indranilbiswas15@gmail.com")

        stackOverflow.add_user(user1)
        stackOverflow.add_user(user2)
        stackOverflow.add_user(user3)

        qsn1 = stackOverflow.create_question("Question on Programming", "What is Python?", user1.uid, ["Python", "Programming"])
        print(qsn1)
        qsn2 = stackOverflow.create_question("New in Programming", "What is Java?", user2.uid, ["Java", "Programming"])
        print(qsn2)
        qsn3 = stackOverflow.create_question("Question on Basic Programming", "What is C++?", user3.uid, ["C++", "Programming"])
        print(qsn3)

        ans1 = stackOverflow.create_answer("Python is a programming language", qsn1.qid, user2.uid)
        ans2 = stackOverflow.create_answer("Java is a programming language", qsn2.qid, user3.uid)
        ans3 = stackOverflow.create_answer("C++ is a programming language", qsn3.qid, user1.uid)

        
        print(stackOverflow.add_comment("Answer is soo naive!", ans1.aid, user1))

        print(stackOverflow.upvote_question(qsn1.qid, user2.uid))
        print(stackOverflow.upvote_question(qsn2.qid, user3.uid))
        print(stackOverflow.upvote_answer(ans2.aid, user2.uid))

        print(stackOverflow.search_qns_by_tag("Programming"))
        print(stackOverflow.search_qns_by_user(user1.uid))
        print(stackOverflow.search_answer_by_user(user2.uid))



if __name__ == '__main__':
    stackOverflowDemo = StackOverflowDemo()
    stackOverflowDemo.run()