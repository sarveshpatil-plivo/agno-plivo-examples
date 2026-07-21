"""A payment reminder ladder built with Agno and Plivo.

How firmly you chase an unpaid invoice should depend on how overdue it is. This
shows a developer embedding an Agno agent in a billing job: the agent picks the
step from the days overdue, sending a gentle SMS early, a firmer SMS after a
week, and placing a phone call once it is badly overdue. A developer calls
remind_payment() from their billing pipeline, so there is no chat interface.

Run with OPENAI_API_KEY, PLIVO_AUTH_ID, PLIVO_AUTH_TOKEN, PLIVO_FROM_NUMBER set,
and PLIVO_TO_NUMBER as the customer's phone.
"""

import os

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.plivo import PlivoTools

billing_agent = Agent(
    name="Payment Reminder Agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[
        PlivoTools(
            enable_send_sms=True,
            enable_make_call=True,
        )
    ],
    instructions=[
        "You chase overdue invoices, matching the firmness to how overdue the invoice is.",
        f"Send every message and call from {os.environ.get('PLIVO_FROM_NUMBER', '')}.",
        "A few days overdue: send one gentle SMS reminder.",
        "A week or more overdue: send a firmer SMS.",
        "Two weeks or more overdue: place a phone call so it is not missed.",
        "When you place a call, use the answer URL https://s3.amazonaws.com/static.plivo.com/answer.xml with answer_method GET.",
        "Stay professional and never threatening.",
    ],
    markdown=True,
)


def remind_payment(phone: str, amount: str, days_overdue: int) -> str:
    return billing_agent.run(
        f"An invoice for {amount} on the account with phone {phone} is {days_overdue} days overdue. "
        "Take the right step."
    ).content


if __name__ == "__main__":
    print(remind_payment(os.environ["PLIVO_TO_NUMBER"], amount="$240", days_overdue=16))
