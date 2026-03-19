A/B and multivariate testing methodology. Design experiments, calculate sample sizes, determine statistical significance, avoid common pitfalls, and interpret results. Platform-agnostic framework applicable to landing pages, emails, ads, pricing, and product features. Use when the user asks about A/B testing, split testing, experiment design, statistical significance, or conversion experiments.


# A/B Testing Framework

Design, run, and analyze conversion experiments with statistical rigor.

## Test Design Process

### Step 1: Hypothesis

**Template:** If we [change X], then [metric Y] will [increase/decrease] by [Z%] because [reason].

**Good hypothesis:** "If we change the CTA from Get Started to Start Free Trial, then signup rate will increase by 15% because it reduces uncertainty about cost."

**Bad hypothesis:** "If we change the button color, conversions will improve." (No reasoning, no expected magnitude.)

### Step 2: Sample Size Calculation

To determine how long to run a test:

```
Required sample per variation = 16 * (p * (1-p)) / (MDE^2)

Where:
  p = baseline conversion rate (as decimal)
  MDE = minimum detectable effect (as decimal)
```

| Baseline Rate | 10% MDE | 20% MDE | 30% MDE |
|--------------|---------|---------|---------|
| 1% | 253,414 | 63,354 | 28,157 |
| 3% | 82,369 | 20,592 | 9,152 |
| 5% | 48,640 | 12,160 | 5,404 |
| 10% | 23,040 | 5,760 | 2,560 |
| 20% | 10,240 | 2,560 | 1,138 |

**Minimum test duration:** 2 full business weeks (to capture day-of-week effects), even if sample size is reached sooner.

### Step 3: Test Execution Rules

1. **Random assignment** — visitors must be randomly assigned to control/variant
2. **No peeking** — do not check results before reaching sample size
3. **No mid-test changes** — do not modify variants during the test
4. **Even traffic split** — 50/50 for A/B, even splits for multivariate
5. **Single variable** — change only one thing per test (unless multivariate)
6. **Full duration** — run for the pre-calculated duration, not until significance

### Step 4: Statistical Analysis

#### Frequentist Approach

**Z-test for proportions:**
```
Z = (p1 - p2) / sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2))

Where:
  p1, p2 = conversion rates of control and variant
  p_pooled = (x1 + x2) / (n1 + n2)
  n1, n2 = sample sizes
```

**p-value interpretation:**
- p < 0.05: Statistically significant (95% confidence)
- p < 0.01: Highly significant (99% confidence)
- p >= 0.05: Not significant — do not declare a winner

#### Bayesian Approach

**When to use Bayesian:**
- Low traffic (small sample sizes)
- Need to make decisions faster
- Want probability of each variant being best (not just "significant or not")

**Interpretation:** "There is a 94% probability that Variant B is better than Control" vs frequentist "We reject the null hypothesis at 95% confidence."

### Step 5: Decision Framework

| Result | Significance | Action |
|--------|-------------|--------|
| Variant wins | p < 0.05 | Implement variant |
| Control wins | p < 0.05 | Keep control, learn from failure |
| No difference | p >= 0.05 | Keep control, test something bigger |
| Variant wins | p = 0.05-0.10 | Consider traffic — may need more time |

## Common Testing Pitfalls


(Truncated. See full skill at github.com/thatrebeccarae/claude-marketing)
