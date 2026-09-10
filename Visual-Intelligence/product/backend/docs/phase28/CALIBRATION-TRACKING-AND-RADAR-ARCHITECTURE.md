# Phase 28: Calibration Tracking & Radar Architecture

## 1. Expected Calibration Error (ECE) Formula
To prevent model overconfidence from being mistaken for empirical certainty:

$$\mathrm{ECE} = \sum_{m=1}^{M} \frac{|B_m|}{N} \Big| \mathrm{acc}(B_m) - \mathrm{conf}(B_m) \Big|$$

Where:
- $M = 5$ confidence buckets: `[0.00, 0.20)`, `[0.20, 0.40)`, `[0.40, 0.60)`, `[0.60, 0.80)`, `[0.80, 1.00]`.
- $|B_m|$ is the count of predictions in bucket $m$.
- $\mathrm{acc}(B_m)$ is empirical success rate.
- $\mathrm{conf}(B_m)$ is average model predicted confidence.

Buckets with sample count $n < 50$ are flagged as statistically unreliable.
