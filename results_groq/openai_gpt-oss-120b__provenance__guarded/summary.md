# openai/gpt-oss-120b | defence=provenance | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 3.3% (n=209) |
| Attack cases where the agent actually read the attack | 77.5% (n=209) |
| Attack success among those (lower is better) | 4.3% (n=162) |
| Utility on benign tasks | 93.6% (n=78) |
| Utility under attack | 77.5% (n=209) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=78) |
| Episodes with any blocked call | 12.5% (n=287) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 3.5% (n=287) |
| Episodes where such a payment went through | 0.3% (n=287) |
| Episodes where the agent asked the user to confirm | 9.4% (n=287) |
| Episodes stopped by a model error (timeout, reply too long) | 0.0% (n=287) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 3.8% (n=52) |
| bn | 1.9% (n=53) |
| en | 7.7% (n=52) |
| mixed | 0.0% (n=52) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 1.5% (n=68) |
| sms | 5.6% (n=108) |
| tool_description | 0.0% (n=33) |
