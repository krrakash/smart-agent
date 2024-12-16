import datetime
from agent import AutonomousAgent
from behaviours.behaviour import Behaviour


class CheckBalanceBehaviour(Behaviour):

    def __init__(self, agent: AutonomousAgent):
        super().__init__(agent)

    def guard(self) -> bool:
        return datetime.datetime.now() - self.last_ran_at >= datetime.timedelta(seconds=10)

    async def logic(self):
        balance = await self.agent.interactor.check_balance()
        self.agent.print(f"Current Balance: {balance}")
