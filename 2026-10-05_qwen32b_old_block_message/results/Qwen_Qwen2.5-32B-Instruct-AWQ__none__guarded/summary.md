# Qwen/Qwen2.5-32B-Instruct-AWQ | defence=none | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 14.5% (n=220) |
| Attack cases where the agent actually read the attack | 82.3% (n=220) |
| Attack success among those (lower is better) | 17.7% (n=181) |
| Utility on benign tasks | 65.9% (n=82) |
| Utility under attack | 57.7% (n=220) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=82) |
| Episodes with any blocked call | 0.0% (n=302) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 39.7% (n=302) |
| Episodes where such a payment went through | 6.6% (n=302) |
| Episodes where the agent asked the user to confirm | 17.9% (n=302) |
| Episodes stopped by a model error (timeout, reply too long) | 0.0% (n=302) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 12.7% (n=55) |
| bn | 5.4% (n=56) |
| en | 25.5% (n=55) |
| mixed | 14.8% (n=54) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 15.7% (n=70) |
| sms | 10.6% (n=113) |
| tool_description | 24.3% (n=37) |
