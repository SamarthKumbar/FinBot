# 📊 BalanceAI – Chat with Company Balance Sheets using AI

**BalanceAI** is an intelligent assistant that enables analysts and top management to upload and interact with company balance sheets using natural language. It extracts structured financial data from PDFs and allows you to ask questions powered by a Retrieval-Augmented Generation (RAG) system using LLaMA or GPT via Groq API.

---

## 🚀 Features

- 📝 Register/Login with role-based access (Analyst / Top Management)
- 📤 Upload PDF balance sheets
- 📦 Extracts data using pdfplumber and sentence-transformers
- 💬 Chat with balance sheets using RAG and Groq/OpenAI LLMs
- 🔐 Role-specific access: CEOs see their company; group heads see all
- ✅ Simple, secure, and production-ready

---

## 🧱 Tech Stack

| Layer             | Tech                            |
|------------------|---------------------------------|
| Backend API      | FastAPI                         |
| Auth & Security  | JWT, OAuth2                     |
| Database         | MongoDB (with Motor)            |
| PDF Extraction   | pdfplumber                      |
| Embedding Model  | sentence-transformers (MiniLM)  |
| Vector Store     | FAISS                           |
| LLM              | Groq API with LLaMA-3-70B       |
| Frontend         | Streamlit                       |



## 🗂️ Project Structure

balanceai/
│
├── backend/
│ ├── main.py # FastAPI entry point
│ ├── db.py # MongoDB connection
│ ├── auth.py # JWT auth logic
│ ├── models.py # Pydantic schemas
│ ├── rag.py # PDF parsing + RAG logic
│ └── routers/
│ ├── auth_routes.py # /auth/signup, /auth/login
│ ├── balance.py # /balance/upload-file (CSV)
│ └── rag_routes.py # /upload-pdf and /ask
│
├── frontend/
│ ├── app.py # Streamlit frontend
│ └── utils.py # API interaction helpers
│
├── .env # Secrets and keys
├── requirements.txt # Python dependencies
└── README.md # You are here

yaml
Copy
Edit

---

## ✅ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/balanceai.git
cd balanceai
2. Backend Setup
⬢ Create a virtual environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
🛠 Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
🔐 Configure .env in backend directory
Create a .env file in your backend/ folder:

ini
Copy
Edit
MONGO_URI=mongodb://localhost:27017
SECRET_KEY=your_jwt_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
OPENAI_API_KEY=your_groq_key_here
3. Run the FastAPI Backend
bash
Copy
Edit
uvicorn backend.main:app --reload
Visit API docs at: http://localhost:8000/docs

4. Streamlit Frontend Setup
Open a new terminal and run:

bash
Copy
Edit
cd frontend
streamlit run app.py
🧪 Example Flow
Register as either an analyst or top-management

Login to obtain your JWT token

Upload a PDF balance sheet from the sidebar

Ask questions like:

"What is the profit in Q1 2025?"

"Has revenue grown over time?"

"Compare assets and liabilities."

🧠 Role-Based Access
Role	Access Level
Analyst	Can upload PDFs and ask questions
Top Management	Can only view their assigned company
Group Head	Can view all companies (like Ambani family)

📌 Features to Add Next
📊 Financial trend graphs

🧾 Quarterly comparisons & summaries

🔍 Company/vertical filters

📁 Excel support in addition to PDF

💡 AI-generated action recommendations

🤖 How RAG Works Here
PDF Parsing – Extract raw text from uploaded PDF using pdfplumber.

Chunking – Split long text into manageable chunks (e.g., 500 words).

Embedding – Embed chunks using all-MiniLM-L6-v2.

Indexing – Store them in a FAISS vector index.

Querying – At query time, retrieve top-k similar chunks.

LLM Prompt – Send retrieved context + user question to LLaMA/GPT via Groq API.




