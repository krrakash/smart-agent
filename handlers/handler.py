from abc import abstractmethod
from agent import AutonomousAgent
from message import Message


class Handler:
    """
    Base class for handling messages within an AutonomousAgent.

    This class serves as a blueprint for implementing custom message handling logic.
    Subclasses should implement the `handle_message` method to define specific
    behavior for processing messages.

    Attributes:
        agent (AutonomousAgent): The agent associated with this handler.
    """

    def __init__(self, agent: AutonomousAgent):
        """
        Initializes the Handler class.

        Args:
            agent (AutonomousAgent): The agent to which this handler belongs.
        """
        self.agent = agent

    @abstractmethod
    def handle_message(self, message: Message) -> bool:
        """
        Processes a message sent to the agent.

        This method must be implemented in subclasses. It defines the logic for
        handling incoming messages from other agents or systems.

        Args:
            message (Message): The content of the message being handled.

        Returns:
            bool: True if the message was handled successfully, False otherwise.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        pass
