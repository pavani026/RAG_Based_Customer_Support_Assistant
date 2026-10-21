# RAG-Based Customer Support Assistant

A **Retrieval-Augmented Generation (RAG)** customer support assistant. Instead of relying on an LLM's memory alone, it:

1. **Reads** a PDF knowledge base (product manuals, FAQs, policies)
2. **Stores** it as semantic embeddings in ChromaDB
3. **Retrieves** the most relevant information for each user query
4. **Generates** a grounded answer using OpenAI GPT-4o-mini
5. **Escalates** to a human agent (human-in-the-loop) when no reliable answer is found

You can use it three ways: a terminal chat (`main.py`), a **FastAPI REST API** (`api.py`), or as an **MCP server** (`mcp_server.py`) that any MCP client can call as a tool.

---

## Project Structure

```
RAG-Based-Customer-Support-Assistant/
│
├── PDF's/
│   ├── kb.pdf                    <- Knowledge base (what the bot reads)
│   ├── HLD_RAG_Pdf.pdf           <- High-Level Design document
│   ├── LLD PDF.pdf               <- Low-Level Design document
│   ├── Technical_Document.pdf    <- Full technical documentation
│   └── README.md                 <- PDF folder guide
│
├── db/                           <- ChromaDB vector store (auto-created)
│
├── ingest.py                     <- Load PDF -> chunk -> embed -> store
├── retrieval.py                  <- Search ChromaDB for relevant text
├── generator.py                  <- GPT-4o-mini answer generation
├── hitl.py                       <- Human-in-the-loop escalation (terminal)
├── graph.py                      <- LangGraph 2-node workflow
├── main.py                       <- Terminal chat entry point
├── api.py                        <- FastAPI REST API
├── mcp_server.py                 <- MCP server (tools for MCP clients)
├── requirements.txt              <- Dependencies
└── README.md                     <- This file
```

---

## Tech Stack

| Component       | Technology                                   |
|-----------------|----------------------------------------------|
| Language        | Python 3.10+                                 |
| PDF Loader      | LangChain PyPDFLoader                        |
| Text Splitter   | RecursiveCharacterTextSplitter               |
| Embedding Model | HuggingFace `all-MiniLM-L6-v2` (free, local) |
| Vector Database | ChromaDB (persisted locally)                 |
| LLM             | OpenAI GPT-4o-mini                           |
| Workflow Engine | LangGraph (StateGraph)                       |
| Human fallback  | Terminal input (CLI) / handoff message (API) |
| REST API        | FastAPI + Uvicorn                            |
| Agent tooling   | MCP server (official Python MCP SDK)         |
| Observability   | LangSmith tracing (optional)                 |

---

## System Flow

```
PDF Knowledge Base
       |
   ingest.py          <- chunks + embeds + stores in ChromaDB (once)
       |
  User Question
       |
  LangGraph graph
       |
  process_node        <- retrieval.py searches ChromaDB, generator.py writes the answer
       |
  +--------------------------------+
  | Relevant context found and     |
  | LLM answered?                  |
  |  YES -> escalate = False       |
  |  NO  -> escalate = True        |
  +--------------------------------+
       |
  output_node
       |
  +--------------------------------+
  | escalate == False?             |
  |  YES -> return AI answer       |
  |  NO  -> hitl.py (human)        |
  +--------------------------------+
       |
   Final Answer
```

---

## Setup & Installation

### 1. Clone the repository

```
git clone https://github.com/pavani026/RAG-Based-Customer-Support-Assistant.git
cd RAG-Based-Customer-Support-Assistant
```

### 2. Create a virtual environment

```
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Set your OpenAI API key

```
# Windows (Command Prompt)
set OPENAI_API_KEY=your_openai_api_key_here

# Mac/Linux
export OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Add your knowledge base

Place your PDF in the `PDF's/` folder and update the `PDFS` list at the top of `main.py` if you use a different file. The vector database is built automatically on first run.

---

## Usage

### Option A: Terminal chat

```
python main.py
```

### Option B: REST API (FastAPI)

```
uvicorn api:app --reload
```

Open http://127.0.0.1:8000/docs and call `POST /ask`:

```
{ "question": "What is the return policy?" }
```

Response:

```
{ "answer": "...", "escalated": false }
```

When no reliable answer is found, `escalated` is `true` and the API returns a handoff message instead of asking for terminal input.

### Option C: MCP server

`mcp_server.py` exposes two tools to any MCP client:

| Tool                    | What it does                                                        |
|-------------------------|---------------------------------------------------------------------|
| `search_knowledge_base` | Retrieves the most relevant passage from the ChromaDB knowledge base |
| `ask_support_assistant` | Retrieval + GPT-4o-mini answer generation (needs `OPENAI_API_KEY`)   |

Test it with the MCP Inspector (needs Node.js):

```
mcp dev mcp_server.py
```

To use it from an MCP client such as Claude Desktop, add it to the client's MCP config (use the full path to your venv's Python and to `mcp_server.py`):

```json
{
  "mcpServers": {
    "rag-customer-support": {
      "command": "/full/path/to/venv/bin/python",
      "args": ["/full/path/to/mcp_server.py"],
      "env": { "OPENAI_API_KEY": "your_openai_api_key_here" }
    }
  }
}
```

### Optional: LangSmith tracing

Set these before running any of the above and every graph run and LLM call is traced in LangSmith:

```
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=your_langsmith_key
export LANGSMITH_PROJECT=rag-customer-support
```

---

## Sample Interaction

```
Checking knowledge base...
Created 87 chunks
All PDFs processed and stored successfully
System Ready!

Ask a question (or type 'exit'): What is the return policy?

Final Answer:
ShopEase offers a 30-day easy return policy on most products. Items must be
unused, in original packaging, and with all tags intact.

Ask a question (or type 'exit'): What is the CEO's salary?

Escalating to human support...
User Query: What is the CEO's salary?
Enter human response: I'm sorry, that information is confidential.

Final Answer:
I'm sorry, that information is confidential.
```

---

## Architecture Concepts Applied

| #  | Concept                            | Where Applied                   |
|----|------------------------------------|---------------------------------|
| 1  | What is RAG                        | Entire system design            |
| 2  | PDF -> Chunk -> Embed -> Store     | `ingest.py`                     |
| 3  | Query -> Retrieve -> Answer        | `retrieval.py` + `generator.py` |
| 4  | Graph-based workflow               | `graph.py` (LangGraph)          |
| 5  | 2-node flow (Process -> Output)    | `process_node` + `output_node`  |
| 6  | Conditional routing by escalation  | `escalate` flag in state        |
| 7  | Customer support bot               | Full system use case            |
| 8  | Human-in-the-loop (HITL)           | `hitl.py` + `output_node`       |
| 9  | REST API exposure                  | `api.py` (FastAPI)              |
| 10 | Tool exposure over MCP             | `mcp_server.py`                 |

---

## Documents (`PDF's/` folder)

| File                     | Description                                                      |
|--------------------------|------------------------------------------------------------------|
| `kb.pdf`                 | Knowledge base: FAQs, policies, support content the bot reads    |
| `HLD_RAG_Pdf.pdf`        | High-Level Design: architecture, data flow, component overview   |
| `LLD PDF.pdf`            | Low-Level Design: module design, data structures, routing logic  |
| `Technical_Document.pdf` | Full technical documentation for engineering review              |

---

## Key Design Decisions

- **Chunk size 500, overlap 100**: balances retrieval precision and context completeness
- **Score threshold 1.5**: distance cutoff; above this the match is treated as irrelevant and escalated to a human
- **all-MiniLM-L6-v2**: free local embedding model, no API cost for encoding
- **GPT-4o-mini at temperature 0.3**: factual, consistent, cost-efficient responses
- **LangGraph over simple chains**: explicit state, clean HITL routing, easy to extend
- **Same graph behind CLI, API, and MCP**: one pipeline, three ways to use it

---

## Error Handling

| Scenario              | Handling                                         |
|-----------------------|--------------------------------------------------|
| PDF not found         | try/except in `ingest.py`, skips that file       |
| No relevant chunks    | `retrieve_docs()` returns None -> human fallback |
| Score too high (>1.5) | Returns None -> human fallback                   |
| LLM API failure       | `generate_answer()` returns None -> human fallback |
| ChromaDB error        | Returns None -> human fallback                   |

---

## Future Enhancements

- Multi-document dynamic upload via a web UI
- Async human handoff via Slack/email notifications
- Conversation memory for multi-turn support
- Docker containerization
- Replace ChromaDB with Pinecone for production scale
- Return a confidence score with each answer
- Retrieval evaluation (hit rate on a set of test questions)

---

## Author

**Pavani Korivi**
Innomatics Research Labs, Agentic AI Internship Project
Contact: korivipavani026@gmail.com | [GitHub](https://github.com/pavani026)
