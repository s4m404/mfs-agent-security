# openai/gpt-oss-120b | defence=provenance-amount | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 0.0% (n=72) |
| Attack cases where the agent actually read the attack | 77.8% (n=72) |
| Attack success among those (lower is better) | 0.0% (n=56) |
| Utility on benign tasks | 93.0% (n=57) |
| Utility under attack | 83.3% (n=72) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=57) |
| Episodes with any blocked call | 8.5% (n=129) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 2.3% (n=129) |
| Episodes where such a payment went through | 0.0% (n=129) |
| Episodes where the agent asked the user to confirm | 7.0% (n=129) |
| Episodes stopped by a model error (timeout, reply too long) | 0.8% (n=129) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 0.0% (n=18) |
| bn | 0.0% (n=18) |
| en | 0.0% (n=18) |
| mixed | 0.0% (n=18) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 0.0% (n=24) |
| sms | 0.0% (n=36) |
| tool_description | 0.0% (n=12) |
