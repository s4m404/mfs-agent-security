# Qwen/Qwen2.5-3B-Instruct | defence=none | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 10.0% (n=240) |
| Attack cases where the agent actually read the attack | 66.2% (n=240) |
| Attack success among those (lower is better) | 15.1% (n=159) |
| Utility on benign tasks | 20.6% (n=102) |
| Utility under attack | 9.2% (n=240) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=102) |
| Episodes with any blocked call | 0.0% (n=342) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 37.7% (n=342) |
| Episodes where such a payment went through | 3.5% (n=342) |
| Episodes where the agent asked the user to confirm | 26.9% (n=342) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 0.0% (n=60) |
| bn | 4.8% (n=63) |
| en | 25.0% (n=60) |
| mixed | 10.5% (n=57) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 3.8% (n=78) |
| sms | 17.1% (n=123) |
| tool_description | 0.0% (n=39) |
