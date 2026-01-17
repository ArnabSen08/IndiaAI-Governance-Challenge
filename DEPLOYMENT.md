# Deployment Guide

This guide will help you deploy the Blockchain Lottery DApp to GitHub Pages.

## Prerequisites

1. **GitHub Account**: Make sure you have a GitHub account
2. **MetaMask Wallet**: Install MetaMask browser extension
3. **Test ETH**: Get some Sepolia testnet ETH from faucets
4. **Infura Account**: Sign up for a free Infura account

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Name it `blockchain-lottery-dapp`
3. Make it public (required for free GitHub Pages)
4. Don't initialize with README (we already have one)

## Step 2: Push Code to GitHub

```bash
# Navigate to your project directory
cd blockchain-lottery-dapp

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: Blockchain Lottery DApp"

# Add your GitHub repository as origin
git remote add origin https://github.com/YOUR_USERNAME/blockchain-lottery-dapp.git

# Push to GitHub
git push -u origin main
```

## Step 3: Set Up Environment Variables

1. Create a `.env` file in the root directory:
```env
PRIVATE_KEY="your_metamask_private_key"
INFURA_URL="https://sepolia.infura.io/v3/your_project_id"
```

2. **IMPORTANT**: Never commit the `.env` file to GitHub!

## Step 4: Deploy Smart Contract

1. Install dependencies:
```bash
npm install
```

2. Compile the contract:
```bash
npm run compile
```

3. Deploy to Sepolia testnet:
```bash
npm run deploy
```

4. Copy the deployed contract address from the console output

## Step 5: Update Frontend Configuration

1. Update `frontend/src/lottery.js` with your deployed contract address
2. Update the ABI if you made any changes to the smart contract

## Step 6: Enable GitHub Pages

1. Go to your GitHub repository
2. Click on **Settings** tab
3. Scroll down to **Pages** section
4. Under **Source**, select **GitHub Actions**
5. The deployment will start automatically when you push changes

## Step 7: Access Your DApp

1. After deployment completes, your DApp will be available at:
   `https://YOUR_USERNAME.github.io/blockchain-lottery-dapp`

2. Make sure you're connected to Sepolia testnet in MetaMask

## Troubleshooting

### Common Issues:

1. **MetaMask not connecting**:
   - Make sure you're on Sepolia testnet
   - Refresh the page and try again

2. **Transaction failing**:
   - Check you have enough Sepolia ETH
   - Make sure you're entering at least 0.01 ETH

3. **Contract not found**:
   - Verify the contract address in `lottery.js`
   - Make sure the contract was deployed successfully

4. **GitHub Pages not updating**:
   - Check the Actions tab for deployment status
   - Make sure the workflow completed successfully

### Getting Test ETH:

1. **Google Cloud Faucet**: https://cloud.google.com/application/web3/faucet/ethereum/sepolia
2. **Alchemy Faucet**: https://www.alchemy.com/faucets/ethereum-sepolia
3. **Sepolia PoW Faucet**: https://sepolia-faucet.pk910.de/

## Security Notes

- **Never use real money**: Only use testnet ETH
- **Private Keys**: Never share or commit private keys
- **Development Only**: This is for educational purposes only

## Support

If you encounter issues:
1. Check the browser console for errors
2. Verify MetaMask is connected to Sepolia
3. Ensure you have sufficient test ETH
4. Check the GitHub Actions logs for deployment issues