# openai/gpt-oss-120b | defence=provenance-amount | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 0.0% (n=128) |
| Attack cases where the agent actually read the attack | 68.8% (n=128) |
| Attack success among those (lower is better) | 0.0% (n=88) |
| Utility on benign tasks | 93.6% (n=78) |
| Utility under attack | 86.7% (n=128) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=78) |
| Episodes with any blocked call | 5.8% (n=206) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 1.5% (n=206) |
| Episodes where such a payment went through | 0.0% (n=206) |
| Episodes where the agent asked the user to confirm | 6.8% (n=206) |
| Episodes stopped by a model error (timeout, reply too long) | 0.0% (n=206) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 0.0% (n=32) |
| bn | 0.0% (n=32) |
| en | 0.0% (n=32) |
| mixed | 0.0% (n=32) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 0.0% (n=56) |
| sms | 0.0% (n=60) |
| tool_description | 0.0% (n=12) |
