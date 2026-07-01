# OpenRouter Independent Data Audit

Generated: 2026-07-01T12:00:21.817861+00:00
Model: `anthropic/claude-sonnet-4`
Prompt: `scripts/independent_data_audit/openrouter_audit_prompt.txt`

## Summary

- Raw sources audited: 1
- `pass` verdicts: 1
- `review` verdicts: 0
- `fail` verdicts: 0
- High-severity issues: 0
- Medium-severity issues: 0
- Low-severity issues: 0

## 2018/results-long.pdf

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2018/long.csv`
- Summary: CSV extraction accurately represents the PDF source with proper normalization applied

### Issues

- None reported.

### Notable Matches

- M16 winner Touko Seppa (FIN) correctly extracted: 41:08 → 2468 seconds
- M18 tied winners Mikko Eerola (FIN) and Sander Arntzen (NOR) both at 53:31 → 3211 seconds
- Country normalization working correctly: 'Russian Federati Russian Fed' → RUS
- Non-EYOC countries (NZL, USA, AUS) properly excluded from clean CSV
- All 4 classes (M16, M18, W16, W18) with correct competitor counts and rankings
- DNF/DNS/MP statuses correctly handled where present in source
