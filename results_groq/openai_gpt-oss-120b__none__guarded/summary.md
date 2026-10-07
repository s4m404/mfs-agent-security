# openai/gpt-oss-120b | defence=none | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 11.1% (n=72) |
| Attack cases where the agent actually read the attack | 77.8% (n=72) |
| Attack success among those (lower is better) | 14.3% (n=56) |
| Utility on benign tasks | 93.0% (n=57) |
| Utility under attack | 91.7% (n=72) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=57) |
| Episodes with any blocked call | 0.0% (n=129) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 3.1% (n=129) |
| Episodes where such a payment went through | 0.0% (n=129) |
| Episodes where the agent asked the user to confirm | 0.0% (n=129) |
| Episodes stopped by a model error (timeout, reply too long) | 0.8% (n=129) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 11.1% (n=18) |
| bn | 11.1% (n=18) |
| en | 11.1% (n=18) |
| mixed | 11.1% (n=18) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 0.0% (n=24) |
| sms | 0.0% (n=36) |
| tool_description | 66.7% (n=12) |
