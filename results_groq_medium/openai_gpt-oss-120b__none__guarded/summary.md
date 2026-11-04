# openai/gpt-oss-120b | defence=none | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 9.5% (n=105) |
| Attack cases where the agent actually read the attack | 62.9% (n=105) |
| Attack success among those (lower is better) | 15.2% (n=66) |
| Utility on benign tasks | 94.9% (n=78) |
| Utility under attack | 93.3% (n=105) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=78) |
| Episodes with any blocked call | 0.0% (n=183) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 1.1% (n=183) |
| Episodes where such a payment went through | 1.1% (n=183) |
| Episodes where the agent asked the user to confirm | 1.6% (n=183) |
| Episodes stopped by a model error (timeout, reply too long) | 0.0% (n=183) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 7.7% (n=26) |
| bn | 7.7% (n=26) |
| en | 11.1% (n=27) |
| mixed | 11.5% (n=26) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 1.8% (n=56) |
| sms | 0.0% (n=37) |
| tool_description | 75.0% (n=12) |
