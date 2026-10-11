# openai/gpt-oss-120b | defence=provenance-amount | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 0.0% (n=120) |
| Attack cases where the agent actually read the attack | 69.2% (n=120) |
| Attack success among those (lower is better) | 0.0% (n=83) |
| Utility on benign tasks | 93.6% (n=78) |
| Utility under attack | 88.3% (n=120) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=78) |
| Episodes with any blocked call | 6.6% (n=198) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 2.0% (n=198) |
| Episodes where such a payment went through | 0.0% (n=198) |
| Episodes where the agent asked the user to confirm | 5.1% (n=198) |
| Episodes stopped by a model error (timeout, reply too long) | 0.5% (n=198) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 0.0% (n=30) |
| bn | 0.0% (n=30) |
| en | 0.0% (n=30) |
| mixed | 0.0% (n=30) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 0.0% (n=56) |
| sms | 0.0% (n=52) |
| tool_description | 0.0% (n=12) |
