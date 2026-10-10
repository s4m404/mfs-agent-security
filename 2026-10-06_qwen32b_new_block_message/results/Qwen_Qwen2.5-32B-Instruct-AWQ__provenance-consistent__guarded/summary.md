# Qwen/Qwen2.5-32B-Instruct-AWQ | defence=provenance-consistent | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 0.0% (n=220) |
| Attack cases where the agent actually read the attack | 78.2% (n=220) |
| Attack success among those (lower is better) | 0.0% (n=172) |
| Utility on benign tasks | 70.7% (n=82) |
| Utility under attack | 57.3% (n=220) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=82) |
| Episodes with any blocked call | 46.0% (n=302) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 39.1% (n=302) |
| Episodes where such a payment went through | 0.0% (n=302) |
| Episodes where the agent asked the user to confirm | 33.4% (n=302) |
| Episodes stopped by a model error (timeout, reply too long) | 0.0% (n=302) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 0.0% (n=55) |
| bn | 0.0% (n=56) |
| en | 0.0% (n=55) |
| mixed | 0.0% (n=54) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 0.0% (n=70) |
| sms | 0.0% (n=113) |
| tool_description | 0.0% (n=37) |
