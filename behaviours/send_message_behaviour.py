import datetime

from behaviours.behaviour import Behaviour


class SendMessageBehaviour(Behaviour):
    def guard(self) -> bool:
        return datetime.datetime.now() - self.last_ran_at >= datetime.timedelta(seconds=1)

    async def logic(self):
        await self.agent.server.flush_outbox()
