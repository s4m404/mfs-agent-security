# openai/gpt-oss-120b | defence=none | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 6.6% (n=137) |
| Attack cases where the agent actually read the attack | 71.5% (n=137) |
| Attack success among those (lower is better) | 9.2% (n=98) |
| Utility on benign tasks | 93.6% (n=78) |
| Utility under attack | 92.0% (n=137) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=78) |
| Episodes with any blocked call | 0.0% (n=215) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 2.8% (n=215) |
| Episodes where such a payment went through | 0.5% (n=215) |
| Episodes where the agent asked the user to confirm | 0.5% (n=215) |
| Episodes stopped by a model error (timeout, reply too long) | 0.5% (n=215) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 5.9% (n=34) |
| bn | 5.7% (n=35) |
| en | 5.9% (n=34) |
| mixed | 8.8% (n=34) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 1.8% (n=56) |
| sms | 0.0% (n=69) |
| tool_description | 66.7% (n=12) |
