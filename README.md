# TrustTrail 🔍

**A production-ready RAG system that shows its sources, checks its own answers, and says "I don't know" when it should.**

Most RAG projects just answer. TrustTrail answers, proves where each sentence came from, blocks unsafe inputs, and refuses to guess when the documents don't have the info.

---

## Why I built this

Normal RAG systems have three big problems:

1. They **make things up** when the documents don't contain the answer.
2. They **mix old and new versions** of content without telling you.
3. They **trust everything** they read, including hidden instructions inside documents and web pages.

TrustTrail tries to fix all three, and it is built like a real service: API, logging, tests, Docker, and evaluation numbers.

---

## Features

### Ingestion
- Upload **PDF, DOCX, and TXT** files
- **OCR** for scanned PDFs and **table extraction** for tables inside PDFs
- **Web ingestion**: add a single URL, a sitemap, or a whole site section
- Clean text extraction from web pages (removes menus, ads, and footers)
- Scheduled **re-crawl with change detection** (changed content is saved as a new version)
- Duplicate detection using content hashing
- Background processing so uploads don't freeze the app

### Retrieval
- Smart chunking that keeps file name, page or URL, version, and date with every chunk
- **Hybrid search** (BM25 keyword search + vector search)
- **Cross-encoder reranking** for better results
- Metadata filters (for example "as of 2022", or only one source)

### Trust layer (what makes it different)
- **Sentence-level citations**: every sentence links to the exact chunk (file + page or URL)
- **Groundedness check**: a second LLM pass checks each claim against the sources and flags unsupported ones
- **Confidence score + "I don't know" mode**: if confidence is low, the app refuses instead of guessing
- **Version tracking**: newer content becomes v2, v3, and so on
- **Contradiction alert**: if two sources disagree, both are shown side by side

### Guardrails
- **Prompt injection detection**: blocks attempts to override system instructions
- **Off-topic filter**: refuses questions unrelated to the ingested content
- **Content scanning**: retrieved text (documents and web pages) is treated as data, and instruction-like text is flagged
- **PII masking**: phone numbers, emails, and ID numbers are hidden in answers
- **Web safety**: domain allow-list, robots.txt respect, rate limiting, size and timeout limits (protects against SSRF)
- **Safe refusal** for harmful or unsupported requests

### Production layer
- **FastAPI** backend with request validation, API key auth, and rate limiting
- **Logging and tracing** of every query (latency, token cost, retrieved chunks)
- **Caching** for embeddings and repeated queries
- **Model fallback** if one LLM API fails
- Streaming responses
- **Docker** setup and **CI** with automated tests

### Evaluation and tools
- Evaluation page with accuracy, hallucination rate, retrieval recall, and response time
- Retrieval inspector (see found chunks, their scores, and which were used)
- 👍 / 👎 feedback that saves bad answers to a "failed questions" list

---

## Architecture

```
            ┌────────────────────────────┐
            │  Sources                   │
            │  PDF / DOCX / TXT / Web    │
            └─────────────┬──────────────┘
                          ↓
        Guardrails: file checks, domain allow-list, content scan
                          ↓
        Extract text (OCR + tables + web cleaning)
                          ↓
        Chunk + metadata (source, page/URL, version, date)
                          ↓
        Embeddings → Vector DB      +      BM25 index
                          ↓
  User question → Input guardrails (injection, off-topic)
                          ↓
        Hybrid search (top 20) → Rerank (top 5)
                          ↓
        LLM answer with per-sentence citations
                          ↓
        Groundedness check → PII masking → Confidence score
                          ↓
      Final answer   OR   "Not enough info in your sources"
                          ↓
        Logs, metrics, and feedback
```

---

## Tech stack

| Part | Tool |
|------|------|
| Language | Python 3.10+ |
| API | FastAPI + Pydantic |
| UI | Streamlit |
| Vector DB | ChromaDB (or Qdrant / pgvector) |
| Keyword search | rank_bm25 |
| Embeddings + reranker | sentence-transformers |
| PDF / tables / OCR | PyMuPDF, pdfplumber, pytesseract |
| Web extraction | trafilatura, Playwright (for JS-heavy sites) |
| Guardrails | regex rules, presidio, LLM checker |
| LLM | Any LLM API (OpenAI / Gemini / Groq) |
| Observability | Langfuse or OpenTelemetry |
| Caching | Redis or in-memory |
| Deployment | Docker, GitHub Actions, Render / Railway / HF Spaces |

---

## Project structure

```
trusttrail/
├── app.py                     # Streamlit UI
├── api/
│   ├── main.py                # FastAPI app
│   ├── routes.py              # /ingest, /ask, /feedback
│   └── auth.py                # API key + rate limiting
├── ingest/
│   ├── loader.py              # PDF / DOCX / TXT + OCR + tables
│   ├── web_loader.py          # fetch + clean web pages
│   ├── crawler.py             # sitemap / multi-page crawl with limits
│   └── chunker.py             # split text + attach metadata
├── retrieval/
│   ├── embeddings.py          # embedding + cache
│   ├── hybrid.py              # BM25 + vector search
│   └── reranker.py            # cross-encoder reranking
├── generation/
│   ├── answer.py              # answer with citations
│   ├── grounding.py           # groundedness check
│   └── contradiction.py       # find conflicting chunks
├── guardrails/
│   ├── input_check.py         # prompt injection + off-topic filter
│   ├── content_scan.py        # scan documents and web text
│   ├── web_safety.py          # allow-list, robots.txt, limits
│   └── pii.py                 # mask personal info
├── eval/
│   ├── questions.json         # test questions + correct answers
│   ├── attacks.json           # prompt injection test cases
│   └── run_eval.py            # accuracy / hallucination report
├── tests/                     # unit and integration tests
├── data/                      # uploaded documents
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/trusttrail.git
cd trusttrail

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your keys
cp .env.example .env
# open .env and paste your LLM API key

# 4. Run the API
uvicorn api.main:app --reload

# 5. Run the UI (in another terminal)
streamlit run app.py
```

**Run with Docker**

```bash
docker-compose up --build
```

---

## How to use

1. Go to the **Sources** tab and upload files, or paste a URL / sitemap.
2. Go to the **Chat** tab and ask a question.
3. Click any sentence in the answer to see its source.
4. Open the **Inspector** to see which chunks were retrieved and why.
5. Check the **Evaluation** tab to see how well the system performs.

**API example**

```bash
curl -X POST http://localhost:8000/ask \
  -H "x-api-key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the refund policy?"}'
```

---

## Evaluation

I tested TrustTrail on `<N>` questions. Some of them **cannot be answered** from the sources, to check if the system refuses correctly. I also ran `<M>` prompt-injection attacks to test the guardrails.

| Setup | Accuracy | Hallucination rate | Avg. response time |
|-------|----------|--------------------|--------------------|
| Basic RAG (vector search only) | _fill in_ | _fill in_ | _fill in_ |
| + Hybrid search | _fill in_ | _fill in_ | _fill in_ |
| + Reranking | _fill in_ | _fill in_ | _fill in_ |
| + Groundedness check | _fill in_ | _fill in_ | _fill in_ |

| Guardrail test | Result |
|----------------|--------|
| Prompt injection attacks blocked | _X / M_ |
| Off-topic questions refused | _fill in_ |
| PII leaked in answers | _fill in_ |

Run it yourself:

```bash
python eval/run_eval.py
```

---

## Demo

🔗 **Live demo:** `<add-link>`

_Add a screenshot or a short GIF here._

---

## What I learned

- _Add 3-4 real points after building (for example what surprised you about chunk size, OCR quality, or web cleaning)._

---

## Known limitations

- _Be honest here. For example: OCR quality on low-quality scans, JavaScript-heavy sites are slower to crawl._

---

## Future improvements

- Multi-hop questions across several documents
- Conversational memory for follow-up questions
- Hindi + English (multilingual) support
- Images and charts inside PDFs (multimodal)
- Auto-improving retrieval from failed questions

---

## Author

**Himanshi**
GitHub: `<your-link>` · LinkedIn: `<your-link>`

---

## License

MIT