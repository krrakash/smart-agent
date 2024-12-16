from agent import AutonomousAgent
from handlers.handler import Handler
from message import Message


class HelloHandler(Handler):

    def __init__(self, agent: AutonomousAgent):
        super().__init__(agent)

    def handle_message(self, message: Message) -> bool:
        if "hello" in message.message.lower():
            self.agent.print(f"Hello message received: {message.__dict__}")
            return True
        return False
