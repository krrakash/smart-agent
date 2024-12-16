import datetime
import random

from agent import AutonomousAgent
from behaviours.behaviour import Behaviour
from handlers.handler import Message

word_alphabet = ["hello", "sun", "world", "space", "moon", "crypto", "sky", "ocean", "universe", "human"]


class RandomMessageBehaviour(Behaviour):

    def __init__(self, agent: AutonomousAgent):
        super().__init__(agent)
        self.message_id = 1

    def guard(self) -> bool:
        return datetime.datetime.now() - self.last_ran_at >= datetime.timedelta(seconds=2)

    async def logic(self):
        word1 = random.choice(word_alphabet)
        word2 = random.choice(word_alphabet)
        message = f"{word1} {word2}"
        await self.agent.server.send_to_outbox(
            Message(
                message=message,
                id=self.message_id,
            )
        )
        self.message_id += 1
