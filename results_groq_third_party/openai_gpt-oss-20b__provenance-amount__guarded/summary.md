# openai/gpt-oss-20b | defence=provenance-amount | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 0.0% (n=37) |
| Attack cases where the agent actually read the attack | 100.0% (n=37) |
| Attack success among those (lower is better) | 0.0% (n=37) |
| Utility on benign tasks | n/a |
| Utility under attack | 59.5% (n=37) |
| Benign tasks where the correct action was blocked (false blocks) | n/a |
| Episodes with any blocked call | 48.6% (n=37) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 24.3% (n=37) |
| Episodes where such a payment went through | 0.0% (n=37) |
| Episodes where the agent asked the user to confirm | 18.9% (n=37) |
| Episodes stopped by a model error (timeout, reply too long) | 0.0% (n=37) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 0.0% (n=9) |
| bn | 0.0% (n=9) |
| en | 0.0% (n=10) |
| mixed | 0.0% (n=9) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| tool_description | 0.0% (n=37) |
