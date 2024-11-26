class Database:
    def __init__(self):
        # Using in-memory storage for simplicity
        self.users = {}
        self.swipes = {}
        self.matches = set()

    def add_user(self, user):
        self.users[user.id] = user
        return user

    def get_user(self, user_id):
        return self.users.get(user_id)

    def add_swipe(self, swiper_id, swiped_id, direction):
        if swiper_id not in self.swipes:
            self.swipes[swiper_id] = {}
        self.swipes[swiper_id][swiped_id] = direction

    def check_match(self, user1_id, user2_id):
        # Check if both users swiped right on each other
        user1_swipes = self.swipes.get(user1_id, {})
        user2_swipes = self.swipes.get(user2_id, {})
        
        if (user1_swipes.get(user2_id) == 'right' and 
            user2_swipes.get(user1_id) == 'right'):
            self.matches.add(frozenset([user1_id, user2_id]))
            return True
        return False 