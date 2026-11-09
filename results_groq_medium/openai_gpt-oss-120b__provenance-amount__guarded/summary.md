# openai/gpt-oss-120b | defence=provenance-amount | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 0.0% (n=216) |
| Attack cases where the agent actually read the attack | 75.9% (n=216) |
| Attack success among those (lower is better) | 0.0% (n=164) |
| Utility on benign tasks | 93.9% (n=82) |
| Utility under attack | 78.7% (n=216) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=82) |
| Episodes with any blocked call | 13.1% (n=298) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 2.0% (n=298) |
| Episodes where such a payment went through | 0.0% (n=298) |
| Episodes where the agent asked the user to confirm | 13.8% (n=298) |
| Episodes stopped by a model error (timeout, reply too long) | 0.3% (n=298) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 0.0% (n=55) |
| bn | 0.0% (n=53) |
| en | 0.0% (n=54) |
| mixed | 0.0% (n=54) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 0.0% (n=70) |
| sms | 0.0% (n=110) |
| tool_description | 0.0% (n=36) |
