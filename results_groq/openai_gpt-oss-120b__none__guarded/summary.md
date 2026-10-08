# openai/gpt-oss-120b | defence=none | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 5.6% (n=161) |
| Attack cases where the agent actually read the attack | 75.8% (n=161) |
| Attack success among those (lower is better) | 7.4% (n=122) |
| Utility on benign tasks | 93.6% (n=78) |
| Utility under attack | 92.5% (n=161) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=78) |
| Episodes with any blocked call | 0.0% (n=239) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 2.5% (n=239) |
| Episodes where such a payment went through | 0.4% (n=239) |
| Episodes where the agent asked the user to confirm | 0.4% (n=239) |
| Episodes stopped by a model error (timeout, reply too long) | 0.4% (n=239) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 5.0% (n=40) |
| bn | 4.9% (n=41) |
| en | 5.0% (n=40) |
| mixed | 7.5% (n=40) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 1.8% (n=56) |
| sms | 0.0% (n=93) |
| tool_description | 66.7% (n=12) |
