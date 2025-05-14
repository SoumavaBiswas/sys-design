import util
import heapq
import uuid
from util import Location  # Assuming Location(lat, lng) is defined

class DeliveryAgent:
    def __init__(self, name, phn, vehicle_no, location: Location):
        self.aid = str(uuid.uuid4())
        self.name = name
        self.phn = phn
        self.vehicle_no = vehicle_no
        self.is_available = True
        self.current_order = None
        self.location = location  # Track current agent location
        self.completed_orders = []  # Store completed deliveries

    def update_availability(self, availability):
        self.is_available = availability
        if availability:
            self.current_order = None  # Unassign order when available

    def assign_order(self, oid):
        if not self.is_available:
            return f"Agent {self.name} is already assigned to another order!"
        self.update_availability(False)
        self.current_order = oid
        return f"Order {oid} assigned to agent {self.name}."

    def deliver_order(self):
        if self.current_order is None:
            return f"No active order assigned to {self.name}."
        self.completed_orders.append(self.current_order)  # Store delivered order
        self.update_availability(True)
        return f"Order {self.current_order} delivered successfully!"
    
    def update_location(self, new_location: Location):
        """Simulate real-time tracking by updating location"""
        self.location = new_location
        return f"Agent {self.name}'s location updated to {self.location}."




class AgentService:
    def __init__(self):
        self.agents = {}
    

    def add_agent(self, agent: DeliveryAgent):
        self.agents[agent.aid] = agent
    

    def get_available_agent(self, location):
        ans = []
        for agent in self.agents.values():
            if agent.is_available:
                distance = util.get_distance(location.lat, agent.lat, location.lng, agent.lng)
                heapq.heappush(ans, (distance, agent))
        if not ans:
            return None
        return heapq.heappop(ans)[1]
        
    def make_free(self, aid):
        agent = self.agents.get(aid)
        if agent:
            agent.updateAvailability(True)

                    

    
