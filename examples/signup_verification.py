"""Phone verification during signup, built with Agno and Plivo.

A signup flow needs to confirm a user really controls their phone number. This
shows a developer embedding an Agno agent in that flow: the agent checks the
number is a mobile line, sends a one-time code, and validates the code the user
enters. A developer calls start_verification() from their signup endpoint and
complete_verification() from their verify endpoint, so there is no chat
interface.

Run with OPENAI_API_KEY, PLIVO_AUTH_ID, PLIVO_AUTH_TOKEN, PLIVO_FROM_NUMBER set,
and PLIVO_TO_NUMBER as the number to verify. Verify must be enabled on the
Plivo account for the code to send.
"""

import os

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.plivo import PlivoTools

signup_agent = Agent(
    name="Signup Verification Agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[
        PlivoTools(
            enable_lookup_number=True,
            enable_send_verification=True,
            enable_validate_verification=True,
        )
    ],
    instructions=[
        "You verify a new user's phone number during signup.",
        "First look up the number. Only proceed if it is a mobile line, and refuse a landline or voip number.",
        "If it is mobile, send a verification code over SMS and clearly report the verification session id.",
        "When given a session id and a code, validate the code and report whether the user is verified.",
    ],
    markdown=True,
)


def start_verification(phone: str) -> str:
    return signup_agent.run(
        f"A user is signing up with the phone number {phone}. "
        "Check it is a mobile number, and if so send them a verification code."
    ).content


def complete_verification(session_uuid: str, code: str) -> str:
    return signup_agent.run(
        f"Validate the code {code} for verification session {session_uuid}."
    ).content


if __name__ == "__main__":
    phone = os.environ["PLIVO_TO_NUMBER"]
    print("== Step 1: look up the number and send a code ==")
    print(start_verification(phone))
    session_uuid = input("\nEnter the verification session id shown above: ").strip()
    code = input("Enter the code you received by SMS: ").strip()
    print("\n== Step 2: validate the code ==")
    print(complete_verification(session_uuid, code))
