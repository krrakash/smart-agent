import datetime
import random

from behaviours.behaviour import Behaviour

word_alphabet = ["hello", "sun", "world", "space", "moon", "crypto", "sky", "ocean", "universe", "human"]


class RandomMessageBehaviour(Behaviour):
    def guard(self) -> bool:
        return datetime.datetime.now() - self.last_ran_at >= datetime.timedelta(seconds=2)

    async def logic(self):
        word1 = random.choice(word_alphabet)
        word2 = random.choice(word_alphabet)
        message = f"{word1} {word2}"
        print(f"Generated message: {message}")
        if "hello" not in message and "crypto" not in message:
            return
        for address in self.agent.other_agents:
            tx_hash = self.agent.interactor.send_message(self.agent.address, address, message)
            print("sent message to agent ", address, tx_hash)
