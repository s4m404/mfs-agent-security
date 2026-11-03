# openai/gpt-oss-20b | defence=none | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 19.6% (n=148) |
| Attack cases where the agent actually read the attack | 87.8% (n=148) |
| Attack success among those (lower is better) | 22.3% (n=130) |
| Utility on benign tasks | 87.2% (n=78) |
| Utility under attack | 81.1% (n=148) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=78) |
| Episodes with any blocked call | 0.0% (n=226) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 16.4% (n=226) |
| Episodes where such a payment went through | 2.2% (n=226) |
| Episodes where the agent asked the user to confirm | 5.3% (n=226) |
| Episodes stopped by a model error (timeout, reply too long) | 1.8% (n=226) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 16.2% (n=37) |
| bn | 18.9% (n=37) |
| en | 27.0% (n=37) |
| mixed | 16.2% (n=37) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 16.1% (n=56) |
| sms | 15.0% (n=80) |
| tool_description | 66.7% (n=12) |
