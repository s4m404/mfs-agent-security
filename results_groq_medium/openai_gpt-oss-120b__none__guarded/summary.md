# openai/gpt-oss-120b | defence=none | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 12.5% (n=72) |
| Attack cases where the agent actually read the attack | 69.4% (n=72) |
| Attack success among those (lower is better) | 18.0% (n=50) |
| Utility on benign tasks | 95.1% (n=61) |
| Utility under attack | 93.1% (n=72) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=61) |
| Episodes with any blocked call | 0.0% (n=133) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 1.5% (n=133) |
| Episodes where such a payment went through | 1.5% (n=133) |
| Episodes where the agent asked the user to confirm | 1.5% (n=133) |
| Episodes stopped by a model error (timeout, reply too long) | 0.0% (n=133) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 11.1% (n=18) |
| bn | 11.1% (n=18) |
| en | 16.7% (n=18) |
| mixed | 11.1% (n=18) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 0.0% (n=24) |
| sms | 0.0% (n=36) |
| tool_description | 75.0% (n=12) |
