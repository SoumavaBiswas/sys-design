from agentService import DeliveryAgent
import util
import heapq

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

                    

    
