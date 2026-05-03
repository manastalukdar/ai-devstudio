---
name: rag-implement
description: Design and implement Retrieval-Augmented Generation systems — chunking strategy, embedding selection, vector store setup, retrieval pipeline, re-ranking, and evaluation
disable-model-invocation: false
risk: safe
---

# RAG Implementation

Design and implement a production-ready RAG pipeline from document ingestion to grounded generation.

Arguments: `$ARGUMENTS` - domain/use-case description, or `audit` to review an existing RAG pipeline

## Behavior

### 1. Detect Existing RAG Infrastructure

```bash
# Check for vector stores and embedding libraries
grep -r "chromadb\|pinecone\|weaviate\|qdrant\|pgvector\|faiss\|milvus" \
  requirements.txt pyproject.toml package.json 2>/dev/null | head -10

# Check for existing RAG pipeline files
grep -rn "embed\|retriev\|vector_store\|VectorStore\|similarity_search" . \
  --include="*.py" --include="*.ts" -l 2>/dev/null | grep -v node_modules | head -10

# Check LLM framework
grep -r "langchain\|llamaindex\|llama_index\|haystack" \
  requirements.txt pyproject.toml 2>/dev/null | head -5
```

### 2. Architecture Decision

Present options based on detected stack and use case:

```
RAG Architecture Options:
━━━━━━━━━━━━━━━━━━━━━━━━

A. Naive RAG       — embed docs, retrieve top-k, inject into prompt
   Best for: prototypes, small corpora (<10k docs), simple Q&A
   Weakness: no query rewriting, no relevance filtering

B. Advanced RAG    — query rewriting + hybrid search + re-ranking
   Best for: production, large corpora, mixed document types
   Weakness: higher latency, more moving parts

C. Modular RAG     — routing, fusion, step-back prompting, self-RAG
   Best for: multi-domain systems, complex reasoning tasks
   Weakness: significant engineering investment
```

Recommend based on `$ARGUMENTS` context.

### 3. Chunking Strategy

Choose based on document type:

```python
# Fixed-size chunking (code, logs, structured data)
chunk_size = 512        # tokens
chunk_overlap = 64      # preserve sentence context at boundaries

# Semantic chunking (articles, docs, books)
# Split on: paragraph breaks → heading boundaries → sentence boundaries
# Target: 256–1024 tokens, never split mid-sentence

# Recursive character splitting (mixed content)
from langchain.text_splitter import RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=64,
    separators=["\n\n", "\n", ". ", " ", ""]
)

# Metadata to preserve per chunk:
# {source_file, page_number, section_heading, chunk_index, total_chunks}
```

### 4. Embedding Selection

```
Use case → Recommended embedding model:
────────────────────────────────────────
General English text    → text-embedding-3-small (1536d, cheap)
Multilingual            → multilingual-e5-large or cohere-embed-multilingual
Code                    → voyage-code-2 or text-embedding-3-large
Long documents          → voyage-2 (4096 token context)
On-premise / private    → nomic-embed-text (local, MIT license)

Dimensionality tip: reduce to 256d with PCA for corpora < 100k docs
→ 6× faster retrieval, <5% quality loss
```

### 5. Retrieval Pipeline

```python
# Hybrid search: dense (semantic) + sparse (BM25)
def retrieve(query: str, top_k: int = 10) -> list[Document]:
    # 1. Query rewriting (optional but recommended)
    expanded = llm.rewrite_query(query)  # "What is X?" → "X definition, X overview, X explained"

    # 2. Dense retrieval
    dense_results = vector_store.similarity_search(expanded, k=top_k * 2)

    # 3. Sparse retrieval (BM25)
    sparse_results = bm25_index.search(query, top_k=top_k * 2)

    # 4. Reciprocal Rank Fusion
    results = rrf_merge(dense_results, sparse_results)[:top_k * 2]

    # 5. Re-ranking (cross-encoder for precision)
    reranked = cross_encoder.rerank(query, results)[:top_k]

    return reranked
```

### 6. Context Assembly

```python
# Build prompt with retrieved context
def build_prompt(query: str, docs: list[Document]) -> str:
    context = "\n\n---\n\n".join(
        f"Source: {d.metadata['source_file']} (chunk {d.metadata['chunk_index']})\n{d.page_content}"
        for d in docs
    )
    return f"""Answer the question using only the provided context. 
If the answer is not in the context, say "I don't have enough information."

<context>
{context}
</context>

Question: {query}
Answer:"""

# Caching: cache_control on static documents when using Anthropic API
```

### 7. Evaluation Framework

```python
# Key RAG metrics to track:
metrics = {
    "retrieval_precision": "fraction of retrieved docs that are relevant",
    "retrieval_recall":    "fraction of relevant docs that were retrieved",
    "answer_faithfulness": "answer is grounded in retrieved context (no hallucination)",
    "answer_relevance":    "answer addresses the actual question",
    "latency_p95":         "95th percentile end-to-end latency"
}

# Minimum eval set: 50 question-answer pairs with ground truth sources
# Tools: RAGAS (open source), TruLens, LangSmith
```

### 8. For Audits

Check existing pipeline for:
- Missing re-ranking (top cause of irrelevant answers)
- Chunk size too large (>1024 tokens loses precision)
- No hybrid search (dense-only misses keyword matches)
- No metadata filtering (retrieves wrong documents from multi-tenant data)
- Missing citation/source attribution in responses
- No evaluation harness (no way to detect regressions)

## Examples

```
/rag-implement "internal knowledge base for customer support Q&A"
/rag-implement "code documentation search across 50 repos"
/rag-implement audit
```

## Token Optimization

**Expected range**: 800–2,500 tokens (full design), 400–800 tokens (audit)

**Early exit**: Audit with no vector store detected surfaces a "no RAG infrastructure found" summary with setup recommendations, without generating full design.

**Grep-before-Read**: Detects existing stack via dependency grep before reading any source files.

**Patterns used**: Grep-before-Read, early exit, progressive disclosure (architecture choice → chunking → retrieval → eval on request)
