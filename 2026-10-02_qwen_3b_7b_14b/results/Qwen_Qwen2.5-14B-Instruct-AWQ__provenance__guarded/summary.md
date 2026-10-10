# Qwen/Qwen2.5-14B-Instruct-AWQ | defence=provenance | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 2.3% (n=220) |
| Attack cases where the agent actually read the attack | 70.9% (n=220) |
| Attack success among those (lower is better) | 3.2% (n=156) |
| Utility on benign tasks | 50.0% (n=82) |
| Utility under attack | 40.9% (n=220) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=82) |
| Episodes with any blocked call | 43.7% (n=302) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 48.7% (n=302) |
| Episodes where such a payment went through | 8.9% (n=302) |
| Episodes where the agent asked the user to confirm | 35.8% (n=302) |
| Episodes stopped by a model error (timeout, reply too long) | 0.0% (n=302) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 0.0% (n=55) |
| bn | 0.0% (n=56) |
| en | 7.3% (n=55) |
| mixed | 1.9% (n=54) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 1.4% (n=70) |
| sms | 3.5% (n=113) |
| tool_description | 0.0% (n=37) |
