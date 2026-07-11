# Monthly Cost Estimate

## Step 1: Requests per day
```
28 prompts × 5 samples × 2 conditions = 280 requests/day
```

## Step 2: Output tokens per day
```
280 requests × 1,000 tokens/response = 280,000 output tokens/day
```

## Step 3: Scale to monthly (30 days)
```
280,000 tokens/day × 30 days = 8,400,000 output tokens/month
```

## Step 4: Apply pricing
Using **Claude 3 Haiku** (cheapest current model): **$0.25/M input tokens, $1.25/M output tokens**

**Output cost:**
```
8.4M tokens × $1.25/M = $10.50/month
```

**Input cost** — *not specified in your question, so I assumed ~500 tokens/prompt (typical for a test harness with instructions + context). Adjust if your prompts are longer/shorter.*
```
280 requests × 500 tokens = 140,000 input tokens/day
140,000 × 30 = 4,200,000 input tokens/month
4.2M × $0.25/M = $1.05/month
```

## Total
```
$10.50 (output) + $1.05 (input) ≈ $11.55/month
```

---

### Things to double-check on your end:
1. **Input token length** — I guessed 500 tokens/prompt. If your prompts are longer (e.g., include few-shot examples or long context), this could meaningfully change the total. At 2,000 input tokens/prompt, input cost would rise to ~$4.20/month.
2. **Model pricing** — confirm current Haiku pricing on Anthropic's site, as rates change.
3. **Days/month** — I used 30; if you want a more precise 365/12 ≈ 30.4, the difference is negligible (~$0.04).

**Bottom line: expect roughly $10–15/month**, dominated by output token costs, assuming input prompts aren't unusually long.