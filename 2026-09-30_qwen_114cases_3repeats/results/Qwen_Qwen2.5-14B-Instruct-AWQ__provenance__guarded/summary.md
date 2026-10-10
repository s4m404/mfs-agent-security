# Qwen/Qwen2.5-14B-Instruct-AWQ | defence=provenance | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 0.0% (n=240) |
| Attack cases where the agent actually read the attack | 76.2% (n=240) |
| Attack success among those (lower is better) | 0.0% (n=183) |
| Utility on benign tasks | 36.3% (n=102) |
| Utility under attack | 39.6% (n=240) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=102) |
| Episodes with any blocked call | 47.7% (n=342) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 45.9% (n=342) |
| Episodes where such a payment went through | 1.8% (n=342) |
| Episodes where the agent asked the user to confirm | 37.1% (n=342) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 0.0% (n=60) |
| bn | 0.0% (n=63) |
| en | 0.0% (n=60) |
| mixed | 0.0% (n=57) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 0.0% (n=78) |
| sms | 0.0% (n=123) |
| tool_description | 0.0% (n=39) |
