# openai/gpt-oss-120b | defence=provenance | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 0.0% (n=69) |
| Attack cases where the agent actually read the attack | 73.9% (n=69) |
| Attack success among those (lower is better) | 0.0% (n=51) |
| Utility on benign tasks | 90.0% (n=30) |
| Utility under attack | 82.6% (n=69) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=30) |
| Episodes with any blocked call | 13.1% (n=99) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 4.0% (n=99) |
| Episodes where such a payment went through | 0.0% (n=99) |
| Episodes where the agent asked the user to confirm | 8.1% (n=99) |
| Episodes stopped by a model error (timeout, reply too long) | 0.0% (n=99) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 0.0% (n=17) |
| bn | 0.0% (n=17) |
| en | 0.0% (n=18) |
| mixed | 0.0% (n=17) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 0.0% (n=24) |
| sms | 0.0% (n=36) |
| tool_description | 0.0% (n=9) |
