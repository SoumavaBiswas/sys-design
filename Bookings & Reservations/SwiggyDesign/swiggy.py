from restaurantService import RestaurantService
from userService import UserService
from orderService import OrderService
from user import User, UserNotFoundException
from item import Item
from restaurants import Restaurant
from typing import List
from order import OrderStatus
from agentService import AgentService


class Swiggy:
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Swiggy, cls).__new__(cls)
            cls._instance.restaurantService = RestaurantService()
            cls._instance.userService = UserService()
            cls._instance.agentService = AgentService()
            cls._instance.orderService = OrderService()
        return cls._instance
    

    def add_user(self, user: User):
        return self.userService.add_user(user)
    
    def add_restaurant(self, restaurant: Restaurant):
        return self.restaurantService.add_restaurant(restaurant)
    
    def add_food_item(self, rid, food_item: Item):
        return self.restaurantService.add_food_item(rid, food_item)

    def get_nearby_restaurant(self, uid):
        user = self.userService.get_user(uid)
        if not user:
            raise UserNotFoundException("User Not Found!")
        return self.restaurantService.get_nearby_restaurants(user.location.lng, user.location.lat)
    
    def place_order(self, uid, rid, items: List[Item]):
        user = self.userService.get_user(uid)
        restaurant = self.restaurantService.get_restaurant(rid)

        if not user:
            return "User not found!"
        if not restaurant:
            return "Restaurant not found!"
        if not items:
            return "Cannot place an empty order!"
        self.orderService.place_order(uid, rid, items)
    
    def update_order_status(self, oid, status: OrderStatus):
        self.orderService.update_status(status)
        if status == OrderStatus.CONFIRMED:
            order = self.orderService.get(oid)
            restaurant = self.restaurantService.get_restaurant(order.rid)
            agent = self.agentService.get_available_agent(restaurant.location)
            if agent:
                agent.assignOrder(oid)
        if status == OrderStatus.DELIVERED:
            order = self.orderService.get(oid)
            agent = self.agentService.get_agent(order.aid)
            agent.make_free()
    


