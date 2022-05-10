const { ethers } = require("hardhat");
const { BigNumber } = require("ethers");

async function main(){
    const ContractA = await ethers.getContractFactory("ContentBidTokenContract");

    // get contract by address
    let contractA = await ContractA.attach("0x5fbdb2315678afecb367f032d93f642f64180aa3")

    // deploy a new contract
    let contractA = await ContractA.deploy();
    await contractA.deployed();
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
