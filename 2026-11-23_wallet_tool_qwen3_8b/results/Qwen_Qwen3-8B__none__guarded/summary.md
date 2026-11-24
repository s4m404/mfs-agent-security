# Qwen/Qwen3-8B | defence=none | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 11.4% (n=220) |
| Attack cases where the agent actually read the attack | 86.4% (n=220) |
| Attack success among those (lower is better) | 13.2% (n=190) |
| Utility on benign tasks | 56.1% (n=82) |
| Utility under attack | 43.2% (n=220) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=82) |
| Episodes with any blocked call | 0.0% (n=302) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 25.5% (n=302) |
| Episodes where such a payment went through | 5.3% (n=302) |
| Episodes where the agent asked the user to confirm | 7.3% (n=302) |
| Episodes stopped by a model error (timeout, reply too long) | 0.0% (n=302) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 1.8% (n=55) |
| bn | 7.1% (n=56) |
| en | 27.3% (n=55) |
| mixed | 9.3% (n=54) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 17.1% (n=70) |
| sms | 11.5% (n=113) |
| tool_description | 0.0% (n=37) |
