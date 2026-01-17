import React, { useState, useEffect } from "react";
import web3, { isWeb3Available } from "./web3";
import lottery, { isContractConfigured } from "./lottery";
import "./App.css";

function App() {
  const [manager, setManager] = useState("");
  const [players, setPlayers] = useState([]);
  const [balance, setBalance] = useState("");
  const [value, setValue] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [account, setAccount] = useState("");

  useEffect(() => {
    async function fetchData() {
      if (!isWeb3Available) {
        setMessage("⚠️ MetaMask not detected. Please install MetaMask to use this DApp.");
        return;
      }

      if (!isContractConfigured) {
        setMessage("⚠️ Smart contract not deployed yet. Please deploy the contract first.");
        return;
      }

      if (!web3 || !lottery) {
        setMessage("⚠️ Failed to connect to Web3. Please check your MetaMask connection.");
        return;
      }

      try {
        const manager = await lottery.methods.manager().call();
        const players = await lottery.methods.getPlayers().call();
        const balance = await web3.eth.getBalance(lottery.options.address);
        const accounts = await web3.eth.getAccounts();

        setManager(manager);
        setPlayers(players);
        setBalance(balance);
        setAccount(accounts[0] || "");
        setMessage(""); // Clear any error messages
      } catch (error) {
        console.error("Error fetching data:", error);
        setMessage("❌ Error connecting to the smart contract. Please make sure you're on Sepolia testnet.");
      }
    }

    fetchData();
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();
    
    if (!isContractConfigured) {
      setMessage("⚠️ Smart contract not deployed yet.");
      return;
    }
    
    if (!value || parseFloat(value) < 0.01) {
      setMessage("Please enter at least 0.01 ETH to participate!");
      return;
    }

    setLoading(true);
    setMessage("Waiting on transaction success...");

    try {
      const accounts = await web3.eth.getAccounts();
      
      await lottery.methods.enter().send({
        from: accounts[0],
        value: web3.utils.toWei(value, "ether"),
      });

      setMessage("🎉 You have been entered into the lottery!");
      setValue("");
      
      // Refresh data
      const players = await lottery.methods.getPlayers().call();
      const balance = await web3.eth.getBalance(lottery.options.address);
      setPlayers(players);
      setBalance(balance);
    } catch (error) {
      console.error("Error entering lottery:", error);
      setMessage("❌ Transaction failed. Please try again.");
    }
    
    setLoading(false);
  }

  async function handleClick() {
    if (!isContractConfigured) {
      setMessage("⚠️ Smart contract not deployed yet.");
      return;
    }

    setLoading(true);
    setMessage("Waiting on transaction success...");

    try {
      const accounts = await web3.eth.getAccounts();

      await lottery.methods.pickWinner().send({
        from: accounts[0],
      });

      setMessage("🏆 A winner has been picked!");
      
      // Refresh data
      const players = await lottery.methods.getPlayers().call();
      const balance = await web3.eth.getBalance(lottery.options.address);
      setPlayers(players);
      setBalance(balance);
    } catch (error) {
      console.error("Error picking winner:", error);
      setMessage("❌ Transaction failed. Only the manager can pick a winner.");
    }
    
    setLoading(false);
  }

  const isManager = account && manager && account.toLowerCase() === manager.toLowerCase();

  // Show setup instructions if contract is not configured
  if (!isContractConfigured) {
    return (
      <div className="app">
        <div className="container">
          <header className="header">
            <h1>🎰 Blockchain Lottery DApp</h1>
            <p className="subtitle">Smart Contract Setup Required</p>
          </header>

          <div className="info-card">
            <h2>🚀 Ready to Deploy!</h2>
            <p style={{ marginBottom: '20px', fontSize: '1.1rem', lineHeight: '1.6' }}>
              Your DApp is ready, but the smart contract needs to be deployed first.
            </p>
            
            <div className="setup-steps">
              <h3>Setup Steps:</h3>
              <ol style={{ textAlign: 'left', marginLeft: '20px', lineHeight: '1.8' }}>
                <li>Clone the repository: <code>git clone https://github.com/ArnabSen08/blockchain-lottery-dapp.git</code></li>
                <li>Install dependencies: <code>npm install</code></li>
                <li>Create <code>.env</code> file with your MetaMask private key and Infura URL</li>
                <li>Deploy to Sepolia: <code>npm run deploy</code></li>
                <li>Update <code>frontend/src/lottery.js</code> with the deployed contract address</li>
                <li>Rebuild and redeploy the frontend</li>
              </ol>
            </div>

            <div className="warning">
              <p><strong>⚠️ Important:</strong> Use only testnet ETH and a development wallet!</p>
            </div>

            <div style={{ marginTop: '30px' }}>
              <a href="https://github.com/ArnabSen08/blockchain-lottery-dapp" className="btn btn-primary" target="_blank" rel="noopener noreferrer">
                📚 View Setup Guide
              </a>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Show MetaMask connection prompt if Web3 is not available
  if (!isWeb3Available) {
    return (
      <div className="app">
        <div className="container">
          <header className="header">
            <h1>🎰 Blockchain Lottery DApp</h1>
            <p className="subtitle">MetaMask Required</p>
          </header>

          <div className="info-card">
            <h2>🦊 Install MetaMask</h2>
            <p style={{ marginBottom: '20px', fontSize: '1.1rem' }}>
              This DApp requires MetaMask to interact with the Ethereum blockchain.
            </p>
            
            <div style={{ marginBottom: '20px' }}>
              <a href="https://metamask.io/download/" className="btn btn-primary" target="_blank" rel="noopener noreferrer">
                Download MetaMask
              </a>
            </div>

            <p style={{ fontSize: '0.9rem', color: '#666' }}>
              After installing MetaMask, refresh this page to continue.
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>🎰 Blockchain Lottery DApp</h1>
          <p className="subtitle">Decentralized lottery powered by Ethereum</p>
        </header>

        <div className="info-card">
          <h2>Lottery Information</h2>
          <div className="info-grid">
            <div className="info-item">
              <span className="label">Manager:</span>
              <span className="value">{manager || "Loading..."}</span>
            </div>
            <div className="info-item">
              <span className="label">Your Account:</span>
              <span className="value">{account || "Not connected"}</span>
            </div>
            <div className="info-item">
              <span className="label">Players:</span>
              <span className="value">{players.length}</span>
            </div>
            <div className="info-item">
              <span className="label">Prize Pool:</span>
              <span className="value">{web3 ? web3.utils.fromWei(balance, "ether") : "0"} ETH</span>
            </div>
          </div>
        </div>

        <div className="action-card">
          <form onSubmit={handleSubmit}>
            <h3>🎲 Enter the Lottery</h3>
            <p>Minimum entry: 0.01 ETH</p>
            <div className="input-group">
              <label htmlFor="ethAmount">Amount of ETH to enter:</label>
              <input
                id="ethAmount"
                type="number"
                step="0.01"
                min="0.01"
                placeholder="0.01"
                value={value}
                onChange={(event) => setValue(event.target.value)}
                disabled={loading}
              />
            </div>
            <button 
              type="submit" 
              className="btn btn-primary"
              disabled={loading || !value}
            >
              {loading ? "Processing..." : "Enter Lottery"}
            </button>
          </form>
        </div>

        {isManager && (
          <div className="action-card manager-section">
            <h3>👑 Manager Actions</h3>
            <p>You are the manager of this lottery contract.</p>
            <button 
              onClick={handleClick}
              className="btn btn-secondary"
              disabled={loading || players.length === 0}
            >
              {loading ? "Processing..." : "Pick Winner"}
            </button>
          </div>
        )}

        {message && (
          <div className={`message ${message.includes('❌') ? 'error' : 'success'}`}>
            {message}
          </div>
        )}

        <div className="players-section">
          <h3>Current Players ({players.length})</h3>
          {players.length > 0 ? (
            <div className="players-list">
              {players.map((player, index) => (
                <div key={index} className="player-item">
                  <span className="player-number">#{index + 1}</span>
                  <span className="player-address">{player}</span>
                </div>
              ))}
            </div>
          ) : (
            <p className="no-players">No players yet. Be the first to enter!</p>
          )}
        </div>

        <footer className="footer">
          <p>Built with ❤️ using Ethereum, Solidity, and React</p>
          <p>⚠️ This is for educational purposes only. Use testnet ETH.</p>
        </footer>
      </div>
    </div>
  );
}

export default App;