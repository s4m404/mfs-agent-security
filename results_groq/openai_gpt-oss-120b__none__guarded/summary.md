# openai/gpt-oss-120b | defence=none | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 9.3% (n=193) |
| Attack cases where the agent actually read the attack | 74.6% (n=193) |
| Attack success among those (lower is better) | 12.5% (n=144) |
| Utility on benign tasks | 93.6% (n=78) |
| Utility under attack | 90.2% (n=193) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=78) |
| Episodes with any blocked call | 0.0% (n=271) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 3.0% (n=271) |
| Episodes where such a payment went through | 0.4% (n=271) |
| Episodes where the agent asked the user to confirm | 0.4% (n=271) |
| Episodes stopped by a model error (timeout, reply too long) | 0.4% (n=271) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 10.4% (n=48) |
| bn | 6.2% (n=48) |
| en | 12.2% (n=49) |
| mixed | 8.3% (n=48) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 1.5% (n=68) |
| sms | 4.6% (n=108) |
| tool_description | 70.6% (n=17) |
