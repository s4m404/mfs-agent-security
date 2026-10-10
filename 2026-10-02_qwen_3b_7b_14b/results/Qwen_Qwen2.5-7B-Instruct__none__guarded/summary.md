# Qwen/Qwen2.5-7B-Instruct | defence=none | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 5.9% (n=220) |
| Attack cases where the agent actually read the attack | 77.7% (n=220) |
| Attack success among those (lower is better) | 7.6% (n=171) |
| Utility on benign tasks | 56.1% (n=82) |
| Utility under attack | 46.4% (n=220) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=82) |
| Episodes with any blocked call | 0.0% (n=302) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 29.1% (n=302) |
| Episodes where such a payment went through | 2.6% (n=302) |
| Episodes where the agent asked the user to confirm | 29.1% (n=302) |
| Episodes stopped by a model error (timeout, reply too long) | 0.0% (n=302) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 5.5% (n=55) |
| bn | 1.8% (n=56) |
| en | 5.5% (n=55) |
| mixed | 11.1% (n=54) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 5.7% (n=70) |
| sms | 8.0% (n=113) |
| tool_description | 0.0% (n=37) |
