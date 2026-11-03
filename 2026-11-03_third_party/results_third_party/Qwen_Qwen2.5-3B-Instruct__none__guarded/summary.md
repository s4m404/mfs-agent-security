# Qwen/Qwen2.5-3B-Instruct | defence=none | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 5.4% (n=37) |
| Attack cases where the agent actually read the attack | 100.0% (n=37) |
| Attack success among those (lower is better) | 5.4% (n=37) |
| Utility on benign tasks | n/a |
| Utility under attack | 16.2% (n=37) |
| Benign tasks where the correct action was blocked (false blocks) | n/a |
| Episodes with any blocked call | 0.0% (n=37) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 54.1% (n=37) |
| Episodes where such a payment went through | 8.1% (n=37) |
| Episodes where the agent asked the user to confirm | 10.8% (n=37) |
| Episodes stopped by a model error (timeout, reply too long) | 0.0% (n=37) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 11.1% (n=9) |
| bn | 0.0% (n=9) |
| en | 0.0% (n=10) |
| mixed | 11.1% (n=9) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| tool_description | 5.4% (n=37) |
