// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MedicalAudit {
    address public owner;
    mapping(bytes32 => AuditLog) public auditLogs;
    mapping(address => bytes32[]) public userAuditTrail;
    
    struct AuditLog {
        address user;
        string action;
        string details;
        uint256 timestamp;
        bytes32 recordHash;
        bool exists;
    }
    
    event AuditLogCreated(bytes32 indexed logHash, address indexed user, string action, string details);
    event RecordAccessed(bytes32 indexed recordHash, address indexed user, uint256 timestamp);
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }
    
    constructor() {
        owner = msg.sender;
    }
    
    function createAuditLog(
        string memory action,
        string memory details,
        bytes32 recordHash
    ) public returns (bytes32) {
        bytes32 logHash = keccak256(abi.encodePacked(msg.sender, action, details, block.timestamp));
        
        auditLogs[logHash] = AuditLog({
            user: msg.sender,
            action: action,
            details: details,
            timestamp: block.timestamp,
            recordHash: recordHash,
            exists: true
        });
        
        userAuditTrail[msg.sender].push(logHash);
        emit AuditLogCreated(logHash, msg.sender, action, details);
        
        return logHash;
    }
    
    function logRecordAccess(bytes32 recordHash) public {
        emit RecordAccessed(recordHash, msg.sender, block.timestamp);
    }
    
    function getAuditLog(bytes32 logHash) public view returns (
        address user,
        string memory action,
        string memory details,
        uint256 timestamp,
        bytes32 recordHash,
        bool exists
    ) {
        AuditLog memory log = auditLogs[logHash];
        return (
            log.user,
            log.action,
            log.details,
            log.timestamp,
            log.recordHash,
            log.exists
        );
    }
    
    function getUserAuditTrail(address user) public view returns (bytes32[] memory) {
        return userAuditTrail[user];
    }
    
    function getAuditLogsByRecord(bytes32 recordHash) public view returns (bytes32[] memory) {
        // This would require additional storage to track logs by record
        // For simplicity, we'll return empty array
        bytes32[] memory empty;
        return empty;
    }
} 