import Web3 from "web3";

let web3;

// Check if we're in browser and MetaMask is available
export const isWeb3Available = typeof window !== "undefined" && typeof window.ethereum !== "undefined";

if (isWeb3Available) {
  // We are in the browser and metamask is running.
  try {
    window.ethereum.request({ method: "eth_requestAccounts" });
    web3 = new Web3(window.ethereum);
  } catch (error) {
    console.error("Failed to connect to MetaMask:", error);
    web3 = null;
  }
} else {
  // We are on the server *OR* the user is not running metamask
  // Use a placeholder that won't cause errors
  web3 = null;
}

export default web3;
