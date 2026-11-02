# openai/gpt-oss-120b | defence=none | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 0.0% (n=52) |
| Attack cases where the agent actually read the attack | 57.7% (n=52) |
| Attack success among those (lower is better) | 0.0% (n=30) |
| Utility on benign tasks | 93.3% (n=30) |
| Utility under attack | 96.2% (n=52) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=30) |
| Episodes with any blocked call | 0.0% (n=82) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 0.0% (n=82) |
| Episodes where such a payment went through | 0.0% (n=82) |
| Episodes where the agent asked the user to confirm | 0.0% (n=82) |
| Episodes stopped by a model error (timeout, reply too long) | 0.0% (n=82) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 0.0% (n=13) |
| bn | 0.0% (n=13) |
| en | 0.0% (n=13) |
| mixed | 0.0% (n=13) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 0.0% (n=24) |
| sms | 0.0% (n=28) |
