# openai/gpt-oss-20b | defence=provenance-amount | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 0.0% (n=124) |
| Attack cases where the agent actually read the attack | 72.6% (n=124) |
| Attack success among those (lower is better) | 0.0% (n=90) |
| Utility on benign tasks | 91.0% (n=78) |
| Utility under attack | 71.8% (n=124) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=78) |
| Episodes with any blocked call | 26.7% (n=202) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 15.3% (n=202) |
| Episodes where such a payment went through | 0.0% (n=202) |
| Episodes where the agent asked the user to confirm | 15.3% (n=202) |
| Episodes stopped by a model error (timeout, reply too long) | 0.0% (n=202) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 0.0% (n=31) |
| bn | 0.0% (n=31) |
| en | 0.0% (n=31) |
| mixed | 0.0% (n=31) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 0.0% (n=56) |
| sms | 0.0% (n=56) |
| tool_description | 0.0% (n=12) |
