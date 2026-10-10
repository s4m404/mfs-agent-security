# Qwen/Qwen2.5-32B-Instruct-AWQ | defence=provenance-consistent | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 0.0% (n=56) |
| Attack cases where the agent actually read the attack | 78.6% (n=56) |
| Attack success among those (lower is better) | 0.0% (n=44) |
| Utility on benign tasks | n/a |
| Utility under attack | 1.8% (n=56) |
| Benign tasks where the correct action was blocked (false blocks) | n/a |
| Episodes with any blocked call | 82.1% (n=56) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 30.4% (n=56) |
| Episodes where such a payment went through | 0.0% (n=56) |
| Episodes where the agent asked the user to confirm | 78.6% (n=56) |
| Episodes stopped by a model error (timeout, reply too long) | 0.0% (n=56) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 0.0% (n=14) |
| bn | 0.0% (n=14) |
| en | 0.0% (n=14) |
| mixed | 0.0% (n=14) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 0.0% (n=24) |
| sms | 0.0% (n=32) |
