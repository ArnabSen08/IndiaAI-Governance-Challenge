# Quick Start Guide

## ✅ Project Status
This project is **fully functional** and matches the course requirements from the Ethereum and Solidity course.

## 🚀 Deploy to GitHub in 5 Minutes

### Step 1: Create GitHub Repository
1. Go to [GitHub](https://github.com) and create a new repository
2. Name it: `blockchain-lottery-dapp`
3. Make it **public** (required for free GitHub Pages)
4. **Don't** initialize with README

### Step 2: Push to GitHub
```bash
cd blockchain-lottery-dapp
git remote add origin https://github.com/YOUR_USERNAME/blockchain-lottery-dapp.git
git branch -M main
git push -u origin main
```

### Step 3: Enable GitHub Pages
1. Go to your repository on GitHub
2. Click **Settings** tab
3. Scroll to **Pages** section
4. Under **Source**, select **GitHub Actions**
5. Wait for deployment (check **Actions** tab)

### Step 4: Deploy Smart Contract
1. Get Sepolia testnet ETH from faucets:
   - [Google Cloud Faucet](https://cloud.google.com/application/web3/faucet/ethereum/sepolia)
   - [Alchemy Faucet](https://www.alchemy.com/faucets/ethereum-sepolia)

2. Create `.env` file:
```env
PRIVATE_KEY="your_metamask_private_key"
INFURA_URL="https://sepolia.infura.io/v3/your_project_id"
```

3. Deploy contract:
```bash
npm run deploy
```

4. Copy the deployed contract address from console output

### Step 5: Update Frontend
1. Open `frontend/src/lottery.js`
2. Replace `YOUR_DEPLOYED_CONTRACT_ADDRESS_HERE` with your actual contract address
3. Commit and push changes:
```bash
git add .
git commit -m "Update contract address"
git push
```

## 🎯 Your DApp Will Be Live At:
`https://YOUR_USERNAME.github.io/blockchain-lottery-dapp`

## ⚠️ Important Notes
- Use **Sepolia testnet** only (never mainnet)
- Keep your private key secure
- This is for educational purposes only

## 🆘 Need Help?
- Check `DEPLOYMENT.md` for detailed instructions
- Ensure MetaMask is on Sepolia network
- Verify you have sufficient testnet ETH