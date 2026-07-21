"""An appointment reminder agent with channel fallback, built with Agno and Plivo.

A reminder is useless if it goes out on a channel the number cannot receive. An
SMS to a landline never lands. This shows a developer embedding an Agno agent in
a reminder job: the agent looks up the number, sends an SMS when it is a mobile,
and places a voice call instead when it is a landline. A developer calls
send_reminder() from their scheduler, so there is no chat interface.

Run with OPENAI_API_KEY, PLIVO_AUTH_ID, PLIVO_AUTH_TOKEN, PLIVO_FROM_NUMBER set,
and PLIVO_TO_NUMBER as the number to remind.
"""

import os

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.plivo import PlivoTools

reminder_agent = Agent(
    name="Appointment Reminder Agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[
        PlivoTools(
            enable_lookup_number=True,
            enable_send_sms=True,
            enable_make_call=True,
        )
    ],
    instructions=[
        "You send appointment reminders.",
        f"Send every message and call from {os.environ.get('PLIVO_FROM_NUMBER', '')}.",
        "First look up the number to find its line type.",
        "If it is a mobile, send one short SMS reminder.",
        "If it is a landline, place a voice call instead, since an SMS will not reach a landline.",
        "When you place a call, use the answer URL https://s3.amazonaws.com/static.plivo.com/answer.xml with answer_method GET.",
        "Report which channel you used and why.",
    ],
    markdown=True,
)


def send_reminder(phone: str, appointment: str) -> str:
    return reminder_agent.run(
        f"Remind the patient at {phone} about their appointment: {appointment}."
    ).content


if __name__ == "__main__":
    print(
        send_reminder(
            os.environ["PLIVO_TO_NUMBER"],
            appointment="a dental cleaning tomorrow at 3pm",
        )
    )
    """
    Example output (mobile number)

    INFO Looked up number: +1415xxxxxxx
    INFO SMS sent. UUID: 88aa9e96-dbd8-46e1-b94b-aef6409b6ea1, to: +1415xxxxxxx

    - Reminder sent by SMS because the number is a mobile line.
    """
