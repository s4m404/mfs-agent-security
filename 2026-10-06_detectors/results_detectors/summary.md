## Attack texts flagged (higher is better)

| Detector | All | en | bn | banglish | mixed | Instructions to the AI | Ordinary scam messages |
|---|---:|---:|---:|---:|---:|---:|---:|
| keyword | 34% (59/174; 27 to 41) | 40% (17/43; 26 to 54) | 43% (19/44; 30 to 58) | 45% (20/44; 32 to 60) | 7% (3/43; 2 to 19) | 57% (59/104; 47 to 66) | 0% (0/70; 0 to 5) |
| protectai/deberta-v3-base-prompt-injection-v2 | 59% (102/174; 51 to 66) | 47% (20/43; 33 to 61) | 57% (25/44; 42 to 70) | 80% (35/44; 65 to 89) | 51% (22/43; 37 to 65) | 66% (69/104; 57 to 75) | 47% (33/70; 36 to 59) |
| deepset/deberta-v3-base-injection | 100% (174/174; 98 to 100) | 100% (43/43; 92 to 100) | 100% (44/44; 92 to 100) | 100% (44/44; 92 to 100) | 100% (43/43; 92 to 100) | 100% (104/104; 96 to 100) | 100% (70/70; 95 to 100) |

## Normal texts flagged: false alarms (lower is better)

| Detector | All | en | bn | banglish | mixed |
|---|---:|---:|---:|---:|---:|
| keyword | 7% (4/54; 3 to 18) | 0% (0/16; 0 to 19) | 11% (2/19; 3 to 31) | 9% (1/11; 2 to 38) | 12% (1/8; 2 to 47) |
| protectai/deberta-v3-base-prompt-injection-v2 | 39% (21/54; 27 to 52) | 12% (2/16; 3 to 36) | 84% (16/19; 62 to 94) | 9% (1/11; 2 to 38) | 25% (2/8; 7 to 59) |
| deepset/deberta-v3-base-injection | 87% (47/54; 76 to 94) | 56% (9/16; 33 to 77) | 100% (19/19; 83 to 100) | 100% (11/11; 74 to 100) | 100% (8/8; 68 to 100) |
