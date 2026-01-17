# Blockchain Lottery DApp

A decentralized lottery application built with Ethereum smart contracts and React frontend.

## 🚀 Features

- **Smart Contract**: Ethereum-based lottery contract with secure random winner selection
- **Web3 Integration**: Connect with MetaMask wallet
- **React Frontend**: Modern UI built with Vite and React
- **Hardhat Development**: Complete development environment with testing and deployment

## 🛠 Tech Stack

- **Blockchain**: Ethereum, Solidity
- **Frontend**: React, Vite, Web3.js
- **Development**: Hardhat, Node.js
- **Testing**: Mocha, Chai

## 📁 Project Structure

```
blockchain-lottery-dapp/
├── contracts/          # Smart contracts
│   └── Lottery.sol
├── frontend/           # React frontend application
│   ├── src/
│   ├── public/
│   └── package.json
├── ignition/           # Deployment scripts
├── test/              # Smart contract tests
├── hardhat.config.js  # Hardhat configuration
└── package.json       # Backend dependencies
```

## 🚀 Quick Start

### Prerequisites

- Node.js (v16 or higher)
- MetaMask browser extension
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/ArnabSen08/blockchain-lottery-dapp.git
cd blockchain-lottery-dapp
```

2. Install backend dependencies:
```bash
npm install
```

3. Install frontend dependencies:
```bash
cd frontend
npm install
cd ..
```

### Development

1. **Compile Smart Contracts**:
```bash
npm run compile
```

2. **Run Tests**:
```bash
npm run test
```

3. **Start Frontend Development Server**:
```bash
cd frontend
npm run dev
```

4. **Deploy to Testnet** (Sepolia):
```bash
npm run deploy
```

## 🔧 Configuration

1. Create `.env` file in the root directory:
```env
PRIVATE_KEY="your_metamask_private_key"
INFURA_URL="your_infura_sepolia_url"
```

2. Get test ETH from Sepolia faucet:
   - [Google Cloud Sepolia Faucet](https://cloud.google.com/application/web3/faucet/ethereum/sepolia)
   - [Alchemy Sepolia Faucet](https://www.alchemy.com/faucets/ethereum-sepolia)

## 🎮 How to Play

1. Connect your MetaMask wallet
2. Enter the lottery with minimum 0.01 ETH
3. Wait for other players to join
4. Manager can pick a winner (winner gets all ETH)

## 🧪 Smart Contract Features

- **Manager Role**: Contract deployer manages the lottery
- **Entry Fee**: Minimum 0.01 ETH to participate
- **Random Selection**: Secure pseudo-random winner selection
- **Automatic Payout**: Winner receives entire contract balance

## 📝 Available Scripts

### Backend (Smart Contract)
- `npm run compile` - Compile smart contracts
- `npm run test` - Run contract tests
- `npm run deploy` - Deploy to Sepolia testnet

### Frontend
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

## 🌐 Live Demo

Visit the live application: [https://arnabsen08.github.io/blockchain-lottery-dapp](https://arnabsen08.github.io/blockchain-lottery-dapp)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This is an educational project. Do not use real money on mainnet without proper security audits.

## 🔗 Resources

- [Ethereum Documentation](https://ethereum.org/developers/)
- [Hardhat Documentation](https://hardhat.org/docs)
- [React Documentation](https://reactjs.org/)
- [Web3.js Documentation](https://web3js.readthedocs.io/)