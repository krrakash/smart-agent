from abc import abstractmethod
from datetime import datetime

from agent import AutonomousAgent


class Behaviour:
    """
    Base class for defining a behavior for an AutonomousAgent. This class provides
    a structure for implementing guarded logic that runs asynchronously.

    Attributes:
        agent (AutonomousAgent): The agent associated with this behavior.
        last_ran_at (datetime): The timestamp of the last successful run of the behavior.
    """

    def __init__(self, agent: AutonomousAgent):
        """
        Initializes the Behaviour class.

        Args:
            agent (AutonomousAgent): The agent to which this behavior belongs.
        """
        self.agent = agent
        self.last_ran_at = datetime.now()

    @abstractmethod
    def guard(self) -> bool:
        """
        Determines whether the behavior should execute its logic.

        This method must be implemented in subclasses. It should return a boolean
        indicating whether the behavior is allowed to run.

        Returns:
            bool: True if the behavior's logic should execute, False otherwise.
        """
        pass

    @abstractmethod
    async def logic(self):
        """
        The main logic of the behavior.

        This method must be implemented in subclasses. It contains the
        asynchronous logic to be executed when the guard condition is met.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        pass

    async def run(self):
        """
        Executes the behavior if the guard condition is met.

        If `guard()` returns True, the `logic()` method is executed, and
        the `last_ran_at` timestamp is updated to the current time.
        """
        if self.guard():
            await self.logic()
            self.last_ran_at = datetime.now()
