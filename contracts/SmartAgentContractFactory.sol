// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./SmartAgent.sol"; // Ensure the SmartAgent contract is in the same directory or update the path accordingly

/**
 * @title SmartAgentContractFactory
 * @dev A factory contract to manage the creation and tracking of SmartAgent contracts.
 */
contract SmartAgentContractFactory {
    /// @notice Mapping to store deployed SmartAgent contracts per user.
    mapping(address => address) public smartAgentContractMapping;

    /// @notice Array to store all deployed SmartAgent contract addresses.
    address[] public smartAgents;

    /**
     * @dev Emitted when a new SmartAgent contract is created.
     * @param creator The address of the user who created the SmartAgent.
     * @param smartAgentAddress The address of the newly deployed SmartAgent contract.
     */
    event SmartAgentCreated(address indexed creator, address indexed smartAgentAddress);

    /**
     * @notice Deploys a new instance of the SmartAgent contract or returns an existing one for the sender.
     * @dev If the sender already has a SmartAgent contract, the existing address is returned. Otherwise, a new
     * SmartAgent contract is created and its address is stored and returned.
     * @return The address of the newly deployed or existing SmartAgent contract.
     */
    function createSmartAgent() public returns (address) {
        // Check if a SmartAgent already exists for the sender
        if (smartAgentContractMapping[msg.sender] != address(0)) {
            return smartAgentContractMapping[msg.sender]; // Return existing contract
        }

        // Deploy a new SmartAgent contract
        SmartAgent newSmartAgent = new SmartAgent(msg.sender);

        // Store the new SmartAgent contract address in the mapping
        smartAgentContractMapping[msg.sender] = address(newSmartAgent);

        // Add the new SmartAgent contract address to the array
        smartAgents.push(address(newSmartAgent));

        // Emit the creation event
        emit SmartAgentCreated(msg.sender, address(newSmartAgent));

        // Return the address of the newly created contract
        return address(newSmartAgent);
    }

    /**
     * @notice Gets the total number of SmartAgent contracts created.
     * @return The total number of SmartAgent contracts.
     */
    function getSmartAgentCount() public view returns (uint256) {
        return smartAgents.length;
    }

    /**
     * @notice Gets the address of a SmartAgent contract by its index.
     * @param index The index of the SmartAgent contract in the array.
     * @return The address of the specified SmartAgent contract.
     */
    function getSmartAgent(uint256 index) public view returns (address) {
        require(index < smartAgents.length, "Index out of bounds");
        return smartAgents[index];
    }
}
