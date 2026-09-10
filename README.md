# 🏦 Multi-Agent AI Banking Assistant (CrewAI + MCP + Streamlit)

A production-grade proof-of-concept conversational banking assistant powered by **CrewAI**, **Model Context Protocol (MCP)** tool integration, and a **Streamlit** chat frontend.

The application relies on a **Coordinator Agent** (Banking Operations Manager) that delegates financial queries to specialized sub-agents. Each sub-agent communicates with dedicated database endpoints via simulated MCP server tools.

---

## 🌟 Key Features & Rate-Limit Safeguards

1. **Multi-Agent Orchestration**: Built with CrewAI, delegating tasks between 4 specialized agents.
2. **Model Context Protocol (MCP) Mock Tools**: Simulates MCP server endpoints (Accounts, Transactions, Service Requests) querying a SQLite database.
3. **Strict 1000 RPM Limit Safeguards (`qwen/qwen3.6-27b`)**:
   - **`max_rpm=900`**: Enforced across Crew and Agent configurations for API rate compliance.
   - **Exponential Backoff Retries**: Uses `tenacity` retry decorators (`wait_exponential`, `stop_after_attempt=5`) to catch and gracefully retry `HTTP 429 Too Many Requests` errors.
   - **Throttling**: Integrated micro-delays between agent actions to avoid request spikes.
4. **Interactive Streamlit UI**: Chat layout with `st.session_state` history, account balance sidebar widgets, and quick-action prompt buttons.
5. **No Auth Friction**: Uses pre-seeded mock user ID `USER101` and accounts (`ACC1001`, `ACC1002`) for instant testing without login screens.

---

## 🏗️ Agent Architecture & Workflow

```
                        ┌────────────────────────┐
                        │      Streamlit UI      │
                        │    (User Query Input)  │
                        └───────────┬────────────┘
                                    │
                                    ▼
                        ┌────────────────────────┐
                        │   Coordinator Agent    │
                        │ (Operations Manager)   │
                        └───────────┬────────────┘
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         │                          │                          │
         ▼                          ▼                          ▼
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│ Accounts Agent  │       │Transaction Agent│       │  Service Agent  │
│(Account Details)│       │ (Ledger & Audit)│       │(Customer Support│
└────────┬────────┘       └────────┬────────┘       └────────┬────────┘
         │                         │                         │
         ▼                         ▼                         ▼
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│  Accounts MCP   │       │ Transactions MCP│       │   Service MCP   │
│   Server Tools  │       │   Server Tools  │       │   Server Tools  │
└────────┬────────┘       └────────┬────────┘       └────────┬────────┘
         │                         │                         │
         └─────────────────────────┼─────────────────────────┘
                                   │
                                   ▼
                       ┌────────────────────────┐
                       │  SQLite Database       │
                       │     (bank_data.db)     │
                       └────────────────────────┘
```

### Agent Roles:
- **Coordinator Agent** (*Banking Operations Manager*): Analyzes user input, decides routing strategy, delegates to specialists, and synthesizes final answers.
- **Accounts Agent** (*Account Details Specialist*): Queries balances, profile information, and account statuses via Accounts MCP endpoints.
- **Transaction Agent** (*Transaction & Statement Specialist*): Retrieves ledger history and performs category-wise spending analysis via Transactions MCP endpoints.
- **Service Agent** (*Customer Service Specialist*): Submits new service requests (cheque books, address updates, KYC) and tracks request statuses via Service MCP endpoints.

---

## 📁 Project Structure (MVC Architecture)

```
Crew_AI_bankingagent/
├── models/               # Model Layer: Data access & SQLite database schema
│   ├── database.py       # SQLite database initialization & seeding (bank_data.db)
│   └── banking_model.py  # Data access functions for Accounts, Transactions, & Service Tickets
├── views/                # View Layer: Streamlit UI components & aesthetic styling
│   ├── styles.py         # Custom CSS styling tokens
│   ├── sidebar_view.py   # Profile info, linked accounts cards, & LLM configuration
│   └── chat_view.py      # Streamlit chat interface, quick prompt buttons, & message rendering
├── controllers/          # Controller Layer: Business logic & LLM agent orchestration
│   ├── llm_controller.py # Groq LLM configuration, ChatGroq, & litellm patch safeguards
│   ├── agent_controller.py # CrewAI 4-Agent setup, MCP tool bindings, & tenacity retries
│   └── banking_controller.py # Primary orchestrator for processing user queries
├── mcp_tools.py          # Simulated MCP server tools connecting CrewAI agents to models
├── app.py                # Main Streamlit bootstrapper integrating Views & Controllers
├── agents_and_tasks.py   # Backward-compatibility wrapper for controllers layer
├── database_setup.py     # Backward-compatibility wrapper for models layer
├── bank_data.db          # Auto-generated SQLite database file
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation & setup instructions
```

---

## 🚀 Setup & Installation Guide

### Prerequisites
- Python **3.10** or **3.12** recommended.
- Git (optional).

### Step 1: Create & Activate Virtual Environment (`.venv`)

**PowerShell:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt (CMD):**
```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

### Step 2: Install Dependencies inside Virtual Environment
```bash
pip install -r requirements.txt
```

### Step 3: Configure Groq API Key (Free Tier)
Obtain a free API key from [Groq Console](https://console.groq.com/keys) and set your environment variable:
```bash
# Windows Command Prompt (CMD):
set GROQ_API_KEY=gsk_your_groq_api_key_here

# PowerShell:
$env:GROQ_API_KEY="gsk_your_groq_api_key_here"

# (Optional) Switch Groq Model (Default is qwen-qwq-32b):
$env:GROQ_MODEL="qwen-qwq-32b"
# or
$env:GROQ_MODEL="llama-3.3-70b-versatile"
```
*Note: You can also enter your `GROQ_API_KEY` and select your `Groq Model Name` directly inside the Streamlit sidebar input box upon running.*

### Step 4: Initialize Mock Database (Optional - Happens Automatically on Launch)
```bash
py -3.12 database_setup.py
```

### Step 5: Launch the Streamlit App
```bash
py -3.12 -m streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501`.

---

## 💬 Sample Prompts to Try

- **Account Balances**: *"What are my current account balances for savings and checking?"*
- **Recent Transactions**: *"Show my recent transactions for account ACC1001."*
- **Spending Analysis**: *"Analyze my spending habits by category for account ACC1001."*
- **Service Requests**: *"I want to request a new cheque book for account ACC1001."*
- **Service Status**: *"What is the status of my existing service requests?"*

---

## 🛡️ Security & Scope Note

This codebase is a **Proof of Concept (POC)** designed for instant execution:
- Authentication and authorization are explicitly disabled.
- Queries default to hardcoded user ID `USER101` and primary account `ACC1001`.
