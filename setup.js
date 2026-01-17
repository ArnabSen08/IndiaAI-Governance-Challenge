#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('🎰 Blockchain Lottery DApp Setup');
console.log('================================\n');

// Check if Node.js version is compatible
const nodeVersion = process.version;
const majorVersion = parseInt(nodeVersion.slice(1).split('.')[0]);

if (majorVersion < 16) {
    console.error('❌ Node.js version 16 or higher is required');
    console.error(`Current version: ${nodeVersion}`);
    process.exit(1);
}

console.log('✅ Node.js version check passed');

// Install dependencies
console.log('\n📦 Installing dependencies...');
try {
    execSync('npm install', { stdio: 'inherit' });
    console.log('✅ Backend dependencies installed');
} catch (error) {
    console.error('❌ Failed to install backend dependencies');
    process.exit(1);
}

// Install frontend dependencies
console.log('\n📦 Installing frontend dependencies...');
try {
    execSync('npm install', { cwd: 'frontend', stdio: 'inherit' });
    console.log('✅ Frontend dependencies installed');
} catch (error) {
    console.error('❌ Failed to install frontend dependencies');
    process.exit(1);
}

// Compile smart contracts
console.log('\n🔨 Compiling smart contracts...');
try {
    execSync('npm run compile', { stdio: 'inherit' });
    console.log('✅ Smart contracts compiled successfully');
} catch (error) {
    console.error('❌ Failed to compile smart contracts');
    process.exit(1);
}

// Run tests
console.log('\n🧪 Running tests...');
try {
    execSync('npm run test', { stdio: 'inherit' });
    console.log('✅ All tests passed');
} catch (error) {
    console.error('❌ Tests failed');
    process.exit(1);
}

// Create .env file if it doesn't exist
const envPath = '.env';
const envExamplePath = '.env.example';

if (!fs.existsSync(envPath) && fs.existsSync(envExamplePath)) {
    console.log('\n📝 Creating .env file...');
    fs.copyFileSync(envExamplePath, envPath);
    console.log('✅ .env file created from .env.example');
    console.log('⚠️  Please update .env with your actual values before deploying');
}

console.log('\n🎉 Setup completed successfully!');
console.log('\nNext steps:');
console.log('1. Update .env file with your MetaMask private key and Infura URL');
console.log('2. Get Sepolia testnet ETH from faucets');
console.log('3. Deploy contract: npm run deploy');
console.log('4. Start frontend: npm run dev');
console.log('\nFor more details, see README.md and DEPLOYMENT.md');