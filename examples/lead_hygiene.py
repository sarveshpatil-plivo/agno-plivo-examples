"""A lead-list hygiene gate built with Agno and Plivo.

Before an outreach pipeline spends money dialing or texting a raw lead list, it
should drop the numbers that cannot be reached. This shows a developer embedding
an Agno agent as that pre-flight filter: the agent looks up every number, keeps
only the mobile lines, and reports which leads were dropped and why. A developer
calls screen_leads() from their pipeline, so there is no chat interface.

Run with OPENAI_API_KEY, PLIVO_AUTH_ID, PLIVO_AUTH_TOKEN set, and PLIVO_TO_NUMBER
as one reachable number to include in the demo list.
"""

import os

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.plivo import PlivoTools

lead_screener = Agent(
    name="Lead Hygiene Agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[PlivoTools(enable_lookup_number=True)],
    instructions=[
        "You screen a list of phone numbers before an outreach pipeline contacts them.",
        "Look up every number and read its line type.",
        "Keep only mobile lines. Drop landline, voip, and any number that fails lookup.",
        "Return two clear sections: the reachable mobile numbers, and the dropped numbers with the reason each was dropped.",
    ],
    markdown=True,
)


def screen_leads(numbers: list[str]) -> str:
    roster = "\n".join(f"- {n}" for n in numbers)
    return lead_screener.run(f"Screen these leads:\n{roster}").content


if __name__ == "__main__":
    leads = [
        os.environ["PLIVO_TO_NUMBER"],
        "+14155550100",
        "+14155550101",
    ]
    print(screen_leads(leads))
    """
    Example output

    Reachable mobile numbers
    - +1415xxxxxxx

    Dropped
    - +14155550100 (line type could not be determined)
    - +14155550101 (line type could not be determined)
    """
