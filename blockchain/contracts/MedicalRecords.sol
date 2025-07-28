// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MedicalRecords {
    address public owner;
    mapping(bytes32 => MedicalRecord) public records;
    mapping(address => bool) public authorizedDoctors;
    mapping(address => bytes32[]) public patientRecords;
    
    struct MedicalRecord {
        string patientId;
        string diagnosis;
        string treatment;
        uint256 timestamp;
        address doctor;
        bool exists;
    }
    
    event RecordCreated(bytes32 indexed recordHash, string patientId, address doctor);
    event DoctorAuthorized(address indexed doctor);
    event DoctorRevoked(address indexed doctor);
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }
    
    modifier onlyAuthorizedDoctor() {
        require(authorizedDoctors[msg.sender] || msg.sender == owner, "Not authorized doctor");
        _;
    }
    
    constructor() {
        owner = msg.sender;
    }
    
    function authorizeDoctor(address doctor) public onlyOwner {
        authorizedDoctors[doctor] = true;
        emit DoctorAuthorized(doctor);
    }
    
    function revokeDoctor(address doctor) public onlyOwner {
        authorizedDoctors[doctor] = false;
        emit DoctorRevoked(doctor);
    }
    
    function createMedicalRecord(
        string memory patientId,
        string memory diagnosis,
        string memory treatment
    ) public onlyAuthorizedDoctor returns (bytes32) {
        bytes32 recordHash = keccak256(abi.encodePacked(patientId, diagnosis, treatment, block.timestamp));
        
        records[recordHash] = MedicalRecord({
            patientId: patientId,
            diagnosis: diagnosis,
            treatment: treatment,
            timestamp: block.timestamp,
            doctor: msg.sender,
            exists: true
        });
        
        patientRecords[msg.sender].push(recordHash);
        emit RecordCreated(recordHash, patientId, msg.sender);
        
        return recordHash;
    }
    
    function getMedicalRecord(bytes32 recordHash) public view returns (
        string memory patientId,
        string memory diagnosis,
        string memory treatment,
        uint256 timestamp,
        address doctor,
        bool exists
    ) {
        MedicalRecord memory record = records[recordHash];
        return (
            record.patientId,
            record.diagnosis,
            record.treatment,
            record.timestamp,
            record.doctor,
            record.exists
        );
    }
    
    function getPatientRecords(address patient) public view returns (bytes32[] memory) {
        return patientRecords[patient];
    }
} 