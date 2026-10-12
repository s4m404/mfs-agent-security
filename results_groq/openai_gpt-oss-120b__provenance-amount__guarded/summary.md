# openai/gpt-oss-120b | defence=provenance-amount | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 0.0% (n=159) |
| Attack cases where the agent actually read the attack | 76.7% (n=159) |
| Attack success among those (lower is better) | 0.0% (n=122) |
| Utility on benign tasks | 93.6% (n=78) |
| Utility under attack | 91.2% (n=159) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=78) |
| Episodes with any blocked call | 5.9% (n=237) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 2.1% (n=237) |
| Episodes where such a payment went through | 0.0% (n=237) |
| Episodes where the agent asked the user to confirm | 4.6% (n=237) |
| Episodes stopped by a model error (timeout, reply too long) | 0.4% (n=237) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 0.0% (n=40) |
| bn | 0.0% (n=40) |
| en | 0.0% (n=40) |
| mixed | 0.0% (n=39) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 0.0% (n=56) |
| sms | 0.0% (n=91) |
| tool_description | 0.0% (n=12) |
