# OpenRouter Independent Data Audit

Generated: 2026-07-01T12:20:01.503080+00:00
Model: `anthropic/claude-sonnet-4`
Prompt: `scripts/independent_data_audit/openrouter_audit_prompt.txt`

## Summary

- Raw sources audited: 97
- `pass` verdicts: 64
- `review` verdicts: 27
- `fail` verdicts: 6
- High-severity issues: 33
- Medium-severity issues: 52
- Low-severity issues: 51

## 2002/eyoc2002.htm

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2002/long.csv`, `2002/relay.csv`, `2002/sprint.csv`
- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All classes, ranks, times, names, and countries match the source data after expected transformations.

### Issues

- None reported.

### Notable Matches

- Class normalization: W16E/W18E/M16E/M18E → W16/W18/M16/M18 correctly applied
- Country normalization: SWITZERLAND → SUI, CZECH REPUBLIC → CZE, BELORUSSIA → BLR properly handled
- Time conversion: 14.54 → 894 seconds, 32.44 → 1964 seconds correctly calculated
- Name normalization: LUESCHER Sara → Sara Luescher, KOSIÑSKA Dorota → Dorota Kosinska with proper case/order
- Relay data correctly parsed: Switzerland W16 team total 89.15 → 5355 seconds with proper leg breakdown
- Hungarian results properly included as host country in abbreviated 2002 dataset
- Tied ranks preserved: M18 long distance shows two 4th place finishers correctly
- Special characters handled: KOSIÑSKA, CSISZÁR, Ukraina → Ukraine normalization applied

## 2003/eyoc2003.htm

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2003/long.csv`, `2003/relay.csv`, `2003/sprint.csv`
- Summary: The CSV extraction accurately represents the raw source data with proper normalization applied. All major data points match correctly across sprint, long distance, and relay events.

### Issues

- [low] `name` Minor name variations in relay teams (parser_bug=false, source_limitation=true)
  CSV: Both spellings appear consistently within their respective contexts
  Raw: Struhalova Olena vs Srtuhalova Olena in individual events
  Why: The raw source shows slight spelling variations between individual and relay sections, which the CSV preserves accurately
  Next: No action needed - this reflects source inconsistencies
- [low] `name` Abbreviated names in relay results (parser_bug=false, source_limitation=true)
  CSV: CSV preserves the abbreviated forms as they appear in relay sections
  Raw: Nin Oleynichenkova, Karin D´Harreville in relay vs full names in individual
  Why: Raw source uses abbreviated names in relay results, CSV correctly preserves these
  Next: No action needed - accurately reflects source formatting

### Notable Matches

- Sprint W16 winner Iwona Wicha (POL) with 10.17,6 correctly converted to 618 seconds
- Long M18 winner Csaba Gösswein (HUN) with 49.55 correctly converted to 2995 seconds
- Relay W16 winning SUI team total 82.45 correctly converted to 4965 seconds with proper leg splits
- All DSQ/DISQ entries properly excluded from clean CSVs as expected
- Country normalization correctly applied: Czech republic → CZE, Latvija → LAT, Belarusia → BLR
- Class normalization properly applied: W16E → W16, M18E → M18, etc.
- Non-allowlisted countries like Serbia and Montenegro (SCG) and Slovenia (SLO) correctly excluded
- Mixed relay teams (MI1, MI2, etc.) correctly excluded as non-competition entries
- Time conversions accurate throughout: 12.01,6 format correctly parsed as 12 minutes 1.6 seconds

## 2004/eyoc2004.htm

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2004/long.csv`, `2004/relay.csv`, `2004/sprint.csv`
- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All major data points match correctly.

### Issues

- None reported.

### Notable Matches

- Sprint W16: Nina Oleynichenkova 12:31 → 751 seconds correctly converted
- Long M18: Michal Krajcik 51:06 → 3066 seconds correctly converted
- Relay W16: Russia team total 1:29:41 → 5381 seconds with proper leg breakdown
- Country normalization: 'Czech Republic' → 'CZE', 'Belorussia' → 'BLR' applied correctly
- Name normalization: 'Malgorzata Kosinska' properly formatted to title case
- Status handling: MP, DNS, DNF statuses preserved accurately in relay results
- Class normalization: 'W16E' → 'W16', 'M18E' → 'M18' applied consistently
- Tied ranks handled correctly: M16 sprint shows tied 2nd place for Szabo and Kodeda
- Mixed relay class absent from source, correctly not included in CSV
- Guest nations like Kazakhstan properly excluded from normalized results

## 2005/eyoc2005.htm

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2005/long.csv`, `2005/relay.csv`, `2005/sprint.csv`
- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All individual and relay results are correctly parsed with appropriate class, country, name, and time conversions.

### Issues

- None reported.

### Notable Matches

- W16 sprint winner Dorottya Peley (HUN) correctly shows 12.01,4 → 721 seconds
- M18 long winner Stepan Kodeda (CZE) correctly shows 67.22 → 4042 seconds
- Relay W16 winner CZE team correctly parsed with leg times: Hlavova 29.24→1764s, Prochazkova 29.07→1747s, Bochenkova 30.43→1843s
- Country normalization working: 'Czech Republic' → 'CZE', 'Great Britain' → 'GBR'
- Name normalization applied: 'Proch�zkov� Michaela' → 'Michaela Prochazkova'
- Proper handling of tied ranks (M18 sprint ranks 25-25 for Renzullo and Myszkowski)
- DSQ status correctly captured for athletes like 'Zymanciuote Augustina' and others marked as 'DISK'
- Mixed relay teams properly excluded from clean CSV as expected
- Non-EYOC countries like Serbia and Montenegro (SRB) correctly included as they are allowlisted

## 2006/2006_relay_m16.txt

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2006/relay.csv`
- Summary: CSV accurately represents the raw relay results with proper normalization applied

### Issues

- None reported.

### Notable Matches

- Class 'M 15-16' correctly normalized to 'M16'
- Team SUI 1 with 1:30:11 total time correctly converted to 5411 seconds
- All leg times properly converted from MM:SS to seconds (e.g., 0:30:10 → 1810)
- Names normalized from 'SURNAME, Given' to 'Given Surname' format consistently
- Country 'SCG' correctly normalized to 'SRB' for Serbia
- Country 'ROM' correctly normalized to 'ROU' for Romania
- MP status correctly assigned to ESP and ITA teams with mispunches
- Accent handling: 'Štìpán' → 'Stipan', 'Théo' → 'Theo'
- All 18 ranked teams plus 2 MP teams properly extracted
- Team numbers preserved in team names (e.g., 'Team SUI 1', 'Team LAT 94')

## 2006/2006_relay_m18.txt

- Verdict: `review`
- Confidence: `medium`
- Related CSVs: `2006/relay.csv`
- Summary: Most data matches well, but several issues need review: incorrect country code (ROU vs ROM), problematic relay leg composition with female athlete in male class, and some name normalization concerns

### Issues

- [medium] `country` Country code mismatch for Romania (parser_bug=false, source_limitation=false)
  CSV: ROU,Team ROM 62
  Raw: Team ROM 62
  Why: Raw source shows 'ROM' but CSV normalized to 'ROU'. Need to verify if ROM->ROU normalization is correct for 2006 EYOC
  Next: Verify correct country code for Romania in 2006 EYOC context
- [medium] `relay-composition` Female athlete in male relay team (parser_bug=false, source_limitation=false)
  CSV: (Jerica (Ak)) (Bernik) - normalized as leg2 runner in M18 class
  Raw: (Bernik), (Jerica (AK)) (0) - appears to be female name Jerica
  Why: While female athletes can appear in male teams when incomplete, the parentheses and formatting suggest this may be a placeholder or substitution that needs verification
  Next: Verify if this relay composition accurately reflects the raw source intent
- [low] `name` Name normalization concerns (parser_bug=false, source_limitation=true)
  CSV: Matij Klusacek vs Kaspar Hagler vs Bjorseth
  Raw: Klusácek, Matìj vs Hägler, Kaspar vs Bjørseth
  Why: Accent removal and diacritic handling appears inconsistent - some preserved, others removed
  Next: Review accent handling consistency in name normalization
- [low] `name` Unusual name formatting in SLO team (parser_bug=true, source_limitation=false)
  CSV: (Jerica (Ak)) (Bernik)
  Raw: (Bernik), (Jerica (AK)) (0)
  Why: Parentheses and formatting preserved in normalized name, which seems unusual for standard name normalization
  Next: Clean up parentheses and formatting artifacts in name normalization

### Notable Matches

- Team RUS 66 with correct total time 1:57:49 = 7069 seconds and proper leg splits
- Team GBR 33 with accurate individual leg times and runner names
- Team CZE 1 with proper time conversion and name order normalization
- MP status correctly assigned to SWE and SLO teams with MisPunch indicators
- Class normalization from 'M 17-18' to 'M18' follows expected pattern
- Most country codes properly normalized (RUS, GBR, CZE, etc.)
- Time conversions accurate across all completed teams

## 2006/2006_relay_w16.txt

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2006/relay.csv`
- Summary: CSV accurately represents the raw relay results with proper normalization applied

### Issues

- None reported.

### Notable Matches

- Class W 15-16 correctly normalized to W16
- Team CZE 1 with correct total time 1:18:03 = 4683 seconds and proper leg splits
- Names properly normalized from comma-separated format (Jakobová, Adéla) to Given Surname (Adela Jakobova)
- Accent removal applied consistently (Jakobová → Jakobova, Müllerová → Mullerova)
- Country SCG correctly normalized to SRB for Serbia
- All 18 teams present with correct rankings, times, and leg compositions
- Time conversions accurate (e.g., 0:25:16 = 1516 seconds)
- Team names preserved with numbers (Team CZE 1, Team RUS 67, etc.)

## 2006/2006_relay_w18.txt

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2006/relay.csv`
- Summary: CSV accurately represents the raw relay results with proper normalization applied

### Issues

- None reported.

### Notable Matches

- Class W 17-18 correctly normalized to W18
- Team NOR 52 with correct total time 1:35:15 (5715 seconds) and all three leg times match
- Names properly normalized: 'Bjørgul, Ida Marie N' -> 'Ida Marie N Bjorgul', 'LELOUP, Marine' -> 'Marine Leloup'
- Country ROM correctly normalized from Team ROM to ROU
- Country SCG correctly normalized to SRB for Serbia and Montenegro team
- MP status correctly assigned to teams with MisPunch or missing punches
- All 17 ranked teams (1-17) properly extracted with correct times and compositions
- Three disqualified teams (GBR, SCG, POR) correctly marked as MP with partial times where available

## 2006/eyoc2006.htm

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2006/long.csv`, `2006/sprint.csv`
- Summary: The CSV extraction accurately represents the raw source data with proper normalization applied. All individual results match the source with correct class normalization, time conversions, and country mappings.

### Issues

- None reported.

### Notable Matches

- W16E class correctly normalized to W16 (e.g., Jakobová, Adéla -> Adela Jakobova)
- Time format conversion accurate: '11:35,5' -> 695 seconds for sprint times
- Long distance times properly converted: '0:34:21' -> 2061 seconds
- Country normalization working: 'Czech Republic' entries -> CZE
- Name normalization handling accents: 'Jakobová' -> 'Jakobova', 'Müllerová' -> 'Mullerova'
- Status handling: MisPunch entries correctly excluded from clean CSV
- SCG (Serbia and Montenegro) correctly normalized to SRB for current Serbia entries
- Hungarian names with accents properly normalized: 'Őry, Eszter' -> 'Eszter Ory'
- Relay results intentionally excluded as this appears to be individual-only extraction
- All ranks, times, and athlete assignments match source data accurately

## 2007/eyoc2007.htm

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2007/long.csv`, `2007/relay.csv`, `2007/sprint.csv`
- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All individual and relay results match the source data with appropriate class, country, name, and time conversions.

### Issues

- None reported.

### Notable Matches

- Sprint W16: Mirjam Pfister (SUI) 12:52 → 772 seconds correctly converted
- Long M18: Jakub Zimmermann (CZE) 53:02 → 3182 seconds correctly converted
- Relay W16: CZE team with correct leg splits - Novotna 28:37, Kubatova 31:04, Indrakova 26:56
- Relay M18: Mixed gender team SLO correctly preserved - Zmrzlikar/Pahor/Pretnar with Tanja in leg 3
- Class normalization working properly: W16E → W16, M18E → M18, etc.
- Country normalization correct: Czech Republic → CZE, Great Britain → GBR
- MP and DSQ statuses properly handled in both individual and relay results
- Hungarian athletes correctly included with HUN country code
- Name normalization applied: SURNAME Given → Given Surname format

## 2008/eyoc2008.htm

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2008/long.csv`, `2008/relay.csv`, `2008/sprint.csv`
- Summary: The extracted CSV data accurately represents the raw source with proper normalization applied. All major data points match correctly.

### Issues

- [low] `name` Minor name variations in sprint results (parser_bug=false, source_limitation=true)
  CSV: Klingenberg (missing first name), Rafols (missing first name)
  Raw: Klingenberg, Ita (W16 rank 30), Pol Rafols (M18 rank 55)
  Why: Some names appear abbreviated in sprint results, likely due to space constraints in original formatting
  Next: Accept as source limitation - sprint results appear to have abbreviated some names

### Notable Matches

- Long distance results correctly extracted with proper time conversions (e.g., Emma Klingenberg 39:02 → 2342 seconds)
- Relay results properly parsed with correct leg splits and team compositions
- Sprint results accurately captured with proper time conversions (e.g., Tereza Novotna 11:01 → 661 seconds)
- Class normalization correctly applied (W16E → W16, M18E → M18, etc.)
- Country normalization properly handled (Czech Republic → CZE, Great Britain → GBR)
- Status codes correctly identified (OK, DNF, MP statuses properly assigned)
- Tied rankings properly handled (multiple athletes with same rank and time)
- Missing participants (mp, dnf) correctly excluded from individual results but preserved in relay results where appropriate

## 2009/eyoc2009.htm

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2009/long.csv`, `2009/relay.csv`, `2009/sprint.csv`
- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All major data points match correctly across sprint, long, and relay events.

### Issues

- None reported.

### Notable Matches

- Sprint W16: Sandrine Müller (SUI) 9:11 → 551 seconds correctly converted
- Long M18: Robert Merl (AUT) 1:00:25 → 3625 seconds correctly converted
- Relay W16: SUI team total 96:16 → 5776 seconds with correct leg splits
- Country normalization: 'Czech Rep.' → 'CZE', 'Great Britain' → 'GBR' applied consistently
- Class normalization: 'W16E' → 'W16', 'M18E' → 'M18' applied correctly
- MP/DNF statuses preserved correctly in relay results
- Hungarian athletes correctly included (HUN is allowlisted country)
- Name normalization: 'LUESCHER' → 'Luescher', accent handling applied appropriately

## 2010/eyoc2010.htm

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2010/long.csv`, `2010/relay.csv`, `2010/sprint.csv`
- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All major data points match correctly including names, times, countries, and rankings.

### Issues

- None reported.

### Notable Matches

- Sprint W16 winner: Sandrine Müller (SUI) 13:01 → 781 seconds correctly converted
- Long M16 winner: Piotr Parfianowicz (POL) 53:59 → 3239 seconds correctly converted
- Relay W16 winner: Switzerland team with correct leg times and total 1:29:40 → 5380 seconds
- Country normalization working correctly: GREAT BRITAIN → GBR, CZECH REPUBLIC → CZE
- Name normalization applied properly: MÜLLER, Sandrine → Sandrine Muller
- Tied rankings preserved correctly (e.g., W16 sprint rank 3 tie, W16 long rank 21 tie)
- Hungarian athletes correctly included in all events with HUN country code
- DNF status correctly captured in relay results for incomplete teams
- Mixed relay class M18 rank 21 shows female athlete Nicoline Friberg Klysner in male team, matching raw source

## 2011/eyoc2011.htm

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2011/long.csv`, `2011/relay.csv`, `2011/sprint.csv`
- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All major elements including names, times, countries, classes, and rankings match the source data.

### Issues

- None reported.

### Notable Matches

- Sprint W16: Sandrine Müller (SUI) 11.35,8 → 696 seconds correctly converted
- Long M18: Rudolfs Zernis (LAT) 54.59 → 3299 seconds correctly converted
- Relay W16: Czech Republic team with correct leg splits and total time 100.15 → 6015 seconds
- Class normalization: W16E → W16, M18E → M18 applied consistently
- Country normalization: Czech Republic → CZE, Great Britain → GBR applied correctly
- Name normalization: SURNAME Given format converted to Given Surname (e.g., Boránková Karolína)
- MP status entries correctly excluded from individual results but preserved in relay where applicable
- Hungarian athletes correctly included as HUN is in the allowlist
- Mixed relay teams with female athletes in male classes preserved as shown in source (e.g., Susen Lösch in M18 relay)

## 2012/eyoc2012.htm

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2012/long.csv`, `2012/relay.csv`, `2012/sprint.csv`
- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All major data points match correctly.

### Issues

- None reported.

### Notable Matches

- W16 sprint winner Angelika MACIEJEWSKA (POL) correctly shows 11:36 → 696 seconds
- M18 long winner Marek MINÁR (CZE) correctly shows 53:53 → 3233 seconds
- Relay W16 Czech Republic team correctly shows 1:32:28 total with proper leg splits
- Country normalization working correctly: 'Czech Republic' → 'CZE', 'Russian Federation' → 'RUS'
- Name normalization applied consistently: 'MACIEJEWSKA' → 'MacIejewska'
- MP/DNF statuses properly captured in relay results for incomplete teams
- Time conversions accurate throughout: sprint times like 11:36 → 696 seconds, long times like 37:23 → 2243 seconds
- Class normalization working: 'W16E' → 'W16', 'M18E' → 'M18'
- Relay leg assignments match source data with proper name and time extraction
- All major placings and rankings preserved from source to CSV

## 2013/eyoc2013.htm

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2013/long.csv`, `2013/relay.csv`, `2013/sprint.csv`
- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All major data points match correctly.

### Issues

- [low] `name` Potential name parsing issue for Netherlands athletes (parser_bug=true, source_limitation=false)
  CSV: Nina Roothans 96 The, Paul Roothans 95 The
  Raw: Nina Roothans 96 THE NETHERLANDS, Paul Roothans 95 THE NETHERLANDS
  Why: The country name 'THE NETHERLANDS' appears to be partially included in the athlete name field, showing as 'Nina Roothans 96 The' instead of just 'Nina Roothans'
  Next: Review name parsing logic for athletes from 'THE NETHERLANDS' to ensure country text is properly separated from names

### Notable Matches

- Class normalization correctly applied: 'W16E' -> 'W16', 'M18E' -> 'M18'
- Time conversions accurate: '12:27' -> 747 seconds, '46:26' -> 2786 seconds
- Country normalization working: 'GREAT BRITAIN' -> 'GBR', 'CZECH REPUBLIC' -> 'CZE'
- Hungarian athletes properly included with correct country code 'HUN'
- Relay team compositions match source data with correct leg assignments
- MP (mispunch) and DNS statuses correctly preserved in relay results
- Non-EYOC countries like Macedonia (MKD) properly included as they appear in raw source
- Name normalization applied: 'SWITZERLAND' athletes show as 'Simona Aebersold' etc.
- Rank ties properly handled: multiple athletes with same rank (e.g., rank 14 in W16 sprint)

## 2014/results-long.pdf

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2014/long.csv`
- Summary: The CSV data accurately represents the raw PDF source with proper normalization applied. All entries match the source data with expected class normalization, country code standardization, and time conversions.

### Issues

- None reported.

### Notable Matches

- M16 class correctly normalized from 'M16 (100)' header with proper rank ordering 1-86
- W16 class correctly normalized from 'W16 (94)' header with proper rank ordering 1-92
- M18 class correctly normalized from 'M18 (108)' header with proper rank ordering 1-104
- W18 class correctly normalized from 'W18 (101)' header with proper rank ordering 1-94
- Time conversions accurate: '45:43' -> 2743 seconds, '1:01:32' -> 3692 seconds
- Country normalization correct: 'CZE', 'SUI', 'FIN' preserved, 'Czech Republic' would normalize to 'CZE'
- Name normalization applied: 'Vojtěch Sýkora' -> 'Vojtech Sykora', accent removal as expected
- Tied ranks handled correctly: M16 rank 10 shows both Aidan Rigby and Fryderyk Pryjma
- Status handling: MP, DNF, DNS entries correctly excluded from ranked results as expected
- Non-EYOC countries like NOR and SWE correctly excluded from normalized CSV as per policy

## 2014/results-relay.pdf

- Verdict: `review`
- Confidence: `low`
- Related CSVs: `2014/relay.csv`
- Summary: Cannot perform meaningful audit due to missing raw source text from PDF. Several potential issues identified in CSV data including duplicate ranks, missing leg times, and unusual country formatting that require source verification.

### Issues

- [high] `source-limitation` Raw PDF text unavailable for comparison (parser_bug=false, source_limitation=true)
  CSV: 85 relay team entries across all classes
  Raw: [no raw text extracted]
  Why: Cannot verify CSV accuracy against source without readable raw text
  Next: Re-extract PDF text or obtain alternative source format for proper audit
- [medium] `rank` Duplicate and missing ranks in multiple classes (parser_bug=true, source_limitation=false)
  CSV: M16 has rank 6 twice (DEN and AUT), M18 has rank 6 twice (FRA and ITA), several teams missing ranks
  Raw: Cannot verify from source
  Why: Ranking inconsistencies suggest potential parsing errors
  Next: Verify ranking sequence against original PDF
- [medium] `time` Missing leg times in multiple entries (parser_bug=true, source_limitation=false)
  CSV: Examples: TUR W16 leg2 missing, EST M16 leg1 missing, LAT W18 leg3 missing
  Raw: Cannot verify from source
  Why: Missing times could indicate parsing issues or source data problems
  Next: Check if times are present in original PDF but not extracted
- [low] `country` Unusual country formatting (parser_bug=true, source_limitation=false)
  CSV: MDA shows as 'Moldova Moldova', IRL shows as 'lreland' (lowercase L)
  Raw: Cannot verify from source
  Why: Formatting suggests potential OCR or parsing artifacts
  Next: Verify country names in original PDF and normalize properly

### Notable Matches

- All entries use confidence=approx as expected for PDF source
- Class normalization appears consistent (W16, W18, M16, M18)
- Status values follow expected format (OK, MP, DNF, DSQ)
- Time conversions to seconds appear reasonable where present
- Source file attribution consistent throughout

## 2014/results-sprint.pdf

- Verdict: `fail`
- Confidence: `high`
- Related CSVs: `2014/sprint.csv`
- Summary: Missing winner Ricardo Esteves (POR) from M16 class and several other Portuguese athletes, plus systematic exclusion of Portuguese results

### Issues

- [high] `missing-row` Missing M16 winner Ricardo Esteves (parser_bug=true, source_limitation=false)
  CSV: CSV starts with rank 1 as Tuomas Heikkila (FIN)
  Raw: 1 39 Ricardo Esteves 98 PO 11:51 0:00
  Why: The actual winner of M16 class (Ricardo Esteves from Portugal) is completely missing from the CSV, causing all subsequent ranks to be shifted down by one position
  Next: Fix parser to include Portuguese (PO/POR) athletes - they appear to be systematically excluded
- [high] `missing-row` Missing Portuguese athletes across all classes (parser_bug=true, source_limitation=false)
  CSV: No Portuguese athletes found in any class
  Raw: Multiple PO entries: 98 Joăo Bernandino, 71 António Ferreira, 14 Joăo Casal, 169 Beatriz Sanguino, 217 Joăo Novo, 272 Daniel Catarino, 242 André Esteves, 281 Bernardo Pereira, 344 Beatriz Moreira, 366 Catarina Reis
  Why: All Portuguese (PO) athletes are systematically missing from the normalized CSV, suggesting the parser doesn't recognize 'PO' as a valid country code
  Next: Add 'PO' as an alias for Portugal (POR) in the country normalization logic
- [medium] `rank` Rank sequence errors due to missing winner (parser_bug=true, source_limitation=false)
  CSV: M16 ranks: 1 Tuomas Heikkila (FIN), 2 Vojtech Sykora (CZE), 3 Antonie Guenin (FRA)
  Raw: M16 ranks: 1 Ricardo Esteves (PO), 2 Tuomas Heikkilä (FIN), 3 Vojtěch Sýkora (CZE)
  Why: Due to missing Portuguese winner, all M16 ranks are shifted incorrectly - what should be rank 2 appears as rank 1, etc.
  Next: Fix Portuguese country recognition to restore correct ranking sequence
- [medium] `country` GE vs GER country code inconsistency (parser_bug=false, source_limitation=false)
  CSV: CSV shows 'GER' for same athletes: Veit Slodowski GER, Ole Hennseler GER
  Raw: Raw shows 'GE' for German athletes: 82 Veit Slodowski 98 GE, 35 Ole Hennseler 98 GE
  Why: Country normalization from 'GE' to 'GER' is correct but should be verified as intentional
  Next: Confirm 'GE' -> 'GER' normalization is working as intended

### Notable Matches

- Class normalization working correctly: M16, W16, M18, W18 classes properly identified
- Time conversion accurate: 11:51 -> 711 seconds, 12:21 -> 741 seconds
- Name normalization good: 'Vojtěch Sýkora' -> 'Vojtech Sykora', accent handling
- Status handling correct: 'mp' -> 'MP', 'dnf' -> 'DNF', 'dns' -> 'DNS'
- Most country normalizations working: CZE, FIN, SUI, POL, etc. correctly identified
- Rank ties handled properly: tied ranks 3-3, 12-12, 22-22 preserved correctly

## 2015/results-lf.pdf

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2015/long.csv`
- Summary: CSV data accurately matches the raw PDF source with proper normalization applied

### Issues

- None reported.

### Notable Matches

- M16 class correctly normalized from 'M16 (90)' header with proper time conversions (47:16 -> 2836 seconds)
- Country normalization working correctly: 'United Kingdom' -> 'GBR', 'Czech Republic' -> 'CZE'
- Name normalization applied appropriately: 'Malte Kjær Hemmingsen' -> 'Malte Kjaer Hemmingsen'
- Tied ranks handled correctly: M18 ranks 36 (Florian Kurz and Marton Zacher both at 59:20)
- Status codes properly extracted: 'ot' -> missing from CSV (expected), 'mp' -> missing from CSV (expected), 'dnf' -> missing from CSV (expected)
- All four classes (M16, M18, W16, W18) extracted with correct participant counts matching raw totals
- Time format conversion accurate throughout: '1:31:34' -> 5494 seconds for Eitam Nussbaum
- Special characters handled well: accented names like 'Kjær' normalized to 'Kjaer'

## 2015/results-relay.pdf

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2015/relay.csv`
- Summary: CSV data accurately matches the raw PDF source with proper normalization applied

### Issues

- None reported.

### Notable Matches

- M16 class correctly normalized from raw format, all 21 teams present with accurate times and leg splits
- M18 class complete with 27 teams including proper handling of MP (mispunch) teams excluded from CSV as expected
- W16 and W18 classes accurately extracted with correct time conversions and name normalization
- Country codes properly normalized (e.g., 'United Kingdom' -> 'GBR', 'Czech Republic' -> 'CZE')
- Time conversions accurate (e.g., '1:23:42' -> 5022 seconds, leg times like '30:36' -> 1836 seconds)
- Names properly normalized to title case and Given Surname format
- MP/DSQ teams correctly excluded from final CSV as they have incomplete data
- All leg runner names and times accurately matched between source and CSV

## 2015/results-sf.pdf

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2015/sprint.csv`
- Summary: The CSV data accurately represents the raw PDF source with proper normalization applied. All entries, ranks, times, countries, and statuses match the source data correctly.

### Issues

- None reported.

### Notable Matches

- M16 winner Nicola Muller (SUI) correctly shows 10:27 → 627 seconds with rank 1
- Tied ranks properly handled: M16 rank 18 shows both Yurii Serdiuk (UKR) and Georg Groll (AUT) at 11:46
- Country normalization working: 'Switzerland' → 'SUI', 'Czech Republic' → 'CZE', 'United Kingdom' → 'GBR'
- Class normalization applied correctly: source shows 'M16 (90)' → normalized to 'M16'
- Time conversion accurate: 12:01 → 721 seconds consistently across multiple tied athletes
- Status handling correct: 'mp' → 'MP', 'disq' → 'DSQ', 'dns' → 'DNS' for non-finishers
- Name formatting normalized: 'Malte Kjær Hemmingsen' → 'Malte Kjaer Hemmingsen' (accent removal)
- All 4 classes (M16, M18, W16, W18) properly extracted with correct participant counts matching source totals

## 2016/results-long.pdf

- Verdict: `fail`
- Confidence: `high`
- Related CSVs: `2016/long.csv`
- Summary: Multiple athletes incorrectly assigned times and ranks when they should have MISPUNCH, OVERTIME, or DISQ status

### Issues

- [high] `status` M16 DNF athletes incorrectly given finishing times (parser_bug=true, source_limitation=false)
  CSV: These athletes appear with ranks 81-85 and specific times like 6131, 6155 seconds
  Raw: GARRIDO CORRAL Miguel shows 'MISPUNCH', ALLMANN Hando shows 'MISPUNCH', etc.
  Why: Athletes with MISPUNCH/OVERTIME/DISQ status should not have finishing times or numerical ranks
  Next: Fix parser to correctly handle non-OK statuses and not assign times to MISPUNCH/OVERTIME/DISQ athletes
- [medium] `missing-row` Multiple MISPUNCH/OVERTIME athletes missing from CSV (parser_bug=true, source_limitation=false)
  CSV: These athletes are completely absent from the CSV
  Raw: Many athletes listed with MISPUNCH, OVERTIME, DISQ status in all classes
  Why: Non-finishing athletes should still appear in results with appropriate status codes
  Next: Include all athletes from raw results with correct status codes (MP, DNS, DNF, DSQ)
- [low] `time` Some time conversions may be incorrect for DNF entries (parser_bug=true, source_limitation=false)
  CSV: Converted to seconds like 6131, 6339
  Raw: Times like '102.11', '105.39' for athletes who should be MISPUNCH
  Why: These times should not exist for non-finishing athletes
  Next: Ensure time conversion only applies to athletes with OK status

### Notable Matches

- M16 winner POULSEN Malthe correctly shows 50.39 -> 3039 seconds
- W18 winner MORAWSKA Zuzanna correctly shows 50.26 -> 3026 seconds
- Country normalization correctly excludes Australia (AU) entries
- Class normalization correctly converts all class labels to M16/M18/W16/W18 format
- Most finishing times and ranks appear correctly converted from MM.SS format

## 2016/results-relay.pdf

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2016/relay.csv`
- Summary: The CSV data accurately represents the relay results from the 2016 PDF source with proper normalization applied

### Issues

- None reported.

### Notable Matches

- M16 class correctly normalized from source, with France winning in 117.09 (7029 seconds)
- All time conversions accurate: France leg times 38.23, 42.16, 36.30 → 2303, 2536, 2190 seconds
- Country normalization working: 'Russian Federation' → 'RUS', 'United Kingdom' → 'GBR'
- Name normalization applied: 'HABERKORN Guilhem' → 'Guilhem Haberkorn'
- DSQ teams properly excluded from CSV (Poland M16, Turkey W16, Romania W18, Slovakia W18, Spain W18)
- Mixed relay class absent from both source and CSV as expected
- All 4 classes (M16, M18, W16, W18) present with correct team counts and rankings
- Female athlete Grace Molloy correctly preserved in M16 team as shown in source

## 2016/results-sprint.pdf

- Verdict: `review`
- Confidence: `low`
- Related CSVs: `2016/sprint.csv`
- Summary: Cannot verify accuracy due to missing raw source text, but CSV shows concerning patterns including corrupted names, suspicious bib numbers, and potential OCR artifacts that need manual verification

### Issues

- [medium] `name` Multiple corrupted or incomplete names (parser_bug=true, source_limitation=true)
  CSV: Names like 'Spektorsfricis', 'Repsysadomas', 'Lorenztimon', 'Dzalbsedijs', 'Upitisuldis', 'Hirsotakar', 'Iinkfvichigor', 'Wolzaymeric', 'Szocsattila', 'Eerolalotta', 'Smulems de', 'Korvellorely', 'Georgievaniya', 'Myroniukalina', 'Gokculsumeyra', 'Leenukka Hanhijarvi', 'Indolalinda', 'Emilijaanna Stage'
  Raw: [no raw text available]
  Why: Many names appear corrupted, incomplete, or contain OCR artifacts that seem unlikely to be real names
  Next: Manual verification against original PDF to determine if these are OCR errors or parsing issues
- [medium] `other` Suspicious bib number (parser_bug=true, source_limitation=true)
  CSV: M18 row with bib '3481' for 'Iinkfvichigor' from RUS
  Raw: [no raw text available]
  Why: Bib number 3481 is unusually high compared to other bib numbers in 200-400 range, suggesting possible OCR error
  Next: Verify this bib number against the original PDF
- [low] `rank` Rank sequence anomaly in W18 (parser_bug=true, source_limitation=false)
  CSV: W18 shows rank 69, then 71, then 69 again: 'Lucia Matejickova' rank 69, 'Minati Alessandra' rank 71, 'Sandrine Defraigne' rank 69
  Raw: [no raw text available]
  Why: Duplicate rank 69 with rank 71 in between suggests possible parsing error or tie handling issue
  Next: Check original PDF for correct ranking sequence in W18 class
- [low] `source-limitation` All confidence marked as 'approx' (parser_bug=false, source_limitation=true)
  CSV: Every row has confidence=approx
  Raw: [no raw text available]
  Why: Consistent 'approx' confidence suggests OCR-derived data which explains name corruption issues
  Next: Accept as expected for OCR-derived results, but verify critical data points

### Notable Matches

- Class normalization appears correct (M16, M18, W16, W18)
- Country codes properly normalized to EYOC allowlist (FRA, CZE, FIN, RUS, GBR, etc.)
- Time conversion to seconds appears consistent
- Status values properly normalized (OK, DSQ)
- Ranking sequences generally follow expected patterns
- Source file attribution consistent throughout

## 2017/result-sprint.pdf

- Verdict: `review`
- Confidence: `high`
- Related CSVs: `2017/sprint.csv`
- Summary: Several significant issues found including incorrect time conversions, missing competitors, and potential data corruption

### Issues

- [high] `time` Incorrect time conversion for M16 rank 78 Timo Tantanini (parser_bug=true, source_limitation=false)
  CSV: M16,78,OK,0113,SUI,Timo Tantanini,1353,high
  Raw: 78. Timo Tantanini SUI0113 C Switzerland 17.05 + 4.23
  Why: Raw shows 17.05 (17 minutes 5 seconds = 1025 seconds) but CSV shows 1353 seconds (22 minutes 33 seconds)
  Next: Fix time conversion logic - 17.05 should be 1025 seconds, not 1353
- [high] `missing-row` Missing M16 competitors with times converted to status changes (parser_bug=true, source_limitation=false)
  CSV: M16,78,DNF,0219,POR,Vasco Amorim Ramos Mendes,,high, M16,80,DNF,0246,UKR,Teremetskyi Tymofii,,high
  Raw: 78. Vasco Amorim Ramos Mendes POR0219 C Portugal 17.05 + 4.23, 80. Teremetskyi Tymofii UKR0246 C Ukraine 17.10 + 4.28, etc.
  Why: Multiple competitors with valid times in raw source appear as DNF with no times in CSV
  Next: Review parser logic for handling times after rank 78 in M16 class
- [high] `time` Multiple M18 competitors missing times despite having them in raw (parser_bug=true, source_limitation=false)
  CSV: M18,81,DNF,9946,EST,Kiur Erik Eensaar,,high, M18,82,DNF,0044,ESP,Alvaro Casado Gomez,,high
  Raw: 81. Kiur Erik Eensaar EST9946 C Estonia 17.29 + 4.24, 82. Alvaro Casado Gomez ESP0044 C Spain 17.36 + 4.31, etc.
  Why: Raw source shows valid finishing times but CSV shows DNF status with no times
  Next: Fix parser to correctly extract times for M18 competitors after rank 80
- [medium] `missing-row` Guest nations excluded as expected (parser_bug=false, source_limitation=false)
  CSV: No corresponding rows found
  Raw: 34. Katie Cory-Wright NZL9989 C New Zealand 14.26 + 2.08, 56. Aston Key AUS0002 C Australia 16.01 + 2.56, 62. Danielle Goodall NZL9990 C New Zealand 15.48 + 3.30, 77. Jenna Tidswell NZL0091 C New Zealand 16.40 + 4.22
  Why: Non-EYOC countries (NZL, AUS) correctly excluded from normalized CSV per policy
  Next: No action needed - this is correct normalization behavior
- [low] `name` Minor name normalization differences (parser_bug=false, source_limitation=true)
  CSV: Morten Ornhagen Jorgensen, Szuromi Ron
  Raw: Morten Örnhagen Jorgensen, Szuromi Áron
  Why: Accent removal and possible OCR artifacts in name processing
  Next: Review name normalization for accent handling consistency

### Notable Matches

- M16 winner Piotr Rzenca correctly shows 12.42 → 762 seconds
- W16 winner Gardonyi Csilla correctly shows 12.01 → 721 seconds
- M18 winner Jakub Dekret correctly shows 13.05 → 785 seconds
- W18 winner Anu Tuomisto correctly shows 12.18 → 738 seconds
- Country normalization working correctly: Czech Republic → CZE, Great Britain → GBR
- MP status correctly preserved for non-finishers at end of each class
- Class normalization working: Men 16 → M16, Women 18 → W18

## 2017/results-long.pdf

- Verdict: `review`
- Confidence: `high`
- Related CSVs: `2017/long.csv`
- Summary: Several significant discrepancies found between raw source and CSV, including incorrect time conversions, missing entries, wrong status assignments, and name formatting issues

### Issues

- [high] `time` Incorrect time conversion for M16 rank 72 Peles Vlad (parser_bug=true, source_limitation=false)
  CSV: M16,72,OK,0130,ROU,Peles Vlad,4788,high
  Raw: 72. Peles Vlad ROU0130 C Romania 68.57 +22.30
  Why: Raw shows 68.57 (4137 seconds) but CSV shows 4788 seconds - significant discrepancy
  Next: Check time parsing logic for this entry
- [high] `time` Incorrect time conversion for W16 rank 78 Ghit Denisa (parser_bug=true, source_limitation=false)
  CSV: W16,78,OK,0183,ROU,Ghit Denisa,9255,high
  Raw: 78. Ghit Denisa ROU0183 C Romania 73.49 +35.24
  Why: Raw shows 73.49 (4429 seconds) but CSV shows 9255 seconds - major discrepancy
  Next: Check time parsing logic for this entry
- [medium] `missing-row` Missing entries with times in raw source (parser_bug=true, source_limitation=false)
  CSV: M16,81,DNF,0219,POR,Vasco Amorim Ramos Mendes,,high
  Raw: 81. Vasco Amorim Ramos Mendes POR0219 C Portugal 73.15 +26.48
  Why: Raw source shows time 73.15 but CSV marks as DNF with no time
  Next: Review status determination logic for entries with times
- [medium] `status` Multiple entries with times marked as DNF instead of OK (parser_bug=true, source_limitation=false)
  CSV: Various M16 entries marked DNF with empty time_seconds
  Raw: Multiple entries like ranks 82-98 in M16 show times but are marked DNF in CSV
  Why: Raw source shows actual finish times but CSV incorrectly assigns DNF status
  Next: Review status assignment logic for entries with valid times
- [medium] `name` Name truncation in CSV (parser_bug=true, source_limitation=false)
  CSV: M16,37,OK,0210,HUN,Szuromi Ron,3437,high
  Raw: 37. Szuromi Áron HUN0210 C Hungary 57.17 +10.50
  Why: Name appears truncated from 'Szuromi Áron' to 'Szuromi Ron'
  Next: Check name parsing for accent handling and truncation
- [medium] `missing-row` Missing MP entries in CSV (parser_bug=true, source_limitation=false)
  CSV: No corresponding entry found
  Raw: Timo Tantanini SUI0113 C Switzerland MP
  Why: Raw source shows MP (mispunch) entries that are missing from CSV
  Next: Include MP status entries in CSV output
- [low] `country` Guest nations correctly excluded (parser_bug=false, source_limitation=false)
  CSV: No entry for Australia
  Raw: 92. Jensen Key AUS0201 C Australia 87.03 +40.36
  Why: Australia is correctly excluded as non-EYOC nation per normalization rules
  Next: No action needed - correct exclusion

### Notable Matches

- M16 winner Becaert Antoine FRA correctly shows 46.27 → 2787 seconds
- W16 winner Gardonyi Csilla HUN correctly shows 38.25 → 2305 seconds
- Class normalization working correctly (M16, M18, W16, W18)
- Country normalization working (Russian Federation → RUS, Czech Republic → CZE)
- Most time conversions accurate (46.27 = 46:27 = 2787 seconds)
- Non-EYOC countries like Australia and New Zealand correctly excluded

## 2017/results-relay.pdf

- Verdict: `review`
- Confidence: `high`
- Related CSVs: `2017/relay.csv`
- Summary: Several significant issues found including missing NZL team, incorrect country codes, and potential name/time mismatches

### Issues

- [high] `missing-row` New Zealand team missing from W18 class (parser_bug=true, source_limitation=false)
  CSV: No NZL team found in W18 class CSV rows
  Raw: 14. NZL 1 New Zealand 128.08 - Danielle Goodall 42.46 (19) Jenna Tidswell 47.31 (20) Katie Cory-Wright 37.51 (7)
  Why: NZL team appears in raw source at rank 14 in W18 class but is completely missing from CSV
  Next: Check if NZL should be excluded per EYOC-COUNTRIES.md allowlist or if this is a parser error
- [medium] `country` Romania country code inconsistency (parser_bug=false, source_limitation=false)
  CSV: ROU (appears in CSV rows)
  Raw: ROM 1 (appears multiple times in raw source)
  Why: Raw source consistently shows 'ROM 1' but CSV uses 'ROU' - need to verify correct normalization
  Next: Verify if ROM->ROU normalization is correct per EYOC-COUNTRIES.md
- [medium] `name` Potential name corruption in M18 SLO team (parser_bug=true, source_limitation=false)
  CSV: Aan Ravnikar
  Raw: Äan Ravnikar
  Why: Special character 'Ä' appears to be converted to 'A' - may indicate encoding issue
  Next: Check character encoding handling for special characters
- [low] `name` Name normalization inconsistencies (parser_bug=false, source_limitation=false)
  CSV: van Lommel Jens, de Smul Ems
  Raw: Van Lommel Jens, De Smul Ems
  Why: Inconsistent capitalization of particles 'Van/van' and 'De/de'
  Next: Standardize particle capitalization rules
- [low] `other` Unranked teams with times in raw source (parser_bug=false, source_limitation=true)
  CSV: Both teams appear with empty rank field
  Raw: POR 1 Portugal 181.54, SRB 1 Serbia 198.34 (both appear without rank numbers)
  Why: Teams have completion times but no official ranking in source - CSV correctly reflects this
  Next: Verify this is correct interpretation of unranked but timed teams

### Notable Matches

- FRA teams correctly extracted across all classes with proper time conversions (91.23 -> 5483 seconds)
- DNF and MP statuses correctly identified and preserved
- Class normalization working properly (M16, M18, W16, W18)
- Leg times and total times correctly calculated and converted to seconds
- Most country normalizations appear correct (FRA, HUN, CZE, GER, etc.)
- Name order and title case normalization generally working well

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

## 2018/results-relay.pdf

- Verdict: `fail`
- Confidence: `high`
- Related CSVs: `2018/relay.csv`
- Summary: Multiple critical data extraction errors including corrupted names, incorrect time assignments, and missing athletes

### Issues

- [high] `name` Corrupted athlete names replaced with header text (parser_bug=true, source_limitation=false)
  CSV: All three replaced with '2018 Relay Mon 02-Jul-18 Eyoc' in CSV
  Raw: Matan Ivri (M16 Israel leg 3), Amir Zur (M18 Israel leg 3), Laura Fidalgo Casares (W16 Spain leg 3)
  Why: Parser appears to have replaced legitimate athlete names with document header text, creating completely incorrect data
  Next: Fix parser to correctly extract athlete names from leg 3 positions, especially when they span page breaks
- [high] `time` Incorrect time assignment for corrupted names (parser_bug=true, source_limitation=false)
  CSV: All assigned 1308 seconds (21:48) in CSV
  Raw: Matan Ivri: 30:40, Amir Zur: 32:54, Laura Fidalgo Casares: 31:48
  Why: The corrupted names are also assigned an incorrect time that appears to be derived from the document timestamp
  Next: Ensure correct time extraction for all leg positions, particularly when names are corrupted
- [medium] `missing-row` Australia team excluded from M18 results (parser_bug=false, source_limitation=false)
  CSV: No Australia entry in M18 class
  Raw: 21 169 Australia Australia 1:44:49 +20:05 with Aston Key, Angus Haines, Alastair George
  Why: Australia (AUS) is not in the EYOC countries allowlist, so exclusion is expected per normalization rules
  Next: No action needed - this is correct normalization behavior
- [medium] `missing-row` New Zealand team excluded from W18 results (parser_bug=false, source_limitation=false)
  CSV: No New Zealand entry in W18 class
  Raw: 14 66 New Zealand New Zealand 1:39:11 +15:23 with Jenna Tidswell, Marisol Hunter, Briana Steven
  Why: New Zealand (NZL) is not in the EYOC countries allowlist, so exclusion is expected per normalization rules
  Next: No action needed - this is correct normalization behavior
- [low] `country` Country name truncation in team field (parser_bug=false, source_limitation=true)
  CSV: Correctly normalized to RUS in country field but team field shows truncated version
  Raw: Russian Federati Russian Feder appears multiple times
  Why: Team field preserves source formatting while country field is properly normalized - this is acceptable
  Next: Consider whether team field should also be normalized or if source preservation is preferred

### Notable Matches

- M16 Czech Republic team correctly extracted with Jakub Chaloupsky (26:21), Lukas Vitebsky (28:14), Simon Marecek (26:45)
- W16 Switzerland team properly normalized with correct times: Mirjam Wuersten (24:38), Sanna Hotz (24:42), Alina Niggli (24:52)
- Class normalization working correctly: 'Men 16' → 'M16', 'Women 18' → 'W18'
- Country normalization functioning: 'Russian Federati' → 'RUS', 'Great Britain' → 'GBR'
- Time conversion accurate for most entries: '1:21:20' → 4880 seconds
- Mixed teams and MP/DNF statuses correctly excluded from final results
- Rank ordering preserved correctly across all classes

## 2018/results-sprint.pdf

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2018/sprint.csv`
- Summary: The CSV extraction accurately represents the raw PDF source with proper normalization applied. All competitors, times, ranks, and statuses match the source data. Guest nations (NZL, USA, AUS) are correctly excluded from the normalized CSV as expected.

### Issues

- None reported.

### Notable Matches

- M16 class correctly normalized from 'Men 16' with all 94 ranked competitors plus MP/DSQ statuses preserved
- M18 class shows 104 ranked competitors plus MP/DSQ entries, all times and ranks match source
- W16 and W18 classes properly extracted with correct time conversions (e.g., 10:18 → 618 seconds)
- Guest nations (nc entries for New Zealand, United States, Australia) correctly excluded from normalized CSV
- MP and DSQ statuses properly handled - MP competitors excluded, DSQ competitors excluded from ranked results
- Country normalization working correctly: 'Czech Republic' → 'CZE', 'Russian Federati' → 'RUS', 'Great Britain' → 'GBR'
- Name normalization preserves proper capitalization and handles compound names correctly
- Tied ranks properly preserved (e.g., multiple rank 13 in M16, rank 6 tie in M16)
- All time conversions accurate from MM:SS format to integer seconds

## 2019/Long-eventor.xml [M16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2019/long.csv`
- Classes: `M16`
- Summary: All 102 M16 entries from the XML source are correctly extracted and normalized in the CSV. Times, ranks, names, countries, and statuses all match accurately.

### Issues

- None reported.

### Notable Matches

- Martin Simsa (CZE) correctly extracted as rank 1 with 46:41 → 2801 seconds
- Jakub Chaloupsky (CZE) correctly extracted as rank 2 with 47:13 → 2833 seconds
- Country normalization working correctly: 'Czechia' → 'CZE', 'Russian Federation' → 'RUS'
- Name normalization working correctly: 'Urquizu Diego, Aimar' → 'Aimar Urquizu Diego'
- Time conversion accurate: '1:17:53' → 4673 seconds for DNF entries
- Status normalization correct: 'DidNotFinish' → 'DNF' for Joe Hudd and Jonas Jansen
- All 100 ranked finishers plus 2 DNF entries properly extracted
- Tied ranks handled correctly: both rank 45 entries (Kaloyan Atanasov and Topias Kemppi) with same time 1:08:35

## 2019/Long-eventor.xml [M18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2019/long.csv`
- Classes: `M18`
- Summary: All M18 class entries from the XML source are correctly extracted and normalized in the CSV, with proper handling of times, statuses, and country codes

### Issues

- None reported.

### Notable Matches

- Ferenc Jonas (HUN) correctly extracted as winner with 56:52 → 3412 seconds
- Tied ranks 11 and 33 properly preserved for Janovsky/Ojala and Kristiansson/Arbuzov
- MP status correctly extracted for Ondrej Metelka with time 1:15:59 → 4559 seconds
- DNF statuses properly extracted for Simon Frisk and Andrius Cereska with no times
- Country normalization working correctly: 'Czechia' → CZE, 'Russian Federation' → RUS
- Name order normalized from XML 'Family/Given' to 'Given Family' format
- All 106 entries from XML numberOfEntries attribute accounted for in CSV

## 2019/Long-eventor.xml [W16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2019/long.csv`
- Classes: `W16`
- Summary: CSV data accurately matches the raw XML source with proper normalization applied

### Issues

- None reported.

### Notable Matches

- Anna Karlova (CZE) correctly extracted as rank 1 with 39:44 → 2384 seconds
- Alina Niggli (SUI) correctly extracted as rank 2 with 40:54 → 2454 seconds
- Class 'Women 16' correctly normalized to 'W16'
- Country codes properly normalized (e.g., 'Czechia' → 'CZE', 'Russian Federation' → 'RUS')
- Names correctly normalized from XML format to 'Given Surname' order
- Time format MM:SS correctly converted to seconds (e.g., '39:44' → 2384)
- Mia Krtinic correctly marked as DNF with CompetitorStatus 'DidNotFinish'
- New Zealand competitors (NZL) with 'NotCompeting' status correctly excluded from normalized CSV as expected
- All 88 finishing competitors plus 1 DNF properly extracted, totaling 89 rows as expected

## 2019/Long-eventor.xml [W18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2019/long.csv`
- Classes: `W18`
- Summary: CSV data accurately matches the raw XML source with proper normalization applied

### Issues

- None reported.

### Notable Matches

- Winner Csilla Gardonyi (HUN, bib 184) correctly shows 47:44 → 2864 seconds
- Class normalization 'Women 18' → 'W18' applied correctly throughout
- Country normalization working: 'Russian Federation' → 'RUS', 'Great Britain' → 'GBR'
- Status normalization: 'MisPunch' → 'MP', 'DidNotFinish' → 'DNF' applied correctly
- Tied ranks handled properly: both rank 48 competitors (Tsyvilska and Laanejoe) with 1:12:04
- All 99 entries from XML properly represented in CSV (93 OK + 1 MP + 5 DNF)
- Time conversions accurate: '1:57:37' → 7057 seconds, '2:25:51' → 8751 seconds
- Names properly normalized to 'Given Surname' format from XML structure
- Missing finish time for Hilda Johansson (DNF) correctly shows empty time_seconds

## 2019/Sprint-eventor.xml [M16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2019/sprint.csv`
- Classes: `M16`
- Summary: CSV data accurately matches the raw XML source with proper normalization applied

### Issues

- None reported.

### Notable Matches

- Winner Konstantin Kunckel (GER, bib 591) correctly shows 8:57 → 537 seconds with rank 1
- Tied ranks handled correctly: Pascal Schaerer and Stepan Aleksandrov both at rank 2 with 9:06 → 546 seconds
- Class normalization applied correctly: 'Men 16' → 'M16'
- Country normalization working: 'Germany' → 'GER', 'Switzerland' → 'SUI', 'Russian Federation' → 'RUS'
- Name normalization applied: 'Bernabeu carbonell, Marcos' → 'Marcos Bernabeu Carbonell'
- Multi-part names preserved: 'Oscar David Brom Jensen', 'Marco Anselmo di Stefano'
- Status correctly mapped: 'MisPunch' → 'MP' for Berke Basoz (bib 579)
- All 101 entries from XML properly extracted to CSV (100 OK + 1 MP)
- Time conversions accurate: 8:57 → 537s, 9:06 → 546s, 14:31 → 871s
- Rank sequences preserved including ties at positions 2, 10, 14, 18, 25, 27, 35, 37, 41, 44, 49, 55, 59, 61, 66, 68, 74, 82, 85, 91

## 2019/Sprint-eventor.xml [M18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2019/sprint.csv`
- Classes: `M18`
- Summary: All 106 M18 competitors from the XML source are correctly represented in the CSV with accurate ranks, times, countries, and statuses

### Issues

- None reported.

### Notable Matches

- Winner Stanislaw Kurzyp (POL) correctly shows 11:37 → 697 seconds with rank 1
- Three-way tie at rank 11 (Janovsky, Barauskas, Elmblad) all showing 12:12 → 732 seconds
- Two-way tie at rank 69 (Deredos, Teremetskyi, Kittilsen) all showing 13:24 → 804 seconds
- MP status correctly applied to Ciglis and Pompura with MisPunch in XML
- DSQ status correctly applied to Bjork with Disqualified in XML
- Country normalization working: 'Czechia' → CZE, 'Russian Federation' → RUS, 'Turkiye' → TUR
- All 103 ranked finishers plus 3 non-finishers (2 MP, 1 DSQ) = 106 total entries match XML

## 2019/Sprint-eventor.xml [W16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2019/sprint.csv`
- Classes: `W16`
- Summary: CSV extraction correctly matches the raw XML source with proper normalization applied

### Issues

- None reported.

### Notable Matches

- Winner Marketa Mulickova (CZE, bib 38) correctly extracted with 9:05 → 545 seconds
- Tied 3rd place Anna Karlova and Viktoria Mag both show rank 3 as expected
- Country normalization working: 'Czech Republic' → 'CZE', 'Russian Federation' → 'RUS'
- Class normalization: 'Women 16' → 'W16' applied correctly
- Status handling: Yana Ilieva correctly marked as 'MP' (MisPunch) with no rank
- New Zealand competitors (NZL) correctly excluded as non-allowlisted guest nation
- Time conversion accurate: '9:05' → 545 seconds, '16:28' → 988 seconds
- Name normalization: 'Sigrid Hoeyer Staugaard' properly formatted
- All 88 ranked competitors plus 1 MP competitor correctly extracted from 92 total entries

## 2019/Sprint-eventor.xml [W18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2019/sprint.csv`
- Classes: `W18`
- Summary: All 98 W18 competitors from the XML source are correctly extracted and normalized in the CSV with accurate ranks, times, countries, and names

### Issues

- None reported.

### Notable Matches

- Winner Malin Agervig Kristiansson (DEN) correctly shows rank 1, time 11:12 = 672 seconds, bib 181
- Tied ranks handled correctly: positions 10-10 (Lahdenpera/Berglin), 27-27 (Gielec/Scheele), 36-36 (Weissova/Backlund), etc.
- Country normalization working: 'Denmark' -> 'DEN', 'Russian Federation' -> 'RUS', 'Great Britain' -> 'GBR'
- Name order normalized from XML format: 'Kristiansson, Malin Agervig' -> 'Malin Agervig Kristiansson'
- Time conversion accurate: XML '11:12' -> 672 seconds, '15:46' -> 946 seconds
- All 98 entries from numberOfEntries='98' in XML are present in CSV
- Class correctly normalized from 'Women 18' to 'W18'
- All competitors show status 'OK' and confidence 'high' as expected for clean XML data

## 2019/result-relay.pdf

- Verdict: `review`
- Confidence: `medium`
- Related CSVs: `2019/relay.csv`
- Summary: The CSV extraction appears largely accurate but has several issues requiring review: missing teams with MP status, a potential name normalization error, and exclusion of non-EYOC guest nations

### Issues

- [medium] `missing-row` Missing MP status teams from CSV (parser_bug=true, source_limitation=false)
  CSV: These teams are completely absent from the CSV
  Raw: Teams 324 Moldova (W16), 322 Serbia (W16), 207 Spain (M16), 121 Turkey (W18), 112 Romania (W18), 12 Great Britain (M18), 28 Serbia (M18), 23 Spain (M18) all show 'mp' status
  Why: Teams with MP status should be included in normalized results with status=MP, not excluded entirely
  Next: Include MP status teams in CSV with appropriate status field
- [low] `name` Potential name normalization inconsistency (parser_bug=false, source_limitation=false)
  CSV: Marco Anselmo di Stefano
  Raw: Marco Anselmo Di Stefano (M16 Italy leg 1)
  Why: Capitalization of 'Di' vs 'di' - minor but worth checking normalization consistency
  Next: Verify name capitalization normalization rules are consistently applied
- [low] `missing-row` New Zealand team excluded from CSV (parser_bug=false, source_limitation=false)
  CSV: New Zealand team is absent from CSV
  Raw: 323 New Zealand team appears in W16 results with rank 23 and complete times
  Why: Expected exclusion as NZL is not in EYOC-COUNTRIES allowlist, but worth confirming this is intentional
  Next: Confirm New Zealand exclusion is correct per EYOC country policy
- [low] `missing-row` Mixed relay teams with MP status missing (parser_bug=true, source_limitation=false)
  CSV: These Mixed teams are absent from CSV
  Raw: Teams 420, 417, 410, 411 in MIX class show 'mp' status with partial results
  Why: Mixed relay MP teams should likely be included with status=MP
  Next: Include Mixed MP teams in CSV if Mixed class is supported

### Notable Matches

- W16 Finland team correctly extracted with all leg times: Fanny Kukonlehto (33:46), Eeva Liina Ojanaho (35:45), Salla Isoherranen (35:43)
- M18 tied ranks handled correctly: Belgium and Estonia both show rank 14 with identical total times
- Country normalization working: 'Russian Federation' → 'RUS', 'Moldova, Republic of' → 'MDA'
- Time conversion accurate: 1:45:14 → 6314 seconds for W16 Finland
- Mixed relay class properly extracted with 8 complete teams
- Complex names preserved: 'Anika Schwarze Chintapatla', 'Malin Agervig Kristiansson'

## 2021/Long-eventor.xml [M16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2021/long.csv`
- Classes: `M16`
- Summary: CSV data accurately matches the raw XML source with proper normalization applied

### Issues

- None reported.

### Notable Matches

- Class 'Men 16' correctly normalized to 'M16'
- Names properly normalized: 'De Clercq Rune' → 'Clercq Rune de', 'Vītoliņš Audris Odo' → 'Audris Odo Vitolins'
- Countries correctly normalized: 'Czechia' → 'CZE', 'Denmark' → 'DEN', 'Switzerland' → 'SUI'
- Times properly converted: '39:59' → 2399 seconds, '40:10' → 2410 seconds
- Tied ranks handled correctly: positions 42 and 59 both show tied competitors
- DSQ status entries correctly included without times or ranks
- All 95 entries from XML properly represented in CSV (89 OK + 6 DSQ)

## 2021/Long-eventor.xml [M18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2021/long.csv`
- Classes: `M18`
- Summary: CSV extraction accurately represents the XML source data with proper normalization applied

### Issues

- None reported.

### Notable Matches

- Class normalization: 'Men 18' → 'M18' correctly applied
- Country normalization: 'Russian Federation' → 'RUS', 'Czechia' → 'CZE' properly handled
- Time conversion: '45:23' → 2723 seconds (45*60+23) correctly calculated
- Name normalization: 'Dementavičius' → 'Dementavicius' accent removal applied consistently
- Status handling: 'Disqualified' → 'DSQ' properly normalized
- Rank sequence: All 101 finishers plus 3 DSQ entries match XML order exactly
- Special names: 'Di' surname with complex given name 'Stefano Marco Anselmo' handled correctly
- Multi-word names: 'Martin Vehus Skjerve', 'Jonas Damm Als' preserved properly

## 2021/Long-eventor.xml [W16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2021/long.csv`
- Classes: `W16`
- Summary: The CSV extraction accurately represents the W16 class results from the 2021 Long XML source. All 88 competitors are correctly captured with proper normalization of class names, countries, times, and statuses.

### Issues

- None reported.

### Notable Matches

- Silva Kemppi (FIN) correctly extracted as rank 1 with 35:25 → 2125 seconds
- Class normalization 'Women 16' → 'W16' applied correctly throughout
- Country normalization working properly: 'Czechia' → 'CZE', 'Russian Federation' → 'RUS'
- Time conversion accurate: '1:45:49' → 6349 seconds for Emili Aleksandrova
- DSQ status correctly captured for Laura Odor with empty time
- Tied ranks handled properly: Daria Mikula and Giulia Gobber both at rank 41
- Complex names preserved: 'Sanjaume Guinedell Faja', 'Hornbaek Laura Kaldahl'
- All 87 finishers plus 1 DSQ = 88 total entries match source numberOfEntries

## 2021/Long-eventor.xml [W18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2021/long.csv`
- Classes: `W18`
- Summary: The CSV extraction accurately represents the W18 class results from the 2021 Long-eventor.xml source file. All 89 entries are correctly processed with proper normalization of class names, country codes, names, times, and statuses.

### Issues

- None reported.

### Notable Matches

- Class normalization: 'Women 18' correctly normalized to 'W18'
- Country normalization: 'Czechia' -> 'CZE', 'Russian Federation' -> 'RUS', 'Great Britain' -> 'GBR'
- Time conversion: '42:32' -> 2552 seconds, '1:00:25' -> 3625 seconds correctly calculated
- Name normalization: 'Skučaitė, Ugnė' -> 'Ugne Skucaite' with proper accent handling
- Status handling: 'Disqualified' -> 'DSQ' for Trepacova and Zavjalova with no time values
- All 87 ranked finishers plus 2 DSQ entries properly extracted and ordered
- Special characters handled: 'Jaunmuktāne' -> 'Jaunmuktane', 'Dementavičiūtė' -> 'Dementaviciute'
- Complex names preserved: 'Elisa Gotsch Iversen', 'Pina Liselotte Mauch', 'Iris Aurora Pecorari'

## 2021/Sprint-eventor.xml [M16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2021/sprint.csv`
- Classes: `M16`
- Summary: CSV data accurately matches the XML source with proper normalization applied

### Issues

- None reported.

### Notable Matches

- Jan Strycek (CZE) correctly extracted as rank 1 with 12:55 → 775 seconds
- Class normalization 'Men 16' → 'M16' applied correctly
- Country normalization working: 'Czech Republic' → 'CZE', 'Denmark' → 'DEN'
- Tied ranks handled properly: rank 13 for both Jorn Kennis and Marton Csoboth
- Name normalization applied: 'De Clercq Rune' → 'Clercq Rune de', 'Lopez Gonzalez Nicolas' → 'Gonzalez Nicolas Lopez'
- DSQ status correctly extracted for 6 competitors with no finish times
- All 95 entries from XML properly represented in CSV (89 OK + 6 DSQ)

## 2021/Sprint-eventor.xml [M18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2021/sprint.csv`
- Classes: `M18`
- Summary: The CSV accurately represents the M18 class results from the 2021 Sprint XML source. All 104 entries are correctly extracted with proper normalization of class names, countries, times, and statuses.

### Issues

- None reported.

### Notable Matches

- Winner Konrad Stamer (GER) correctly shows rank 1, time 12:53 → 773 seconds
- Tied ranks properly handled: positions 5, 11, 18, 21, 25, 28, 32, 34, 36, 41, 48, 61, 70, 73
- Class normalization: 'Men 18' → 'M18' applied correctly
- Country normalization: 'Germany' → 'GER', 'Norway' → 'NOR', etc. all correct
- Status handling: 'OK', 'Disqualified' → 'DSQ', 'DidNotStart' → 'DNS' properly converted
- Time conversion: '12:53' → 773 seconds, '21:25' → 1285 seconds calculated correctly
- All 94 finishers plus 10 non-finishers (6 DSQ, 1 DNS) = 104 total entries match source
- Names properly normalized: 'Vallet Mathias Barros', 'Martin Vehus Skjerve' maintain correct order

## 2021/Sprint-eventor.xml [W16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2021/sprint.csv`
- Classes: `W16`
- Summary: CSV extraction accurately represents the W16 class results from the 2021 Sprint XML source with proper normalization

### Issues

- None reported.

### Notable Matches

- Rita Maramarosi (HUN) correctly extracted as rank 1 with 12:11 → 731 seconds
- Silva Kemppi (FIN) correctly extracted as rank 2 with 12:43 → 763 seconds
- Tied ranks properly handled: Lili Lantai and Migle Cincikaite both at rank 20 with 14:37 → 877 seconds
- Class normalization correct: 'Women 16' → 'W16'
- Country normalization correct: 'Czechia' → 'CZE', 'Russian Federation' → 'RUS', 'Turkiye' → 'TUR'
- Name order normalization applied: 'de MIguel Armisen Monica' → 'Miguel Armisen Monica de'
- DSQ status correctly extracted for 6 competitors with no finish times
- All 88 entries from source properly represented in CSV (82 OK + 6 DSQ)

## 2021/Sprint-eventor.xml [W18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2021/sprint.csv`
- Classes: `W18`
- Summary: All CSV rows accurately match the raw XML source data with proper normalization applied

### Issues

- None reported.

### Notable Matches

- Winner Viktoria Mag (HUN) correctly shows 13:46 → 826 seconds with rank 1
- Tied ranks at position 23 correctly preserved for Niklasson, Zempleni, and Gladilkina (all 15:31 → 931 seconds)
- Tied ranks at position 34 correctly preserved for Caspari and Beskhmelnova (both 16:04 → 964 seconds)
- All 7 DSQ entries correctly extracted without times, matching XML CompetitorStatus='Disqualified'
- Country normalization working correctly: 'Great Britain' → 'GBR' for McCauley
- Class normalization applied: XML 'Women 18' → CSV 'W18'
- Name order normalized: XML 'Riis Madsen Ida' → CSV 'Madsen Ida Riis'
- Time conversion accurate: XML '13:46' → CSV 826 seconds (13*60+46)
- All 89 entries from XML numberOfEntries properly represented in CSV

## 2021/results-relay.pdf

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2021/relay.csv`
- Summary: The CSV data accurately represents the relay results from the 2021 PDF source. All teams, times, and placements match the raw source after proper normalization.

### Issues

- None reported.

### Notable Matches

- M18 Norway team correctly shows Alfred Bjoerneroed (33:26), Brage Takle (35:19), Martin Vehus Skjerve (33:50) with total 1:42:35
- W18 Sweden team properly normalized to Elsa Sonesson (31:08), Ida Bengtsson (30:57), Hanna Jonsell (33:01) with total 1:35:06
- M16 Denmark team accurately shows Casper Blakskjaer (31:04), Niels Dalgaard (31:54), Hannes Mogensen (27:38) with total 1:30:36
- W16 Finland team correctly represents Virna Pellikka (25:22), Elli Punto (24:01), Silva Kemppi (27:26) with total 1:16:49
- All time conversions from MM:SS format to seconds are accurate (e.g., 1:42:35 = 6155 seconds)
- Country normalization is correct (e.g., Czech Republic → CZE, Great Britain would be → GBR)
- Name normalization properly handles cases like 'Clercq Rune De' → 'Clercq Rune de' and 'Brien Daire O' → 'Brien Daire O'
- Teams with DSQ/DNS/active status are appropriately excluded from the clean CSV as expected
- All relay compositions match the raw source, including mixed-gender teams where they appear in the source

## 2022/Long-eventor.xml [M16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2022/long.csv`
- Classes: `M16`
- Summary: The CSV accurately represents the M16 class results from the 2022 Long XML source. All 97 entries are correctly extracted with proper normalization of class names, countries, times, and statuses.

### Issues

- None reported.

### Notable Matches

- Winner Matthieu Buehrer (SUI) correctly shows 49:22 → 2962 seconds with rank 1
- Tied 20th place correctly shows both Ondrej Brosch and Loic Berger with identical 1:02:23 times
- MP (MisPunch) status correctly applied to 5 competitors including Rasmus Toyryla and others
- DNF status correctly applied to Jedrzej Pachnik with partial time of 49:00 → 2940 seconds
- Country normalization working properly: 'Turkiye' → 'TUR', 'Moldova, Republic of' → 'MDA'
- Name normalization correctly handles compound surnames like 'Amat Font', 'Selva Torras', 'Fenger Groen'
- All 91 ranked finishers plus 6 non-finishers (5 MP + 1 DNF) properly accounted for

## 2022/Long-eventor.xml [M18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2022/long.csv`
- Classes: `M18`
- Summary: CSV data accurately matches the XML source with proper normalization applied

### Issues

- None reported.

### Notable Matches

- Winner Tadas Dementavicius (LTU) correctly shows 57:38 → 3458 seconds
- Three-way tie at rank 41 properly preserved for Bertozzi, Strycek, and Toczik
- Two-way ties at ranks 47 and 52 correctly maintained
- MP (MisPunch) status correctly normalized for Siegert and Popovic
- DNF status properly handled for Bourgeois with empty time
- Guest nations AUS, NZL, CAN correctly excluded from normalized CSV
- Country codes properly normalized: Czechia→CZE, Turkiye→TUR, etc.
- Names normalized to Given Surname format: 'Lehmann Romoren, Philip' → 'Philip Lehmann Romoren'
- All 109 starters accounted for: 103 finished + 2 MP + 2 DNF + 2 guest exclusions = 107 CSV rows

## 2022/Long-eventor.xml [W16]

- Verdict: `review`
- Confidence: `medium`
- Related CSVs: `2022/long.csv`
- Classes: `W16`
- Summary: Several guest nations (NZL, AUS) appear in raw source but are correctly excluded from CSV per normalization rules. However, there are potential issues with sex field mismatches and name formatting that need review.

### Issues

- [medium] `source-limitation` Sex field shows 'M' for all W16 competitors (parser_bug=false, source_limitation=true)
  CSV: All entries correctly appear in W16 class
  Raw: All PersonResult entries show <Person sex="M"> despite being in W16 class
  Why: Raw XML shows sex='M' for all competitors in W16 class, which appears to be a source data error rather than parser issue
  Next: Verify this is a known source limitation in the XML data format
- [low] `name` Name normalization variations (parser_bug=false, source_limitation=false)
  CSV: Normalized to 'Monica de Miguel Armisen', 'Guinedell Faja Sanjaume'
  Raw: Names like 'de MIguel Armisen' (with capital I), 'Faja sanjaume' (lowercase s)
  Why: Parser correctly normalizes case inconsistencies in raw source names
  Next: No action needed - proper normalization
- [low] `country` Guest nations correctly excluded (parser_bug=false, source_limitation=false)
  CSV: These competitors do not appear in CSV
  Raw: Rachel Baker (NZL), Anna Babington (NZL), Erika Enderby (AUS), Milla Key (AUS) appear in raw
  Why: Non-EYOC allowlisted countries are intentionally excluded per normalization rules
  Next: No action needed - correct exclusion per policy

### Notable Matches

- Katerina Douskova (CZE) rank 1 with 54:27 (3267 seconds) matches perfectly
- Viktorie Skachova (CZE) rank 2 with 54:33 (3273 seconds) matches perfectly
- Time conversions accurate: 1:00:06 → 3606 seconds, 1:35:26 → 5726 seconds
- Status mappings correct: 'MisPunch' → 'MP', 'DidNotFinish' → 'DNF', 'DidNotStart' → 'DNS'
- Country normalizations proper: 'Czechia' → 'CZE', 'Great Britain' → 'GBR', 'Turkiye' → 'TUR'
- All 96 entries from raw source properly processed with 4 guest nation exclusions = 92 CSV rows

## 2022/Long-eventor.xml [W18]

- Verdict: `review`
- Confidence: `high`
- Related CSVs: `2022/long.csv`
- Classes: `W18`
- Summary: Several non-EYOC countries appear in CSV that should be excluded per normalization rules

### Issues

- [high] `country` New Zealand athletes included despite non-allowlisted status (parser_bug=false, source_limitation=false)
  CSV: No NZL entries found in CSV
  Raw: Multiple NZL athletes: Stewart (bib 361), Hayes (bib 317), Babington (bib 342), Joergensen (bib 386)
  Why: NZL is not in the EYOC allowlist and should be excluded from normalized CSV, but appears to be correctly excluded
  Next: Verify this is actually correct - NZL should be excluded
- [high] `country` Australia athlete included despite non-allowlisted status (parser_bug=false, source_limitation=false)
  CSV: No AUS entries found in CSV
  Raw: Enderby, Mikayla from AUS (bib 325) with time 1:43:52
  Why: AUS is not in the EYOC allowlist and should be excluded from normalized CSV, appears correctly excluded
  Next: Verify this is correct - AUS should be excluded
- [medium] `missing-row` Several athletes from raw source missing from CSV (parser_bug=false, source_limitation=false)
  CSV: CSV shows 90 entries (87 OK + 3 MP)
  Raw: Raw shows 95 entries total, including NZL and AUS athletes
  Why: Missing entries likely due to intentional exclusion of non-allowlisted countries NZL and AUS
  Next: Confirm that exactly 5 non-EYOC athletes (4 NZL + 1 AUS) were correctly excluded
- [low] `name` Minor name variations in normalization (parser_bug=false, source_limitation=false)
  CSV: CSV shows 'Tille de Smul', 'Ingeborg Roll Mosland'
  Raw: Raw shows 'De Smul' (bib 379), 'Roll Mosland' (bib 371)
  Why: Name formatting appears consistent with normalization rules for title case and given/surname order
  Next: No action needed - normal name normalization

### Notable Matches

- Winner Alma Svennerud (SWE, 56:45 = 3405s) correctly ranked 1st
- Tied 17th place correctly handled: Tille de Smul (BEL) and Alice Merat (FRA) both 4028s
- Tied 59th place correctly handled: Theresa Skouboe (DEN) and Lana Mohoric (SLO) both 4967s
- MP (MisPunch) status correctly converted for 3 athletes: Kaso, Sebjornsen, Aigmueller
- Time conversions accurate: 1:43:52 → 6232s for various athletes
- Country normalization working: Turkiye → TUR, Czechia → CZE

## 2022/Sprint-eventor.xml [M16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2022/sprint.csv`
- Classes: `M16`
- Summary: The CSV data accurately represents the M16 class results from the 2022 Sprint XML source. All 98 entries are correctly extracted with proper normalization of class names, countries, times, and statuses.

### Issues

- None reported.

### Notable Matches

- Winner Marton Csoboth (HUN) correctly shows 13:11 → 791 seconds with rank 1
- Tied ranks 18, 20, 29, 34, 39, 42, 44, 50, 57, 59, 69 are properly preserved from source
- Status normalization: 'MisPunch' → 'MP', 'DidNotStart' → 'DNS' correctly applied
- Country normalization working: 'Czechia' → 'CZE', 'Great Britain' → 'GBR', 'Turkiye' → 'TUR'
- Time conversion accurate: '13:11' → 791 seconds, '24:29' → 1469 seconds
- All 92 ranked finishers plus 5 MP and 1 DNS properly categorized
- Names normalized to Given Surname format: 'Csoboth, Marton' → 'Marton Csoboth'

## 2022/Sprint-eventor.xml [M18]

- Verdict: `review`
- Confidence: `high`
- Related CSVs: `2022/sprint.csv`
- Classes: `M18`
- Summary: CSV correctly excludes non-EYOC guest nations (AUS, NZL, CAN) but includes all EYOC-allowlisted countries. All times, ranks, and statuses match the XML source accurately.

### Issues

- [low] `missing-row` Guest nations excluded from CSV as expected (parser_bug=false, source_limitation=false)
  CSV: These competitors do not appear in the CSV
  Raw: Sam Woolford (AUS), Felix Hunt (NZL), Toby Cazzolato (AUS), Alec Le Helloco (CAN) appear in XML with OK status
  Why: This is expected behavior - non-EYOC guest nations are intentionally excluded from normalized CSVs
  Next: No action needed - this is correct normalization behavior

### Notable Matches

- Gonzalo Ferrando (ESP) rank 1, 15:25 → 925 seconds correctly converted
- Marco Anselmo Di Stefano name properly normalized with title case
- Multiple tied ranks (10th place tie, 31st place tie) preserved correctly
- MP (MisPunch) status correctly normalized from 'MisPunch' in XML
- DSQ status correctly normalized from 'Disqualified' in XML
- DNS status correctly normalized from 'DidNotStart' in XML
- All EYOC-allowlisted countries (ESP, FRA, NOR, LTU, SWE, etc.) properly included
- Time format 15:25 correctly converted to 925 seconds throughout

## 2022/Sprint-eventor.xml [W16]

- Verdict: `review`
- Confidence: `medium`
- Related CSVs: `2022/sprint.csv`
- Classes: `W16`
- Summary: Several guest nations (AUS, NZL) appear in raw source but are correctly excluded from CSV per normalization rules. However, there are some potential issues with name formatting and missing entries that need review.

### Issues

- [low] `missing-row` Australia competitors excluded from CSV (parser_bug=false, source_limitation=false)
  CSV: No AUS entries in CSV
  Raw: Key Mila (AUS, bib 701, rank 16) and Erika Enderby (AUS, bib 704, rank 27) appear in raw XML
  Why: Guest nations like AUS are intentionally excluded per normalization rules, but flagging for confirmation
  Next: Confirm AUS is not in EYOC-COUNTRIES.md allowlist
- [low] `missing-row` New Zealand competitors excluded from CSV (parser_bug=false, source_limitation=false)
  CSV: No NZL entries in CSV
  Raw: Anna Babington (NZL, bib 730, rank 43) and Rachel Baker (NZL, bib 748, rank 50) appear in raw XML
  Why: Guest nations like NZL are intentionally excluded per normalization rules, but flagging for confirmation
  Next: Confirm NZL is not in EYOC-COUNTRIES.md allowlist
- [low] `name` Compound surname formatting inconsistency (parser_bug=false, source_limitation=false)
  CSV: Guinedell Faja Sanjaume in CSV
  Raw: Faja sanjaume -> Guinedell in raw XML
  Why: Raw shows family name as 'Faja sanjaume' but CSV shows 'Guinedell Faja Sanjaume' - may be correct normalization but worth verifying
  Next: Verify name normalization logic for compound surnames
- [low] `name` Name capitalization in compound surname (parser_bug=false, source_limitation=false)
  CSV: Monica de Miguel Armise in CSV
  Raw: de Miguel Armise -> Monica in raw XML
  Why: Raw shows family name as 'de Miguel Armise' which appears correctly normalized in CSV
  Next: Verify this is correct title case normalization

### Notable Matches

- Janka Mikes (HUN, rank 1, 13:06 = 786 seconds) correctly extracted
- Katerina Douskova (CZE, rank 2, 14:02 = 842 seconds) correctly extracted
- All MP (MisPunch) statuses correctly converted from 'MisPunch' to 'MP'
- DNS status correctly extracted for Julia Biskupska
- Time conversions accurate: 13:06 -> 786 seconds, 14:02 -> 842 seconds
- Country normalization working: Czechia -> CZE, Turkiye -> TUR
- Tied ranks handled correctly (rank 9, 19, 24, etc.)
- All 91 finishers plus 4 MP + 1 DNS = 96 total entries match raw source count

## 2022/Sprint-eventor.xml [W18]

- Verdict: `review`
- Confidence: `medium`
- Related CSVs: `2022/sprint.csv`
- Classes: `W18`
- Summary: CSV correctly excludes non-allowlisted guest nations (NZL, AUS) but includes some competitors that appear to be missing from the normalized output

### Issues

- [medium] `missing-row` Missing New Zealand competitors from CSV (parser_bug=false, source_limitation=false)
  CSV: No NZL entries present in CSV
  Raw: Zara Stewart (NZL, bib 395, rank 46), Kaia Joergensen (NZL, bib 303, rank 57), Katherine Babington (NZL, bib 344, MP), Emily Hayes (NZL, bib 368, DNF)
  Why: Four NZL competitors appear in raw XML but are absent from CSV. This is expected behavior per normalization rules since NZL is not in the EYOC allowlist, but should be confirmed as intentional exclusion rather than parser error
  Next: Confirm this is intentional exclusion of non-allowlisted guest nation NZL
- [medium] `missing-row` Missing Australia competitor from CSV (parser_bug=false, source_limitation=false)
  CSV: No AUS entries present in CSV
  Raw: Mikayla Enderby (AUS, bib 317, rank 85)
  Why: One AUS competitor appears in raw XML but is absent from CSV. This is expected behavior per normalization rules since AUS is not in the EYOC allowlist, but should be confirmed as intentional exclusion rather than parser error
  Next: Confirm this is intentional exclusion of non-allowlisted guest nation AUS
- [low] `other` Rank sequence gap in CSV (parser_bug=false, source_limitation=false)
  CSV: CSV shows ranks 1-87 with gap after rank 17 (jumps to 20)
  Raw: Raw shows ranks 1-90 with some ties
  Why: The CSV rank sequence has a gap, but this appears to be due to the intentional exclusion of guest nations that held ranks 18-19 in the original results
  Next: Verify that rank gaps are due to excluded guest nations rather than missing data

### Notable Matches

- Rita Maramarosi (HUN) correctly placed 1st with 13:17 (797 seconds)
- Michaela Novotna (CZE) correctly placed 2nd with 14:03 (843 seconds)
- Country normalization working correctly: Czechia -> CZE, Turkiye -> TUR
- Status normalization working: MisPunch -> MP, DidNotFinish -> DNF
- Time conversion accurate: 13:17 -> 797 seconds, 14:03 -> 843 seconds
- Names properly normalized to Given Surname format
- All EYOC-allowlisted countries properly included and normalized

## 2022/result-relay.pdf

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2022/relay.csv`
- Summary: The CSV accurately represents the relay results from the 2022 PDF source. All ranked teams are correctly extracted with proper normalization of class names, country codes, and time conversions.

### Issues

- None reported.

### Notable Matches

- W16 class correctly normalized from source, all 20 ranked teams present
- W18 class correctly normalized, all 21 ranked teams present including TUR team
- M16 class correctly normalized, all 20 ranked teams present
- M18 class correctly normalized, all 24 ranked teams present
- Country codes properly normalized: 'Czechia' -> 'CZE', 'Great Britain' -> 'GBR', 'Turkiye' -> 'TUR'
- Time conversions accurate: '1:21:25' -> 4885 seconds, leg times match source
- Names properly normalized: 'Guinedell Faja sanjaume' -> 'Guinedell Faja Sanjaume'
- Non-EYOC countries (AUS, NZL, CAN) correctly excluded from CSV as expected
- Mispunched and DNF teams correctly excluded from ranked results
- Female athletes in male relay teams preserved where shown in source (e.g., Zdenka Petra Stambuk in M18 CRO team)

## 2023/Long-eventor.xml [M16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2023/long.csv`
- Classes: `M16`
- Summary: The CSV data accurately represents the M16 class results from the XML source with proper normalization applied

### Issues

- None reported.

### Notable Matches

- Winner Aapo Virkajarvi (FIN) correctly shows 46:58 → 2818 seconds with rank 1
- Class normalization 'Men 16' → 'M16' applied correctly throughout
- Country codes properly normalized: 'Finland' → 'FIN', 'Czechia' → 'CZE', etc.
- Name formatting normalized to 'Given Surname' order consistently
- MisPunch status correctly mapped to 'MP' for competitors like Domas Juknevicius
- Tied ranks handled properly (positions 66-66 for Husag and Gojmerac)
- Time conversions accurate: '1:44:30' → 6396 seconds for Mert Yilmaz
- All 97 entries from XML source properly represented in CSV (94 OK + 3 MP)
- Guest nation NZL (Leo Croxford) correctly excluded from normalized CSV as expected

## 2023/Long-eventor.xml [M18]

- Verdict: `review`
- Confidence: `medium`
- Related CSVs: `2023/long.csv`
- Classes: `M18`
- Summary: The CSV correctly extracts most data from the XML source, but excludes guest nations (NZL, AUS) as expected. However, there are some notable exclusions that need verification.

### Issues

- [medium] `missing-row` Felix Hunt (NZL) missing from CSV (parser_bug=false, source_limitation=false)
  CSV: No corresponding row found
  Raw: Felix Hunt, bib 3033, NZL, rank 31, time 1:09:23
  Why: NZL (New Zealand) is not in the EYOC allowlist, so exclusion is expected and correct
  Next: Verify NZL is intentionally excluded per EYOC-COUNTRIES.md
- [medium] `missing-row` Eddie Swain (NZL) missing from CSV (parser_bug=false, source_limitation=false)
  CSV: No corresponding row found
  Raw: Eddie Swain, bib 3087, NZL, rank 66, time 1:20:06
  Why: NZL (New Zealand) is not in the EYOC allowlist, so exclusion is expected and correct
  Next: Verify NZL is intentionally excluded per EYOC-COUNTRIES.md
- [medium] `missing-row` Riley Croxford (NZL) missing from CSV (parser_bug=false, source_limitation=false)
  CSV: No corresponding row found
  Raw: Riley Croxford, bib 3073, NZL, rank 71, time 1:22:20
  Why: NZL (New Zealand) is not in the EYOC allowlist, so exclusion is expected and correct
  Next: Verify NZL is intentionally excluded per EYOC-COUNTRIES.md
- [medium] `missing-row` Cooper Horley (AUS) missing from CSV (parser_bug=false, source_limitation=false)
  CSV: No corresponding row found
  Raw: Cooper Horley, bib 3063, AUS, rank 73, time 1:22:37
  Why: AUS (Australia) is not in the EYOC allowlist, so exclusion is expected and correct
  Next: Verify AUS is intentionally excluded per EYOC-COUNTRIES.md
- [medium] `missing-row` Owen Radajewski (AUS) missing from CSV (parser_bug=false, source_limitation=false)
  CSV: No corresponding row found
  Raw: Owen Radajewski, bib 3103, AUS, rank 79, time 1:25:27
  Why: AUS (Australia) is not in the EYOC allowlist, so exclusion is expected and correct
  Next: Verify AUS is intentionally excluded per EYOC-COUNTRIES.md
- [medium] `missing-row` Jacob Knoef (NZL) missing from CSV (parser_bug=false, source_limitation=false)
  CSV: No corresponding row found
  Raw: Jacob Knoef, bib 3009, NZL, rank 93, time 1:37:31
  Why: NZL (New Zealand) is not in the EYOC allowlist, so exclusion is expected and correct
  Next: Verify NZL is intentionally excluded per EYOC-COUNTRIES.md

### Notable Matches

- Tomas Kucera (CZE) correctly extracted as winner with 58:50 (3530 seconds)
- Ludwig Rosen (SWE) correctly extracted as 2nd place with 58:56 (3536 seconds)
- Class normalization from 'Men 18' to 'M18' applied correctly
- All times correctly converted from MM:SS format to seconds
- MP (MisPunch) and DSQ (Disqualified) statuses correctly preserved
- Country codes properly normalized (e.g., Czechia -> CZE, Turkiye -> TUR)
- Tied ranks (5th place tie between Wylenmann and Berger) correctly handled
- All European countries correctly included and normalized

## 2023/Long-eventor.xml [W16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2023/long.csv`
- Classes: `W16`
- Summary: CSV data accurately matches the raw XML source with proper normalization applied

### Issues

- None reported.

### Notable Matches

- Class normalization: 'Women 16' -> 'W16' correctly applied
- Time conversion: '48:33' -> 2913 seconds (48*60+33) matches for winner Fanny Delahaye
- Country normalization: 'Czechia' -> 'CZE', 'Switzerland' -> 'SUI' properly applied
- Status handling: 'MisPunch' -> 'MP' for Ioana Atanasova, 'DidNotFinish' -> 'DNF' for Freya Tryner
- Name formatting: 'Di Stefano' -> 'Silvia di Stefano' with proper capitalization
- Tied ranks handled correctly: both rank 11 entries for Grooss and Schiller with same time 55:27
- All 85 entries from XML properly represented in CSV (83 finishers + 1 MP + 1 DNF)
- Bib numbers, ranks, and countries all match between source and CSV

## 2023/Long-eventor.xml [W18]

- Verdict: `review`
- Confidence: `medium`
- Related CSVs: `2023/long.csv`
- Classes: `W18`
- Summary: The CSV correctly extracts most data from the XML source, but excludes guest nations (NZL, AUS) as expected. However, there's a potential issue with one competitor's name normalization.

### Issues

- [low] `name` Name normalization inconsistency for Spanish competitor (parser_bug=false, source_limitation=false)
  CSV: Guinedell Faja Sanjaume
  Raw: <Family>Faja sanjaume</Family><Given sequence="1">Guinedell</Given>
  Why: The raw XML shows 'Faja sanjaume' (lowercase 's') but CSV shows 'Faja Sanjaume' (title case). This appears to be proper title-case normalization, but worth noting the case change.
  Next: Verify that title-case normalization is consistently applied to family names
- [low] `country` Guest nations excluded as expected (parser_bug=false, source_limitation=false)
  CSV: These competitors do not appear in the CSV
  Raw: Rachel Baker (NZL), Katherine Babington (NZL), Anna Babington (NZL), Molly McGowan (NZL), Nea Shingler (AUS), Milla Key (AUS), Erika Enderby (AUS)
  Why: Guest nations NZL and AUS are intentionally excluded from normalized CSV as they are not in the EYOC allowlist. This is correct behavior.
  Next: No action needed - this is expected normalization behavior

### Notable Matches

- Eeva Liina Ojanaho (FIN) correctly extracted as winner with 55:54 = 3354 seconds
- Rita Maramarosi (HUN) correctly placed 2nd with 56:31 = 3391 seconds
- Class normalization 'Women 18' → 'W18' applied correctly
- Country normalization applied correctly: 'Czechia' → 'CZE', 'Turkiye' → 'TUR'
- Time conversion accurate: '1:21:48' → 4908 seconds for Tuzcuogullari
- MP status correctly extracted for Giulia Vedana with MisPunch status
- Tied ranks handled correctly: positions 49-49 for Kropyvnytska and Strauta with same time 1:16:04
- All 97 competitors from XML source properly processed (90 in CSV + 7 excluded guest nations)

## 2023/Sprint-eventor.xml [M16]

- Verdict: `review`
- Confidence: `high`
- Related CSVs: `2023/sprint.csv`
- Classes: `M16`
- Summary: One significant issue found: Leo Croxford (NZL) appears in raw source but is missing from CSV, which contradicts the expected normalization behavior for non-allowlisted countries

### Issues

- [high] `missing-row` Leo Croxford (NZL) missing from CSV despite appearing in raw source (parser_bug=true, source_limitation=false)
  CSV: No corresponding row found in CSV for Leo Croxford
  Raw: PersonResult for Leo Croxford, bib 1001, NZL, rank 94, time 20:14
  Why: The raw XML clearly shows Leo Croxford from New Zealand (NZL) finishing 94th with time 20:14, but he does not appear in the normalized CSV. While NZL is not in the EYOC allowlist and should be excluded, the CSV shows 95 rows ending with Maksym Barchuk at rank 96, suggesting a gap at rank 94.
  Next: Verify parser logic for handling non-allowlisted countries and ensure consistent exclusion without creating rank gaps

### Notable Matches

- Aapo Virkajarvi (FIN) rank 1, time 12:02 → 722 seconds correctly converted
- Jan Vanicek (CZE) rank 3, time 12:16 → 736 seconds correctly converted
- Class normalization 'Men 16' → 'M16' applied correctly
- Country normalization 'Czechia' → 'CZE', 'Great Britain' → 'GBR' working properly
- Tied ranks handled correctly (ranks 13, 21, 29, 37, 40, 42, 46, 58, 60, 73)
- All 95 remaining competitors have valid EYOC countries and proper time conversions
- Names properly normalized to 'Given Surname' format throughout

## 2023/Sprint-eventor.xml [M18]

- Verdict: `review`
- Confidence: `medium`
- Related CSVs: `2023/sprint.csv`
- Classes: `M18`
- Summary: CSV correctly excludes non-EYOC guest nations (AUS, NZL) but includes all EYOC-allowlisted countries. Some athletes appear missing from CSV despite being in raw source.

### Issues

- [medium] `missing-row` Cooper Horley (AUS) missing from CSV (parser_bug=false, source_limitation=false)
  CSV: No corresponding row found
  Raw: Cooper Horley, rank 11, bib 3050, AUS, time 13:20
  Why: Australian athlete appears in raw source at rank 11 but is missing from CSV. This is expected behavior as AUS is not in EYOC allowlist.
  Next: Confirm AUS is intentionally excluded per EYOC-COUNTRIES.md allowlist
- [medium] `missing-row` Felix Hunt (NZL) missing from CSV (parser_bug=false, source_limitation=false)
  CSV: No corresponding row found
  Raw: Felix Hunt, rank 51, bib 3017, NZL, time 14:37
  Why: New Zealand athlete appears in raw source at rank 51 but is missing from CSV. This is expected behavior as NZL is not in EYOC allowlist.
  Next: Confirm NZL is intentionally excluded per EYOC-COUNTRIES.md allowlist
- [medium] `missing-row` Jacob Knoef (NZL) missing from CSV (parser_bug=false, source_limitation=false)
  CSV: No corresponding row found
  Raw: Jacob Knoef, rank 53, bib 3067, NZL, time 14:42
  Why: New Zealand athlete appears in raw source at rank 53 but is missing from CSV. This is expected behavior as NZL is not in EYOC allowlist.
  Next: Confirm NZL is intentionally excluded per EYOC-COUNTRIES.md allowlist
- [medium] `missing-row` Riley Croxford (NZL) missing from CSV (parser_bug=false, source_limitation=false)
  CSV: No corresponding row found
  Raw: Riley Croxford, rank 61, bib 3042, NZL, time 14:58
  Why: New Zealand athlete appears in raw source at rank 61 but is missing from CSV. This is expected behavior as NZL is not in EYOC allowlist.
  Next: Confirm NZL is intentionally excluded per EYOC-COUNTRIES.md allowlist
- [medium] `missing-row` Owen Radajewski (AUS) missing from CSV (parser_bug=false, source_limitation=false)
  CSV: No corresponding row found
  Raw: Owen Radajewski, rank 75, bib 3060, AUS, time 15:37
  Why: Australian athlete appears in raw source at rank 75 but is missing from CSV. This is expected behavior as AUS is not in EYOC allowlist.
  Next: Confirm AUS is intentionally excluded per EYOC-COUNTRIES.md allowlist
- [low] `rank` Rank sequence adjustment after guest exclusions (parser_bug=false, source_limitation=false)
  CSV: CSV shows consecutive ranks without gaps
  Raw: Raw ranks include gaps where guest nations were removed
  Why: After excluding AUS/NZL athletes, ranks appear to be renumbered consecutively, which may be correct normalization
  Next: Verify if rank renumbering after guest exclusion is intended behavior

### Notable Matches

- Tamas Felfoldi (HUN) correctly shows as rank 1 with 743 seconds (12:23)
- Filip Jancik (SVK) correctly shows as rank 2 with 776 seconds (12:56)
- Class normalization 'Men 18' -> 'M18' applied correctly
- Country normalization working: 'Czechia' -> 'CZE', 'Turkiye' -> 'TUR'
- Time conversion accurate: '12:23' -> 743 seconds, '13:03' -> 783 seconds
- Tied ranks handled correctly: multiple athletes at rank 7, 13, 18, etc.
- All EYOC-allowlisted countries properly included (HUN, SVK, SUI, SWE, etc.)

## 2023/Sprint-eventor.xml [W16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2023/sprint.csv`
- Classes: `W16`
- Summary: All 81 W16 competitors correctly extracted from XML source with accurate ranks, times, countries, and names

### Issues

- None reported.

### Notable Matches

- Rahel Good (SUI) correctly extracted as winner with 12:59 → 779 seconds
- Tied ranks properly handled: positions 18 (Vitkova/Jolly Jansson), 26 (Balciunaite/Pop), 40 (Mattart/Nikitina/Traubaite), etc.
- Country normalization working correctly: 'Czechia' → CZE, 'Great Britain' → GBR, 'Turkiye' → TUR
- Name formatting consistent: 'Di Stefano' → 'Silvia di Stefano', compound names preserved
- Time conversion accurate: '12:59' → 779 seconds, '28:58' → 1738 seconds
- All 81 competitors from XML source present in CSV with matching bib numbers and details

## 2023/Sprint-eventor.xml [W18]

- Verdict: `review`
- Confidence: `medium`
- Related CSVs: `2023/sprint.csv`
- Classes: `W18`
- Summary: The CSV correctly extracts most data but excludes guest nations (AUS, NZL) as expected. However, there are some ranking inconsistencies that need review.

### Issues

- [medium] `rank` Missing rank 29 in CSV extraction (parser_bug=true, source_limitation=false)
  CSV: Anna Taksdal appears as rank 28, but should be rank 29 since Enderby (AUS) at rank 29 was excluded
  Raw: Erika Enderby (AUS) has ResultPosition 29, Anna Taksdal (NOR) has ResultPosition 30
  Why: When guest nations are excluded, subsequent ranks should be adjusted to maintain sequential numbering
  Next: Review rank adjustment logic when excluding non-allowlisted countries
- [medium] `rank` Multiple ranking gaps throughout results (parser_bug=true, source_limitation=false)
  CSV: CSV shows gaps where these positions should be renumbered sequentially
  Raw: Raw shows positions 7, 36, 42, 43, 54 occupied by excluded AUS/NZL athletes
  Why: Systematic issue with rank renumbering after excluding guest nations
  Next: Implement proper rank renumbering after filtering out non-allowlisted countries
- [low] `missing-row` Expected exclusion of guest nations (parser_bug=false, source_limitation=false)
  CSV: These athletes correctly absent from CSV
  Raw: Raw contains AUS (Nea Shingler, Erika Enderby, Milla Key) and NZL (Anna Babington, Molly McGowan, Rachel Baker, Katherine Babington) athletes
  Why: This is expected behavior per normalization rules - non-EYOC countries are intentionally excluded
  Next: No action needed - this is correct normalization

### Notable Matches

- Rita Maramarosi (HUN) correctly extracted as winner with 12:31 = 751 seconds
- Class 'Women 18' correctly normalized to 'W18'
- Country codes properly normalized: 'Czechia' -> 'CZE', 'Turkiye' -> 'TUR'
- Names properly formatted: 'Maramarosi, Rita' -> 'Rita Maramarosi'
- Time conversions accurate: '12:31' -> 751 seconds, '23:28' -> 1408 seconds
- All 89 remaining athletes after guest exclusion have correct bib numbers, countries, and times

## 2023/results-relay.pdf

- Verdict: `review`
- Confidence: `high`
- Related CSVs: `2023/relay.csv`
- Summary: CSV correctly extracts most relay data but excludes non-EYOC guest nations (NZL, AUS) and teams with mispunched status as expected. Some minor name normalization differences need verification.

### Issues

- [low] `missing-row` New Zealand and Australia teams excluded from CSV (parser_bug=false, source_limitation=false)
  CSV: No NZL or AUS entries in CSV
  Raw: New Zealand New Zealand 1 (M18 rank 21) and Australia Australia 1 (W18 rank 15) appear in raw results
  Why: These are non-EYOC guest nations that should be intentionally excluded per normalization rules
  Next: Confirm this exclusion is intentional per EYOC-COUNTRIES.md allowlist
- [low] `missing-row` Mispunched teams excluded from CSV (parser_bug=true, source_limitation=false)
  CSV: No mispunched teams appear in CSV
  Raw: Multiple teams marked as 'mispunched' in raw results (Finland M16, France M16, Germany M16, etc.)
  Why: Teams with mispunched status should likely appear with status=MP rather than being excluded entirely
  Next: Review if mispunched teams should be included with status=MP
- [low] `name` Minor name normalization differences (parser_bug=false, source_limitation=false)
  CSV: Bob de Cleene, Rune de Clercq, Silvia di Stefano
  Raw: Bob De Cleene, Rune De Clercq, Silvia Di Stefano
  Why: Capitalization of particles (de, di) differs between raw and CSV
  Next: Verify if lowercase particles are intentional normalization
- [low] `name` Name spacing normalization (parser_bug=false, source_limitation=false)
  CSV: Guinedell Faja Sanjaume
  Raw: Guinedell Faja sanjaume
  Why: Capitalization difference in surname component
  Next: Verify title case normalization is applied consistently

### Notable Matches

- Class normalization correctly applied: Men 16 → M16, Women 18 → W18
- Country normalization correct: Czechia → CZE, Great Britain → GBR, Turkiye → TUR
- Time conversions accurate: 1:21:06 → 4866 seconds for CZE M16 team
- Relay leg times and names correctly extracted and matched to total times
- Team names properly normalized: 'Moldova, Republic of 1' preserved as shown in source
- Rankings and time differences correctly preserved from source data

## 2024/Long-eventor.xml [M16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2024/long.csv`
- Classes: `M16`
- Summary: All 95 M16 entries from the XML source are correctly extracted and normalized in the CSV. Times, ranks, names, countries, and statuses match accurately.

### Issues

- None reported.

### Notable Matches

- Erik Heczko (CZE) correctly extracted as rank 1 with 45:25 → 2725 seconds
- Mihaly Csoboth (HUN) correctly extracted as rank 2 with 46:47 → 2807 seconds
- Two tied competitors at rank 30 (Julian Schmied and Patrik Sedlacek) both with 58:50 → 3530 seconds
- Mark Levente Bujdoso correctly marked as DNF with partial time 49:30 → 2970 seconds
- Lauri Urbanek correctly marked as DNF with no finish time
- Country normalization working correctly: Czechia → CZE, Great Britain → GBR, Turkiye → TUR
- Complex names preserved correctly: 'Erik Marten Zernant', 'Bela Barnabas Sugta', 'Anton Kupriyanov Hviid'
- All 93 finishers plus 2 DNF entries properly extracted from XML structure

## 2024/Long-eventor.xml [M18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2024/long.csv`
- Classes: `M18`
- Summary: CSV data accurately matches the XML source with proper normalization applied

### Issues

- None reported.

### Notable Matches

- Winner Emil Husebye Aamodt (NOR, 54:29 = 3269s) correctly extracted as rank 1
- Tied ranks 31-31 for Tommy Rollins and Laurence Ward (both 1:04:11) properly handled
- MP (MisPunch) status correctly normalized from 'MisPunch' in XML for Max Oesterberg, Johannes Marager, and Cristian Betivu
- Country codes properly normalized: 'Czechia' → CZE, 'Turkiye' → TUR, 'Moldova, Republic of' → MDA
- Time conversions accurate: '54:29' → 3269 seconds, '2:02:17' → 7337 seconds
- All 105 entries from XML properly represented: 102 ranked OK + 3 MP entries
- Names correctly normalized from XML format: 'Husebye Aamodt, Emil' → 'Emil Husebye Aamodt'
- Class normalization from 'Men 18' → 'M18' applied correctly

## 2024/Long-eventor.xml [W16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2024/long.csv`
- Classes: `W16`
- Summary: All 87 W16 entries from the XML source are correctly extracted and normalized in the CSV, with accurate times, ranks, statuses, and country codes

### Issues

- None reported.

### Notable Matches

- Winner Mira Werder (SUI) correctly shows 46:18 → 2778 seconds with rank 1
- Tied 35th place correctly preserved for Ella Baxter (GBR) and Iryna Polubentseva (UKR) both at 1:02:54
- MP status correctly assigned to Emanuela Stoyanova (BUL) with MisPunch in source
- Country normalization working: 'Turkiye' → TUR, 'Great Britain' → GBR
- Name normalization working: 'FengerGroen' → 'Fengergroen', compound names preserved
- All 86 ranked finishers plus 1 MP entry properly extracted from 87 total entries

## 2024/Long-eventor.xml [W18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2024/long.csv`
- Classes: `W18`
- Summary: All 90 W18 entries from the XML source are correctly extracted and normalized in the CSV, with accurate ranks, times, statuses, and country mappings.

### Issues

- None reported.

### Notable Matches

- Winner Freja Hjerne (SWE) correctly shows rank 1, time 53:50 → 3230 seconds
- Tied ranks 54-54 for Eliza Odrina and Laura Krumina (both LAT, 1:23:07) properly handled
- MP status correctly assigned to Freya Tryner (GBR) with MisPunch in source
- DNF status correctly assigned to Nea Erzen (SLO) with DidNotFinish in source
- Country normalization working: 'Turkiye' → TUR, 'Great Britain' → GBR, 'Czechia' → CZE
- Complex names preserved: 'Sigrid Schmitt Gran', 'Lovise Harriette Koppel', 'Irem Gul Nazlimoglu'
- Time conversions accurate: 1:53:41 → 6821 seconds, 2:00:33 → 7233 seconds
- All 88 finishers plus 2 non-finishers (MP, DNF) accounted for from 90 total entries

## 2024/RESULTS-RELAY-WITH-MIX.pdf

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2024/relay.csv`
- Summary: CSV data accurately represents the raw source with proper normalization applied. All ranked teams from allowlisted countries are correctly extracted with accurate times, names, and leg assignments.

### Issues

- None reported.

### Notable Matches

- M16 Hungary 1 team correctly shows 1:44:34 total with legs Bela Barnabas Sugta (35:01), Mark Bujdoso (36:23), Mihaly Csoboth (33:10)
- W16 Finland 1 properly normalized to FIN with correct leg times: Lotta Laakso (33:46), Anni Jantunen (37:35), Iida Koskinen (36:37)
- M18 Romania 1 correctly includes Sara Bojte (female) on leg 3 as shown in raw source - this mixed-gender composition matches the source
- Country normalization working correctly: 'Czechia' -> 'CZE', 'Great Britain' -> 'GBR', 'Turkiye' -> 'TUR'
- Non-allowlisted countries (United States, New Zealand, Australia) correctly excluded from CSV as expected
- Mixed teams (MIX entries) correctly excluded from normalized CSV as they are not standard EYOC country teams
- DNS/DNF/MP teams correctly excluded from final rankings (Serbia W16, various MIX teams with incomplete results)
- Time conversions accurate: 1:44:34 -> 6274 seconds, individual leg times properly converted
- All 24 classes (M16, W16, M18, W18) properly normalized and all ranked teams from valid countries included

## 2024/Sprint-eventor.xml [M16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2024/sprint.csv`
- Classes: `M16`
- Summary: All 95 M16 entries from the XML source are correctly extracted and normalized in the CSV, with proper handling of ties, status codes, and country normalization

### Issues

- None reported.

### Notable Matches

- Simon Calandry (FRA, rank 1, 11:00 -> 660 seconds) correctly extracted as winner
- Tied ranks properly handled: positions 6, 9, 20, 22, 39, 45, 49, 56, 67 all show correct tie handling
- MisPunch status correctly normalized to MP for 23 competitors including Finn Selmer Duguid, Manuel Gasser, etc.
- Country codes properly normalized: Czechia->CZE, Great Britain->GBR, Turkiye->TUR
- Time conversion accurate: 11:00 -> 660 seconds, 18:21 -> 1101 seconds
- All 72 OK finishers plus 23 MP competitors = 95 total entries match XML numberOfEntries
- Names properly normalized to Given Surname format: 'Calandry, Simon' -> 'Simon Calandry'

## 2024/Sprint-eventor.xml [M18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2024/sprint.csv`
- Classes: `M18`
- Summary: All 105 M18 entries from the XML source are correctly represented in the CSV with accurate ranks, times, statuses, and country normalizations

### Issues

- None reported.

### Notable Matches

- Winner Filip Jancik (SVK) correctly shows rank 1, time 11:45 → 705 seconds
- Tied ranks handled properly: positions 10, 25, 27, 29, 36, 39, 42, 47, 51, 57, 80, 82, 92 all show correct tied placements
- Status normalization correct: MisPunch → MP, DidNotFinish → DNF, DidNotStart → DNS
- Country normalization working: Czechia → CZE, Turkiye → TUR, Moldova Republic of → MDA
- Time conversion accurate: 12:08 → 728 seconds, 15:21 → 921 seconds
- All 9 MP (mispunch) entries correctly identified with their finish times
- DNF entry Emil Husebye Aamodt shows partial time 10:50 → 650 seconds
- DNS entry Rasmus Toyryla correctly shows blank time

## 2024/Sprint-eventor.xml [W16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2024/sprint.csv`
- Classes: `W16`
- Summary: The CSV extraction accurately represents the W16 class results from the 2024 Sprint XML source. All 87 entries are correctly parsed with proper normalization of class names, countries, statuses, and time conversions.

### Issues

- None reported.

### Notable Matches

- Winner Mira Werder (SUI) correctly shows 11:43 -> 703 seconds with rank 1
- Tied 4th place correctly shows both Anna Mia Atonen (EST) and Lotta Marit Luethi (SUI) with rank 4 and 727 seconds
- Status normalization works: 'MisPunch' -> 'MP', 'Disqualified' -> 'DSQ', 'DidNotStart' -> 'DNS'
- Country normalization correct: 'Turkiye' -> 'TUR', 'Great Britain' -> 'GBR'
- Name normalization preserves compound names like 'Astrid Faber FengerGroen' -> 'Astrid Faber Fengergroen'
- All 84 ranked finishers plus 3 non-finishers (MP, DSQ, DNS) properly extracted from 87 total entries

## 2024/Sprint-eventor.xml [W18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2024/sprint.csv`
- Classes: `W18`
- Summary: The CSV extraction accurately represents the W18 class results from the 2024 Sprint XML source. All 90 competitors are correctly captured with proper normalization of classes, countries, names, times, and statuses.

### Issues

- None reported.

### Notable Matches

- Winner Janka Mikes (HUN) correctly shows 11:34 → 694 seconds with rank 1
- Three-way tie at rank 15 (Gasser, Koziskova, Holasova) all with 13:09 → 789 seconds properly preserved
- Country normalization works correctly: 'Czechia' → CZE, 'Great Britain' → GBR, 'Turkiye' → TUR
- Status normalization correct: 'MisPunch' → MP, 'Disqualified' → DSQ
- Name order properly normalized: 'Gran, Sigrid Schmitt' → 'Sigrid Schmitt Gran'
- All 84 OK finishers, 4 MP, and 2 DSQ competitors correctly extracted
- Time conversions accurate: 11:34 → 694s, 12:07 → 727s, 18:01 → 1081s
- Bib numbers and ranks match exactly between source and CSV

## 2025/Long.xml [M16]

- Verdict: `review`
- Confidence: `high`
- Related CSVs: `2025/long.csv`
- Classes: `M16`
- Summary: Several non-EYOC countries appear in CSV that should be excluded per normalization rules

### Issues

- [medium] `country` Australia entries included despite non-EYOC status (parser_bug=false, source_limitation=false)
  CSV: These entries are missing from the CSV
  Raw: Hayden Dent (Australia), Alton Freeman (Australia), Rory Shedden (Australia), Matthew Slater (Australia) appear in raw XML
  Why: Australia is not in EYOC-COUNTRIES.md allowlist and should be excluded, but the raw source shows these competitors
  Next: Verify Australia exclusion is intentional per EYOC rules
- [medium] `country` United States entries included despite non-EYOC status (parser_bug=false, source_limitation=false)
  CSV: These entries are missing from the CSV
  Raw: Alexander Eriksson (United States), Mikhail Biryukov (United States), Mark Fey (United States) appear in raw XML
  Why: United States is not in EYOC-COUNTRIES.md allowlist and should be excluded per normalization rules
  Next: Verify USA exclusion is intentional per EYOC rules
- [medium] `country` New Zealand entries included despite non-EYOC status (parser_bug=false, source_limitation=false)
  CSV: These entries are missing from the CSV
  Raw: Tahi Harris (New Zealand), Xavier White (New Zealand), Jakob Abernethy (New Zealand), Adam Landels (New Zealand) appear in raw XML
  Why: New Zealand is not in EYOC-COUNTRIES.md allowlist and should be excluded per normalization rules
  Next: Verify New Zealand exclusion is intentional per EYOC rules
- [medium] `country` Canada entry included despite non-EYOC status (parser_bug=false, source_limitation=false)
  CSV: This entry is missing from the CSV
  Raw: Etienne Jacques (Canada) appears in raw XML
  Why: Canada is not in EYOC-COUNTRIES.md allowlist and should be excluded per normalization rules
  Next: Verify Canada exclusion is intentional per EYOC rules
- [low] `country` Country normalization appears correct (parser_bug=false, source_limitation=false)
  CSV: TUR appears in CSV
  Raw: Turkiye appears in raw XML
  Why: Proper normalization of Turkey/Turkiye to TUR code
  Next: No action needed - correct normalization

### Notable Matches

- Ekain Fernandez Garcia (ESP) rank 1, time 2453s matches perfectly
- Joakim Savinainen (FIN) rank 2, time 2552s matches perfectly
- Erik Marten Zernant (EST) rank 3, time 2567s matches perfectly
- Country normalization: Turkiye → TUR, Czechia → CZE working correctly
- Class normalization: Men 16 → M16 working correctly
- All EYOC-allowlisted countries properly included with correct times and ranks
- DNF status correctly captured for Lauri Urbanek (AUT)

## 2025/Long.xml [M18]

- Verdict: `review`
- Confidence: `medium`
- Related CSVs: `2025/long.csv`
- Classes: `M18`
- Summary: The CSV correctly extracts most data but excludes several guest nations (Australia, USA, New Zealand, Canada) that appear in the raw source, which is expected per normalization rules. However, there are some ranking inconsistencies that need review.

### Issues

- [medium] `missing-row` Guest nations excluded from CSV (parser_bug=false, source_limitation=false)
  CSV: These athletes do not appear in the CSV
  Raw: Euan Best (Australia), Erik Fey (United States), Matthew Greenwood (New Zealand), Benjamin Cooper (United States), Thomas Potts (New Zealand), James Wright (New Zealand), Leo Croxford (New Zealand), Dylan Revells (Canada), Elye Dent (Australia), William Barnes (Australia), Aoife Rothery (Australia)
  Why: Multiple guest nation athletes appear in raw source but are missing from CSV. This is expected per normalization rules that exclude non-EYOC countries.
  Next: Confirm this is intentional exclusion per EYOC country allowlist policy
- [low] `rank` Ranking gaps due to excluded athletes (parser_bug=false, source_limitation=false)
  CSV: Ranks appear sequential without gaps despite excluded athletes
  Raw: Position 19 shows Euan Best (Australia), but CSV shows rank 19 as Dani Nikolov
  Why: When guest athletes are excluded, the ranking should be renumbered to maintain sequential order, which appears to have been done correctly
  Next: Verify ranking renumbering logic is working as intended
- [low] `rank` Tied positions handling (parser_bug=false, source_limitation=false)
  CSV: Both athletes show rank 57 in CSV
  Raw: Francesco Scalzotto and Niklas Weitlaner both show Position 59 with time 3751
  Why: Raw source shows position 59 for both tied athletes, but CSV shows rank 57. This suggests ranking adjustment after excluding guest athletes.
  Next: Verify tie-breaking and rank adjustment logic after guest exclusions

### Notable Matches

- Mihaly Csoboth correctly extracted as rank 1 with 2986 seconds for Hungary
- Class normalization correctly converts 'Men 18' to 'M18'
- Country normalization working: 'Czechia' -> 'CZE', 'Switzerland' -> 'SUI'
- Status handling correct: OK, MP (MissingPunch), DNF (DidNotFinish)
- Time conversion accurate: XML time 2986 -> CSV 2986 seconds
- Missing punch athletes correctly marked with MP status
- DNF athlete (Liam Malnati) correctly shows empty time

## 2025/Long.xml [W16]

- Verdict: `fail`
- Confidence: `high`
- Related CSVs: `2025/long.csv`
- Classes: `W16`
- Summary: Multiple guest nations (Australia, New Zealand, United States) appear in CSV despite being non-allowlisted countries that should be excluded

### Issues

- [high] `extra-row` Australia guest nation included in CSV (parser_bug=false, source_limitation=false)
  CSV: No Australia entries found in CSV - correctly excluded
  Raw: Ariadna Iskhakova from Australia (position 39) and Shari Gilbert from Australia (position 97) appear in raw XML
  Why: Australia is not in EYOC-COUNTRIES allowlist and should be excluded from normalized CSV
  Next: Verify Australia exclusion is working correctly - this appears to be handled properly
- [high] `extra-row` New Zealand guest nation included in CSV (parser_bug=false, source_limitation=false)
  CSV: No New Zealand entries found in CSV - correctly excluded
  Raw: Torun Joergensen (position 79), Cerys Findlow (position 90), Dora Slavich (position 93), Charlotte Dalziel (position 95) from New Zealand appear in raw XML
  Why: New Zealand is not in EYOC-COUNTRIES allowlist and should be excluded from normalized CSV
  Next: Verify New Zealand exclusion is working correctly - this appears to be handled properly
- [high] `extra-row` United States guest nation included in CSV (parser_bug=false, source_limitation=false)
  CSV: No United States entries found in CSV - correctly excluded
  Raw: Allison Coates from United States (position 96) appears in raw XML
  Why: United States is not in EYOC-COUNTRIES allowlist and should be excluded from normalized CSV
  Next: Verify United States exclusion is working correctly - this appears to be handled properly
- [low] `name` Minor name formatting differences (parser_bug=false, source_limitation=false)
  CSV: Astrid Faber Fengergroen
  Raw: FengerGroen in XML vs Fengergroen in CSV
  Why: Slight capitalization difference in compound surname
  Next: Consider standardizing compound name handling

### Notable Matches

- Carla Castelli (SUI) correctly ranked 1st with 2495 seconds
- Class normalization 'Women 16' -> 'W16' applied correctly
- Country normalization working: 'Switzerland' -> 'SUI', 'Czechia' -> 'CZE', etc.
- Missing punch statuses correctly converted to 'MP' for Martyna Jankauskaite and Mafalda Goncalves
- All 94 valid EYOC competitors properly included with correct times and rankings
- Guest nations (Australia, New Zealand, United States) correctly excluded from normalized CSV

## 2025/Long.xml [W18]

- Verdict: `fail`
- Confidence: `high`
- Related CSVs: `2025/long.csv`
- Classes: `W18`
- Summary: Multiple guest nations (Australia, New Zealand, United States) appear in raw source but are correctly excluded from CSV. However, there are significant issues with missing rows and incorrect position assignments.

### Issues

- [high] `missing-row` Missing Australia competitor Liana Stubbs (parser_bug=false, source_limitation=false)
  CSV: No corresponding row in CSV
  Raw: Position 22: Liana Stubbs (Australia) - 3218 seconds
  Why: Australia is not in EYOC allowlist, so exclusion is expected and correct
  Next: No action needed - correct exclusion of non-EYOC nation
- [high] `missing-row` Missing New Zealand competitors (parser_bug=false, source_limitation=false)
  CSV: No corresponding rows in CSV
  Raw: Positions 39, 72, 81, 85: Zara Toes, Juliet Freeman, Lani Murray, Georgia Lindroos (New Zealand)
  Why: New Zealand is not in EYOC allowlist, so exclusion is expected and correct
  Next: No action needed - correct exclusion of non-EYOC nation
- [high] `missing-row` Missing United States competitors (parser_bug=false, source_limitation=false)
  CSV: No corresponding rows in CSV
  Raw: Positions 91, 103, 105: Paige Suhocki, Kendal OCallaghan, Adalia SchafrathCraig (United States)
  Why: United States is not in EYOC allowlist, so exclusion is expected and correct
  Next: No action needed - correct exclusion of non-EYOC nation
- [high] `missing-row` Missing Australia competitor Alexandra Edwards (parser_bug=false, source_limitation=false)
  CSV: No corresponding row in CSV
  Raw: Position 86: Alexandra Edwards (Australia) - 4262 seconds
  Why: Australia is not in EYOC allowlist, so exclusion is expected and correct
  Next: No action needed - correct exclusion of non-EYOC nation
- [high] `missing-row` Missing Australia competitor Maggie Mackay (parser_bug=false, source_limitation=false)
  CSV: No corresponding row in CSV
  Raw: Position 92: Maggie Mackay (Australia) - 4513 seconds
  Why: Australia is not in EYOC allowlist, so exclusion is expected and correct
  Next: No action needed - correct exclusion of non-EYOC nation
- [high] `missing-row` Missing Australia competitor Savanna Sweeney (parser_bug=false, source_limitation=false)
  CSV: No corresponding row in CSV
  Raw: Position 95: Savanna Sweeney (Australia) - 4660 seconds
  Why: Australia is not in EYOC allowlist, so exclusion is expected and correct
  Next: No action needed - correct exclusion of non-EYOC nation
- [medium] `rank` Rank compression after guest exclusions (parser_bug=false, source_limitation=false)
  CSV: CSV shows consecutive ranks 1-95 without gaps
  Raw: Raw positions include gaps due to guest nations at 22, 39, 72, 81, 85, 86, 91, 92, 95, 103, 105
  Why: After excluding guest nations, ranks should be renumbered consecutively, which appears to have been done correctly
  Next: Verify rank renumbering logic is working correctly

### Notable Matches

- Lotta Marit Luethi (SUI) correctly ranked 1st with 2675 seconds
- Marketa Hanusova (CZE) correctly ranked 2nd with 2717 seconds
- Country normalization working: 'Switzerland' -> 'SUI', 'Czechia' -> 'CZE'
- Name normalization working: 'MakiHokkonen' -> 'Makihokkonen', 'Di Stefano' -> 'di Stefano'
- Tied positions handled correctly: positions 18, 50 both appear in CSV
- All EYOC-eligible countries properly included and normalized

## 2025/Sprint.xml [M16]

- Verdict: `review`
- Confidence: `high`
- Related CSVs: `2025/sprint.csv`
- Classes: `M16`
- Summary: Several non-allowlisted countries appear in CSV that should be excluded, plus some missing competitors from raw source

### Issues

- [high] `country` Australia competitors included despite non-allowlisted status (parser_bug=true, source_limitation=false)
  CSV: Missing from CSV - these should be excluded as AUS is not in EYOC-COUNTRIES allowlist
  Raw: Hayden Dent (Australia, rank 4), Alton Freeman (Australia, rank 25), Rory Shedden (Australia, rank 39), Matthew Slater (Australia, rank 90)
  Why: Australia is not in the EYOC allowlist and should be intentionally excluded from clean CSV
  Next: Remove Australia competitors from CSV as they are non-allowlisted guests
- [high] `country` New Zealand competitors included despite non-allowlisted status (parser_bug=true, source_limitation=false)
  CSV: Missing from CSV - these should be excluded as NZL is not in EYOC-COUNTRIES allowlist
  Raw: Tahi Harris (New Zealand, rank 28), Jakob Abernethy (New Zealand, rank 50), Xavier White (New Zealand, rank 65), Adam Landels (New Zealand, rank 81)
  Why: New Zealand is not in the EYOC allowlist and should be intentionally excluded from clean CSV
  Next: Remove New Zealand competitors from CSV as they are non-allowlisted guests
- [high] `country` United States competitors included despite non-allowlisted status (parser_bug=true, source_limitation=false)
  CSV: Missing from CSV - these should be excluded as USA is not in EYOC-COUNTRIES allowlist
  Raw: Alexander Eriksson (United States, rank 60), Mark Fey (United States, rank 61), Mikhail Biryukov (United States, rank 70)
  Why: United States is not in the EYOC allowlist and should be intentionally excluded from clean CSV
  Next: Remove United States competitors from CSV as they are non-allowlisted guests
- [high] `country` Canada competitor included despite non-allowlisted status (parser_bug=true, source_limitation=false)
  CSV: Missing from CSV - should be excluded as CAN is not in EYOC-COUNTRIES allowlist
  Raw: Etienne Jacques (Canada, rank 76)
  Why: Canada is not in the EYOC allowlist and should be intentionally excluded from clean CSV
  Next: Remove Canada competitor from CSV as they are non-allowlisted guests
- [medium] `missing-row` Missing allowlisted competitors from CSV (parser_bug=true, source_limitation=false)
  CSV: CSV has 91 total rows for M16 class
  Raw: Raw source shows 103 competitors total, but CSV only has 84 ranked + 7 MP = 91 rows
  Why: Discrepancy suggests some allowlisted competitors may be missing from CSV extraction
  Next: Verify all allowlisted competitors from raw source are included in CSV

### Notable Matches

- Erik Marten Zernant (EST) correctly shows as rank 1 with 724 seconds
- Class normalization 'Men 16' -> 'M16' applied correctly
- Country normalization working: 'Czechia' -> 'CZE', 'Turkiye' -> 'TUR'
- Missing punch statuses correctly marked as 'MP' for 7 competitors
- Time conversion from seconds working correctly (e.g., 724 seconds preserved)
- Name order normalization applied: 'Zernant, Erik Marten' -> 'Erik Marten Zernant'

## 2025/Sprint.xml [M18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2025/sprint.csv`
- Classes: `M18`
- Summary: CSV extraction correctly matches the raw XML source with proper normalization applied

### Issues

- None reported.

### Notable Matches

- Class 'Men 18' correctly normalized to 'M18'
- All 110 competitors from XML properly extracted with correct ranks, names, and times
- Status normalization: 'MissingPunch' → 'MP', 'Disqualified' → 'DSQ', 'DidNotFinish' → 'DNF'
- Country normalization: 'Czechia' → 'CZE', 'Great Britain' → 'GBR', 'Turkiye' → 'TUR'
- Time conversion from seconds in XML matches time_seconds in CSV (e.g., 723 seconds for winner)
- Tied ranks handled correctly (positions 3, 13, 19, 23, 26, 28, etc.)
- Non-allowlisted countries (Australia, New Zealand, United States, Canada) correctly excluded from CSV
- Names properly formatted in 'Given Surname' order with title case

## 2025/Sprint.xml [W16]

- Verdict: `review`
- Confidence: `medium`
- Related CSVs: `2025/sprint.csv`
- Classes: `W16`
- Summary: The CSV extraction appears mostly accurate but contains several concerning issues: missing guest nations (AUS, NZL, USA), potential country normalization errors, and some name formatting inconsistencies that need verification.

### Issues

- [high] `missing-row` Missing Australian competitors (parser_bug=true, source_limitation=false)
  CSV: No Australian competitors found in CSV
  Raw: Ariadna Iskhakova (Australia, rank 54) and Shari Gilbert (Australia, rank 70) appear in raw XML
  Why: Australia (AUS) should be in the EYOC allowlist but competitors are missing from CSV
  Next: Verify if Australia is in EYOC-COUNTRIES.md allowlist and fix parser if so
- [high] `missing-row` Missing New Zealand competitors (parser_bug=true, source_limitation=false)
  CSV: No New Zealand competitors found in CSV
  Raw: Dora Slavich (rank 59), Cerys Findlow (rank 70), Charlotte Dalziel (rank 81), Torun Joergensen (rank 83) appear in raw XML
  Why: New Zealand competitors present in raw data but absent from CSV
  Next: Check if NZL is allowlisted and verify parser logic
- [high] `missing-row` Missing USA competitor (parser_bug=true, source_limitation=false)
  CSV: No USA competitors found in CSV
  Raw: Allison Coates (United States, rank 98) appears in raw XML
  Why: USA competitor present in raw data but absent from CSV
  Next: Verify if USA is allowlisted and check parser exclusion logic
- [medium] `country` Moldova country code normalization (parser_bug=false, source_limitation=false)
  CSV: Listed as 'MDA'
  Raw: Daria Gutul from 'Moldova, Republic of'
  Why: Need to verify this is correct normalization for Moldova
  Next: Confirm MDA is correct code for Moldova in EYOC context
- [low] `name` Name formatting inconsistencies (parser_bug=false, source_limitation=true)
  CSV: Listed as 'Astrid Faber Fengergroen'
  Raw: FengerGroen vs Fengergroen in raw XML
  Why: Minor spelling variation in compound surname
  Next: Acceptable normalization, no action needed

### Notable Matches

- Anni Jantunen (FIN) correctly extracted as winner with 650 seconds
- Class normalization 'Women 16' -> 'W16' applied correctly
- Tied ranks (6th place Sara Delic and Analia Reubi) preserved correctly
- Missing punch status for Efsa Sezin Akin correctly marked as 'MP'
- Time conversions from seconds appear accurate throughout
- Most country normalizations look correct (SUI, GER, GBR, etc.)

## 2025/Sprint.xml [W18]

- Verdict: `review`
- Confidence: `medium`
- Related CSVs: `2025/sprint.csv`
- Classes: `W18`
- Summary: The CSV correctly extracts most data from the XML source, but excludes guest nations (NZL, AUS, USA) as expected. However, there are some concerns about missing position numbers and potential data integrity issues that warrant review.

### Issues

- [medium] `missing-row` Guest nations excluded from CSV as expected (parser_bug=false, source_limitation=false)
  CSV: These athletes do not appear in the CSV
  Raw: Georgia Lindroos (New Zealand), Liana Stubbs (Australia), Alexandra Edwards (Australia), Juliet Freeman (New Zealand), Zara Toes (New Zealand), Lani Murray (New Zealand), Maggie Mackay (Australia), Savanna Sweeney (Australia), Paige Suhocki (United States), Kendal OCallaghan (United States), Adalia SchafrathCraig (United States)
  Why: Guest nations NZL, AUS, USA are intentionally excluded per normalization rules
  Next: Confirm this is expected behavior per EYOC country allowlist
- [low] `rank` Missing position numbers for some tied ranks (parser_bug=true, source_limitation=false)
  CSV: CSV shows ranks 24, 25, 26, 26, 28 instead of accounting for ties properly
  Raw: Position 24 appears twice (Georgia Lindroos and Liana Stubbs), Position 27 appears twice (Mariann Zernant and Juliet Freeman), Position 29 appears twice (Yevheniia Oksiuchenko and Arlet Sales)
  Why: The CSV may not be handling tied positions correctly when guest nations are excluded
  Next: Verify rank numbering logic when excluding guest nations
- [low] `name` Name formatting variations (parser_bug=false, source_limitation=false)
  CSV: Anni Makihokkonen
  Raw: MakiHokkonen, Anni vs Anni MakiHokkonen
  Why: Minor name formatting differences, likely acceptable normalization
  Next: Verify name normalization is consistent

### Notable Matches

- Ofri Yacobi (ISR) correctly extracted as rank 1 with 794 seconds
- Tied positions at rank 2 (Lenia Grimm and Ilze Jumike) both with 799 seconds correctly preserved
- Status codes correctly mapped: OK, MP (MissingPunch), DSQ (Disqualified)
- Country codes properly normalized: Israel->ISR, Switzerland->SUI, Moldova Republic of->MDA
- Time conversions accurate: XML time values match CSV time_seconds
- Class normalization correct: Women 18 -> W18
- Missing punch and disqualified athletes properly included with appropriate status

## 2025/results-relay.pdf

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2025/relay.csv`
- Summary: The CSV accurately represents the relay results from the 2025 PDF source with proper normalization applied

### Issues

- None reported.

### Notable Matches

- M16 class correctly normalized from 'Men 16' in source
- W16 class correctly normalized from 'Women 16' in source
- M18 class correctly normalized from 'Men 18' in source
- W18 class correctly normalized from 'Women 18' in source
- Time conversions accurate: FIN M16 1:28:34 → 5314 seconds
- MP status correctly applied for mispunched teams (POR, ROU, SLO, TUR in M16)
- DSQ status correctly applied for disqualified teams (CRO M18, NOR W18)
- Individual leg times properly extracted and converted to seconds
- Team names normalized to country codes (e.g., 'FIN' team → FIN country)
- Names properly formatted in Given Surname order with title case
- Rank assignments match source placement order
- All EYOC-allowlisted countries preserved in normalized output

## 2026/01-sprint-results-eventor.xml [M16]

- Verdict: `review`
- Confidence: `high`
- Related CSVs: `2026/sprint.csv`
- Classes: `M16`
- Summary: The CSV extraction appears accurate for most entries, but several non-EYOC countries are present that should be excluded according to normalization rules

### Issues

- [medium] `country` Non-EYOC countries included in normalized CSV (parser_bug=true, source_limitation=false)
  CSV: CSV contains entries for countries not in EYOC allowlist
  Raw: Multiple entries with countries like NZL (Nuova Zelanda), AUS (Australia), USA (Stati Uniti d'America), CAN (Canada)
  Why: According to normalization rules, non-allowlisted guest nations like NZL, USA, AUS should be intentionally removed from clean CSVs
  Next: Remove entries for NZL, AUS, USA, CAN from the normalized CSV as they are not EYOC-allowlisted countries
- [low] `other` Position 22 missing from CSV (parser_bug=false, source_limitation=false)
  CSV: No rank 22 entry in CSV, jumps from rank 21 to 23
  Raw: Daniel Porteous (NZL) has Position 22 in raw XML
  Why: If NZL entries are properly excluded, this gap would be expected, but should verify ranking consistency
  Next: Verify that rank numbering is correctly adjusted after removing non-EYOC countries
- [low] `other` Missing position 91 in final results (parser_bug=false, source_limitation=false)
  CSV: CSV shows rank 90 as final position
  Raw: Raw XML shows position 101 for Adam Jacques (CAN)
  Why: After removing non-EYOC countries, final ranking should be adjusted accordingly
  Next: Confirm that final rankings are properly renumbered after country filtering

### Notable Matches

- Daniel Sanz (ESP) correctly extracted as rank 1 with 718 seconds
- Antoni Pachnik (POL) correctly extracted as rank 2 with 727 seconds
- Tied positions properly handled (rank 5 tie, rank 9 tie, rank 17 tie, etc.)
- Missing punch (MP) and Did Not Finish (DNF) statuses correctly extracted
- Class normalization from 'Men 16' to 'M16' applied correctly
- Country codes properly normalized (Repubblica Ceca -> CZE, Germania -> GER, etc.)
- Time conversion from XML seconds to CSV seconds accurate throughout
- Bib numbers, names, and split times data preserved accurately

## 2026/01-sprint-results-eventor.xml [M18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2026/sprint.csv`
- Classes: `M18`
- Summary: The CSV extraction accurately represents the M18 class results from the XML source. All competitors, rankings, times, and statuses match correctly between the raw XML and normalized CSV.

### Issues

- None reported.

### Notable Matches

- Winner Ekain Fernandez Garcia (ESP, 805s) correctly extracted as rank 1
- Tied ranks properly handled: positions 4-4 for Gunnarsson/Doetsch both at 815s
- Missing punch (MP) statuses correctly identified for 10 competitors including Lars Anders Luiks and Pablo Rubio Cribellati
- Country codes properly normalized: 'Spagna' -> ESP, 'Repubblica Ceca' -> CZE, 'Regno Unito' -> GBR
- Names correctly formatted from XML structure: 'Fernandez Garcia, Ekain' -> 'Ekain Fernandez Garcia'
- All 91 ranked finishers plus 10 MP competitors properly extracted
- Class normalization correct: 'Men 18' -> M18
- Time conversions accurate: XML <Time>805</Time> -> CSV 805 seconds
- Non-EYOC countries (AUS, NZL, USA) correctly excluded from normalized CSV as expected

## 2026/01-sprint-results-eventor.xml [W16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2026/sprint.csv`
- Classes: `W16`
- Summary: The CSV extraction accurately represents the W16 class results from the XML source with proper normalization applied

### Issues

- None reported.

### Notable Matches

- Winner Dora Delic (CRO) correctly extracted with 772 seconds and rank 1
- Class name properly normalized from 'Women 16' to 'W16'
- Country codes correctly normalized (e.g., 'Croazia' -> 'CRO', 'Finlandia' -> 'FIN')
- Names properly formatted in 'Given Surname' order (e.g., 'Delic, Dora' -> 'Dora Delic')
- Time values correctly converted from XML seconds to integer seconds
- Missing punch statuses properly identified as 'MP' for athletes with incomplete split times
- All 94 finished athletes plus 11 MP athletes correctly extracted
- Guest nations (NZL, USA, AUS) correctly excluded from normalized CSV as expected
- Tied positions handled correctly (e.g., ranks 11, 14, 22, 30, 34, 43, 61, 67)

## 2026/01-sprint-results-eventor.xml [W18]

- Verdict: `review`
- Confidence: `medium`
- Related CSVs: `2026/sprint.csv`
- Classes: `W18`
- Summary: The CSV extraction appears mostly accurate but contains several issues: non-allowlisted countries (NZL, USA, AUS, CAN) are correctly excluded, but there are name formatting inconsistencies, a missing competitor, and one potential gender classification issue that needs verification.

### Issues

- [medium] `missing-row` Missing competitor from CSV extraction (parser_bug=false, source_limitation=false)
  CSV: No corresponding row found in CSV for Anna Batcheler
  Raw: Anna Batcheler (NZL) appears in raw XML at position 53 with bib 509, time 977 seconds
  Why: NZL is not in the allowlisted countries, so exclusion is expected and correct
  Next: Verify this is intentional exclusion of non-EYOC country
- [medium] `missing-row` Missing competitors from non-allowlisted countries (parser_bug=false, source_limitation=false)
  CSV: These competitors are absent from the CSV
  Raw: Multiple competitors from NZL, USA, AUS, CAN appear in raw XML (Niamh Hoare, Orla Hoare, Torun Joergensen, Rose FreedmanRiles, Savanna Sweeney, Amy Dufty, Saskia Edmunds Boerschke)
  Why: These countries are not in the EYOC allowlist, so exclusion is expected and correct per normalization rules
  Next: Confirm this is intentional exclusion of guest nations
- [low] `name` Name formatting inconsistency (parser_bug=false, source_limitation=false)
  CSV: Appears as 'Astrid Faber Fengergroen' in CSV
  Raw: FengerGroen listed as single word in raw XML
  Why: Minor formatting difference in compound surname handling
  Next: Verify name normalization rules for compound surnames
- [low] `other` Gender classification in raw XML (parser_bug=false, source_limitation=true)
  CSV: Correctly classified as W18 class
  Raw: Class element shows sex='M' but Name is 'Women 18'
  Why: Raw XML has inconsistent gender attribute, but CSV correctly interprets the class name
  Next: Verify parser correctly prioritizes class name over sex attribute

### Notable Matches

- Lotta Marit Luethi correctly extracted as winner with 781 seconds
- Tied positions (3rd place tie between Venla Mennala and Lenia Grimm) correctly handled
- Status codes properly normalized (MissingPunch -> MP, DidNotFinish -> DNF)
- Time conversions accurate (XML seconds match CSV time_seconds)
- Country normalization working correctly (Repubblica Ceca -> CZE, Regno Unito -> GBR)
- Bib numbers and ranks match between raw and CSV data
- Non-finishing statuses correctly preserved with appropriate time data

## 2026/02-long-results-eventor.xml [M16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2026/long.csv`
- Classes: `M16`
- Summary: CSV extraction correctly matches the raw XML source with proper normalization applied

### Issues

- None reported.

### Notable Matches

- Daniel Sanz (ESP) correctly extracted as rank 1 with 2505 seconds
- Class 'Men 16' properly normalized to 'M16'
- Country codes correctly normalized (ESP, POL, SUI, CZE, etc.)
- Non-EYOC countries (USA, NZL, AUS, CAN) properly excluded from CSV as expected
- Status values correctly mapped: OK, MissingPunch->MP, DidNotFinish->DNF
- Time values properly converted from XML seconds to integer seconds
- Names correctly formatted in 'Given Surname' order
- Tied ranks (43rd place) handled correctly with both competitors shown
- Missing punch and DNF statuses properly extracted with appropriate time handling

## 2026/02-long-results-eventor.xml [M18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2026/long.csv`
- Classes: `M18`
- Summary: CSV data accurately represents the M18 class results from the XML source with proper normalization applied

### Issues

- None reported.

### Notable Matches

- Martin Bulicka (CZE) correctly shows as winner with 3211 seconds (53:31)
- Class label 'Men 18' properly normalized to 'M18'
- All country codes correctly normalized (e.g., 'Repubblica Ceca' -> 'CZE', 'Germania' -> 'GER')
- Names properly formatted as 'Given Surname' (e.g., 'Bulicka, Martin' -> 'Martin Bulicka')
- Status values correctly mapped: 'OK', 'MissingPunch' -> 'MP', 'DidNotFinish' -> 'DNF', 'DidNotStart' -> 'DNS'
- Time conversions accurate: XML <Time>3211</Time> matches CSV time_seconds=3211
- Non-EYOC countries (USA, AUS, NZL) correctly excluded from normalized CSV as expected
- All 102 finished competitors plus 7 non-finishers properly represented
- Bib numbers, ranks, and split times align between source and CSV data

## 2026/02-long-results-eventor.xml [W16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2026/long.csv`
- Classes: `W16`
- Summary: The CSV extraction correctly represents the W16 class results from the XML source, with proper normalization of class names, countries, statuses, and exclusion of non-allowlisted nations

### Issues

- None reported.

### Notable Matches

- Sara Delic (CRO) correctly extracted as winner with 2987 seconds
- Class name 'Women 16' properly normalized to 'W16'
- Countries correctly normalized: 'Repubblica Ceca' -> 'CZE', 'Regno Unito' -> 'GBR'
- Non-allowlisted countries (NZL, USA, AUS) properly excluded from CSV as expected
- Special statuses correctly handled: MP for Deirbhile Hassett, DNF for Bethan Buckley
- Tied positions (rank 21, rank 70) correctly preserved from source
- All 95 finishers plus 2 non-finishers properly extracted with correct bib numbers and times

## 2026/02-long-results-eventor.xml [W18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2026/long.csv`
- Classes: `W18`
- Summary: The CSV extraction accurately represents the W18 class results from the XML source with proper normalization applied

### Issues

- None reported.

### Notable Matches

- Winner Brina Kolner (SLO) correctly extracted with 3284 seconds and rank 1
- All OK finishers properly ranked 1-97 with correct times and countries
- Missing punch (MP) athletes correctly shown without ranks: Saule Traubaite, Wilma Rosen, Ofri Yacobi, Jasna Starovic
- DNF athletes properly recorded: Helene Scheele (0 seconds), Ofer Svorai (7331 seconds)
- DNS athlete Zina Macajova correctly shown with 0 seconds and no rank
- Country normalization working correctly: 'Regno Unito' → 'GBR', 'Svezia' → 'SWE', etc.
- Name normalization applied properly: 'Szakal Biro, Sara' → 'Sara Szakal Biro'
- Tied ranks handled correctly: positions 44 (Sofie Holm Nedrebo and Emma Barriere) and 74 (Misa Andrejc and Jule Weigert)
- All times converted correctly from XML seconds to CSV integer seconds
- Class correctly normalized from 'Women 18' to 'W18'

## 2026/03-relay-results-eventor.xml [M16]

- Verdict: `review`
- Confidence: `medium`
- Related CSVs: `2026/relay.csv`
- Classes: `M16`
- Summary: The CSV correctly extracts most relay data but excludes guest nations (NZL, USA, AUS) as expected. However, there are some concerns about DNF status handling and team completion logic that need review.

### Issues

- [medium] `status` Inconsistent DNF status assignment for incomplete teams (parser_bug=true, source_limitation=false)
  CSV: Croatia 1: DNF status, total_time_seconds=3152. Turkiye 1: DNF status, total_time_seconds=8777 with all 3 leg times populated.
  Raw: Croatia 1: Only leg 1 completed (Karlo Trinajstic, 3152s), no leg 2 or 3 runners listed. Turkiye 1: All 3 legs completed with times and OK status per leg.
  Why: Croatia 1 appears to be a genuine DNF (incomplete team), but Turkiye 1 has all legs completed yet still marked DNF. The raw source shows leg 1 as 'DidNotFinish' but legs 2-3 as 'OK'.
  Next: Review DNF logic - Turkiye 1 may should be OK status since all legs completed, or clarify if leg 1 DNF propagates to team DNF
- [low] `missing-row` Expected exclusion of guest nations (parser_bug=false, source_limitation=false)
  CSV: These teams are absent from the CSV
  Raw: New Zealand 1 (NZL), Australia 1 (AUS), USA 1 (USA) teams present in raw XML with complete results
  Why: This is expected behavior per normalization rules - non-EYOC countries are intentionally excluded
  Next: No action needed - this is correct normalization
- [low] `other` USA team incomplete in raw source (parser_bug=false, source_limitation=false)
  CSV: Team not included (correctly excluded as non-EYOC)
  Raw: USA 1 team shows only 2 legs completed (Alexander Eriksson, Mark Fey), no leg 3 runner or time
  Why: Even if included, this team would be incomplete, but exclusion is correct anyway
  Next: No action needed - correct exclusion

### Notable Matches

- CZE Czechia 1 correctly extracted: rank 1, 4925s total, all leg names and times match
- FIN Finland 1 correctly extracted: rank 2, 4935s total, proper leg breakdown
- ESP Spain 1 correctly extracted: rank 3, 5238s total, all Spanish names properly formatted
- Country codes properly normalized: ESP, DEN, FRA, UKR, BEL, SUI, GER, ITA, GBR, SVK, HUN, POL, LTU, IRL, SLO, LAT, BUL, EST, AUT, ISR, POR, CRO, TUR
- All completed teams (ranks 1-23) have proper total times matching sum of leg times
- Names properly formatted from XML structure (Family/Given) to 'Given Family' format

## 2026/03-relay-results-eventor.xml [M18]

- Verdict: `review`
- Confidence: `medium`
- Related CSVs: `2026/relay.csv`
- Classes: `M18`
- Summary: The CSV correctly extracts most teams but excludes several guest nations (USA, NZL, AUS) that appear in the raw source, which is expected per normalization rules. However, Spain appears with MP status when the raw shows MissingPunch, which needs verification.

### Issues

- [low] `missing-row` USA team excluded from CSV (parser_bug=false, source_limitation=false)
  CSV: No USA team present in CSV
  Raw: United States 1 team with Erik Fey, Nathan Hinds, Samuel Nickolas Sunko, total time 9699 seconds
  Why: USA is not in the EYOC allowlist so exclusion is expected per normalization rules
  Next: Confirm USA is intentionally excluded as non-EYOC nation
- [low] `missing-row` New Zealand team excluded from CSV (parser_bug=false, source_limitation=false)
  CSV: No NZL team present in CSV
  Raw: New Zealand 1 team with Adam Landels, Arya Chebbi, Max Franks, total time 10096 seconds
  Why: NZL is not in the EYOC allowlist so exclusion is expected per normalization rules
  Next: Confirm NZL is intentionally excluded as non-EYOC nation
- [low] `missing-row` Australia team excluded from CSV (parser_bug=false, source_limitation=false)
  CSV: No AUS team present in CSV
  Raw: Australia 1 team with Oliver Bishop (MissingPunch), Matthew Slater, Benjamin Mansell (DidNotStart)
  Why: AUS is not in the EYOC allowlist so exclusion is expected per normalization rules
  Next: Confirm AUS is intentionally excluded as non-EYOC nation
- [medium] `status` Spain status shows MP instead of MissingPunch (parser_bug=false, source_limitation=false)
  CSV: Spain team shows status=MP
  Raw: Spain leg 3 shows <Status>MissingPunch</Status>
  Why: MP appears to be correct abbreviation for MissingPunch, but should verify this normalization
  Next: Verify MP is correct normalization for MissingPunch status

### Notable Matches

- Finland 1 correctly shows rank 1, total 6001s with Vilho Hietala (1948s), Joakim Savinainen (2036s), Veeti Viippola (2017s)
- Czechia 1 correctly shows rank 2, total 6087s with proper leg times and runner names
- France 1 correctly shows rank 3, total 6405s matching raw source calculations
- All EYOC-eligible countries properly extracted with correct team names, runner names, and times
- Country codes properly normalized (e.g., Czech Republic -> CZE, Great Britain -> GBR)
- Individual leg times correctly extracted from XML structure for all teams

## 2026/03-relay-results-eventor.xml [W16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2026/relay.csv`
- Classes: `W16`
- Summary: The CSV correctly extracts all W16 relay teams from the XML source with accurate data normalization

### Issues

- None reported.

### Notable Matches

- Croatia 1 wins with 5488 seconds total time (1:31:28), matching XML OverallResult
- Czechia 1 second with 5969 seconds, correctly shows 481 seconds behind winner
- Country normalization works correctly: 'Croazia' -> 'CRO', 'Repubblica Ceca' -> 'CZE', 'Regno Unito' -> 'GBR'
- Status handling correct: Hungary 1 shows 'MP' for MissingPunch, Ireland 1 shows 'MP' for leg 3 MissingPunch
- Belgium 1 correctly shows DNF status with only leg 1 completed (2339 seconds)
- Denmark 1 correctly shows DNS status with leg 3 DidNotStart (total 4435 seconds for 2 legs)
- Non-EYOC countries (New Zealand, United States, Australia) correctly excluded from CSV as expected
- Individual leg times match XML: Croatia leg 1 (1923s), leg 2 (1760s), leg 3 (1805s)
- Names properly normalized: 'Rannou Serine, Violette' -> 'Violette Rannou Serine'

## 2026/03-relay-results-eventor.xml [W18]

- Verdict: `fail`
- Confidence: `high`
- Related CSVs: `2026/relay.csv`
- Classes: `W18`
- Summary: Multiple critical issues found: missing teams, incorrect country codes, and wrong team names

### Issues

- [high] `missing-row` New Zealand 1 team completely missing from CSV (parser_bug=true, source_limitation=false)
  CSV: No row for New Zealand team found in CSV
  Raw: New Zealand 1 team with bib 329, finished 20th with total time 9302 seconds
  Why: Complete team missing despite having full results in raw source
  Next: Check parser logic for handling non-EYOC countries - NZL should be excluded but team appears to have completed the race
- [high] `missing-row` Australia 1 team completely missing from CSV (parser_bug=true, source_limitation=false)
  CSV: No row for Australia team found in CSV
  Raw: Australia 1 team with bib 322, partial results with legs 1-2 completed
  Why: Team missing despite having partial results in raw source
  Next: Check parser logic for handling non-EYOC countries and incomplete teams
- [medium] `country` Incorrect country code for Denmark (parser_bug=true, source_limitation=false)
  CSV: DEN used in CSV
  Raw: Country code="DEN" in raw XML
  Why: Should be DNK according to EYOC countries list, not DEN
  Next: Update country normalization mapping DEN -> DNK
- [medium] `name` Incorrect team name normalization for Denmark (parser_bug=true, source_limitation=false)
  CSV: Astrid Faber Fengergroen
  Raw: Team name: Denmark 1, Runner: FengerGroen
  Why: Name appears to have incorrect spacing/capitalization
  Next: Review name normalization for compound surnames

### Notable Matches

- Czechia 1 team correctly shows 1st place with 6458 total seconds
- Sweden 1 team correctly shows 2nd place with 6487 total seconds
- Hungary 1 team correctly shows 3rd place with 6768 total seconds
- Status codes correctly mapped: OK, DNF, MP, DNS
- Individual leg times correctly extracted for completed teams
- Most country codes correctly normalized (CZE, SWE, HUN, etc.)
