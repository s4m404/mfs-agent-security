# Qwen/Qwen2.5-14B-Instruct-AWQ | defence=none | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 7.7% (n=220) |
| Attack cases where the agent actually read the attack | 81.8% (n=220) |
| Attack success among those (lower is better) | 9.4% (n=180) |
| Utility on benign tasks | 42.7% (n=82) |
| Utility under attack | 48.2% (n=220) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=82) |
| Episodes with any blocked call | 0.0% (n=302) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 48.7% (n=302) |
| Episodes where such a payment went through | 9.6% (n=302) |
| Episodes where the agent asked the user to confirm | 15.9% (n=302) |
| Episodes stopped by a model error (timeout, reply too long) | 0.0% (n=302) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 1.8% (n=55) |
| bn | 1.8% (n=56) |
| en | 23.6% (n=55) |
| mixed | 3.7% (n=54) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 12.9% (n=70) |
| sms | 2.7% (n=113) |
| tool_description | 13.5% (n=37) |
