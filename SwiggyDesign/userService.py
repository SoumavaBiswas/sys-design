from user import User

class userService:
    def __init__(self):
        self.users = {}
    

    def add_user(self, user: User):
        self.users[user.uid] = user
    
    def get_user(self, uid):
        return self.users.get(uid, None)