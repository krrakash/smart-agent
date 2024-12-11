from agent import AutonomousAgent
from handlers.handler import Handler


class HelloHandler(Handler):

    def __init__(self, agent: AutonomousAgent):
        super().__init__(agent)

    def handle_message(self, sender: str, message: str) -> bool:
        if "hello" in message.lower():
            print(f"Hello message: {message} received from {sender}")
            return True
        return False
