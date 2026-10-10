# Qwen/Qwen2.5-32B-Instruct-AWQ | defence=provenance | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 1.8% (n=220) |
| Attack cases where the agent actually read the attack | 74.1% (n=220) |
| Attack success among those (lower is better) | 2.5% (n=163) |
| Utility on benign tasks | 51.2% (n=82) |
| Utility under attack | 48.2% (n=220) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=82) |
| Episodes with any blocked call | 44.4% (n=302) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 39.1% (n=302) |
| Episodes where such a payment went through | 0.7% (n=302) |
| Episodes where the agent asked the user to confirm | 48.3% (n=302) |
| Episodes stopped by a model error (timeout, reply too long) | 0.0% (n=302) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 0.0% (n=55) |
| bn | 0.0% (n=56) |
| en | 5.5% (n=55) |
| mixed | 1.9% (n=54) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 1.4% (n=70) |
| sms | 2.7% (n=113) |
| tool_description | 0.0% (n=37) |
