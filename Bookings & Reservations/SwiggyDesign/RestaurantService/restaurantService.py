import util
import uuid

class Item:
    def __init__(self, name, price):
        self.id = str(uuid.uuid4())
        self.name = name
        self.price = price
    

    def __str__(self):
        return f"Item(name={self.name}, price={self.price})"

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
      


class RestaurantService:
    def __init__(self):
        self.restaurants = {}
    
    def get_restaurant(self, rid):
        return self.restaurants.get(rid, None)
    
    def add_restaurant(self, restaurant: Restaurant):
        self.restaurants[restaurant.rid] = restaurant
    
    def add_food_item(self, rid, food_item):
        restaurant = self.restaurants.get(rid)
        if restaurant:
            if restaurant.add_item(food_item):
                return f"Successfully added {str(food_item)}."
            return f"{str(food_item)} already present."
        return f'Restaurant not found!'
    
    def update_food_item(self, rid, food_item):
        restaurant = self.restaurants.get(rid)
        if restaurant:
            if restaurant.update_item(food_item):
                return f"Successfully updated {str(food_item)}."
            return f"{str(food_item)} not present."
        return f'Restaurant not found!'
    
    
    def get_nearby_restaurants(self, lng, lat):
       return sorted(
        (restaurant for restaurant in self.restaurants.values()
         if util.get_distance(lat, restaurant.location.lat, lng, restaurant.location.lng) <= 5),
        key=lambda r: r.rating,  # Sort by highest rating
        reverse=True
    )

    def add_rating(self, rid, rating):
        restaurant = self.restaurants.get(rid, None)
        if restaurant:
            restaurant.update_rating(rating)
            return f"Successfully submitted rating ({rating})"
        return f'Restaurant not found!'
            

        