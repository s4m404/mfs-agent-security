# openai/gpt-oss-120b | defence=none | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 6.7% (n=165) |
| Attack cases where the agent actually read the attack | 75.8% (n=165) |
| Attack success among those (lower is better) | 8.8% (n=125) |
| Utility on benign tasks | 94.9% (n=78) |
| Utility under attack | 93.3% (n=165) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=78) |
| Episodes with any blocked call | 0.0% (n=243) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 1.6% (n=243) |
| Episodes where such a payment went through | 1.6% (n=243) |
| Episodes where the agent asked the user to confirm | 2.5% (n=243) |
| Episodes stopped by a model error (timeout, reply too long) | 0.4% (n=243) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 4.9% (n=41) |
| bn | 4.9% (n=41) |
| en | 9.5% (n=42) |
| mixed | 7.3% (n=41) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 1.8% (n=56) |
| sms | 1.0% (n=97) |
| tool_description | 75.0% (n=12) |
