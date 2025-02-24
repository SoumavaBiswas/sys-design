import uuid

class UserNotFoundException(Exception):
    def __init__(self, msg):
        self.message = msg
        super().__init__(self.message)

class User:
    def __init__(self, name, email, phn_no, location):
        self.uid = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.phn = phn_no
        self.location = location