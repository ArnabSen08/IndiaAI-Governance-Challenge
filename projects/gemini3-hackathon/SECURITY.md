# Security Notice

## API Key Management

🔐 **This repository does NOT contain any API keys for security reasons.**

### For Users:
- **Get your own API key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Local development**: Copy `.env.example` to `.env` and add your key
- **Web demo**: Enter your API key directly in the interface
- **Never commit API keys**: Always use environment variables or user input

### Security Best Practices Implemented:

✅ **No hardcoded API keys** in source code  
✅ **Environment variables** for local development  
✅ **User-provided keys** for web demo  
✅ **Clear documentation** on obtaining API keys  
✅ **Gitignore** includes `.env` files  

### For Contributors:
- Never commit `.env` files
- Use `.env.example` for documentation
- Always prompt users for their own API keys
- Follow principle of least privilege

## Reporting Security Issues

If you discover a security vulnerability, please email the repository owner rather than opening a public issue.

---

**Remember**: Treat your API keys like passwords. Never share them publicly or commit them to version control.