// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PatientConsent {
    address public owner;
    mapping(address => Consent) public patientConsents;
    mapping(address => bool) public authorizedProviders;
    
    struct Consent {
        bool dataSharing;
        bool researchParticipation;
        bool emergencyAccess;
        uint256 lastUpdated;
        address patient;
        bool exists;
    }
    
    event ConsentUpdated(address indexed patient, bool dataSharing, bool researchParticipation, bool emergencyAccess);
    event ProviderAuthorized(address indexed provider);
    event ProviderRevoked(address indexed provider);
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }
    
    modifier onlyAuthorizedProvider() {
        require(authorizedProviders[msg.sender] || msg.sender == owner, "Not authorized provider");
        _;
    }
    
    constructor() {
        owner = msg.sender;
    }
    
    function authorizeProvider(address provider) public onlyOwner {
        authorizedProviders[provider] = true;
        emit ProviderAuthorized(provider);
    }
    
    function revokeProvider(address provider) public onlyOwner {
        authorizedProviders[provider] = false;
        emit ProviderRevoked(provider);
    }
    
    function updateConsent(
        bool dataSharing,
        bool researchParticipation,
        bool emergencyAccess
    ) public {
        patientConsents[msg.sender] = Consent({
            dataSharing: dataSharing,
            researchParticipation: researchParticipation,
            emergencyAccess: emergencyAccess,
            lastUpdated: block.timestamp,
            patient: msg.sender,
            exists: true
        });
        
        emit ConsentUpdated(msg.sender, dataSharing, researchParticipation, emergencyAccess);
    }
    
    function getConsent(address patient) public view returns (
        bool dataSharing,
        bool researchParticipation,
        bool emergencyAccess,
        uint256 lastUpdated,
        address patientAddr,
        bool exists
    ) {
        Consent memory consent = patientConsents[patient];
        return (
            consent.dataSharing,
            consent.researchParticipation,
            consent.emergencyAccess,
            consent.lastUpdated,
            consent.patient,
            consent.exists
        );
    }
    
    function hasValidConsent(address patient) public view returns (bool) {
        Consent memory consent = patientConsents[patient];
        return consent.exists && consent.dataSharing;
    }
} 