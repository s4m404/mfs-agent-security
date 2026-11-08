# openai/gpt-oss-120b | defence=provenance-amount | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 0.0% (n=155) |
| Attack cases where the agent actually read the attack | 74.2% (n=155) |
| Attack success among those (lower is better) | 0.0% (n=115) |
| Utility on benign tasks | 93.6% (n=78) |
| Utility under attack | 89.0% (n=155) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=78) |
| Episodes with any blocked call | 5.6% (n=233) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 1.7% (n=233) |
| Episodes where such a payment went through | 0.0% (n=233) |
| Episodes where the agent asked the user to confirm | 6.4% (n=233) |
| Episodes stopped by a model error (timeout, reply too long) | 0.4% (n=233) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 0.0% (n=39) |
| bn | 0.0% (n=39) |
| en | 0.0% (n=39) |
| mixed | 0.0% (n=38) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 0.0% (n=56) |
| sms | 0.0% (n=87) |
| tool_description | 0.0% (n=12) |
