# master_agent.py
# The Master Agent decides how to handle user messages.
# It either responds directly or delegates to a subworkflow (e.g. gmail_workflow).

import json
from llm import call_llm
from gmail_workflow import gmail_workflow
from tools import get_current_time

SYSTEM_PROMPT = (
    "You are a helpful personal assistant. "
    "You have access to tools that let you delegate tasks to specialized agents. "
    "Use the gmail_workflow tool for anything related to email. "
    "Use the get_current_time tool when the user asks about the current time or date. "
    "For everything else, respond directly."
)

# The Master Agent's tools — a mix of simple tools and agent subworkflows.
# Adding new capabilities = adding a new entry here and a mapping in WORKFLOW_MAP.
MASTER_TOOLS = [
    {
        "name": "gmail_workflow",
        "description": (
            "Delegate an email-related task to the Gmail agent. "
            "Use this for reading, summarizing, or managing emails."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "task": {
                    "type": "string",
                    "description": "A plain-English description of the email task to perform.",
                }
            },
            "required": ["task"],
        },
    },
    {
        "name": "get_current_time",
        "description": "Returns the current local date and time.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
]

# Maps tool names to their implementations.
# gmail_workflow is a full sub-agent; get_current_time is a plain function.
WORKFLOW_MAP = {
    "gmail_workflow": lambda inputs: gmail_workflow(inputs["task"]),
    "get_current_time": lambda inputs: get_current_time(),
}


def master_agent(user_message: str) -> str:
    """
    Run the Master Agent loop for a single user message.
    Returns the final response string to display to the user.
    """
    print("[Master Agent] Thinking...")
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = call_llm(messages, tools=MASTER_TOOLS, system=SYSTEM_PROMPT)
        stop_reason = response.get("stop_reason")
        content = response.get("content", [])

        # Claude wants to delegate to a subworkflow.
        if stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": content})

            tool_results = []
            for block in content:
                if block["type"] == "tool_use":
                    workflow_name = block["name"]
                    workflow_inputs = block.get("input", {})
                    print(f"[Master Agent] Routing to {workflow_name}...")

                    result = WORKFLOW_MAP[workflow_name](workflow_inputs)

                    print("[Master Agent] Received result from subworkflow.")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block["id"],
                        "content": result,
                    })

            messages.append({"role": "user", "content": tool_results})

        # Claude produced a direct final response.
        else:
            for block in content:
                if block["type"] == "text":
                    return block["text"]
