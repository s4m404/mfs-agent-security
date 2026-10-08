# openai/gpt-oss-120b | defence=none | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 8.4% (n=107) |
| Attack cases where the agent actually read the attack | 63.6% (n=107) |
| Attack success among those (lower is better) | 13.2% (n=68) |
| Utility on benign tasks | 93.6% (n=78) |
| Utility under attack | 91.6% (n=107) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=78) |
| Episodes with any blocked call | 0.0% (n=185) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 2.7% (n=185) |
| Episodes where such a payment went through | 0.0% (n=185) |
| Episodes where the agent asked the user to confirm | 0.0% (n=185) |
| Episodes stopped by a model error (timeout, reply too long) | 0.5% (n=185) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 7.4% (n=27) |
| bn | 7.4% (n=27) |
| en | 7.4% (n=27) |
| mixed | 11.5% (n=26) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 1.8% (n=56) |
| sms | 0.0% (n=39) |
| tool_description | 66.7% (n=12) |
