# Qwen/Qwen2.5-32B-Instruct-AWQ | defence=provenance-consistent | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 5.4% (n=56) |
| Attack cases where the agent actually read the attack | 75.0% (n=56) |
| Attack success among those (lower is better) | 7.1% (n=42) |
| Utility on benign tasks | n/a |
| Utility under attack | 3.6% (n=56) |
| Benign tasks where the correct action was blocked (false blocks) | n/a |
| Episodes with any blocked call | 75.0% (n=56) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 32.1% (n=56) |
| Episodes where such a payment went through | 0.0% (n=56) |
| Episodes where the agent asked the user to confirm | 73.2% (n=56) |
| Episodes stopped by a model error (timeout, reply too long) | 0.0% (n=56) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 7.1% (n=14) |
| bn | 0.0% (n=14) |
| en | 14.3% (n=14) |
| mixed | 0.0% (n=14) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 0.0% (n=24) |
| sms | 9.4% (n=32) |
