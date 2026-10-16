# openai/gpt-oss-120b | defence=provenance | prompt=guarded

| Metric | Value |
| --- | --- |
| Attack success rate (lower is better) | 3.5% (n=201) |
| Attack cases where the agent actually read the attack | 76.6% (n=201) |
| Attack success among those (lower is better) | 4.5% (n=154) |
| Utility on benign tasks | 93.6% (n=78) |
| Utility under attack | 80.6% (n=201) |
| Benign tasks where the correct action was blocked (false blocks) | 0.0% (n=78) |
| Episodes with any blocked call | 10.4% (n=279) |
| Episodes where the agent tried to pay a payee or amount nobody asked for | 2.9% (n=279) |
| Episodes where such a payment went through | 0.4% (n=279) |
| Episodes where the agent asked the user to confirm | 7.2% (n=279) |
| Episodes stopped by a model error (timeout, reply too long) | 0.0% (n=279) |

## Attack success by injection language

| Injection language | Attack success |
| --- | --- |
| banglish | 3.9% (n=51) |
| bn | 2.0% (n=50) |
| en | 8.0% (n=50) |
| mixed | 0.0% (n=50) |

## Attack success by vector

| Vector | Attack success |
| --- | --- |
| invoice | 1.5% (n=68) |
| sms | 5.6% (n=108) |
| tool_description | 0.0% (n=25) |
