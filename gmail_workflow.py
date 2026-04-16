# gmail_workflow.py
# Contains the Gmail Agent and its tool loop.
# gmail_workflow() is the entry point called by the Master Agent.

import json
from llm import call_llm
from tools import get_unread_emails

SYSTEM_PROMPT = (
    "You are a Gmail assistant. You help users manage their email. "
    "Use the get_unread_emails tool to fetch emails, then summarize them yourself in a clear, readable format."
)

# Tool schemas tell Claude what tools are available and how to call them.
GMAIL_TOOLS = [
    {
        "name": "get_unread_emails",
        "description": "Fetch the user's unread emails. Returns a list of email objects.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
]

# Maps tool names to their actual Python functions.
def call_get_unread_emails(inputs):
    return get_unread_emails()

TOOL_MAP = {
    "get_unread_emails": call_get_unread_emails,
}


def gmail_workflow(task: str) -> str:
    """
    Entry point for the Gmail subworkflow.
    Runs the Gmail Agent loop until it produces a final text response.
    """
    print(f"[Gmail Agent] Starting task: {task}")
    messages = [{"role": "user", "content": task}]

    while True:
        response = call_llm(messages, tools=GMAIL_TOOLS, system=SYSTEM_PROMPT)
        stop_reason = response.get("stop_reason")
        content = response.get("content", [])

        # Claude wants to call one or more tools.
        if stop_reason == "tool_use":
            # Append Claude's response (which includes tool_use blocks) to history.
            messages.append({"role": "assistant", "content": content})

            # Execute each requested tool and collect results.
            tool_results = []
            for block in content:
                if block["type"] == "tool_use":
                    tool_name = block["name"]
                    tool_inputs = block.get("input", {})
                    print(f"[Gmail Agent] Calling tool: {tool_name}")

                    result = TOOL_MAP[tool_name](tool_inputs)

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block["id"],
                        "content": json.dumps(result),
                    })

            # Feed tool results back to Claude so it can continue reasoning.
            messages.append({"role": "user", "content": tool_results})

        # Claude produced a final text response — we're done.
        else:
            for block in content:
                if block["type"] == "text":
                    print("[Gmail Agent] Done.")
                    return block["text"]
