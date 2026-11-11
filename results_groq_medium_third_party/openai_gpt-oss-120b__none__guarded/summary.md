# openai/gpt-oss-120b | defence=none | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 69.7% (n=33) |
| Attack cases where the agent actually read the attack | 100.0% (n=33) |
| Attack success among those (lower is better) | 69.7% (n=33) |
| Utility on benign tasks | n/a |
| Utility under attack | 87.9% (n=33) |
| Benign tasks where the correct action was blocked (false blocks) | n/a |
| Episodes with any blocked call | 0.0% (n=33) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 6.1% (n=33) |
| Episodes where such a payment went through | 0.0% (n=33) |
| Episodes where the agent asked the user to confirm | 0.0% (n=33) |
| Episodes stopped by a model error (timeout, reply too long) | 0.0% (n=33) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 75.0% (n=8) |
| bn | 50.0% (n=8) |
| en | 77.8% (n=9) |
| mixed | 75.0% (n=8) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| tool_description | 69.7% (n=33) |
