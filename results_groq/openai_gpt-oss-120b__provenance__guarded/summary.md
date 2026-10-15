# openai/gpt-oss-120b | defence=provenance | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 0.0% (n=143) |
| Attack cases where the agent actually read the attack | 74.1% (n=143) |
| Attack success among those (lower is better) | 0.0% (n=106) |
| Utility on benign tasks | 93.6% (n=78) |
| Utility under attack | 87.4% (n=143) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=78) |
| Episodes with any blocked call | 8.1% (n=221) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 3.2% (n=221) |
| Episodes where such a payment went through | 0.5% (n=221) |
| Episodes where the agent asked the user to confirm | 4.5% (n=221) |
| Episodes stopped by a model error (timeout, reply too long) | 0.0% (n=221) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 0.0% (n=36) |
| bn | 0.0% (n=36) |
| en | 0.0% (n=36) |
| mixed | 0.0% (n=35) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 0.0% (n=56) |
| sms | 0.0% (n=75) |
| tool_description | 0.0% (n=12) |
