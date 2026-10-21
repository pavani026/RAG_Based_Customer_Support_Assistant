# 📁 PDF's Folder — Document Guide

This folder contains all documents related to the RAG-Based Customer Support Assistant project.

---

## 📄 Files in This Folder

### 1. `kb.pdf` — Knowledge Base
**Purpose:** This is the core knowledge base that the RAG system reads and indexes.  
**Content:** Customer support Q&A covering orders, shipping, returns, payments, account management, products, technical support, and loyalty rewards for a fictional e-commerce platform (ShopEase).  
**Used by:** `ingest.py` → loaded, chunked, embedded, and stored in ChromaDB  
**When queried:** `retrieval.py` searches this content to answer user questions  

---

### 2. `HLD_RAG_Pdf.pdf` — High-Level Design
**Purpose:** Defines the overall system architecture.  
**Content includes:**
- System overview and problem definition
- Architecture diagram (all 10 system layers)
- Component descriptions (Document Loader, Chunking, Embedding, VectorStore, Retriever, LLM, Graph, Routing, HITL)
- Data flow tables (ingestion + query lifecycle)
- Technology choices with justifications (ChromaDB, LangGraph, all-MiniLM-L6-v2, GPT-4o-mini)
- Scalability considerations

---

### 3. `LLD PDF.pdf` — Low-Level Design
**Purpose:** Defines how the system is implemented internally at module level.  
**Content includes:**
- Detailed module-level design for all 6 Python files
- Data structures (Document, Chunk, Embedding, State object with code)
- LangGraph workflow design (nodes, edges, state transitions)
- Conditional routing logic (all 5 escalation triggers)
- HITL design (when/what/how escalation works)
- API and interface design
- Error handling table

---

### 4. `Technical_Document.pdf` — Technical Documentation
**Purpose:** Complete engineering reference — explains the system as if presenting to engineers.  
**Content includes:**
- What is RAG and why it's needed
- Full offline and online pipeline explanation
- Component interaction table
- Design decisions (chunk size, embedding strategy, retrieval approach, prompt design)
- LangGraph workflow with state transition diagram
- Conditional logic and intent detection explanation
- HITL benefits and limitations
- Challenges and trade-offs (5 comparisons)
- Testing strategy with sample queries
- Future enhancements roadmap

---

## 🔗 How These Files Connect to the Code

```
kb.pdf
  └── ingested by ingest.py
  └── searched by retrieval.py
  └── answers come from generator.py

HLD_RAG_Pdf.pdf
  └── describes the big picture of the whole system

LLD PDF.pdf
  └── describes each Python file in detail

Technical_Document.pdf
  └── explains WHY each decision was made
```

---

## 📌 Note for Submission

All 4 PDFs are required for the final submission:
- ✅ `HLD_RAG_Pdf.pdf` — 20% weight (HLD Quality)
- ✅ `LLD PDF.pdf` — 20% weight (LLD Depth)
- ✅ `Technical_Document.pdf` — 25% weight (Technical Documentation)
- ✅ `kb.pdf` — Used by the Working Project (optional but preferred)
