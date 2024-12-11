import datetime

from behaviours.behaviour import Behaviour


class IncomingMessageBehaviour(Behaviour):
    def guard(self) -> bool:
        return datetime.datetime.now() - self.last_ran_at >= datetime.timedelta(seconds=1)

    async def logic(self):
        message = self.agent.interactor.get_inbox()
        if message:
            await self.agent.process_message(message[1], message[0])
            self.agent.interactor.ack_msg(0)
