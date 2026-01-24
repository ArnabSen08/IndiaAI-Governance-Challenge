# Setup Guide

## Prerequisites

- Python 3.8+
- pip or conda
- Git
- OpenAI API key (for LLM access)
- GitHub account (for repository)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ready-tensor.git
cd ready-tensor
```

### 2. Create Virtual Environment

**On Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# .env
OPENAI_API_KEY=your_openai_api_key_here
```

**Getting your OpenAI API Key:**
1. Go to https://platform.openai.com/api-keys
2. Create a new secret key
3. Copy and paste into `.env`

### 5. Prepare Your Documents

Place your documents in the `data/documents/` folder:

```
data/
└── documents/
    ├── document1.txt
    ├── document2.pdf
    └── document3.md
```

Supported formats:
- `.txt` - Plain text files
- `.pdf` - PDF documents
- `.md` - Markdown files

### 6. Build the Vector Store

```bash
python src/document_loader.py
```

This will:
- Load all documents from `data/documents/`
- Split them into chunks
- Create embeddings
- Store in `data/vectorstore/`

### 7. Run the Assistant

```bash
python src/rag_assistant.py
```

Or use the Jupyter notebook:

```bash
jupyter notebook notebooks/demo.ipynb
```

## Project Structure

```
ready-tensor/
├── src/
│   ├── rag_assistant.py       # Main QA system
│   ├── document_loader.py     # Document ingestion
│   ├── retriever.py           # Retrieval logic
│   └── __init__.py
├── data/
│   ├── documents/             # Your documents here
│   └── vectorstore/           # Vector store (generated)
├── notebooks/
│   └── demo.ipynb             # Interactive demo
├── docs/
│   ├── index.html             # GitHub Pages home
│   ├── architecture.md        # System design
│   ├── examples.md            # Usage examples
│   └── setup.md               # This file
├── requirements.txt           # Python dependencies
├── _config.yml                # Jekyll config
├── .gitignore
├── .env.example               # Environment template
└── README.md
```

## Configuration

### Vector Store Options

Edit `src/rag_assistant.py` to use different vector stores:

```python
# Using FAISS (default)
from langchain.vectorstores import FAISS
vectorstore = FAISS.from_documents(docs, embeddings)

# Using Chroma
from langchain.vectorstores import Chroma
vectorstore = Chroma.from_documents(docs, embeddings)
```

### LLM Options

Switch between different language models:

```python
from langchain.chat_models import ChatOpenAI

# GPT-4
llm = ChatOpenAI(model="gpt-4", temperature=0.7)

# GPT-3.5 Turbo (default)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# Claude (with Anthropic API)
from langchain.chat_models import ChatAnthropic
llm = ChatAnthropic(model="claude-instant")
```

### Retrieval Parameters

Adjust retrieval behavior:

```python
retriever = vectorstore.as_retriever(
    search_type="similarity",  # or "mmr"
    search_kwargs={"k": 3}     # number of documents to retrieve
)
```

## Troubleshooting

### Issue: API Key Error
**Solution**: Ensure your `.env` file contains the correct `OPENAI_API_KEY`

### Issue: Module Not Found
**Solution**: Make sure your virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: Out of Memory
**Solution**: Reduce chunk size or number of documents:
```python
text_splitter = CharacterTextSplitter(
    chunk_size=500,      # Reduce from 1000
    chunk_overlap=50
)
```

### Issue: Slow Retrieval
**Solution**: Use MMR search type for diversity:
```python
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 3, "lambda_mult": 0.25}
)
```

## Next Steps

1. **Customize**: Modify the RAG pipeline for your use case
2. **Optimize**: Tune parameters for your dataset
3. **Deploy**: Create a REST API or web interface
4. **Monitor**: Add logging and error tracking
5. **Scale**: Use production-grade vector stores (Pinecone, Weaviate)

## Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Docs](https://platform.openai.com/docs/api-reference)
- [FAISS Documentation](https://faiss.ai/)
- [Vector Database Comparison](https://www.datacamp.com/blog/the-complete-guide-to-vector-databases)

## Support

For issues and questions:
- Check the [GitHub Issues](https://github.com/yourusername/ready-tensor/issues)
- Review [Architecture Guide](./architecture.md)
- See [Examples](./examples.md)

Happy learning! 🚀
