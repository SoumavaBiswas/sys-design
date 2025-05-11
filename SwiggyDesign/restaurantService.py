import util
from restaurants import Restaurant

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
            

        