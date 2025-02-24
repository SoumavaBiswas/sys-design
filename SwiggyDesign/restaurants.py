import uuid
from item import Item

class Restaurant:
    def __init__(self, name, location):
        self.rid = str(uuid.uuid4())
        self.name = name
        self.location = location
        self.rating = 0
        self.total_rating = 0
        self.rating_count = 0
        self.food_items = {}
    

    def add_item(self, item: Item):
        if item.id not in self.food_items:
            self.food_items[item.id] = item
            return True
        return False
    
    def update_item(self, item: Item):
        if item.id in self.food_items:
            self.food_items[item.id] = item
            return True
        return False
    
    def remove_item(self, item):
        if item.id in self.food_items:
            del self.food_items[item.id]
            return True
        return False
    
    def update_rating(self, new_rating):
      self.total_rating += new_rating
      self.rating_count += 1
      self.rating = self.total_rating / self.rating_count
      return self