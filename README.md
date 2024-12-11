# Smart Decentralised Agent Framework Documentation

[Sample Agent](https://github.com/krrakash/smart-agent/blob/main/sample.png)

#### Here's brief summary of the framework. For more detailed documentation of the Behaviour, Handler & AutonomousAgent classes. please go through respective files in [behaviour.py](https://github.com/krrakash/smart-agent/blob/main/behaviours/behaviour.py), [handler.py](https://github.com/krrakash/smart-agent/blob/main/handlers/handler.py), [agent.py](https://github.com/krrakash/smart-agent/blob/main/agent.py). There I've have added doc comments, which can be used to generate pydocs as well

### Note: 
1. **Make sure to use factory_address = 0xF2F1473545Cc0B63E8b5B6031E6e37F444291248 or you have deployed the factory contract responsible for deploying new agents using the [SmartContractFactoryDeployer](https://github.com/krrakash/SmartAgentFactoryDeployer)**
2. **Make sure different private keys are provided for each new instance of agent, and those accounts have enough eth and dai**

## Overview

The Autonomous Agent Framework provides a modular approach for creating, deploying, and managing blockchain-based
autonomous agents capable of performing periodic tasks and handling messages. Supports more than 2 agents. Everytime a
new agent is added is will be automatically discovered by other agents and its outBox will be inBox for all the other
agents and vice versa.

This documentation is split into:

1. **Agents**: Core logic for autonomous agents.
2. **Handlers**: Message processing modules.
3. **Behaviors**: Asynchronous task execution modules.
4. **Running the Project**: Steps to set up and execute the framework.
5. **Docker Setup**: Instructions for containerization and deployment.
6. **Development Notes**: Guidance on extending and maintaining the framework.

---

# 1. Agents

### AutonomousAgent Class

The main class representing an autonomous agent with deployment, message handling, and behavior execution capabilities.

#### **Attributes**

- **`factory_helper`**: Handles agent deployment via a smart contract factory.
- **`address`**: Blockchain address of the deployed agent.
- **`web3`**: Web3 instance for blockchain interaction.
- **`interactor`**: Interacts with the agent’s smart contract.
- **`other_agents`**: List of connected agents.
- **`handlers`**: Registered message handlers.
- **`behaviours`**: Registered behaviors for periodic execution.

#### **Methods**

- **`register_behaviour(behaviour)`**: Adds a behavior.
- **`register_handler(handler)`**: Adds a handler.
- **`run_behaviours()`**: Runs behaviors asynchronously.
- **`process_message(message, sender)`**: Processes incoming messages.
- **`run()`**: Starts the agent.

#### **Usage Example**

```python
agent = AutonomousAgent(provider_url, private_key, factory_address)
agent.register_behaviour(CheckBalanceBehaviour(agent))
agent.register_handler(HelloHandler(agent))
agent.run()
```

## 2. **Handlers**

### Handler Class

Abstract base class for processing incoming messages.

#### **Attributes**

- **`agent`**: Reference to the associated `AutonomousAgent`.

#### **Methods**

- **`handle_message(sender, message)`**: Custom logic for processing messages. Must be implemented in subclasses.

#### **Implementation Example**

```python
class HelloHandler(Handler):
    def handle_message(self, sender, message):
        if message == "hello":
            print(f"Hello received from {sender}")
            return True
        return False
```

## 3. **Behaviors**

### Behaviour Class

The `Behaviour` class serves as an abstract base class for defining asynchronous, periodic tasks executed by
an `AutonomousAgent`.

#### **Attributes**

- **`agent`**: The `AutonomousAgent` instance associated with this behavior.
- **`last_ran_at`**: Timestamp indicating the last execution of the behavior.

#### **Methods**

- **`guard()`**: Determines if the behavior should execute. Must be implemented in subclasses.
- **`logic()`**: Core asynchronous logic for the behavior. Must be implemented in subclasses.
- **`run()`**: Executes the behavior when `guard()` returns `True`.

#### **Implementation Example**

```python
class CheckBalanceBehaviour(Behaviour):
    def guard(self):
        # Executes logic only if the agent's balance is below a threshold.
        return self.agent.get_balance() < 1

    async def logic(self):
        # Logic for refilling the balance.
        print("Refilling balance...")
```

## 4. **Running the Project using Python**

deplyer_factory_address = 0xF2F1473545Cc0B63E8b5B6031E6e37F444291248
The agents can exceed limits on my free tenderly account, if above does not work, or you want to deploy your own factory, refer to [SmartContractFactoryDeployer](https://github.com/krrakash/SmartAgentFactoryDeployer)
```bash
pip install -r requirements.txt

python main.py \
-k private_key \
-f factory_address \
-r tenderly_rpc \
-d dai_contract_address (optional)
```

## 5. **Running Project using Docker**

```bash
docker build -t agent .
docker run agent \
  -k your_private_key \
  -f factory_address \
  -r tenderly_rpc \
  -d dai_address(optional)
```

### Parameter Details:

- **`-k`**: Private key for signing transactions.
- **`-f`**: Address of the smart contract factory used for deploying the agent.
- **`-r`**: RPC URL for blockchain communication (e.g., Tenderly, Infura, or Alchemy).
- **`-d`**: (Optional) Address of the DAI or any other token contract if needed.

## 6. **Development Notes**

### Extending Handlers

To add custom message processing logic:

1. **Create a subclass** of `Handler`.
2. **Implement the `handle_message` method** to define how the handler processes incoming messages.
3. **Register the handler** with the agent using the following code:
   ```python
   agent.register_handler(YourCustomHandler(agent))

### Extending Behaviors

To add custom periodic tasks:

1. **Create a subclass of** `Behaviour`.
2. **Implement the guard method to define when the behavior should execute.**
3. **Implement the logic method to define the behavior's asynchronous task logic.**
4. **Register the behavior with the agent using the following code:**
```python
agent.register_behaviour(YourCustomBehaviour(agent))
```
