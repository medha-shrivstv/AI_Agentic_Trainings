# react_agent.py

import cohere
import json
import os

from refinery_tools import (
    get_sensor_reading,
    get_equipment_status,
    check_maintenance_schedule,
    get_historical_trend,
    trigger_safety_alert,
)
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key
# # Cohere Client
co = cohere.ClientV2(
    api_key=os.environ.get("COHERE_API_KEY")
)

MODEL = "command-a-03-2025"

# Map tool names to actual Python functions
AVAILABLE_TOOLS = {
    "get_sensor_reading": get_sensor_reading,
    "get_equipment_status": get_equipment_status,
    "check_maintenance_schedule": check_maintenance_schedule,
    "get_historical_trend": get_historical_trend,
    "trigger_safety_alert": trigger_safety_alert,
}

# Tool Schemas
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_sensor_reading",
            "description": "Get the current live reading of a sensor on a refinery unit.",
            "parameters": {
                "type": "object",
                "properties": {
                    "equipment_id": {
                        "type": "string",
                        "description": "e.g. CDU-1, FCC-2, HDS-3",
                    },
                    "sensor_type": {
                        "type": "string",
                        "description": "temperature_C, pressure_bar, flow_rate_m3h",
                    },
                },
                "required": ["equipment_id", "sensor_type"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_equipment_status",
            "description": "Get the current operational status of a refinery unit.",
            "parameters": {
                "type": "object",
                "properties": {
                    "equipment_id": {"type": "string"}
                },
                "required": ["equipment_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_maintenance_schedule",
            "description": "Get maintenance information for a refinery unit.",
            "parameters": {
                "type": "object",
                "properties": {
                    "equipment_id": {"type": "string"}
                },
                "required": ["equipment_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_historical_trend",
            "description": "Retrieve sensor history over the last N hours.",
            "parameters": {
                "type": "object",
                "properties": {
                    "equipment_id": {"type": "string"},
                    "sensor_type": {"type": "string"},
                    "hours": {"type": "integer"},
                },
                "required": [
                    "equipment_id",
                    "sensor_type",
                    "hours",
                ],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "trigger_safety_alert",
            "description": "Raise a control room alert when strong evidence supports escalation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "equipment_id": {"type": "string"},
                    "message": {"type": "string"},
                },
                "required": [
                    "equipment_id",
                    "message",
                ],
            },
        },
    },
]

# Agent Instructions
SYSTEM_PROMPT = """
You are an AI operations assistant for an oil refinery control room.

You help shift engineers diagnose anomalies and decide on next steps.

Follow the ReAct method:

1. Think about what information you need.
2. Call one tool.
3. Observe the result.
4. Think again.
5. Repeat until enough evidence is gathered.

When finished provide:

1. Diagnosis
2. Evidence
3. Recommendation

Be concise and safety-conscious.

Only use trigger_safety_alert if escalation is clearly justified.
"""

def run_react_agent(
    user_query: str,
    max_steps: int = 6,
    verbose: bool = True,
):
    """
    ReAct Agent Loop
    """

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": user_query,
        },
    ]

    for step in range(1, max_steps + 1):

        try:
            response = co.chat(
                model=MODEL,
                messages=messages,
                tools=tools,
            )
        except Exception as e:
            return f"Error during model interaction: {str(e)}"

        thought_text = ""

        if response.message.content:
            thought_text = response.message.content[0].text

        if verbose and thought_text:
            print(f"\n===== STEP {step}: THOUGHT =====")
            print(thought_text)

        tool_calls = response.message.tool_calls

        # Final answer
        if not tool_calls:

            if verbose:
                print(f"\n===== STEP {step}: FINAL ANSWER =====")
                print(thought_text)

            return thought_text

        messages.append(
            {
                "role": "assistant",
                "content": response.message.content,
                "tool_calls": tool_calls,
            }
        )

        for call in tool_calls:

            function_name = call.function.name
            try:
                function_args = json.loads(
                    call.function.arguments
                )
            except json.JSONDecodeError as e:
                result = {"error": f"Invalid arguments for tool {function_name}: {str(e)}"}
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": json.dumps(result),
                    }
                )
                continue

            if verbose:
                print(f"\n===== STEP {step}: ACTION =====")
                print(
                    f"{function_name}({function_args})"
                )

            function = AVAILABLE_TOOLS.get(
                function_name
            )

            if function:
                try:
                    result = function(**function_args)
                except Exception as e:
                    result = {"error": f"Error executing tool {function_name}: {str(e)}"}
            else:
                result = {
                    "error": f"Unknown tool {function_name}"
                }

            if verbose:
                print(f"\n===== STEP {step}: OBSERVATION =====")
                print(result)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(result),
                }
            )

    return "The agent reached the maximum number of reasoning steps without reaching a conclusion. Please refine your query."