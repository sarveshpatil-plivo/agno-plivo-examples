"""An autonomous on-call alerting agent built with Agno and Plivo.

A monitoring system does not chat with a bot, it calls a function. This shows a
developer embedding an Agno agent in their alerting pipeline: when an incident
fires, the agent triages the severity and reaches the on-call engineer through
Plivo, sending an SMS for a warning and escalating to a phone call for a
critical incident. There is no chat interface.

Run with OPENAI_API_KEY, PLIVO_AUTH_ID, PLIVO_AUTH_TOKEN, PLIVO_FROM_NUMBER set,
and PLIVO_TO_NUMBER for the on-call engineer.
"""

import os

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.plivo import PlivoTools

on_call_agent = Agent(
    name="On-Call Alerting Agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[
        PlivoTools(
            enable_send_sms=True,
            enable_make_call=True,
        )
    ],
    instructions=[
        "You are an on-call alerting agent for a backend engineering team.",
        "You are given an incident and the on-call engineer's phone number.",
        f"Send alerts from the number {os.environ.get('PLIVO_FROM_NUMBER', '')}.",
        "For a warning severity, send one concise SMS.",
        "For a critical severity, send an SMS and also place a phone call so the engineer is reached immediately.",
        "When you place a call, use the answer URL https://s3.amazonaws.com/static.plivo.com/answer.xml with answer_method GET.",
        "Keep messages short and factual.",
    ],
    markdown=True,
)


def handle_incident(service: str, severity: str, summary: str, on_call_number: str) -> str:
    task = (
        f"Incident on {service}. Severity: {severity}. Details: {summary}. "
        f"Notify the on-call engineer at {on_call_number}."
    )
    return on_call_agent.run(task).content


if __name__ == "__main__":
    result = handle_incident(
        service="payments-api",
        severity="critical",
        summary="Error rate above 40 percent, checkout is failing",
        on_call_number=os.environ["PLIVO_TO_NUMBER"],
    )
    print(result)
    """
    Example output (critical incident)

    INFO SMS sent. UUID: 5a8c1042-70af-4b95-a179-8eb9ff80ef38, to: +1415xxxxxxx
    INFO Call placed. request_uuid: 612e6a41-f4fd-4386-9cf5-e3893ff1e32f, to: +1415xxxxxxx

    - SMS Sent: Critical Alert for payments-api, error rate above 40 percent, checkout is failing.
    - Call Placed: An outbound call has been placed so the engineer is reached immediately.
    """
