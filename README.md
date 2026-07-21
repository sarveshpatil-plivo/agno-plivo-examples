# agno + Plivo examples

Runnable examples that give an [Agno](https://github.com/agno-agi/agno) agent real communication
abilities through [Plivo](https://www.plivo.com) — sending SMS, placing voice calls, sending
WhatsApp messages, verifying phone numbers, and looking up carrier details.

Each example is a small, self-contained script built around a developer use case. There is no chat
interface. The agent sits behind a normal function you call from your own code, which is how these
abilities show up in a real application.

The agent uses `PlivoTools`, which ships with Agno, so a plain `pip install agno` is all you need.

## Examples

### On-call alerting (featured)

`examples/on_call_alerting.py`

An incident fires, the agent triages the severity, and it reaches the on-call engineer through
Plivo. A warning sends one SMS. A critical incident sends an SMS and also places a phone call, so
the engineer is reached immediately. Drop it into a monitoring pipeline and call `handle_incident()`
when an alert fires. The agent decides the channel from the severity, you do not hard-code it.

### Signup verification

`examples/signup_verification.py`

Confirms a new user controls their phone number during signup. The agent checks the number is a
mobile line, sends a one-time code, and validates the code the user enters. Call
`start_verification()` from your signup endpoint and `complete_verification()` from your verify
endpoint. Verify must be enabled on the Plivo account for the code to send.

### Plans coordinator

`examples/plans_coordinator.py`

A small assistant that invites friends to a get-together over each person's preferred channel —
WhatsApp, SMS, or a phone call for the friend who never checks messages. Call `invite_friends()`
from your own code. WhatsApp delivery needs a WhatsApp-enabled Plivo sender.

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

Load the environment and run any script.

```
export $(grep -v '^#' .env | xargs)
python examples/on_call_alerting.py
```

## What you see when it runs

For the on-call example with a critical incident, the agent reasons about the severity, calls
`send_sms` to notify the engineer, and then calls `make_call` to place a follow-up voice call. Both
land on the destination number. Switch the severity to `warning` and it sends only the SMS.

## License

MIT
