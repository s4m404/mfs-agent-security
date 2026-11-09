# openai/gpt-oss-20b | defence=none | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 31.2% (n=16) |
| Attack cases where the agent actually read the attack | 100.0% (n=16) |
| Attack success among those (lower is better) | 31.2% (n=16) |
| Utility on benign tasks | n/a |
| Utility under attack | 81.2% (n=16) |
| Benign tasks where the correct action was blocked (false blocks) | n/a |
| Episodes with any blocked call | 0.0% (n=16) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 43.8% (n=16) |
| Episodes where such a payment went through | 6.2% (n=16) |
| Episodes where the agent asked the user to confirm | 12.5% (n=16) |
| Episodes stopped by a model error (timeout, reply too long) | 0.0% (n=16) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 0.0% (n=4) |
| bn | 50.0% (n=4) |
| en | 40.0% (n=5) |
| mixed | 33.3% (n=3) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| tool_description | 31.2% (n=16) |
