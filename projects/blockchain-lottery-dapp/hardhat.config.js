require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

const PRIVATE_KEY = process.env.PRIVATE_KEY;
const INFURA_URL = process.env.INFURA_URL;

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.19",
  networks: {
    hardhat: {
      // Default Hardhat network configuration
    },
    ...(PRIVATE_KEY && INFURA_URL ? {
      sepolia: {
        url: INFURA_URL,
        accounts: [PRIVATE_KEY]
      }
    } : {})
  },
  paths: {
    sources: "./contracts",
    tests: "./test",
    cache: "./cache",
    artifacts: "./artifacts"
  }
};