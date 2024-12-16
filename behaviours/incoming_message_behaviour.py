import datetime

from behaviours.behaviour import Behaviour


class IncomingMessageBehaviour(Behaviour):
    def guard(self) -> bool:
        return datetime.datetime.now() - self.last_ran_at >= datetime.timedelta(seconds=1)

    async def logic(self):
        message = self.agent.get_message_to_process()
        while message:
            await self.agent.process_message(message)
            message = self.agent.get_message_to_process()
