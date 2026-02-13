# Quick Start - Publish Ready Tensor Repositories

## The Problem
Ready Tensor team got 404 errors trying to access your project repositories.

## The Solution (3 Steps)

### 1. Authenticate with GitHub (One-time setup)
```powershell
gh auth login
```
Follow the prompts to authenticate via web browser.

### 2. Run the Setup Script
```powershell
cd IndiaAI-Governance-Challenge
.\setup-ready-tensor-repos.ps1
```

This creates and publishes all 3 repositories automatically.

### 3. Update Your Publications

Use these URLs in your Ready Tensor publications:

#### Project 1: Production-Ready Multi-Agent AI System
```
https://github.com/ArnabSen08/agentic-ai-production-system
https://arnabsen08.github.io/agentic-ai-production-system/
```

#### Project 2: Agentic AI Essentials (RAG System)
```
https://github.com/ArnabSen08/ready-tensor
https://arnabsen08.github.io/ready-tensor/
```

#### Project 3: Multi-Agent Publication Assistant
```
https://github.com/ArnabSen08/publication-assistant
https://arnabsen08.github.io/publication-assistant/
```

---

## Verify Everything Works
```powershell
.\verify-repos.ps1
```

---

## Email Ready Tensor Team

Copy the email template from `READY_TENSOR_RESPONSE.md` and send it to the Ready Tensor team.

---

**That's it!** Your repositories will be public and accessible.

For detailed instructions, see: `READY_TENSOR_REPO_SETUP.md`
