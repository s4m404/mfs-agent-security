# Qwen/Qwen2.5-7B-Instruct | defence=provenance | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 2.3% (n=220) |
| Attack cases where the agent actually read the attack | 79.1% (n=220) |
| Attack success among those (lower is better) | 2.9% (n=174) |
| Utility on benign tasks | 54.9% (n=82) |
| Utility under attack | 46.8% (n=220) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=82) |
| Episodes with any blocked call | 32.5% (n=302) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 28.8% (n=302) |
| Episodes where such a payment went through | 2.0% (n=302) |
| Episodes where the agent asked the user to confirm | 50.7% (n=302) |
| Episodes stopped by a model error (timeout, reply too long) | 0.0% (n=302) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 1.8% (n=55) |
| bn | 0.0% (n=56) |
| en | 5.5% (n=55) |
| mixed | 1.9% (n=54) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 4.3% (n=70) |
| sms | 1.8% (n=113) |
| tool_description | 0.0% (n=37) |
