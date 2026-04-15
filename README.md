# Building with AI Agents — Workshop Template

A minimal multi-agent system showing how a Master Agent delegates tasks to
specialized sub-agents via tool calls. No external frameworks — just Python,
plain function calls, and the Anthropic Claude API.

---

## How It Works

```
You (CLI)
  └─▶ Master Agent          decides what to do
        └─▶ gmail_workflow  subworkflow for email tasks
              └─▶ Gmail Agent
                    ├─▶ get_unread_emails()   mock tool
                    └─▶ summarize_emails()    mock tool
```

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

**Try:** `Summarize my unread emails`

---

## File Tour

| File | What it does |
|---|---|
| `main.py` | CLI loop — reads input, prints output |
| `master_agent.py` | Master Agent: routes to subworkflows or replies directly |
| `gmail_workflow.py` | Gmail Agent: fetches and summarizes emails |
| `tools.py` | Mock tools: returns hardcoded email data |
| `llm.py` | `call_llm()` — the only file that touches the network |

---

## Workshop Challenge

Add a **Calendar workflow** as a second tool for the Master Agent:

1. Add mock tools to `tools.py` (e.g. `get_upcoming_events()`)
2. Create `calendar_workflow.py` following the same pattern as `gmail_workflow.py`
3. Register it in `master_agent.py` under `MASTER_TOOLS` and `WORKFLOW_MAP`

Test with: `What's on my calendar this week?`