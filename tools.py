# tools.py
# Tool implementations used by the agents.

import base64
import datetime
import os
from email import message_from_bytes


# get_current_time
def get_current_time() -> str:
    """Return the current local date and time as a formatted string."""
    print("[Tool] get_current_time() called")
    now = datetime.datetime.now()
    return now.strftime("%A, %B %d, %Y at %I:%M %p")


# get_unread_emails  (real Gmail API)

# OAuth scopes — read-only is enough for this workshop.
_SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# Where the one-time OAuth token is cached after the first login.
_TOKEN_PATH = "token.json"
_CREDS_PATH = "credentials.json"


def _build_gmail_service():
    """Return an authenticated Gmail API service, running the OAuth flow if needed."""
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    creds = None

    if os.path.exists(_TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(_TOKEN_PATH, _SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(_CREDS_PATH, _SCOPES)
            creds = flow.run_local_server(port=0)
        with open(_TOKEN_PATH, "w") as token_file:
            token_file.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def _decode_body(payload: dict) -> str:
    """Recursively extract plain-text body from a Gmail message payload."""
    mime_type = payload.get("mimeType", "")

    if mime_type == "text/plain":
        data = payload.get("body", {}).get("data", "")
        if data:
            return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")

    for part in payload.get("parts", []):
        text = _decode_body(part)
        if text:
            return text

    return ""


def get_unread_emails(max_results: int = 10) -> list[dict]:
    """Fetch unread emails from Gmail. Falls back to mock data if credentials.json is missing."""
    print("[Tool] get_unread_emails() called")

    if not os.path.exists(_CREDS_PATH):
        print("[Tool] credentials.json not found — returning mock data. IF YOU ARE SEEING THIS, MAKE SURE YOU HAVE A credentials.json FILE IN THE SAME DIRECTORY AS THIS FILE.")
        return _mock_emails()

    try:
        service = _build_gmail_service()
        result = (
            service.users()
            .messages()
            .list(userId="me", labelIds=["INBOX", "UNREAD"], maxResults=max_results)
            .execute()
        )

        messages = result.get("messages", [])
        emails = []

        for msg_ref in messages:
            msg = (
                service.users()
                .messages()
                .get(userId="me", id=msg_ref["id"], format="full")
                .execute()
            )

            headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
            emails.append(
                {
                    "from": headers.get("From", "Unknown"),
                    "subject": headers.get("Subject", "(no subject)"),
                    "body": _decode_body(msg["payload"])[:500],  # cap at 500 chars
                }
            )

        return emails

    except Exception as exc:
        print(f"[Tool] Gmail API error: {exc} — returning mock data.")
        return _mock_emails()

# returns mock data if credentials.json is missing so we can still follow along
def _mock_emails() -> list[dict]:
    return [
        {
            "from": "alice@example.com",
            "subject": "Project deadline moved",
            "body": "Hey, just wanted to let you know the project deadline has been pushed to next Friday.",
        },
        {
            "from": "bob@example.com",
            "subject": "Lunch tomorrow?",
            "body": "Are you free for lunch tomorrow around noon? Let me know!",
        },
        {
            "from": "newsletter@techdigest.com",
            "subject": "This week in AI",
            "body": "Top stories: GPT-5 rumors, new open-source models, and a deep dive into agent frameworks.",
        },
    ]

