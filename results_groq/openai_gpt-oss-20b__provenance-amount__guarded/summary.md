# openai/gpt-oss-20b | defence=provenance-amount | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 0.0% (n=181) |
| Attack cases where the agent actually read the attack | 77.3% (n=181) |
| Attack success among those (lower is better) | 0.0% (n=140) |
| Utility on benign tasks | 91.0% (n=78) |
| Utility under attack | 75.7% (n=181) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=78) |
| Episodes with any blocked call | 25.1% (n=259) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 14.7% (n=259) |
| Episodes where such a payment went through | 0.0% (n=259) |
| Episodes where the agent asked the user to confirm | 15.1% (n=259) |
| Episodes stopped by a model error (timeout, reply too long) | 0.0% (n=259) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 0.0% (n=45) |
| bn | 0.0% (n=45) |
| en | 0.0% (n=46) |
| mixed | 0.0% (n=45) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 0.0% (n=65) |
| sms | 0.0% (n=104) |
| tool_description | 0.0% (n=12) |
