from user import User
from swiggy import Swiggy 
from util import Location
from restaurants import Restaurant
from item import Item
from order import OrderStatus
from agentService import DeliveryAgent


class SwiggyDemo:
    @staticmethod
    def run():
        swiggy = Swiggy()

        # Creating users
        user1 = User(name="Soumava Biswas", email="soumavabiswas@gmail.com", phn_no=9178905678, location=Location(lat=22.603366, lng=88.414618))
        user2 = User(name="Sumana Biswas", email="sumana@gmail.com", phn_no=9178905679, location=Location(lat=22.603366, lng=88.414618))
        user3 = User(name="Indranil Biswas", email="indranil@gmail.com", phn_no=9178905680, location=Location(lat=22.6418497, lng=88.8692347))

        print(swiggy.add_user(user1))
        print(swiggy.add_user(user2))
        print(swiggy.add_user(user3))

        # Creating restaurants
        restaurant1 = Restaurant(name="Hatari", location=Location(lat=22.5929425, lng=88.4124183))
        restaurant2 = Restaurant(name="Oudh1590", location=Location(lat=22.592061, lng=88.4092296))

        print(swiggy.add_restaurant(restaurant1))
        print(swiggy.add_restaurant(restaurant2))

        # Adding menu items
        food1 = Item(name="Fried Rice", price=200)
        food2 = Item(name="Crispy Chilly Babycorn", price=250)
        food3 = Item(name="Chilli Paneer", price=280)

        print(swiggy.add_food_item(restaurant1.rid, food1))
        print(swiggy.add_food_item(restaurant1.rid, food2))
        print(swiggy.add_food_item(restaurant1.rid, food3))

        food4 = Item(name="Jeera Rice", price=350)
        food5 = Item(name="Shahi Paneer", price=380)
        food6 = Item(name="Dal Fry", price=180)

        print(swiggy.add_food_item(restaurant2.rid, food4))
        print(swiggy.add_food_item(restaurant2.rid, food5))
        print(swiggy.add_food_item(restaurant2.rid, food6))

        # Finding nearby restaurants
        print("Nearby Restaurants for User1:", swiggy.get_nearby_restaurant(user1.uid))
        print("Nearby Restaurants for User2:", swiggy.get_nearby_restaurant(user2.uid))
        print("Nearby Restaurants for User3:", swiggy.get_nearby_restaurant(user3.uid))

        # Placing an order
        print("\nPlacing an order for User1 at Hatari...")
        order = swiggy.place_order(user1.uid, restaurant1.rid, [food1, food2])
        if isinstance(order, str):
            print("Error:", order)
        else:
            print(f"Order placed successfully! Order ID: {order.oid}")

        # Creating delivery agents
        agent1 = DeliveryAgent(name="Rahul", location=Location(lat=22.5949425, lng=88.4124183), vehicle_no="WB12AB3456", location=Location(lat=22.59, lng=88.41))
        agent2 = DeliveryAgent(name="Amit", location=Location(lat=22.599061, lng=88.4092296), vehicle_no="WB12AB8496", location=Location(lat=22.53, lng=88.31))

        print(swiggy.agentService.add_agent(agent1))
        print(swiggy.agentService.add_agent(agent2))

        # Updating order status and assigning agent
        if not isinstance(order, str):  # Only proceed if order was placed successfully
            print("\nUpdating order status to CONFIRMED...")
            swiggy.update_order_status(order.oid, OrderStatus.CONFIRMED)

            print("\nUpdating order status to OUT_FOR_DELIVERY...")
            swiggy.update_order_status(order.oid, OrderStatus.OUT_FOR_DELIVERY)

            print("\nUpdating order status to DELIVERED...")
            swiggy.update_order_status(order.oid, OrderStatus.DELIVERED)

            # Rating the restaurant after delivery
            print("\nUser rating the restaurant...")
            print(swiggy.restaurantService.add_rating(restaurant1.rid, 4.5))


if __name__ == "__main__":
    SwiggyDemo.run()
