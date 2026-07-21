"""A plans coordinator agent built with Agno and Plivo.

You build a small personal assistant with Agno whose job is to coordinate a
get-together. It reaches people through Plivo: WhatsApp for friends who use it,
SMS for those who do not, and a phone call for the friend who never checks
messages. A developer calls invite_friends() from their own code, so there is
no chat interface.

Run with OPENAI_API_KEY, PLIVO_AUTH_ID, PLIVO_AUTH_TOKEN, PLIVO_FROM_NUMBER set,
and PLIVO_TO_NUMBER as the demo recipient. WhatsApp only delivers from a
WhatsApp-enabled Plivo sender. Without one, switch a friend's channel to "sms"
for a fully live run; the agent will still call send_whatsapp otherwise and
report Plivo's sender error.
"""

import os

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.plivo import PlivoTools

coordinator = Agent(
    name="Plans Coordinator",
    model=OpenAIChat(id="gpt-4o"),
    tools=[
        PlivoTools(
            answer_url="https://s3.amazonaws.com/static.plivo.com/answer.xml",
            enable_send_sms=True,
            enable_send_whatsapp=True,
            enable_make_call=True,
        )
    ],
    instructions=[
        "You help the user invite friends to a get-together.",
        f"Send every message and call from {os.environ.get('PLIVO_FROM_NUMBER', '')}.",
        "Use each friend's preferred channel: send_whatsapp for whatsapp, send_sms for sms.",
        "If a friend is marked unreliable, also place a short call after messaging so they do not miss it.",
        "Write one short, warm, personal invite that names the friend and includes the plan and time.",
    ],
    markdown=True,
)


def invite_friends(plan: str, friends: list[dict]) -> str:
    roster = "\n".join(
        f"- {f['name']} ({f['number']}), channel: {f['channel']}"
        + (", unreliable" if f.get("unreliable") else "")
        for f in friends
    )
    return coordinator.run(f"Invite these friends to {plan}:\n{roster}").content


if __name__ == "__main__":
    recipient = os.environ["PLIVO_TO_NUMBER"]
    friends = [
        {"name": "Aditi", "number": recipient, "channel": "whatsapp"},
        {"name": "Meera", "number": recipient, "channel": "sms"},
        {"name": "Rohan", "number": recipient, "channel": "whatsapp", "unreliable": True},
    ]
    print(invite_friends("dinner this Saturday at 7pm at my place", friends))
