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
git clone <repo-url>
cd ubacm_agents
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv

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

Open `.env` and paste in the `PROXY_URL` your instructor shares at the start of the workshop:

```
PROXY_URL=https://your-n8n-webhook-url-here
```

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

---

## Instructor: n8n Proxy Setup

Before the event, set up a 3-node n8n workflow so students don't need their own API keys:

1. **Webhook node** — Method: POST, "Respond Using Respond to Webhook Node"
2. **HTTP Request node** — POST to `https://api.anthropic.com/v1/messages`
   - Header: `anthropic-version: 2023-06-01`
   - Header: `x-api-key` → use an n8n Anthropic credential
   - Body: pass through `{{ $json.body }}` from the webhook
3. **Respond to Webhook node** — Response Body: `{{ $json }}`

Share the webhook's **Production URL** with students as their `PROXY_URL`.
