// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract InventoryManager {
    address public owner;

    struct Product {
        string metrcId;
        string strain;
        uint256 weight;
        bool verified;
    }

    mapping(string => Product) public products; // key: METRC ID

    event ProductAdded(string metrcId, string strain, uint256 weight);
    event ProductVerified(string metrcId);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function addProduct(string memory _metrcId, string memory _strain, uint256 _weight) public onlyOwner {
        products[_metrcId] = Product(_metrcId, _strain, _weight, false);
        emit ProductAdded(_metrcId, _strain, _weight);
    }

    function verifyProduct(string memory _metrcId) public onlyOwner {
        require(bytes(products[_metrcId].metrcId).length > 0, "Product not found");
        products[_metrcId].verified = true;
        emit ProductVerified(_metrcId);
    }

    function isVerified(string memory _metrcId) public view returns (bool) {
        return products[_metrcId].verified;
    }

    function getProduct(string memory _metrcId) public view returns (string memory, string memory, uint256, bool) {
        Product memory p = products[_metrcId];
        return (p.metrcId, p.strain, p.weight, p.verified);
    }
}
