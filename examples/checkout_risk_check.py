"""A checkout risk-check agent built with Agno and Plivo.

A voip number or a phone whose country does not match the order is a common
signal of a risky checkout. This shows a developer embedding an Agno agent at
the checkout step: the agent looks up the buyer's phone, weighs the line type
and country against the order, and for a risky order sends an SMS step-up so the
buyer has to confirm. A developer calls assess_checkout() from their checkout
handler, so there is no chat interface.

Run with OPENAI_API_KEY, PLIVO_AUTH_ID, PLIVO_AUTH_TOKEN, PLIVO_FROM_NUMBER set,
and PLIVO_TO_NUMBER as the buyer's phone.
"""

import os

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.plivo import PlivoTools

risk_agent = Agent(
    name="Checkout Risk Agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[
        PlivoTools(
            enable_lookup_number=True,
            enable_send_sms=True,
        )
    ],
    instructions=[
        "You assess the risk of a checkout from the buyer's phone number.",
        f"Send any confirmation message from {os.environ.get('PLIVO_FROM_NUMBER', '')}.",
        "Look up the phone and read its line type and country.",
        "Treat a voip line or a country that does not match the order country as high risk.",
        "For high risk, send a short SMS asking the buyer to confirm the order, and report the order as held for confirmation.",
        "For low risk, approve the order without sending anything.",
    ],
    markdown=True,
)


def assess_checkout(phone: str, order_country: str) -> str:
    return risk_agent.run(
        f"A checkout is being placed with phone {phone} for an order shipping to {order_country}. "
        "Assess the risk and act."
    ).content


if __name__ == "__main__":
    print(assess_checkout(os.environ["PLIVO_TO_NUMBER"], order_country="United States"))
    """
    Example output (buyer number's country does not match the order)

    The buyer receives this SMS:
      "Please confirm your recent order. Reply YES to verify it was you."
    and the order is held until they confirm.
    """
