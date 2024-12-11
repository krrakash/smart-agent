import datetime

from behaviours.behaviour import Behaviour


class DiscoverAgentsBehaviour(Behaviour):
    def guard(self) -> bool:
        return datetime.datetime.now() - self.last_ran_at >= datetime.timedelta(seconds=10)

    async def logic(self):
        other_agents = self.agent.factory_helper.get_all_smart_agents()
        for agent in other_agents:
            if agent not in self.agent.other_agents:
                print(f"Discovered new agent at {agent}")
                self.agent.other_agents.append(agent)
