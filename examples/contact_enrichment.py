"""A contact enrichment tool built with Agno and Plivo.

A CRM often stores phone numbers as messy free text. This shows a developer
using an Agno agent to turn a raw phone string into a clean, enriched record:
normalized E.164 format, country, carrier, and line type, ready to write back to
the contact. A developer calls enrich_contact() from their own code, so there is
no chat interface.

Run with OPENAI_API_KEY, PLIVO_AUTH_ID, PLIVO_AUTH_TOKEN set, and PLIVO_TO_NUMBER
as the number to enrich.
"""

import os

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.plivo import PlivoTools

enrichment_agent = Agent(
    name="Contact Enrichment Agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[PlivoTools(enable_lookup_number=True)],
    instructions=[
        "You enrich a contact from a raw phone string.",
        "Look up the number and return a clean record with the normalized E.164 number, country, carrier, and line type.",
        "If the number cannot be looked up, say so plainly instead of guessing.",
    ],
    markdown=True,
)


def enrich_contact(raw_phone: str) -> str:
    return enrichment_agent.run(f"Enrich the contact with phone number: {raw_phone}").content


if __name__ == "__main__":
    print(enrich_contact(os.environ["PLIVO_TO_NUMBER"]))
    """
    Example output

    - Number (E.164): +1415xxxxxxx
    - Country: United States
    - Carrier: T-Mobile USA
    - Line type: mobile
    """
