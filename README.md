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
                    └─▶ get_unread_emails()   fetches your real inbox via Gmail API
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

### 4. Connect your Gmail account

This step is required to get real email data in the workshop.

> **Stuck?** Don't worry — if `credentials.json` is missing or something goes wrong with Google OAuth, the app automatically falls back to sample emails so you can still follow along :D

#### 4a. Create a Google Cloud project & enable Gmail

1. Go to <https://console.cloud.google.com/> and sign in with the Google account whose Gmail you want to read(if you aren't already signed in).
2. Click the project dropdown at the top → **New project** → give it any name → **Create**.
3. Switch over to your newly created Project.
4. In the left sidebar choose **APIs & Services → Library**.
5. Search for **Gmail API** → click it → **Enable**.

#### 4b. Create OAuth 2.0 credentials

1. Go to **APIs & Services → Credentials** → **+ Create Credentials → OAuth client ID**.
2. If prompted to configure the consent screen, click **Configure consent screen → Get started**.
3. Fill in an app name (anything) and select your email for user support email, choose **External** for audience, enter your email for contact information, then agree to terms of service, and hit **Create**.
4. Back on the OAuth Overview screen, click **Create OAuth client**, for **Application type** choose **Desktop app** → **Create**.
5. CLICK **Download JSON** on the confirmation dialog. Rename the file to `credentials.json`.
6. PLACE THE `credentials.json` FILE INTO THE ROOT OF YOUR PROJECT!

> `credentials.json` is listed in `.gitignore` — it will **not** be committed.

#### 4c. First-run auth

The first time you run `python main.py` and ask about emails, a browser tab will open asking you to sign in and grant read-only access to your Gmail. After you approve, a `token.json` file is saved locally so you won't be asked again.

> `token.json` is also in `.gitignore`.

#### 4d. If you see a "Google hasn't verified this app" warning

1. Go back to your Google Cloud project, then navigate to **Audience** tab, then click **Add users** under **Test users** section and type in YOUR email that you used to create the project, then click **Save**.
2. Now run the `Summarize my unread emails` command in your app to open the pop up tab again select your Gmail Account then click continue then continue. Now you can run email related commands as you have successfully completed Google OAuth. 

---

### 5. Run it

```bash
python main.py
```

Type a message at the `You:` prompt. Press **Ctrl+C** to quit.

**Try:**
- `What is the current time?` — uses the plain `get_current_time` tool
- `Summarize my unread emails` — delegates to the Gmail sub-agent and reads your real inbox

---

## File Tour

| File | What it does |
|---|---|
| `main.py` | CLI loop — reads input, prints output |
| `master_agent.py` | Master Agent: routes to subworkflows or replies directly |
| `gmail_workflow.py` | Gmail Agent: fetches and summarizes emails |
| `tools.py` | Tools: `get_current_time()` and `get_unread_emails()` (real Gmail API, mock fallback) |
| `llm.py` | `call_llm()` — the only file that touches the network |
