# OpenRouter Independent Data Audit

Generated: 2026-07-01T11:04:50.729000+00:00
Model: `anthropic/claude-sonnet-4`
Prompt: `scripts/independent_data_audit/openrouter_audit_prompt.txt`

## Summary

- Raw sources audited: 4
- `pass` verdicts: 4
- `review` verdicts: 0
- `fail` verdicts: 0
- High-severity issues: 0
- Medium-severity issues: 0
- Low-severity issues: 0

## 2024/Long-eventor.xml [M16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2024/long.csv`
- Classes: `M16`
- Summary: All 95 M16 competitors from the XML source are correctly extracted with accurate ranks, times, countries, and names. Two DNF entries are properly handled.

### Issues

- None reported.

### Notable Matches

- Erik Heczko (CZE) correctly extracted as winner with 45:25 (2725 seconds)
- Mihaly Csoboth (HUN) correctly placed 2nd with 46:47 (2807 seconds)
- Two tied competitors at rank 30 (Julian Schmied and Patrik Sedlacek) both with 58:50 correctly handled
- Mark Levente Bujdoso correctly marked as DNF with partial time 49:30
- Lauri Urbanek correctly marked as DNF with no finish time
- Country codes properly normalized: Czechia→CZE, Great Britain→GBR, Turkiye→TUR
- Names properly normalized: 'Fernandez Garcia, Ekain' → 'Ekain Fernandez Garcia'
- All 93 finishers plus 2 DNF entries match the XML source exactly

## 2024/Long-eventor.xml [M18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2024/long.csv`
- Classes: `M18`
- Summary: All 105 M18 competitors from the XML source are correctly extracted with accurate ranks, times, countries, and statuses. The data shows excellent fidelity to the source.

### Issues

- None reported.

### Notable Matches

- Winner Emil Husebye Aamodt (NOR) correctly shows 54:29 = 3269 seconds with rank 1
- Tied competitors Tommy Rollins and Laurence Ward both correctly show rank 31 with identical 1:04:11 times
- MP (MisPunch) statuses correctly extracted for Max Oesterberg, Johannes Marager, and Cristian Betivu
- Country codes properly normalized: 'Czechia' → CZE, 'Turkiye' → TUR, 'Moldova, Republic of' → MDA
- Complex names handled well: 'Asbjoern Faber Fenger Groen', 'Altar Ilgaz Tuzcuogullari', 'Idar Elias Jongenburger'
- Time conversions accurate throughout: 2:02:17 → 7337 seconds for slowest finisher
- All 102 OK finishers plus 3 MP competitors properly accounted for

## 2024/Long-eventor.xml [W16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2024/long.csv`
- Classes: `W16`
- Summary: All 87 W16 competitors correctly extracted from XML source with accurate data mapping

### Issues

- None reported.

### Notable Matches

- Winner Mira Werder (SUI) correctly shows 46:18 → 2778 seconds with rank 1
- Gabija Stankeviciute (LTU) correctly shows 48:50 → 2930 seconds with rank 2
- All time conversions accurate: 1:00:21 → 3621 seconds for Karina Fedoryshyn
- Tied ranks handled correctly: both Ella Baxter and Iryna Polubentseva at rank 35
- MP status correctly assigned to Emanuela Stoyanova (bib 2055) with MisPunch in XML
- Country codes properly normalized: Turkiye → TUR, Czechia → CZE
- Complex names preserved: 'Astrid Faber FengerGroen' → 'Astrid Faber Fengergroen'
- All 87 entries from XML numberOfEntries match CSV row count including MP competitor

## 2024/Long-eventor.xml [W18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2024/long.csv`
- Classes: `W18`
- Summary: All 90 W18 competitors from the XML source are correctly extracted with accurate ranks, times, countries, and statuses

### Issues

- None reported.

### Notable Matches

- Winner Freja Hjerne (SWE) correctly extracted with 53:50 → 3230 seconds
- Tied 54th place correctly handled: Eliza Odrina and Laura Krumina both at 1:23:07 → 4987 seconds
- MP status correctly extracted for Freya Tryner with MisPunch → MP and time 1:12:31 → 4351 seconds
- DNF status correctly extracted for Nea Erzen with DidNotFinish → DNF and blank time
- Country normalization working: 'Turkiye' → TUR, 'Great Britain' → GBR, 'Czechia' → CZE
- Complex names handled well: 'Sigrid Schmitt Gran', 'Lovise Harriette Koppel', 'Irem Gul Nazlimoglu'
- Time conversions accurate: 53:50 → 3230s, 2:00:33 → 7233s, 1:46:08 → 6368s
