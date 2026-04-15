# tools.py
# Mock tool implementations for the Gmail Agent.
# In a real system these would call actual APIs — here they return hardcoded data
# so the workshop can run without any external service credentials.


def get_unread_emails() -> list[dict]:
    """Return a mock list of unread emails."""
    print("[Tool] get_unread_emails() called")
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


def summarize_emails(emails: list[dict]) -> str:
    """Return a plain-text summary of a list of emails."""
    print("[Tool] summarize_emails() called")
    lines = []
    for i, email in enumerate(emails, start=1):
        lines.append(f"{i}. From {email['from']} — \"{email['subject']}\": {email['body']}")
    return "\n".join(lines)
