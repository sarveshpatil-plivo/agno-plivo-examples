# Agno + Plivo examples

[![License MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)

Runnable examples that give an [Agno](https://github.com/agno-agi/agno) agent real communication
abilities through [Plivo](https://www.plivo.com) — sending SMS, placing voice calls, and looking up
the carrier and line type of a number.

Each example is a small, self-contained script built around a developer use case. There is no chat
interface. The agent sits behind a normal function you call from your own code, which is how these
abilities show up in a real application.

`PlivoTools` ships with Agno. Install Agno, the OpenAI client, and the Plivo SDK with
`pip install -r requirements.txt`. OpenAI is used only as the agent's LLM, to decide which tool to
call. These examples trigger communication actions and do not include text-to-speech or
speech-to-text, so they are not a voice-bot pipeline.

## Examples

### On-call alerting (featured)

`examples/on_call_alerting.py`

An incident fires, the agent triages the severity, and it reaches the on-call engineer through
Plivo. A warning sends one SMS. A critical incident sends an SMS and also places a phone call, so
the engineer is reached immediately. Drop it into a monitoring pipeline and call `handle_incident()`
when an alert fires. The agent decides the channel from the severity, you do not hard-code it.

### Lead-list hygiene gate

`examples/lead_hygiene.py`

A pre-flight filter for an outreach pipeline. The agent looks up every number in a raw lead list,
keeps only the mobile lines, and reports which leads were dropped and why. Call `screen_leads()`
before you spend anything contacting a list.

### Checkout risk check

`examples/checkout_risk_check.py`

Runs at the checkout step. The agent looks up the buyer's phone, treats a voip line or a country
that does not match the order as high risk, and for a risky order sends an SMS step-up so the buyer
has to confirm. Call `assess_checkout()` from your checkout handler.

### Contact enrichment

`examples/contact_enrichment.py`

Turns a messy phone string into a clean record — normalized E.164 format, country, carrier, and line
type — ready to write back to a CRM. Call `enrich_contact()` from your own code.

### Appointment reminder with fallback

`examples/appointment_reminder.py`

Sends a reminder on a channel the number can actually receive. The agent looks up the number, sends
an SMS to a mobile, and places a voice call instead to a landline, since an SMS will not reach one.
Call `send_reminder()` from your scheduler.

### Payment reminder ladder

`examples/payment_reminder.py`

Matches the firmness of an invoice reminder to how overdue it is — a gentle SMS early, a firmer SMS
after a week, and a phone call once it is badly overdue. Call `remind_payment()` from your billing
pipeline.

## Prerequisites

- Python 3.11 or newer
- An OpenAI API key
- A Plivo account with an SMS-enabled number (Auth ID, Auth Token, and the number)

## Setup

1. Create and activate a virtual environment.

   ```
   python -m venv .venv && source .venv/bin/activate
   ```

2. Install the dependencies.

   ```
   pip install -r requirements.txt
   ```

3. Copy the environment template and fill in your keys.

   ```
   cp .env.example .env
   ```

You need an OpenAI API key and a Plivo account with an SMS-enabled number. Set `PLIVO_FROM_NUMBER`
to a number on your Plivo account and `PLIVO_TO_NUMBER` to the destination you want to reach.

## Running an example

Load the environment and run any of the scripts in `examples/`.

```
export $(grep -v '^#' .env | xargs)
python examples/on_call_alerting.py
```

Every example ends with an "Example output" block showing what a run looks like.

## What you see when it runs

The `__main__` block in `on_call_alerting.py` fires a **critical** incident on `payments-api`. The
agent judges that a critical severity needs both channels, so it makes two tool calls in order —
`send_sms`, then `make_call` — and both reach the on-call number.

The run prints two things. First, `PlivoTools` logs each API call as it happens, showing the id
Plivo returns (a `message_uuid` for the SMS, a `request_uuid` for the call):

```
INFO SMS sent. UUID: 5a8c1042-70af-4b95-a179-8eb9ff80ef38, to: +1415xxxxxxx
INFO Call placed. request_uuid: 612e6a41-f4fd-4386-9cf5-e3893ff1e32f, to: +1415xxxxxxx
```

Then the agent returns a short summary of what it did, which the script prints:

```
- SMS Sent: Critical Alert for payments-api, error rate above 40%, checkout is failing. Immediate attention needed.
- Call Placed: An outbound call has been initiated to ensure the engineer is informed immediately.
```

Set the severity to `warning` instead and the agent sends only the SMS, no call. The channel is the
agent's decision, not something which needs to be hardcoded.

## License

MIT
