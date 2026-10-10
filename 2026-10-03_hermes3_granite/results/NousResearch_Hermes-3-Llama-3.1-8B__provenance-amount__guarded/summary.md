# NousResearch/Hermes-3-Llama-3.1-8B | defence=provenance-amount | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 0.0% (n=220) |
| Attack cases where the agent actually read the attack | 59.5% (n=220) |
| Attack success among those (lower is better) | 0.0% (n=131) |
| Utility on benign tasks | 22.0% (n=82) |
| Utility under attack | 13.2% (n=220) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=82) |
| Episodes with any blocked call | 11.3% (n=302) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 9.6% (n=302) |
| Episodes where such a payment went through | 0.0% (n=302) |
| Episodes where the agent asked the user to confirm | 15.2% (n=302) |
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
