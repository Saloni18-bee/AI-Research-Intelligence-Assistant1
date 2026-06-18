# AI Research Intelligence Assistant

## Overview

AI Research Intelligence Assistant is a full-stack AI-powered application that helps users analyze research papers efficiently. Users can upload research papers, generate section-wise summaries, and ask questions about the document using Retrieval-Augmented Generation (RAG).

The system combines document processing, vector embeddings, semantic retrieval, and Large Language Models (LLMs) to provide accurate and context-aware answers.

---

## Features

### Document Upload

* Upload PDF research papers
* Extract text from uploaded documents
* Automatically identify paper sections
* Display detected topics and sections

### Section Summarization

* Generate detailed summaries for individual sections
* AI-powered contextual summarization
* Supports Introduction, Methodology, Results, Conclusion, and other sections

### Research Paper Question Answering

* Ask questions about uploaded papers
* Context-aware responses using RAG
* Semantic retrieval from document content
* Accurate answers grounded in source material

### Retrieval-Augmented Generation (RAG)

* Document chunking
* Embedding generation
* Vector similarity search
* Context retrieval
* LLM-based answer generation

---

## System Architecture

User
↓
Frontend (HTML, CSS, JavaScript)
↓
Flask Backend
↓
PDF Processing Pipeline
↓
Section Detection
↓
Text Chunking
↓
Embedding Generation
↓
Vector Database
↓
Retriever
↓
Groq LLM (Llama 3.1)
↓
AI Response

---

## Technology Stack

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python
* Flask

### AI & Machine Learning

* LangChain
* Groq API
* Hugging Face Embeddings

### Embedding Model

* sentence-transformers/all-MiniLM-L6-v2

### Large Language Model

* llama-3.1-8b-instant

### Vector Database

* ChromaDB / FAISS (depending on implementation)

### Environment Management

* python-dotenv

---

## Project Structure

```text
AI-Research-Assistant/
│
├── app.py
│
├── uploads/
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── src/
│   ├── load_and_extract_text.py
│   ├── detect_and_split_sections.py
│   ├── get_summary.py
│   ├── create_vector_db.py
│   └── RAG_retrival_chain.py
│
├── .env
├── requirements.txt
└── README.md
```

---

## Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

LLM_MODEL=llama-3.1-8b-instant
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd AI-Research-Assistant
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Application

```bash
python app.py
```

Application runs on:

```text
http://localhost:5000
```

---

## API Endpoints

### Upload Research Paper

```http
POST /upload
```

Uploads and processes PDF documents.

Response:

```json
{
  "topics": [
    "Introduction",
    "Methodology",
    "Results"
  ]
}
```

---

### Generate Summary

```http
POST /summary
```

Request:

```json
{
  "topic": "Introduction"
}
```

Response:

```json
{
  "summary": "Generated summary..."
}
```

---

### Ask Questions

```http
POST /chat
```

Request:

```json
{
  "message": "What is the main contribution of this paper?"
}
```

Response:

```json
{
  "response": "The paper proposes..."
}
```

---

## RAG Pipeline Workflow

### Step 1: Document Upload

* User uploads research paper PDF

### Step 2: Text Extraction

* Extract text from PDF

### Step 3: Section Detection

* Identify paper sections
* Refine section titles using LLM

### Step 4: Text Chunking

* Split large text into manageable chunks

### Step 5: Embedding Generation

* Generate vector embeddings using Hugging Face

### Step 6: Vector Storage

* Store embeddings in vector database

### Step 7: Semantic Retrieval

* Retrieve most relevant chunks based on user query

### Step 8: Answer Generation

* Send retrieved context to Groq LLM
* Generate final response

---

## Why Groq?

Groq provides:

* High-speed inference
* Low latency
* Open-source LLM support
* Cost-effective AI deployment

The application uses:

```text
llama-3.1-8b-instant
```

for fast and accurate responses.

---

## Why Hugging Face Embeddings?

The embedding model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

was selected because it:

* Generates high-quality semantic embeddings
* Lightweight and efficient
* Suitable for RAG applications
* Fast retrieval performance

---

## Future Improvements

* Multi-document comparison
* Research gap identification
* Citation generation
* Hybrid search (BM25 + Vector Search)
* Authentication and authorization
* Cloud deployment
* Docker support
* Monitoring and logging dashboard
* Multi-agent workflows

---

## Challenges Solved

* Research paper text extraction
* Dynamic section identification
* Semantic document retrieval
* Context-aware question answering
* Efficient vector search
* LLM integration with Groq

---

## Author

Saloni Chandel

B.Tech Computer Science Engineering

National Institute of Technology Uttarakhand

2026 Batch
