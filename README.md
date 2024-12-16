# Smart Decentralized Agent Framework Documentation

![Sample Agent](https://github.com/krrakash/smart-agent/blob/main/Project_Running.mp4)

## Overview

The Smart Decentralized Agent Framework provides a modular structure for creating, deploying, and managing autonomous agents on the blockchain. Each agent can interact with other agents, perform periodic tasks, and handle messages in a decentralized, scalable environment. The framework supports multiple agents, with dynamic discovery of new agents. When a new agent is added, its outbox becomes the inbox for all other agents, and vice versa.

---

## Table of Contents

1. [Running the Project](#1-running-the-project-using-python)
2. [Docker Setup](#2-running-the-project-using-docker)
3. [Agents](#3-agents)
4. [Server-Modes](#4-Server-Modees)
5. [Handlers](#5-handlers)
6. [Behaviors](#6-behaviors)
7. [Development Notes](#7-development-notes)

---

## 1. **Running the Project using Python**

The .env file has two section of parameters one for each agent. Run the ```python main.py``` in two different terminal for two different instances of agents.
### Generating venv
```bash
python -m venv <venv_name>
source <venv>/bin/activate
```

### Running the project
```bash
pip install -r requirements.txt
python main.py 
```

## 2. **Running Project using Docker**

```bash
docker build -t agent .
docker run agent
```

## 3. Agents

### AutonomousAgent Class

The `AutonomousAgent` class is the main representation of an autonomous agent that can interact with the blockchain, other agents, and perform asynchronous tasks.

#### **Attributes**

- **`server`**: Manages communication, including message inboxes and outboxes.
- **`web3`**: Web3 instance for interacting with the Ethereum blockchain.
- **`interactor`**: Helper class for interacting with the agent’s smart contract.
- **`handlers`**: List of registered message handlers for processing incoming messages.
- **`behaviours`**: List of registered behaviors for periodic execution.

#### **Methods**

- **`register_behaviour(behaviour)`**: Adds a behavior to the agent's periodic task loop.
- **`register_handler(handler)`**: Adds a handler for processing incoming messages.
- **`run_behaviours()`**: Executes all registered behaviors in an asynchronous loop.
- **`process_message(message)`**: Processes an incoming message using registered handlers.
- **`run()`**: Starts the agent and orchestrates its behaviors and message processing.

#### **Usage Example**

```python
agent = AutonomousAgent(provider_url, private_key)
agent.register_behaviour(CheckBalanceBehaviour(agent))
agent.register_handler(HelloHandler(agent))
agent.run()
```
## 4. Server Modes Documentation

This project supports multiple server modes, enabling communication between agents using different protocols. Below are the details for configuring and running the server in **HTTP** and **Socket** modes. Additionally, the framework allows adding new server modes with minimal effort by inheriting the BaseServer class and implementing the required methods.

---

### Supported Server Modes

The server can operate in the following modes:

1. **HTTP Mode**: Uses HTTP protocol for communication between agents.
2. **Socket Mode**: Uses raw socket communication for lightweight and faster interactions.

---

### Configuration

The server's mode and parameters can be configured using environment variables.


## 5. Handlers

### Handler Class

The `Handler` class defines the logic for processing incoming messages. Each handler processes a specific type of message or implements custom logic based on the message's content.

#### **Attributes**

- **`agent`**: A reference to the associated `AutonomousAgent`. The handler uses this to interact with the agent and its components.

#### **Methods**

- **`handle_message(message)`**:  
  An abstract method that defines the logic for processing incoming messages. This method must be implemented in any subclass of `Handler`.

#### **Implementation Example**

Below is an example of a simple `Handler` subclass that processes "hello" messages:

```python
class HelloHandler(Handler):
    def handle_message(self, message):
        if message == "hello":
            print("Hello received!")
            return True
        return False
```

## 6. Behaviors

### Behaviour Class

The `Behaviour` class defines periodic tasks that an `AutonomousAgent` can execute asynchronously. Behaviors are modular and allow agents to perform tasks like monitoring, responding to events, or interacting with the blockchain at regular intervals.

#### **Attributes**

- **`agent`**: A reference to the associated `AutonomousAgent`. The behavior interacts with the agent's resources and environment.
- **`last_ran_at`**: A timestamp indicating when the behavior was last executed.

#### **Methods**

- **`guard()`**:  
  Determines whether the behavior should execute. This method must be implemented in subclasses. It should return `True` if the behavior's conditions for execution are met.

- **`logic()`**:  
  Defines the core asynchronous logic of the behavior. This method must be implemented in subclasses. It contains the task that the behavior performs.

- **`run()`**:  
  Combines the `guard()` and `logic()` methods. If `guard()` returns `True`, the `logic()` method is executed.

#### **Implementation Example**

Below is an example of a behavior that checks the agent's balance and refills it if it falls below a threshold:

```python
class CheckBalanceBehaviour(Behaviour):
    def guard(self):
        # Executes only if the agent's balance is below 1 unit.
        return self.agent.interactor.check_balance() < 1

    async def logic(self):
        # Logic for refilling the balance.
        print("Refilling balance...")
        # Example logic to send tokens or perform an action.
```
## 7. **Development Notes**

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

