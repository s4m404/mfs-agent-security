# openai/gpt-oss-20b | defence=none | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 26.8% (n=220) |
| Attack cases where the agent actually read the attack | 89.5% (n=220) |
| Attack success among those (lower is better) | 29.9% (n=197) |
| Utility on benign tasks | 87.8% (n=82) |
| Utility under attack | 78.2% (n=220) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=82) |
| Episodes with any blocked call | 0.0% (n=302) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 17.5% (n=302) |
| Episodes where such a payment went through | 3.0% (n=302) |
| Episodes where the agent asked the user to confirm | 4.0% (n=302) |
| Episodes stopped by a model error (timeout, reply too long) | 1.3% (n=302) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 21.8% (n=55) |
| bn | 26.8% (n=56) |
| en | 36.4% (n=55) |
| mixed | 22.2% (n=54) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 22.9% (n=70) |
| sms | 16.8% (n=113) |
| tool_description | 64.9% (n=37) |
