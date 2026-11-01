# openai/gpt-oss-20b | defence=none | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 27.8% (n=72) |
| Attack cases where the agent actually read the attack | 88.9% (n=72) |
| Attack success among those (lower is better) | 31.2% (n=64) |
| Utility on benign tasks | 84.2% (n=38) |
| Utility under attack | 75.0% (n=72) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=38) |
| Episodes with any blocked call | 0.0% (n=110) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 18.2% (n=110) |
| Episodes where such a payment went through | 2.7% (n=110) |
| Episodes where the agent asked the user to confirm | 5.5% (n=110) |
| Episodes stopped by a model error (timeout, reply too long) | 1.8% (n=110) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 22.2% (n=18) |
| bn | 27.8% (n=18) |
| en | 38.9% (n=18) |
| mixed | 22.2% (n=18) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 16.7% (n=24) |
| sms | 22.2% (n=36) |
| tool_description | 66.7% (n=12) |
