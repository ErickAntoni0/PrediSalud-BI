// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MegaMarketLoyalty {
    address public owner;
    mapping(address => uint256) public customerPoints;

    event PointsAwarded(address indexed customer, uint256 points);
    event PointsRedeemed(address indexed customer, uint256 points);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function awardPoints(address customer, uint256 points) public onlyOwner {
        customerPoints[customer] += points;
        emit PointsAwarded(customer, points);
    }

    function redeemPoints(uint256 points) public {
        require(customerPoints[msg.sender] >= points, "Not enough points");
        customerPoints[msg.sender] -= points;
        emit PointsRedeemed(msg.sender, points);
    }

    function getPoints(address customer) public view returns (uint256) {
        return customerPoints[customer];
    }
}