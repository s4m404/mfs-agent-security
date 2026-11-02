# openai/gpt-oss-120b | defence=none | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 0.0% (n=19) |
| Attack cases where the agent actually read the attack | 10.5% (n=19) |
| Attack success among those (lower is better) | 0.0% (n=2) |
| Utility on benign tasks | 93.3% (n=30) |
| Utility under attack | 89.5% (n=19) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=30) |
| Episodes with any blocked call | 0.0% (n=49) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 0.0% (n=49) |
| Episodes where such a payment went through | 0.0% (n=49) |
| Episodes where the agent asked the user to confirm | 0.0% (n=49) |
| Episodes stopped by a model error (timeout, reply too long) | 0.0% (n=49) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 0.0% (n=5) |
| bn | 0.0% (n=5) |
| en | 0.0% (n=4) |
| mixed | 0.0% (n=5) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 0.0% (n=19) |
