# openai/gpt-oss-120b | defence=none | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 15.0% (n=220) |
| Attack cases where the agent actually read the attack | 76.8% (n=220) |
| Attack success among those (lower is better) | 19.5% (n=169) |
| Utility on benign tasks | 92.7% (n=82) |
| Utility under attack | 90.5% (n=220) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=82) |
| Episodes with any blocked call | 0.0% (n=302) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 4.3% (n=302) |
| Episodes where such a payment went through | 0.3% (n=302) |
| Episodes where the agent asked the user to confirm | 0.3% (n=302) |
| Episodes stopped by a model error (timeout, reply too long) | 0.3% (n=302) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 16.4% (n=55) |
| bn | 14.3% (n=56) |
| en | 14.5% (n=55) |
| mixed | 14.8% (n=54) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 1.4% (n=70) |
| sms | 4.4% (n=113) |
| tool_description | 73.0% (n=37) |
