TrustTrail 🔍

A RAG app that shows its sources, checks its own answers, and says "I don't know" when it should.

Most RAG projects just answer. TrustTrail answers, proves where each sentence came from, and refuses to guess when your documents don't have the info.

Why I built this

Normal RAG systems have two big problems:

They make things up when the documents don't contain the answer.
They mix old and new versions of documents without telling you.

TrustTrail tries to fix both. Every answer is checked against the source chunks, and the app knows which version of a document is the latest.

Features

Core

Upload PDF, DOCX, and TXT files
Smart chunking that keeps file name and page number with every chunk
Hybrid search (BM25 keyword search + vector search)
Reranking with a cross-encoder for better results

What makes it different

Sentence-level citations: every sentence in the answer links to the exact chunk (file + page)
Groundedness check: a second LLM pass checks each claim against the sources and flags unsupported ones
Confidence score + "I don't know" mode: if confidence is low, the app refuses instead of guessing
Version tracking: newer uploads become v2, v3, etc. You can ask "what was the rule as of 2022?"
Contradiction alert: if two sources disagree, both are shown side by side

Extras

Evaluation page with accuracy, hallucination rate, and response time
Retrieval inspector (see which chunks were found, their scores, and which were used)
👍 / 👎 feedback that saves bad answers to a "failed questions" list
How it works
Upload files
     ↓
Extract text → Chunk (keep file + page + version + date)
     ↓
Store in vector DB + BM25 index
     ↓
User asks a question
     ↓
Hybrid search (top 20) → Rerank (top 5)
     ↓
LLM writes answer with per-sentence citations
     ↓
Groundedness check on every claim
     ↓
Confidence score → Answer  OR  "Not enough info in your documents"
Tech stack
Part	Tool
Language	Python 3.10+
UI	Streamlit
Vector DB	ChromaDB
Keyword search	rank_bm25
Embeddings + reranker	sentence-transformers
PDF parsing	PyMuPDF
LLM	Any LLM API (OpenAI / Gemini / Groq)
Project structure
trusttrail/
├── app.py                 # Streamlit app
├── ingest/
│   ├── loader.py          # read PDF / DOCX / TXT
│   └── chunker.py         # split text + attach metadata
├── retrieval/
│   ├── hybrid.py          # BM25 + vector search
│   └── reranker.py        # cross-encoder reranking
├── generation/
│   ├── answer.py          # answer with citations
│   ├── grounding.py       # groundedness check
│   └── contradiction.py   # find conflicting chunks
├── eval/
│   ├── questions.json     # test questions + correct answers
│   └── run_eval.py        # accuracy / hallucination report
├── data/                  # uploaded documents
├── requirements.txt
└── README.md
Setup
bash
# 1. Clone the repo
git clone https://github.com/<your-username>/trusttrail.git
cd trusttrail

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your API key
cp .env.example .env
# open .env and paste your key

# 4. Run the app
streamlit run app.py
How to use
Go to the Documents tab and upload your files.
Go to the Chat tab and ask a question.
Click any sentence in the answer to see its source.
Check the Evaluation tab to see how well the system performs.
Evaluation

I tested TrustTrail on a set of <N> questions. Some of them cannot be answered from the documents, to check if the system refuses correctly.

Setup	Accuracy	Hallucination rate	Avg. response time
Basic RAG (vector search only)	fill in	fill in	fill in
+ Hybrid search	fill in	fill in	fill in
+ Reranking	fill in	fill in	fill in
+ Groundedness check	fill in	fill in	fill in

(Fill this table with your real results after running eval/run_eval.py.)

Demo

Add a screenshot or a short GIF here.

What I learned
Add 3-4 real points after building, for example what surprised you about chunk size, reranking, or the groundedness check.
Future improvements
Support for tables and images inside PDFs
Hindi + English (multilingual) questions
Learning from failed questions to improve retrieval automatically
Author

Himanshi GitHub: <your-link> · LinkedIn: <your-link>

License

MIT
