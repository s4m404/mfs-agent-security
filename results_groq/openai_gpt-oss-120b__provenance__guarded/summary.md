# openai/gpt-oss-120b | defence=provenance | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 1.1% (n=177) |
| Attack cases where the agent actually read the attack | 76.3% (n=177) |
| Attack success among those (lower is better) | 1.5% (n=135) |
| Utility on benign tasks | 93.6% (n=78) |
| Utility under attack | 87.0% (n=177) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=78) |
| Episodes with any blocked call | 7.5% (n=255) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 3.1% (n=255) |
| Episodes where such a payment went through | 0.4% (n=255) |
| Episodes where the agent asked the user to confirm | 3.9% (n=255) |
| Episodes stopped by a model error (timeout, reply too long) | 0.0% (n=255) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 0.0% (n=44) |
| bn | 0.0% (n=44) |
| en | 4.4% (n=45) |
| mixed | 0.0% (n=44) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 0.0% (n=62) |
| sms | 1.9% (n=103) |
| tool_description | 0.0% (n=12) |
