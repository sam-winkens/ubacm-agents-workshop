# Building with AI Agents — Workshop Template

A minimal multi-agent system showing how a Master Agent delegates tasks to
specialized sub-agents via tool calls. No external frameworks — just Python,
plain function calls, and the Anthropic Claude API.

---

## How It Works

```
You (CLI Input)
  └─▶ Master Agent                  -->  decides what to do
        ├─▶ get_current_time()      -->  plain tool (returns the current time)
        └─▶ gmail_workflow          -->  subworkflow for email related tasks
              └─▶ Gmail Agent
                    ├─▶ get_unread_emails()   mock tool
                    └─▶ summarize_emails()    mock tool
```

The Master Agent's tools come in two flavors:
- **Plain tools** like `get_current_time` — a simple Python function, no LLM involved.
- **Agent tools** like `gmail_workflow` — spins up a full sub-agent with its own LLM loop and tools.

From the Master Agent's perspective, both look identical: call a tool, get a string back.

---

## Student Setup

### 1. Clone / download the template

```bash
git clone https://github.com/sam-winkens/ubacm-agents-workshop.git
cd ubacm-agents-workshop
```

### 2. Create a virtual environment and install dependencies

> **Requires Python 3.9 or newer.** Check your version with `python --version`.

```bash
python3 -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Configure your environment

```bash
cp .env.example .env
```

Open `.env` and paste in the `PROXY_URL` your instructor shares at the start of the workshop.


### 4. Run it

```bash
python main.py
```

Type a message at the `You:` prompt. Press **Ctrl+C** to quit.

**Try:**
- `What is the current time?` — uses the plain `get_current_time` tool
- `Summarize my unread emails` — delegates to the Gmail sub-agent

---

## File Tour

| File | What it does |
|---|---|
| `main.py` | CLI loop — reads input, prints output |
| `master_agent.py` | Master Agent: routes to subworkflows or replies directly |
| `gmail_workflow.py` | Gmail Agent: fetches and summarizes emails |
| `tools.py` | Tools: `get_current_time()` and mock email data |
| `llm.py` | `call_llm()` — the only file that touches the network |