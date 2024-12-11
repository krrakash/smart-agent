// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title SmartAgent
 * @dev A contract for managing messages sent to an agent, including the ability to acknowledge messages.
 */
contract SmartAgent {
    /// @notice The owner of the SmartAgent.
    address public owner;

    /**
     * @dev Initializes the SmartAgent contract and sets the owner.
     * @param _owner The address of the owner of the SmartAgent.
     * @notice The owner must be a valid address (not the zero address).
     */
    constructor(address _owner) {
        require(_owner != address(0), "Invalid owner address");
        owner = _owner;
    }

    /**
     * @dev Restricts function execution to only the owner of the contract.
     */
    modifier onlyOwner() {
        require(msg.sender == owner, "Caller is not the owner");
        _;
    }

    /**
     * @dev Represents a message in the SmartAgent's inbox.
     * @param message The content of the message.
     * @param sender The address of the sender of the message.
     */
    struct Message {
        string message;   // The message content
        address sender;   // The address of the sender
    }

    /// @notice Array to store all messages sent to the SmartAgent.
    Message[] public inBox;

    /**
     * @dev Emitted when a message is sent to the SmartAgent.
     * @param sender The address of the sender.
     * @param receiver The address of the receiver (the SmartAgent).
     * @param messageId The ID of the message in the inbox.
     * @param message The content of the message.
     */
    event MessageSent(address indexed sender, address indexed receiver, uint256 messageId, string message);

    /**
     * @dev Emitted when a message is acknowledged by the owner.
     * @param messageId The ID of the acknowledged message.
     */
    event MessageAcknowledged(uint256 indexed messageId);

    /**
     * @notice Adds a message to the SmartAgent's inbox.
     * @dev The sender must not be the SmartAgent itself.
     * @param sender The address of the sender.
     * @param message The content of the message.
     */
    function addToInbox(address sender, string memory message) public {
        require(sender != address(this), "Cannot send a message to self");

        // Add the message to the inbox
        inBox.push(Message(message, sender));

        // Emit the message sent event
        emit MessageSent(sender, address(this), inBox.length - 1, message);
    }

    /**
     * @notice Acknowledges a message and removes it from the inbox.
     * @dev Only the owner can acknowledge messages. The message ID must be valid.
     * @param messageId The ID of the message to acknowledge.
     */
    function ackMsg(uint256 messageId) public onlyOwner {
        require(messageId < inBox.length, "Invalid message ID");

        // Emit the message acknowledged event
        emit MessageAcknowledged(messageId);

        // Remove the message from the inbox by replacing it with the last message and then popping the array
        inBox[messageId] = inBox[inBox.length - 1];
        inBox.pop();
    }
}
