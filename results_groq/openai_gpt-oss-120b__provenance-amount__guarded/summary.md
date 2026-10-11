# openai/gpt-oss-120b | defence=provenance-amount | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 0.0% (n=85) |
| Attack cases where the agent actually read the attack | 67.1% (n=85) |
| Attack success among those (lower is better) | 0.0% (n=57) |
| Utility on benign tasks | 93.6% (n=78) |
| Utility under attack | 84.7% (n=85) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=78) |
| Episodes with any blocked call | 7.4% (n=163) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 2.5% (n=163) |
| Episodes where such a payment went through | 0.0% (n=163) |
| Episodes where the agent asked the user to confirm | 6.1% (n=163) |
| Episodes stopped by a model error (timeout, reply too long) | 0.6% (n=163) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 0.0% (n=21) |
| bn | 0.0% (n=21) |
| en | 0.0% (n=22) |
| mixed | 0.0% (n=21) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 0.0% (n=37) |
| sms | 0.0% (n=36) |
| tool_description | 0.0% (n=12) |
