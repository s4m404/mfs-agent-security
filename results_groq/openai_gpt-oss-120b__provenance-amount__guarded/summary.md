# openai/gpt-oss-120b | defence=provenance-amount | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 0.0% (n=207) |
| Attack cases where the agent actually read the attack | 78.3% (n=207) |
| Attack success among those (lower is better) | 0.0% (n=162) |
| Utility on benign tasks | 93.6% (n=78) |
| Utility under attack | 81.2% (n=207) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=78) |
| Episodes with any blocked call | 13.0% (n=285) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 3.2% (n=285) |
| Episodes where such a payment went through | 0.0% (n=285) |
| Episodes where the agent asked the user to confirm | 10.9% (n=285) |
| Episodes stopped by a model error (timeout, reply too long) | 0.4% (n=285) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 0.0% (n=51) |
| bn | 0.0% (n=52) |
| en | 0.0% (n=52) |
| mixed | 0.0% (n=52) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 0.0% (n=68) |
| sms | 0.0% (n=108) |
| tool_description | 0.0% (n=31) |
