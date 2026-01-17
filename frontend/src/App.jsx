import React, { useState, useEffect } from "react";
import web3 from "./web3";
import lottery from "./lottery";
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
      try {
        const manager = await lottery.methods.manager().call();
        const players = await lottery.methods.getPlayers().call();
        const balance = await web3.eth.getBalance(lottery.options.address);
        const accounts = await web3.eth.getAccounts();

        setManager(manager);
        setPlayers(players);
        setBalance(balance);
        setAccount(accounts[0] || "");
      } catch (error) {
        console.error("Error fetching data:", error);
        setMessage("Error connecting to the blockchain. Please check your MetaMask connection.");
      }
    }

    fetchData();
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();
    
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
              <span className="value">{manager}</span>
            </div>
            <div className="info-item">
              <span className="label">Your Account:</span>
              <span className="value">{account}</span>
            </div>
            <div className="info-item">
              <span className="label">Players:</span>
              <span className="value">{players.length}</span>
            </div>
            <div className="info-item">
              <span className="label">Prize Pool:</span>
              <span className="value">{web3.utils.fromWei(balance, "ether")} ETH</span>
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