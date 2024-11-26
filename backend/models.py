import uuid
from datetime import datetime

class User:
    def __init__(self, name, age, bio, photos):
        self.id = str(uuid.uuid4())
        self.name = name
        self.age = age
        self.bio = bio
        self.photos = photos

class Match:
    def __init__(self, user1_id, user2_id):
        self.id = str(uuid.uuid4())
        self.user1_id = user1_id
        self.user2_id = user2_id
        self.timestamp = datetime.now() 