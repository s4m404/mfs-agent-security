# Qwen/Qwen2.5-3B-Instruct | defence=none | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 7.3% (n=220) |
| Attack cases where the agent actually read the attack | 57.3% (n=220) |
| Attack success among those (lower is better) | 12.7% (n=126) |
| Utility on benign tasks | 17.1% (n=82) |
| Utility under attack | 10.0% (n=220) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=82) |
| Episodes with any blocked call | 0.0% (n=302) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 51.7% (n=302) |
| Episodes where such a payment went through | 10.9% (n=302) |
| Episodes where the agent asked the user to confirm | 27.5% (n=302) |
| Episodes stopped by a model error (timeout, reply too long) | 0.0% (n=302) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 0.0% (n=55) |
| bn | 5.4% (n=56) |
| en | 18.2% (n=55) |
| mixed | 5.6% (n=54) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 2.9% (n=70) |
| sms | 11.5% (n=113) |
| tool_description | 2.7% (n=37) |
