# OpenRouter Independent Data Audit

Generated: 2026-07-01T11:26:11.862672+00:00
Model: `anthropic/claude-sonnet-4`
Prompt: `scripts/independent_data_audit/openrouter_audit_prompt.txt`

## Summary

- Raw sources audited: 97
- `pass` verdicts: 62
- `review` verdicts: 34
- `fail` verdicts: 1
- High-severity issues: 33
- Medium-severity issues: 40
- Low-severity issues: 50

## 2002/eyoc2002.htm

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2002/long.csv`, `2002/relay.csv`, `2002/sprint.csv`
- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All major data points match correctly despite some expected formatting differences.

### Issues

- [low] `name` Minor name variations in relay data (parser_bug=false, source_limitation=true)
  CSV: Sara Luscher in relay, Sara Luescher in individual
  Raw: LUSCHER Sara vs LUESCHER Sara in individual results
  Why: Slight spelling inconsistency between relay and individual sections, but both refer to the same Swiss athlete
  Next: Accept as source-level variation - common in multi-format HTML documents
- [low] `name` Accent handling variations (parser_bug=false, source_limitation=false)
  CSV: Dorota Kosinska, Adrienn Csiszar without accents
  Raw: KOSIÑSKA Dorota with HTML entity, CSISZÁR Adrienn with accent
  Why: Expected normalization of accents and HTML entities as documented in normalization rules
  Next: No action needed - proper accent normalization applied

### Notable Matches

- Sprint W16 winner Sara Luescher 14.54 → 894 seconds correctly converted
- Long M18 tie at rank 4 (Pogorelovas and Kowalczyk both 39.13) properly preserved
- Relay team compositions match source data with proper leg time conversions
- Hungarian athletes correctly included as host country in abbreviated 2002 data
- Country normalization working correctly: BELORUSSIA → BLR, Ukraina → UKR
- Time conversions accurate: 32.44 → 1964 seconds, 89.15 → 5355 seconds
- Proper handling of NKL (non-classified) status in relay results excluded from clean CSV
- Class filtering working: only M16, M18, W16, W18 classes extracted as expected

## 2003/eyoc2003.htm

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2003/long.csv`, `2003/relay.csv`, `2003/sprint.csv`
- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All major data points match correctly.

### Issues

- [low] `name` Minor name normalization differences (parser_bug=false, source_limitation=false)
  CSV: Jana Krsiakova, Sona Berzinska
  Raw: Kriaková Jana vs Krsiakova Jana, Berinská Soňa vs Berzinska Sona
  Why: Accent removal and transliteration differences are expected normalization artifacts
  Next: No action needed - this is expected normalization behavior
- [low] `country` Country code normalization (parser_bug=false, source_limitation=false)
  CSV: SRB, BLR, LAT
  Raw: Serbia and Montenegr SCG, Belarusia BLR, Latvija LAT
  Why: Country names properly normalized to standard codes, including handling of truncated 'Serbia and Montenegr'
  Next: No action needed - correct normalization

### Notable Matches

- Sprint W16 winner Iwona Wicha (POL) with time 10.17,6 correctly converted to 618 seconds
- Long M18 winner Csaba Gösswein (HUN) with time 49.55 correctly converted to 2995 seconds
- Relay W16 winner Switzerland with total time 82.45 correctly converted to 4965 seconds
- All rank positions match exactly between raw source and CSV
- DSQ/DISQ statuses properly excluded from clean CSV as expected
- Mixed relay teams properly excluded from clean CSV as expected
- Time conversions from MM.SS format to seconds are accurate throughout
- Country normalizations like 'Czech republic' → 'CZE' applied correctly
- Name order flips from 'SURNAME Given' to 'Given Surname' handled properly

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
- Name normalization: 'Malgorzata Kosinska' properly handled despite accent variations
- Status handling: MP, DNF, DNS entries correctly preserved in relay data
- Class filtering: Only M16, M18, W16, W18 classes extracted as expected
- Non-European countries like Kazakhstan excluded from clean CSVs as intended

## 2005/eyoc2005.htm

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2005/long.csv`, `2005/relay.csv`, `2005/sprint.csv`
- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All major results sections (sprint, long, relay) are correctly parsed with appropriate time conversions, name formatting, and country normalization.

### Issues

- None reported.

### Notable Matches

- Sprint W16 winner Dorottya Peley (HUN) correctly shows 12.01,4 → 721 seconds
- Long M18 winner Stepan Kodeda (CZE) correctly shows 67.22 → 4042 seconds
- Relay W16 Czech team correctly combines Hlavova (29.24) + Prochazkova (29.07) + Bochenkova (30.43) = 89.14 total
- Names properly normalized: 'Proch�zkov� Michaela' → 'Michaela Prochazkova'
- Countries properly normalized: 'Czech Republic' → 'CZE', 'Great Britain' → 'GBR'
- DSQ statuses correctly captured for several athletes across all disciplines
- Mixed relay teams appropriately excluded from clean CSV as non-European composite teams
- Time format conversion accurate: '12.01,4' interpreted as 12 minutes 1.4 seconds = 721 seconds

## 2006/2006_relay_m16.txt

- Verdict: `review`
- Confidence: `medium`
- Related CSVs: `2006/relay.csv`
- Summary: Generally accurate extraction with some normalization concerns around country codes, name formatting, and MP status handling

### Issues

- [medium] `country` SCG country code normalization to SRB (parser_bug=false, source_limitation=false)
  CSV: SRB,Team SCG 69
  Raw: Team SCG 69 with STEVANOVIC, Marko etc.
  Why: Raw shows 'SCG' (Serbia and Montenegro) but CSV shows 'SRB' (Serbia). In 2006, SCG was still the official code before Montenegro independence.
  Next: Verify if SCG->SRB normalization is appropriate for 2006 data or if SCG should be preserved
- [medium] `country` ROM country code normalization to ROU (parser_bug=false, source_limitation=false)
  CSV: ROU,Team ROM 61
  Raw: Team ROM 61
  Why: Raw shows 'ROM' but CSV shows 'ROU'. Both are valid codes for Romania, but should verify consistency with normalization rules.
  Next: Confirm ROM->ROU normalization is intended and consistent
- [low] `name` Accent handling in Czech names (parser_bug=false, source_limitation=false)
  CSV: Stipan Zimmermann and Milos Nykodym
  Raw: Zimmermann, Štìpán and Nykodým, Miloš
  Why: Accents removed/simplified in normalization, which is expected but worth noting
  Next: Acceptable normalization artifact
- [low] `name` Name case normalization (parser_bug=false, source_limitation=false)
  CSV: Tadas Vidzikauskas
  Raw: VIDZIKAUSKAS, TADAS and other all-caps names
  Why: All-caps names properly converted to title case with order flip
  Next: Acceptable normalization
- [medium] `status` MP status interpretation for incomplete teams (parser_bug=false, source_limitation=false)
  CSV: Both teams have status=MP with some missing leg times
  Raw: Team ESP 21 and Team ITA 43 show MisPunch for individual legs
  Why: Teams with mispunching legs correctly marked as MP, but should verify if partial times should be preserved or blanked
  Next: Verify MP handling policy for teams with partial completion

### Notable Matches

- SUI team correctly extracted with all three leg times: 1810, 1883, 1718 seconds
- LAT team properly shows 5798 total seconds matching 1:36:38 raw time
- Rank order 1-18 correctly preserved for completed teams
- Team names like 'Team SUI 1' and 'Team LAT 94' properly extracted
- Individual leg times correctly converted from MM:SS to seconds (e.g., 0:30:10 -> 1810)
- Names properly flipped from 'Surname, Given' to 'Given Surname' format
- MP teams correctly excluded from ranking but included in data

## 2006/2006_relay_m18.txt

- Verdict: `review`
- Confidence: `medium`
- Related CSVs: `2006/relay.csv`
- Summary: Most data extracted correctly, but several issues need review including name normalization problems, potential time assignment errors, and questionable MP status handling

### Issues

- [medium] `name` Corrupted relay leg 2 name for Slovenia team (parser_bug=false, source_limitation=true)
  CSV: leg2_name: (Jerica (Ak)) (Bernik)
  Raw: 2	0	(Bernik), (Jerica (AK)) (0)	1:41:58
  Why: The raw source shows a corrupted entry with ID 0 and parenthetical formatting that suggests missing or placeholder data. The CSV normalized this to a name format, but this appears to be corrupted source data rather than a real athlete name.
  Next: Verify if this represents a real athlete or if it should be handled as missing/corrupted data
- [medium] `time` Duplicate time value for Slovenia leg 2 (parser_bug=false, source_limitation=true)
  CSV: Slovenia leg2_time_seconds: 6118, Ireland leg2_time_seconds: 6118
  Raw: Slovenia leg 2: 1:41:58, Ireland leg 2: 1:41:58
  Why: Both Slovenia and Ireland teams show identical leg 2 times of 1:41:58 (6118 seconds). Given Slovenia's corrupted leg 2 data, this may indicate the Slovenia time was incorrectly copied or the source has data corruption.
  Next: Verify if this time duplication is legitimate or indicates source corruption
- [low] `name` Accent removal in multiple names (parser_bug=false, source_limitation=false)
  CSV: Names normalized without accents
  Raw: Matìj -> Matij, Máté -> Mate, Bjørseth -> Bjorseth, Hägler -> Hagler, Jasiñski -> Jasinski, Tammemäe -> Tammemae, Röhnert -> Rohnert, Oľhava -> Olhava
  Why: Multiple names had accents removed during normalization, which is expected behavior but worth noting for completeness
  Next: No action needed - this is expected normalization
- [low] `country` ROM vs ROU country code normalization (parser_bug=false, source_limitation=false)
  CSV: country: ROU
  Raw: Team ROM 62
  Why: Raw source shows 'ROM' but CSV shows 'ROU'. This appears to be correct normalization to current IOC standard, but worth confirming the mapping is intentional.
  Next: Confirm ROM->ROU mapping is correct for 2006 data

### Notable Matches

- Russia team correctly extracted with all leg times: 40:06, 38:23, 39:20 matching 2406, 2303, 2360 seconds
- GBR team rank 2 with total 1:59:40 correctly converted to 7180 seconds
- MP status correctly assigned to Sweden (MisPunch on leg 3) and Slovenia (MisPunch on leg 1)
- All 20 completed teams properly ranked and extracted with correct total times
- Team names and numbers correctly preserved (e.g., 'Team RUS 66', 'Team GBR 33')
- Complex names like 'Sommerstad Juveli, Jonas' correctly normalized to 'Jonas Sommerstad Juveli'

## 2006/2006_relay_w16.txt

- Verdict: `review`
- Confidence: `medium`
- Related CSVs: `2006/relay.csv`
- Summary: Data extraction is mostly accurate with proper time conversions and name normalization, but there are two country code issues that need review: SCG->SRB conversion and a potential time discrepancy for POR team

### Issues

- [medium] `country` SCG country code converted to SRB without clear justification (parser_bug=false, source_limitation=false)
  CSV: country=SRB for Team SCG 71
  Raw: Team SCG 71 - Radulovic, Cosic, Karic (Serbian names)
  Why: SCG (Serbia and Montenegro) was converted to SRB, but this needs verification as SCG was a valid country code in 2006 before Montenegro's independence
  Next: Verify if SCG->SRB conversion is appropriate for 2006 data or if SCG should be preserved
- [low] `time` Minor time discrepancy in POR team total vs leg sum (parser_bug=false, source_limitation=true)
  CSV: total_time_seconds=7324 (2:02:04), leg times sum to 7323 (2:02:03)
  Raw: Place 15: 2:02:04 total, but leg 2 shows 2:02:03
  Why: 1-second difference between stated total time and sum of leg times, likely due to rounding or timing precision in source
  Next: Accept as minor timing precision issue from source data

### Notable Matches

- All 18 teams correctly extracted with proper W16 class assignment
- Time conversions accurate: 1:18:03 -> 4683 seconds for CZE team
- Name normalization working well: 'Jakobová, Adéla' -> 'Adela Jakobova'
- Accent removal consistent: 'Müllerová' -> 'Mullerova', 'Alizée' -> 'Alizee'
- Team numbers preserved correctly: 'Team CZE 1', 'Team RUS 67', etc.
- All leg times converted accurately from MM:SS format to seconds
- Ranks 1-18 correctly preserved in sequential order

## 2006/2006_relay_w18.txt

- Verdict: `review`
- Confidence: `medium`
- Related CSVs: `2006/relay.csv`
- Summary: Most data extracted correctly, but several issues need review: country code normalization (ROM->ROU, SCG->SRB), missing total times for MP teams, and some name accent handling discrepancies

### Issues

- [low] `country` Country code normalization ROM to ROU (parser_bug=false, source_limitation=false)
  CSV: ROU,Team ROM 64
  Raw: Team ROM 64
  Why: Raw shows ROM but CSV shows ROU - need to verify if this normalization is correct for Romania
  Next: Verify ROM->ROU normalization is intended for Romania
- [low] `country` Country code normalization SCG to SRB (parser_bug=false, source_limitation=false)
  CSV: SRB,Team SCG 72
  Raw: Team SCG 72
  Why: Raw shows SCG but CSV shows SRB - SCG was Serbia and Montenegro, need to verify this normalization
  Next: Verify SCG->SRB normalization is appropriate for 2006 timeframe
- [medium] `time` Missing total times for MP status teams (parser_bug=true, source_limitation=false)
  CSV: total_time_seconds field is empty for MP teams
  Raw: Teams GBR, SCG, POR show individual leg times but have MP/DSQ status
  Why: MP teams should probably still show total time if calculable from leg times, or have consistent handling
  Next: Review whether MP teams should have total times calculated or consistently blank
- [low] `name` Accent handling inconsistencies (parser_bug=false, source_limitation=true)
  CSV: Names show accent removal but inconsistent patterns
  Raw: Bjørgul vs Bjorgul, Péley vs Peley, Koós vs Koos
  Why: Some accents removed (ø->o, é->e, ó->o) while others preserved - should be consistent
  Next: Document accent handling policy or ensure consistent normalization
- [low] `time` Missing leg2 time for GBR team (parser_bug=false, source_limitation=false)
  CSV: leg2_time_seconds is empty
  Raw: Taylor, Catherine (2112214) MisPunch
  Why: Raw shows MisPunch for leg 2, CSV correctly leaves time blank
  Next: Confirm this is correct handling for mispunch legs

### Notable Matches

- Rank 1 NOR team total time 1:35:15 = 5715 seconds correctly calculated
- Individual leg times correctly converted: 0:35:05 = 2105 seconds
- Team names preserved correctly: Team NOR 52, Team HUN 41, etc.
- MP status correctly assigned to teams with mispunches/disqualifications
- Name order normalized correctly: Nilsen, Inger Liv -> Inger Liv Nilsen
- All 17 ranked teams plus 3 MP teams extracted (20 total teams)

## 2006/eyoc2006.htm

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2006/long.csv`, `2006/sprint.csv`
- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All times, names, countries, and rankings match the source data.

### Issues

- None reported.

### Notable Matches

- W16 sprint winner Adela Jakobova (CZE) correctly converted from 11:35,5 to 695 seconds
- M18 long winner Christian Wartbichler (AUT) correctly converted from 0:55:08 to 3308 seconds
- Country normalization working correctly: SCG → SRB for Serbian competitors
- Name normalization applied consistently: Jakobová → Jakobova, Müllerová → Mullerova
- Accent removal and HTML entity decoding handled properly throughout
- All MisPunch statuses correctly excluded from CSV as expected
- Time format conversion accurate: lazarus format 12:01,5 = 12 minutes 1.5 seconds = 721 seconds
- Rankings preserved exactly as shown in raw source for both sprint and long distance events

## 2007/eyoc2007.htm

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2007/long.csv`, `2007/relay.csv`, `2007/sprint.csv`
- Summary: The extracted CSV data accurately represents the 2007 EYOC results from the raw HTML source. All individual and relay results are correctly parsed with proper time conversions, name normalization, and country standardization.

### Issues

- None reported.

### Notable Matches

- Sprint W16 winner Mirjam Pfister (SUI) correctly shows 12:52 → 772 seconds
- Long M18 winner Jakub Zimmermann (CZE) correctly shows 53:02 → 3182 seconds
- Relay W16 winning CZE team correctly shows 86:37 total with proper leg splits
- MP (mispunch) statuses correctly preserved for athletes like Magali Cordeiro-Mendes
- DSQ (disqualified) statuses correctly preserved for athletes like Patricia Roxana Carauoan
- Country normalization working properly: Czech Republic → CZE, Great Britain → GBR
- Name normalization handling accents and HTML entities correctly: Petrželová, Kršiaková
- Tied ranks properly handled (e.g., W16 sprint rank 3 tie between Réka Tóth and Malgorzata Wicha)
- Relay team compositions correctly extracted with proper leg runner assignments
- All time conversions from MM:SS format to seconds are mathematically correct

## 2008/eyoc2008.htm

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2008/long.csv`, `2008/relay.csv`, `2008/sprint.csv`
- Summary: The extracted CSV data accurately represents the raw source with proper normalization applied. All major data points match correctly.

### Issues

- [low] `name` Minor name variations in sprint results (parser_bug=false, source_limitation=true)
  CSV: Klingenberg (missing first name), Rafols (missing first name)
  Raw: Klingenberg, Ita (W16 sprint rank 30), Pol Rafols (M18 sprint rank 55)
  Why: Some names appear abbreviated in sprint results, likely due to space constraints in original formatting
  Next: Accept as-is since source appears to have abbreviated names in these instances
- [low] `name` Accent normalization variations (parser_bug=false, source_limitation=false)
  CSV: Hellmuller, Losch, Rohnert (accents removed)
  Raw: Hellmüller, Mirjam; Lösch, Susen; Röhnert, Karoline
  Why: Standard accent removal normalization applied consistently
  Next: No action needed - this is expected normalization

### Notable Matches

- Long distance results correctly extracted with proper time conversions (e.g., Emma Klingenberg 39:02 → 2342 seconds)
- Relay results properly parsed with correct team compositions and leg times for all classes
- Sprint results accurately captured with proper time conversions (e.g., Tereza Novotna 11:01 → 661 seconds)
- Country normalization working correctly (Czech Republic → CZE, Great Britain → GBR)
- Status codes properly identified including DNF and MP entries
- All class assignments (W16, W18, M16, M18) correctly mapped
- Tied rankings handled correctly (e.g., multiple athletes with same time getting same rank)
- Mixed relay class properly identified and excluded from individual results

## 2009/eyoc2009.htm

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2009/long.csv`, `2009/relay.csv`, `2009/sprint.csv`
- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All major results sections (sprint, long, relay) are correctly parsed with appropriate time conversions, country normalization, and name formatting.

### Issues

- None reported.

### Notable Matches

- Sprint W16: Sandrine Müller SUI 9:11 correctly converted to 551 seconds
- Long M18: Robert Merl AUT 1:00:25 correctly converted to 3625 seconds
- Relay W16: SUI team total 96:16 correctly converted to 5776 seconds with proper leg splits
- Country normalization: 'Czech Rep.' → 'CZE', 'Great Britain' → 'GBR' applied consistently
- Name normalization: 'LUESCHER' style names converted to proper case 'Luescher'
- Hungarian competitors properly identified with HUN country code
- MP (mispunch) and DNF statuses correctly preserved in relay results
- Tied ranks handled correctly (e.g., M16 sprint rank 2 shared by Schneider and Polovinko)
- All bib numbers correctly omitted as they appear to be internal reference numbers
- Time format 'mm:ss' consistently converted to integer seconds across all disciplines

## 2010/eyoc2010.htm

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2010/long.csv`, `2010/relay.csv`, `2010/sprint.csv`
- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All major results sections (sprint, long, relay) are correctly parsed with appropriate time conversions, country normalization, and name formatting.

### Issues

- None reported.

### Notable Matches

- Sprint W16 winner Sandrine Müller (SUI) correctly shows 13:01 → 781 seconds
- Long M16 winner Piotr Parfianowicz (POL) correctly shows 53:59 → 3239 seconds
- Relay W16 winner Switzerland team correctly shows 1:29:40 → 5380 seconds with proper leg splits
- Country normalization working correctly: 'CZECH REPUBLIC' → 'CZE', 'GREAT BRITAIN' → 'GBR'
- Name formatting properly applied: 'MÜLLER, Sandrine' → 'Sandrine Muller' with accent removal
- Tied ranks handled correctly (e.g., W16 sprint ranks 3-3, long ranks 21-21)
- DNF status properly captured in relay results for Latvia, Slovenia, Ireland teams
- Hungarian athletes correctly identified and included (e.g., Márton Kazal, Filoména Kovács)
- Mixed relay class not present in source, correctly omitted from relay CSV
- Time format conversion accurate throughout: MM:SS format → total seconds

## 2011/eyoc2011.htm

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2011/long.csv`, `2011/relay.csv`, `2011/sprint.csv`
- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All major results sections (sprint, long, relay) are correctly parsed with appropriate time conversions, name formatting, and country normalization.

### Issues

- None reported.

### Notable Matches

- Sprint W16 winner: Sandrine Müller (SUI) 11.35,8 → 696 seconds correctly converted
- Long M18 winner: Rudolfs Zernis (LAT) 54.59 → 3299 seconds correctly converted
- Relay W16 winner: Czech Republic team with correct leg splits and total time 100.15 → 6015 seconds
- Name normalization working: 'Boránková Karolína' → 'Karolina Borankova' with accent removal
- Country normalization working: 'Czech Republic' → 'CZE', 'Great Britain' → 'GBR'
- Status handling: MP entries correctly excluded from CSV output
- Hungarian athletes properly included with HUN country code
- Time format conversion: '12.01,8' correctly interpreted as 12:01.8 = 722 seconds for Grosberga

## 2012/eyoc2012.htm

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2012/long.csv`, `2012/relay.csv`, `2012/sprint.csv`
- Summary: The extracted CSV data accurately represents the 2012 EYOC results from the raw HTML source. All major data points including names, countries, times, and rankings are correctly captured with proper normalization applied.

### Issues

- None reported.

### Notable Matches

- Sprint W16 winner Angelika MACIEJEWSKA (POL) correctly extracted with 11:36 → 696 seconds
- Long M16 winner Mikkel AAEN (DEN) properly captured with 45:04 → 2704 seconds
- Relay W16 Czech Republic team correctly assembled with proper leg splits and total time 1:32:28 → 5548 seconds
- Country normalization working properly: 'Czech Republic' → 'CZE', 'Great Britain' → 'GBR', 'Russian Federation' → 'RUS'
- Name normalization applied consistently: 'MACIEJEWSKA' → 'MacIejewska', maintaining proper capitalization
- MP/DNF statuses correctly preserved in relay results for incomplete teams
- Hungarian athletes properly included with HUN country code despite being host nation
- Time conversions accurate throughout: sprint times like 11:36 correctly become 696 seconds
- Relay leg compositions match raw source data with proper athlete-to-leg assignments
- All major placings and time gaps preserved accurately across all disciplines

## 2013/eyoc2013.htm

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2013/long.csv`, `2013/relay.csv`, `2013/sprint.csv`
- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All major results sections (sprint, long, relay) are correctly parsed with appropriate time conversions, country normalization, and name formatting.

### Issues

- [low] `name` Inconsistent handling of 'The Netherlands' suffix (parser_bug=true, source_limitation=false)
  CSV: Nina Roothans 96 The
  Raw: Nina Roothans 96 THE NETHERLANDS
  Why: The country normalization appears to have truncated part of the name when processing 'THE NETHERLANDS'
  Next: Review country extraction logic to avoid contaminating name fields with country suffixes
- [low] `name` Special character handling in Lithuanian name (parser_bug=false, source_limitation=true)
  CSV: Jogvil? Susinskait?
  Raw: Jogvil? Susinskait? 96 LITHUANIA
  Why: Question marks appear to be replacement characters for accented letters, but this matches the source corruption
  Next: No action needed - source already contains replacement characters
- [low] `country` Macedonia country code normalization (parser_bug=false, source_limitation=false)
  CSV: MKD
  Raw: Milovoj Velinovikj MECEDONIA
  Why: Correctly normalized misspelled 'MECEDONIA' to MKD, but worth noting the source typo
  Next: No action needed - correct normalization applied

### Notable Matches

- Sprint W16 winner Simona Aebersold correctly parsed with 12:27 → 747 seconds
- Long M18 winner Tobia Pezzati correctly parsed with 46:26 → 2786 seconds
- Relay teams properly assembled with correct leg splits and total times
- Hungarian athletes correctly identified and normalized (e.g., 'Mate Dalos 97 HUNGARY' → 'HUN, Mate Dalos')
- MP (mispunch) and DNS statuses correctly preserved in relay results
- Country normalization working well (SWITZERLAND→SUI, GREAT BRITAIN→GBR, etc.)
- Time formats consistently converted from MM:SS to total seconds
- Rank ties properly handled (e.g., W16 sprint rank 14 tie, W18 long rank 19 tie)

## 2014/results-long.pdf

- Verdict: `review`
- Confidence: `low`
- Related CSVs: `2014/long.csv`
- Summary: Cannot verify extraction accuracy due to missing raw source text from PDF file

### Issues

- [high] `source-limitation` PDF source text unavailable for verification (parser_bug=false, source_limitation=true)
  CSV: 404 rows extracted with high confidence from 2014/results-long.pdf
  Raw: [no raw text extracted]
  Why: The PDF file could not be rendered as text, making it impossible to verify the accuracy of the extracted data against the source
  Next: Manual verification of PDF content against CSV extraction required

### Notable Matches

- CSV shows reasonable structure with 4 classes (M16, M18, W16, W18) and expected European countries
- Time values appear reasonable for long distance orienteering (45-180+ minutes)
- Rankings appear sequential within each class
- All confidence values marked as 'high' suggesting clean source data
- Country codes follow expected EYOC European federation normalization

## 2014/results-relay.pdf

- Verdict: `review`
- Confidence: `low`
- Related CSVs: `2014/relay.csv`
- Summary: Cannot perform meaningful audit due to missing raw source text from PDF. CSV data appears structurally sound but requires manual verification against original PDF.

### Issues

- [high] `source-limitation` Raw PDF text extraction failed (parser_bug=false, source_limitation=true)
  CSV: 84 relay rows extracted with confidence=approx
  Raw: [no raw text extracted]
  Why: Cannot verify accuracy of extracted data without access to source content
  Next: Manual verification against original PDF required
- [medium] `rank` Inconsistent ranking sequences (parser_bug=true, source_limitation=false)
  CSV: M16 class shows rank 6 twice (DEN and AUT), rank 8 for GER before rank 6 AUT
  Raw: N/A - no raw text
  Why: Ranking sequence appears corrupted or source may have ties/corrections
  Next: Verify ranking sequence against original PDF
- [medium] `time` Missing leg times in multiple entries (parser_bug=false, source_limitation=true)
  CSV: Multiple entries missing leg2_time_seconds (e.g., TUR W16, EST M16, CRO W18, SLO M18)
  Raw: N/A - no raw text
  Why: Systematic missing times could indicate parsing issues or source data gaps
  Next: Check if source PDF has blank/missing times in these positions
- [low] `country` Potential country formatting inconsistency (parser_bug=true, source_limitation=false)
  CSV: M18 MDA shows 'Moldova Moldova' as team name
  Raw: N/A - no raw text
  Why: Team name appears to duplicate country name, may indicate parsing artifact
  Next: Verify team name format in original PDF
- [low] `country` Ireland country code inconsistency (parser_bug=false, source_limitation=true)
  CSV: W18 and M18 Ireland entries show 'lreland' (lowercase L) instead of 'Ireland'
  Raw: N/A - no raw text
  Why: Appears to be OCR error or typo in country field
  Next: Verify country name spelling in original PDF

### Notable Matches

- All 84 rows have confidence=approx, consistent with OCR/PDF extraction
- Class distribution appears reasonable: W16(21), M16(22), W18(24), M18(26)
- Status values properly normalized: OK, MP, DNF, DSQ as expected
- Country codes appear properly normalized to 3-letter IOF codes
- Time conversions to seconds appear mathematically consistent where present
- Name formatting follows Given Surname pattern consistently

## 2014/results-sprint.pdf

- Verdict: `review`
- Confidence: `low`
- Related CSVs: `2014/sprint.csv`
- Summary: Cannot verify extraction accuracy due to missing raw source text from PDF file

### Issues

- [high] `source-limitation` Raw PDF text extraction failed (parser_bug=false, source_limitation=true)
  CSV: 489 rows extracted across M16, W16, M18, W18 classes
  Raw: [no raw text extracted]
  Why: Unable to audit extraction accuracy without access to source content. PDF may require OCR or specialized parsing.
  Next: Re-attempt PDF text extraction or manual verification of sample rows
- [medium] `other` High confidence claimed despite PDF extraction issues (parser_bug=false, source_limitation=false)
  CSV: All rows marked confidence=high
  Raw: PDF text unavailable
  Why: If PDF required OCR or complex parsing, confidence should likely be 'approx' rather than 'high'
  Next: Verify confidence levels are appropriate for PDF extraction method used

### Notable Matches

- CSV structure follows expected schema with class, rank, status, bib, country, name, time_seconds, confidence, source_file
- Classes limited to allowed values: M16, W16, M18, W18
- All statuses are 'OK' which is plausible for sprint results
- Countries appear to be normalized European federations (FIN, CZE, SUI, etc.)
- Time values are in reasonable ranges for sprint orienteering (700-2000+ seconds)
- Names appear properly formatted in 'Given Surname' order with title case
- Ranks appear sequential with appropriate ties (e.g., M16 ranks 3,3,5 and 12,12,14)

## 2015/results-lf.pdf

- Verdict: `review`
- Confidence: `low`
- Related CSVs: `2015/long.csv`
- Summary: Cannot verify extraction accuracy due to missing raw source text from PDF file

### Issues

- [high] `source-limitation` Raw PDF source text unavailable for verification (parser_bug=false, source_limitation=true)
  CSV: 384 individual long-distance results extracted with high confidence
  Raw: [no raw text extracted]
  Why: The PDF file could not be rendered as text, making it impossible to verify the accuracy of the 384 extracted results across M16, M18, W16, and W18 classes
  Next: Manual verification of PDF content against CSV extraction, or attempt alternative PDF text extraction method

### Notable Matches

- All 384 rows marked with confidence=high and consistent source_file reference
- Proper class distribution: M16 (84), M18 (103), W16 (87), W18 (89) - reasonable for EYOC long distance
- Time values appear reasonable for long-distance orienteering (2329-7191 seconds = ~39min-2h)
- Country codes properly normalized to European federations only
- Names follow consistent Given Surname format with proper title casing
- Sequential ranking within each class with appropriate tied positions (e.g., M18 ranks 36, 45)

## 2015/results-relay.pdf

- Verdict: `review`
- Confidence: `low`
- Related CSVs: `2015/relay.csv`
- Summary: Cannot audit extracted data against raw source due to PDF text extraction failure. The CSV contains 95 relay results across 4 classes with plausible structure, but verification is impossible without source text.

### Issues

- [high] `source-limitation` PDF text extraction failed completely (parser_bug=false, source_limitation=true)
  CSV: 95 relay results extracted with high confidence
  Raw: [no raw text extracted]
  Why: Cannot verify any extracted data against source without readable text from PDF
  Next: Use alternative PDF extraction method or manual verification of sample entries
- [medium] `other` All entries marked as high confidence despite PDF extraction failure (parser_bug=true, source_limitation=false)
  CSV: All 95 rows have confidence=high
  Raw: No source text available for verification
  Why: High confidence rating seems inconsistent with complete source text extraction failure
  Next: Review confidence assignment logic for PDF parsing failures

### Notable Matches

- CSV structure follows expected relay schema with class, rank, country, team, times, and leg details
- Classes M16, M18, W16, W18 are appropriate for EYOC relay competition
- Country codes appear normalized to European federations (FRA, AUT, EST, etc.)
- Time values are in reasonable ranges for orienteering relay legs (1300-5500 seconds)
- Names follow Given Surname format with proper title casing
- Rankings appear sequential within each class (1-21 for M16, 1-27 for M18, etc.)

## 2015/results-sf.pdf

- Verdict: `review`
- Confidence: `low`
- Related CSVs: `2015/sprint.csv`
- Summary: Cannot verify extraction accuracy due to missing raw source text from PDF file

### Issues

- [high] `source-limitation` PDF source text unavailable for verification (parser_bug=false, source_limitation=true)
  CSV: 434 rows extracted with high confidence
  Raw: [no raw text extracted]
  Why: The PDF file could not be rendered as text, making it impossible to verify the accuracy of the extracted data against the source
  Next: Manual verification of PDF content against CSV extraction required
- [medium] `other` All extractions marked as high confidence despite PDF limitations (parser_bug=false, source_limitation=true)
  CSV: All 434 rows have confidence=high
  Raw: PDF rendering failed
  Why: Given that PDF text extraction failed, it's questionable whether high confidence is appropriate for all entries
  Next: Consider marking PDF-sourced data as approx confidence when text extraction fails

### Notable Matches

- Data structure appears consistent with EYOC sprint format: M16, M18, W16, W18 classes
- Time values are reasonable for sprint orienteering (600-1300 seconds range)
- Country codes follow expected European federation format (SUI, CZE, FIN, etc.)
- Ranking sequences appear logical with appropriate tie handling
- Bib numbers follow expected patterns for each class range
- Names follow normalized Given Surname format consistently

## 2016/results-long.pdf

- Verdict: `review`
- Confidence: `low`
- Related CSVs: `2016/long.csv`
- Summary: Cannot perform meaningful audit due to missing raw source text from PDF file

### Issues

- [high] `source-limitation` PDF source text extraction failed (parser_bug=false, source_limitation=true)
  CSV: 340 rows extracted with high confidence
  Raw: [no raw text extracted]
  Why: The PDF file could not be rendered as text, making it impossible to verify the accuracy of the extracted data against the source
  Next: Manual verification of PDF content against CSV data, or attempt alternative PDF text extraction method

### Notable Matches

- CSV contains 340 total rows across M16, M18, W16, W18 classes
- All extracted rows have confidence=high and proper source_file attribution
- Time values appear reasonable for long distance (2649-5994 seconds, roughly 44-100 minutes)
- Country codes follow expected European federation format (DEN, FIN, FRA, RUS, etc.)
- Names appear properly formatted in Given Surname order
- Ranks are sequential with appropriate handling of ties (e.g., M16 ranks 30,30,32)
- DNF entries properly show empty time_seconds values
- Classes match expected EYOC format (M16, M18, W16, W18)

## 2016/results-relay.pdf

- Verdict: `review`
- Confidence: `low`
- Related CSVs: `2016/relay.csv`
- Summary: Cannot audit extracted CSV data against raw source due to PDF text extraction failure. The CSV contains 88 relay rows across 4 classes with consistent formatting, but verification is impossible without source text.

### Issues

- [high] `source-limitation` PDF text extraction failed completely (parser_bug=false, source_limitation=true)
  CSV: 88 relay rows extracted with high confidence
  Raw: [no raw text extracted]
  Why: Cannot verify any extracted data against source without readable text from PDF
  Next: Use alternative PDF extraction method or manual verification of sample rows
- [medium] `name` Potentially truncated or corrupted names (parser_bug=true, source_limitation=false)
  CSV: Names like 'Knobloch-Esztergar', 'O'SULLIVAN-HOURIH', 'Vmccavana Eadaoin' appear incomplete
  Raw: N/A - no source text
  Why: Some names appear truncated or contain unusual formatting that suggests extraction issues
  Next: Verify these specific names against original PDF
- [low] `name` Inconsistent name formatting patterns (parser_bug=false, source_limitation=true)
  CSV: Mix of 'Given Surname' and potentially reversed names like 'Ivanow Tzwetan'
  Raw: N/A - no source text
  Why: Without source verification, cannot confirm if name order normalization was applied correctly
  Next: Spot-check name formatting against original PDF

### Notable Matches

- All 88 rows have consistent relay schema with class, rank, country, team, and 3 leg times
- Time values appear reasonable for relay races (7000-14000 seconds total)
- Country codes are properly normalized to European federations
- Classes M16, M18, W16, W18 are correctly represented
- All rows marked with 'high' confidence and proper source file reference

## 2016/results-sprint.pdf

- Verdict: `review`
- Confidence: `low`
- Related CSVs: `2016/sprint.csv`
- Summary: Cannot verify extraction accuracy due to missing raw PDF text, but CSV shows concerning patterns including malformed names, suspicious bib numbers, and potential OCR artifacts that need validation

### Issues

- [high] `name` Multiple malformed names suggest OCR corruption (parser_bug=false, source_limitation=true)
  CSV: Names like 'Spektorsfricis', 'Repsysadomas', 'Lorenztimon', 'Dzalbsedijs', 'Upitisuldis', 'Ruoholaakseli', 'Hirsotakar', 'Iinkfvichigor'
  Raw: [no raw text available]
  Why: These appear to be corrupted single-word names missing spaces or proper formatting, suggesting systematic OCR issues
  Next: Verify against original PDF to confirm if these are OCR artifacts or actual name formats
- [medium] `other` Suspicious bib number in M18 class (parser_bug=false, source_limitation=true)
  CSV: M18 class has bib '3481' for 'Iinkfvichigor' while others are 3-digit
  Raw: [no raw text available]
  Why: Bib number 3481 is inconsistent with the 3-digit pattern used elsewhere, may indicate OCR misread
  Next: Check original PDF for correct bib number
- [medium] `name` Names with apparent formatting issues (parser_bug=false, source_limitation=true)
  CSV: Names like 'Smulems de', 'Eerolalotta', 'Korvellorely', 'Georgievaniya', 'Myroniukalina', 'Gokculsumeyra'
  Raw: [no raw text available]
  Why: These names appear to have spacing or word-order issues that may indicate OCR problems
  Next: Verify name formatting against original PDF
- [low] `rank` Potential rank sequence issue in W18 (parser_bug=true, source_limitation=false)
  CSV: W18 shows rank 69 followed by rank 71, then rank 69 again, then rank 72
  Raw: [no raw text available]
  Why: Rank sequence shows 69, 71, 69, 72 which may indicate a parsing or source formatting issue
  Next: Check if this reflects tied ranks or is a parsing error
- [low] `source-limitation` All confidence marked as 'approx' for PDF source (parser_bug=false, source_limitation=true)
  CSV: Every row has confidence=approx
  Raw: [no raw text available]
  Why: Consistent 'approx' confidence suggests OCR-derived data which explains name formatting issues
  Next: Document that this is OCR-derived data with expected quality limitations

### Notable Matches

- Standard European countries properly normalized (FRA, CZE, FIN, RUS, GBR, etc.)
- Time conversions appear consistent (619-1464 seconds range is reasonable for sprint)
- Class structure follows expected EYOC format (M16, M18, W16, W18)
- Rank sequences generally follow expected patterns with some ties
- DSQ status properly captured for disqualified competitors

## 2017/result-sprint.pdf

- Verdict: `review`
- Confidence: `low`
- Related CSVs: `2017/sprint.csv`
- Summary: Cannot perform meaningful audit due to missing raw source text from PDF file

### Issues

- [high] `source-limitation` Raw PDF source text unavailable for comparison (parser_bug=false, source_limitation=true)
  CSV: 391 rows extracted across M16, M18, W16, W18 classes
  Raw: [no raw text extracted]
  Why: Without the raw source text, cannot verify accuracy of extracted data, names, times, ranks, or countries
  Next: Re-extract PDF text or obtain alternative source format for proper audit

### Notable Matches

- CSV structure follows expected schema with class, rank, status, bib, country, name, time_seconds, confidence, source_file
- All classes (M16, M18, W16, W18) are represented with reasonable participant counts
- Time values appear consistent (700-1800 seconds range typical for sprint)
- Countries appear to be normalized European federations (POL, DEN, HUN, CZE, FRA, etc.)
- Status values follow allowed set (OK, DNF) with appropriate blank times for DNF
- Confidence consistently marked as 'high' suggesting clean source data
- Names appear properly formatted in 'Given Surname' order

## 2017/results-long.pdf

- Verdict: `review`
- Confidence: `low`
- Related CSVs: `2017/long.csv`
- Summary: Cannot perform meaningful audit due to missing raw source text from PDF file

### Issues

- [high] `source-limitation` Raw PDF text extraction failed (parser_bug=false, source_limitation=true)
  CSV: 394 rows extracted with high confidence
  Raw: [no raw text extracted]
  Why: Without the raw source text, cannot verify if extracted data matches the original PDF content
  Next: Re-attempt PDF text extraction or obtain alternative text format of source file

### Notable Matches

- CSV contains 394 rows across M16, M18, W16, W18 classes with reasonable distribution
- Time values appear consistent (2305-9255 seconds for finishers)
- Country codes follow expected European federation format
- Names follow normalized Given Surname format
- DNF entries properly have empty time_seconds fields
- All entries marked with high confidence level
- Bib numbers appear reasonable for EYOC competition format

## 2017/results-relay.pdf

- Verdict: `review`
- Confidence: `low`
- Related CSVs: `2017/relay.csv`
- Summary: Cannot audit extracted data against raw source due to PDF text extraction failure. The CSV contains 95 relay entries across 4 classes with reasonable structure, but verification is impossible without source text.

### Issues

- [high] `source-limitation` PDF text extraction failed completely (parser_bug=false, source_limitation=true)
  CSV: 95 relay entries extracted with high confidence
  Raw: [no raw text extracted]
  Why: Cannot verify any extracted data against source without readable text
  Next: Use alternative PDF extraction method or manual verification
- [medium] `other` Suspicious ranking gaps in some classes (parser_bug=true, source_limitation=false)
  CSV: M18 has rank 20 followed by unranked entries; W16 has rank 18 followed by unranked; W18 has rank 24 followed by unranked
  Raw: Cannot verify from source
  Why: Ranking sequences suggest possible missing entries or extraction issues
  Next: Verify complete extraction of all ranked teams from PDF
- [low] `name` Potential name truncation in some entries (parser_bug=true, source_limitation=false)
  CSV: Names like 'Florencio Garcia Go', 'Gustav Wiren Gonzal', 'Manuele Ren' appear truncated
  Raw: Cannot verify from source
  Why: Several names end abruptly suggesting possible extraction truncation
  Next: Check PDF for complete names and verify extraction accuracy
- [low] `other` Mixed gender names in M18 Serbia entry (parser_bug=true, source_limitation=false)
  CSV: M18 Serbia team has 'Olga Stanojevic' and 'Lenka Ciric' (female names) with 'Dusan Markovic'
  Raw: Cannot verify from source
  Why: Male relay class contains apparent female names, suggesting possible data corruption
  Next: Verify this is actually a Mixed relay or check for extraction error

### Notable Matches

- Class distribution appears reasonable: M16 (23 teams), M18 (28 teams), W16 (21 teams), W18 (25 teams)
- Country codes are properly normalized to European federations
- Time formats are consistently converted to integer seconds
- DNF status handling appears consistent with missing times
- Team names follow expected country-based patterns

## 2018/results-long.pdf

- Verdict: `review`
- Confidence: `low`
- Related CSVs: `2018/long.csv`
- Summary: Cannot perform meaningful audit due to missing raw source text from PDF file

### Issues

- [high] `source-limitation` Raw PDF text extraction failed (parser_bug=false, source_limitation=true)
  CSV: 377 rows extracted with high confidence
  Raw: [no raw text extracted]
  Why: Without access to the raw PDF content, cannot verify accuracy of extracted data including names, times, ranks, countries, or classes
  Next: Re-attempt PDF text extraction or obtain alternative source format for verification
- [medium] `other` High confidence rating despite extraction limitations (parser_bug=true, source_limitation=false)
  CSV: All 377 rows marked confidence=high
  Raw: PDF text unavailable
  Why: All extracted rows show high confidence despite PDF extraction failure, which may indicate overconfident parsing
  Next: Review confidence assignment logic for PDF sources with extraction issues

### Notable Matches

- Data structure appears consistent: 4 classes (M16, M18, W16, W18) with expected European countries
- Time values are reasonable for long distance orienteering (40-125 minutes converted to seconds)
- Ranking sequences appear continuous within each class
- Country codes follow expected EYOC European federation format
- Names follow normalized Given Surname format consistently

## 2018/results-relay.pdf

- Verdict: `review`
- Confidence: `low`
- Related CSVs: `2018/relay.csv`
- Summary: Cannot verify data accuracy due to unreadable PDF source, but CSV shows concerning anomalies including corrupted names and suspicious team naming patterns

### Issues

- [high] `name` Corrupted runner names containing event metadata (parser_bug=true, source_limitation=false)
  CSV: Multiple rows show '2018 Relay Mon 02-Jul-18 Eyoc' as runner name (M16 rank 13 leg3, M18 rank 15 leg3, W16 rank 13 leg3)
  Raw: [no raw text extracted]
  Why: Runner names appear contaminated with event date/title information, suggesting parser confusion between data fields
  Next: Re-examine PDF parsing logic to prevent event metadata from being extracted as runner names
- [medium] `country` Duplicated country names in team field (parser_bug=true, source_limitation=false)
  CSV: Team names show pattern like 'Czech Republic Czech Republic', 'Finland Finland', 'Russian Federati Russian Feder'
  Raw: [no raw text extracted]
  Why: Team field appears to duplicate country names, possibly indicating parser confusion between country and team columns
  Next: Review team name extraction logic to avoid country name duplication
- [medium] `country` Truncated country names (parser_bug=true, source_limitation=false)
  CSV: 'Russian Federati Russian Feder' appears truncated compared to expected 'Russian Federation'
  Raw: [no raw text extracted]
  Why: Country names appear cut off mid-word, suggesting field width limitations or parsing boundaries
  Next: Check field extraction boundaries to ensure complete country names
- [low] `source-limitation` Cannot verify data completeness or accuracy (parser_bug=false, source_limitation=true)
  CSV: 108 relay rows extracted across 4 classes
  Raw: [no raw text extracted]
  Why: PDF source unreadable prevents verification of extracted data against original
  Next: Attempt alternative PDF extraction methods or manual verification of source file

### Notable Matches

- Class distribution appears reasonable: M16(20), M18(28), W16(22), W18(21)
- Time values are in reasonable ranges for relay events (4000-9000+ seconds)
- Country codes follow expected EYOC European federation pattern
- Rank sequences appear consecutive within each class

## 2018/results-sprint.pdf

- Verdict: `review`
- Confidence: `low`
- Related CSVs: `2018/sprint.csv`
- Summary: Cannot verify extraction accuracy due to missing raw PDF text, but CSV data appears structurally sound with reasonable patterns

### Issues

- [high] `source-limitation` Raw PDF text unavailable for verification (parser_bug=false, source_limitation=true)
  CSV: 394 rows extracted with high confidence
  Raw: [no raw text extracted]
  Why: Cannot audit extraction accuracy without access to source content
  Next: Attempt PDF text extraction with different tools or manual verification
- [low] `other` All confidence values marked as 'high' despite PDF extraction issues (parser_bug=true, source_limitation=false)
  CSV: All 394 rows have confidence=high
  Raw: PDF text extraction failed
  Why: Confidence should potentially be 'approx' if PDF parsing was problematic
  Next: Review confidence assignment logic for PDF sources

### Notable Matches

- Extracted 394 individual sprint results across M16, M18, W16, W18 classes
- Rank sequences appear continuous and logical (M16: 1-94, M18: 1-104, W16: 1-94, W18: 1-84)
- Time progressions look reasonable within each class (M16: 618-1035s, M18: 724-1653s)
- Country codes properly normalized to European federations (FIN, CZE, SUI, etc.)
- Names appear in proper Given Surname format with title casing
- Status values consistently 'OK' which is typical for sprint results
- Tied ranks handled correctly (e.g., M16 rank 6 appears twice, next rank is 8)

## 2019/Long-eventor.xml [M16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2019/long.csv`
- Classes: `M16`
- Summary: All 102 M16 competitors from the XML source are correctly extracted with accurate ranks, times, countries, and names. Two DNF entries are properly handled.

### Issues

- None reported.

### Notable Matches

- Martin Simsa (CZE, rank 1, 46:41 = 2801s) correctly extracted as winner
- Jakub Chaloupsky (CZE, rank 2, 47:13 = 2833s) with proper time conversion
- Two DNF entries (Joe Hudd GBR, Jonas Jansen BEL) correctly marked with DNF status
- Country codes properly normalized: Czechia->CZE, Russian Federation->RUS, Great Britain->GBR
- Names correctly normalized from XML format: 'Urquizu Diego, Aimar' -> 'Aimar Urquizu Diego'
- Tied ranks handled correctly: both rank 45 entries (Kaloyan Atanasov BUL, Topias Kemppi FIN) with same time 1:08:35
- All 102 entries from XML numberOfEntries match CSV row count including DNFs
- Time format conversion accurate: XML '46:41' -> CSV 2801 seconds
- Complex names preserved: 'Oscar David Brom Jensen', 'Marco Anselmo di Stefano', 'Bora Ugur Ozkaranfil'

## 2019/Long-eventor.xml [M18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2019/long.csv`
- Classes: `M18`
- Summary: All extracted CSV rows accurately match the raw XML source data with proper normalization applied

### Issues

- None reported.

### Notable Matches

- Ferenc Jonas (HUN) correctly extracted as winner with 56:52 = 3412 seconds
- Tied ranks 11 and 33 properly handled for Janovsky/Ojala and Kristiansson/Arbuzov
- Country normalization working correctly: Czechia->CZE, Russian Federation->RUS, Great Britain->GBR
- Name order properly normalized from XML <Family>/<Given> to Given Family format
- Status codes correctly mapped: MisPunch->MP, DidNotFinish->DNF
- All 106 entries from XML properly accounted for in CSV (103 OK + 1 MP + 2 DNF)
- Time conversions accurate: 1:15:59 -> 4559 seconds for MP entry
- Bib numbers, ranks, and countries all match source data exactly

## 2019/Long-eventor.xml [W16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2019/long.csv`
- Classes: `W16`
- Summary: All W16 class data correctly extracted from XML source with accurate times, ranks, and competitor details

### Issues

- None reported.

### Notable Matches

- Winner Anna Karlova (CZE, bib 79) correctly shows 39:44 → 2384 seconds with rank 1
- Runner-up Alina Niggli (SUI, bib 58) correctly shows 40:54 → 2454 seconds with rank 2
- DNF status correctly captured for Mia Krtinic (SRB, bib 18) with partial time 1:34:08 → 5648 seconds
- Non-European competitors (New Zealand) correctly excluded from CSV as expected
- Country normalization working properly: 'Russian Federation' → 'RUS', 'Czechia' → 'CZE'
- Name order normalized correctly: XML 'Bluma, Aiga Irbe' → CSV 'Aiga Irbe Bluma'
- All 88 finished competitors plus 1 DNF properly extracted from 92 total entries

## 2019/Long-eventor.xml [W18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2019/long.csv`
- Classes: `W18`
- Summary: All 99 W18 competitors from the XML source are correctly extracted with accurate ranks, times, countries, and statuses. No material discrepancies found.

### Issues

- None reported.

### Notable Matches

- Winner Csilla Gardonyi (HUN) correctly shows 47:44 = 2864 seconds with rank 1
- Runner-up Elza Kuze (LAT) correctly shows 49:52 = 2992 seconds with rank 2
- Tied 48th place correctly handled: Feia Tsyvilska (UKR) and Anita Laanejoe (EST) both show 1:12:04 = 4324 seconds
- MP status correctly assigned to Anika Schwarze Chintapatla (GBR) with MisPunch in XML
- DNF statuses correctly assigned to 5 competitors with DidNotFinish in XML
- Country normalization working properly: Russian Federation → RUS, Great Britain → GBR, etc.
- Name normalization working: Family/Given XML structure converted to Given Surname format
- All 93 ranked finishers plus 6 non-finishers (1 MP + 5 DNF) = 99 total matches XML count

## 2019/Sprint-eventor.xml [M16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2019/sprint.csv`
- Classes: `M16`
- Summary: All 101 M16 competitors from the XML source are correctly extracted with accurate ranks, times, countries, and names. One MP (MisPunch) status is properly handled.

### Issues

- None reported.

### Notable Matches

- Winner Konstantin Kunckel (GER, 8:57 = 537s) correctly extracted as rank 1
- Tied ranks 2, 10, 14, 25, 27, 35, 37, 41, 44, 49, 55, 59, 61, 66, 68, 74, 82, 85, 91 all properly handled
- Country normalization working: 'Russian Federation' → 'RUS', 'Czechia' → 'CZE', 'Great Britain' → 'GBR'
- Name normalization working: 'Bernabeu carbonell' → 'Bernabeu Carbonell', compound names preserved
- Time conversion accurate: '8:57' → 537 seconds, '14:31' → 871 seconds
- MisPunch status correctly extracted for Berke Basoz (bib 579) with no rank assigned

## 2019/Sprint-eventor.xml [M18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2019/sprint.csv`
- Classes: `M18`
- Summary: All 106 M18 competitors from the XML source are correctly extracted with accurate ranks, times, countries, and statuses

### Issues

- None reported.

### Notable Matches

- Winner Stanislaw Kurzyp (POL) correctly extracted as rank 1 with 11:37 = 697 seconds
- Three-way tie at rank 11 (Janovsky, Barauskas, Elmblad) properly handled with same rank and times
- MP (MisPunch) status correctly extracted for Ciglis and Pompura with their finish times
- DSQ (Disqualified) status correctly extracted for Bjork with time 17:50 = 1070 seconds
- Country normalization working properly: CZE for Czech Republic, GBR for Great Britain, etc.
- Name order correctly normalized from XML Family/Given to Given Family format
- All 103 ranked finishers plus 3 non-finishers (2 MP, 1 DSQ) properly accounted for

## 2019/Sprint-eventor.xml [W16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2019/sprint.csv`
- Classes: `W16`
- Summary: All W16 competitors correctly extracted from XML source with accurate times, ranks, and statuses

### Issues

- None reported.

### Notable Matches

- Winner Marketa Mulickova (CZE) correctly shows 9:05 time = 545 seconds, rank 1
- Tied 3rd place Anna Karlova and Viktoria Mag both show 9:19 time = 559 seconds, rank 3
- MP status correctly assigned to Yana Ilieva (BUL) with MisPunch in XML
- Non-European competitors (New Zealand) correctly excluded from CSV as expected
- All country codes properly normalized (Czech Republic -> CZE, Russian Federation -> RUS, etc.)
- Names properly formatted from XML Family/Given structure to Given Surname order

## 2019/Sprint-eventor.xml [W18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2019/sprint.csv`
- Classes: `W18`
- Summary: All 98 W18 competitors correctly extracted with accurate ranks, times, countries, and names

### Issues

- None reported.

### Notable Matches

- Winner Malin Agervig Kristiansson (DEN) correctly shows 11:12 → 672 seconds with rank 1
- Tied ranks handled properly: positions 10, 27, 36, 40, 49, 54, 67, 74, 81, 84, 96 all show correct tied competitors
- Country normalization working: 'Russian Federation' → RUS, 'Great Britain' → GBR, 'Czechia' → CZE
- Name order correctly normalized: 'Kristiansson, Malin Agervig' → 'Malin Agervig Kristiansson'
- Complex names preserved: 'Misas Bernardino, Lucia' → 'Lucia Misas Bernardino', 'O Sullivan, Aoife' → 'Aoife O Sullivan'
- All 98 entries from XML properly extracted with no missing or extra rows

## 2019/result-relay.pdf

- Verdict: `review`
- Confidence: `low`
- Related CSVs: `2019/relay.csv`
- Summary: Cannot perform meaningful audit due to missing raw source text from PDF file. The extracted CSV data appears structurally sound with 78 relay teams across 4 classes, but verification against source is impossible.

### Issues

- [high] `source-limitation` Raw PDF text extraction failed (parser_bug=false, source_limitation=true)
  CSV: 78 relay rows extracted with high confidence
  Raw: [no raw text extracted]
  Why: Cannot verify any extracted data against source without readable raw text
  Next: Re-extract PDF text or obtain alternative source format for verification
- [medium] `country` Moldova country format inconsistency (parser_bug=true, source_limitation=false)
  CSV: M18 rank 25: country='Moldova, Republic of'
  Raw: Cannot verify from source
  Why: Country should be normalized to 'MDA' per normalization rules, not left as full formal name
  Next: Normalize Moldova country code to 'MDA'
- [low] `other` Tied rank handling (parser_bug=false, source_limitation=false)
  CSV: M18 has two teams at rank 14 (BEL and EST), then continues to rank 16
  Raw: Cannot verify from source
  Why: Need to verify if this tie and rank sequence matches the source document
  Next: Verify tie handling matches source when PDF becomes readable

### Notable Matches

- All 78 rows have consistent relay structure with 3 legs and total times
- Time calculations appear internally consistent (leg times sum to totals within reasonable rounding)
- Classes M16, M18, W16, W18 are all properly represented
- Most country codes appear properly normalized (FIN, RUS, SUI, CZE, etc.)
- Names follow expected 'Given Surname' format consistently
- All confidence levels marked as 'high' suggesting clean source data

## 2021/Long-eventor.xml [M16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2021/long.csv`
- Classes: `M16`
- Summary: The extracted CSV data accurately represents the M16 class results from the 2021 Long eventor.xml file. All 95 competitors are correctly captured with proper normalization of names, countries, times, and statuses.

### Issues

- None reported.

### Notable Matches

- Dan Bolehovsky (CZE) correctly placed 1st with 39:59 (2399 seconds)
- Hannes Mogensen (DEN) correctly placed 2nd with 40:10 (2410 seconds)
- Name normalization working correctly: 'De Clercq Rune' → 'Clercq Rune de'
- Country normalization working: 'Czechia' → 'CZE', 'Denmark' → 'DEN'
- Time conversion accurate: '39:59' → 2399 seconds, '40:10' → 2410 seconds
- Tied ranks handled correctly: Syrovy and Balabanov both at rank 42 with 58:59
- DSQ status correctly captured for 6 disqualified competitors
- All 89 finishers plus 6 DSQ entries = 95 total entries matching source

## 2021/Long-eventor.xml [M18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2021/long.csv`
- Classes: `M18`
- Summary: All extracted CSV rows accurately match the raw XML source data with proper normalization applied

### Issues

- None reported.

### Notable Matches

- Aarni Ronkainen (FIN) correctly extracted as rank 1 with 45:23 = 2723 seconds
- Mark Tutynin (RUS) correctly extracted as rank 2 with 46:01 = 2761 seconds
- Martin Vehus Skjerve (NOR) correctly extracted as rank 3 with 47:04 = 2824 seconds
- Tadas Dementavičius (LTU) correctly normalized to 'Tadas Dementavicius' removing diacritic
- Matīss Saulīte (LAT) correctly normalized to 'Matiss Saulite' removing diacritics
- Austris Kalniņš (LAT) correctly normalized to 'Austris Kalnins' removing diacritic
- Gustavs Staņa (LAT) correctly normalized to 'Gustavs Stana' removing diacritic
- Emīls Lazdāns (LAT) correctly normalized to 'Emils Lazdans' removing diacritics
- Adomas Časas (LTU) correctly normalized to 'Adomas Casas' removing diacritic
- Jürgen Joonas (EST) correctly normalized to 'Jurgen Joonas' removing diacritic
- All three DSQ entries (Anton Buschek, Antoine Mattart, Noel Braun) correctly extracted with empty time_seconds
- All 104 competitors from XML source properly represented in CSV (101 OK + 3 DSQ)
- Country codes properly normalized (e.g., 'Czechia' → 'CZE', 'Russian Federation' → 'RUS')
- Time conversions accurate throughout (e.g., '1:00:25' → 3625 seconds for Vit Cech)

## 2021/Long-eventor.xml [W16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2021/long.csv`
- Classes: `W16`
- Summary: The extracted CSV data accurately represents the W16 class results from the 2021 Long-eventor.xml source file with proper normalization applied

### Issues

- [low] `name` Minor name normalization differences (parser_bug=false, source_limitation=false)
  CSV: Names appear with accents removed in CSV
  Raw: Davidavičiūtė -> Davidaviciute, Činčikaitė -> Cincikaite, Ziaziulytė -> Ziaziulyte
  Why: Expected normalization artifact - accent removal is standard practice for compatibility
  Next: No action needed - this is expected normalization
- [low] `name` Complex Spanish name handling (parser_bug=false, source_limitation=false)
  CSV: Spanish names reordered to Given Surname format
  Raw: Faja sanjaume Guinedell -> Sanjaume Guinedell Faja, de MIguel Armisen Monica -> Miguel Armisen Monica de, Munoz del Campo Alba -> del Campo Alba Munoz
  Why: Parser appears to handle complex Spanish naming conventions reasonably well
  Next: No action needed - reasonable normalization of complex names

### Notable Matches

- Silva Kemppi (FIN) correctly extracted as winner with 35:25 -> 2125 seconds
- All 88 competitors properly extracted including tied 41st place (Daria Mikula and Giulia Gobber both at 58:50)
- DSQ status correctly captured for Laura Odor (HUN) with no time
- Time conversions accurate: 35:25 -> 2125 seconds, 1:59:00 -> 7140 seconds
- Country codes properly normalized: Czechia -> CZE, Russian Federation -> RUS, Turkiye -> TUR
- All ranks 1-87 plus DSQ entry correctly preserved
- Class W16 consistently applied to all entries

## 2021/Long-eventor.xml [W18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2021/long.csv`
- Classes: `W18`
- Summary: All W18 results correctly extracted from XML source with accurate times, ranks, names, and countries

### Issues

- None reported.

### Notable Matches

- Winner Salla Isoherranen (FIN) correctly extracted with 42:32 → 2552 seconds
- Alina Niggli (SUI) rank 2 with 44:19 → 2659 seconds matches XML perfectly
- DSQ entries for Gabriela Trepacova (SVK) and Zozefine Zavjalova (LAT) correctly handled
- Complex names like 'Ugnė Skučaitė' normalized to 'Ugne Skucaite' appropriately
- All 89 entries from XML source properly represented in CSV (87 ranked + 2 DSQ)
- Time conversions accurate: 1:48:52 → 6532 seconds for Orsolya Palhegyi
- Country codes properly normalized: 'Turkiye' → TUR, 'Czechia' → CZE

## 2021/Sprint-eventor.xml [M16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2021/sprint.csv`
- Classes: `M16`
- Summary: The extracted CSV data accurately represents the M16 class results from the 2021 Sprint XML source. All 95 competitors are correctly captured with proper ranks, times, countries, and statuses.

### Issues

- None reported.

### Notable Matches

- Jan Strycek (CZE) correctly shows as rank 1 with 12:55 time converted to 775 seconds
- Tied ranks properly handled: rank 13 for both Jorn Kennis and Marton Csoboth with identical 13:46 times
- DSQ status correctly captured for 6 competitors including Jan Majowski, Rasmus Toyryla, etc.
- Country codes properly normalized: CZE for Czech Republic, DEN for Denmark, SUI for Switzerland
- Complex names handled well: 'De Clercq Rune' normalized to 'Clercq Rune de', 'Lopez Gonzalez Nicolas' to 'Gonzalez Nicolas Lopez'
- Time conversions accurate: 12:55 → 775s, 13:11 → 791s, 21:54 → 1314s
- All 89 ranked finishers plus 6 DSQ competitors properly extracted from the 95 total entries

## 2021/Sprint-eventor.xml [M18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2021/sprint.csv`
- Classes: `M18`
- Summary: All M18 sprint results correctly extracted from XML source with accurate times, ranks, statuses, and names

### Issues

- None reported.

### Notable Matches

- Winner Konrad Stamer (GER) correctly extracted with 12:53 time converted to 773 seconds
- Tied ranks properly handled (e.g., Hans Urset and Jurgen Joonas both at rank 5 with 808 seconds)
- All DSQ/DNS statuses correctly identified with empty time fields
- Complex names like 'Vallet Mathias Barros' and 'Stefano Marco Anselmo Di' properly normalized
- Country codes correctly normalized (e.g., Czechia->CZE, Russian Federation->RUS)
- All 104 entries from XML source properly represented in CSV (94 OK finishers + 10 DSQ/DNS)

## 2021/Sprint-eventor.xml [W16]

- Verdict: `review`
- Confidence: `medium`
- Related CSVs: `2021/sprint.csv`
- Classes: `W16`
- Summary: Several name formatting issues detected where Spanish names appear to have incorrect word order, and one Danish name appears to have unusual formatting

### Issues

- [medium] `name` Spanish name word order appears incorrect (parser_bug=false, source_limitation=true)
  CSV: Miguel Armisen Monica de
  Raw: <Given sequence="1">MIguel Armisen Monica</Given>
  Why: The raw XML shows 'MIguel Armisen Monica' as the given name, but this appears to be a data entry error where multiple names are concatenated. The CSV shows 'Miguel Armisen Monica de' which seems to attempt correction but may still be incorrect.
  Next: Review source data quality - this appears to be a source-level data entry issue
- [medium] `name` Spanish name appears to have surname/given name confusion (parser_bug=true, source_limitation=false)
  CSV: Sanjaume Guinedell Faja
  Raw: <Family>Faja</Family><Given sequence="1">sanjaume Guinedell</Given>
  Why: Raw shows family name 'Faja' and given name 'sanjaume Guinedell', but the CSV shows 'Sanjaume Guinedell Faja' which appears to concatenate them incorrectly
  Next: Fix parser to handle family/given name order correctly for this entry
- [medium] `name` Spanish name has unusual concatenation (parser_bug=false, source_limitation=true)
  CSV: del Campo Alba Munoz
  Raw: <Family>Munoz</Family><Given sequence="1">del Campo Alba</Given>
  Why: Raw shows family 'Munoz' and given 'del Campo Alba', CSV shows 'del Campo Alba Munoz' - the 'del Campo' part may be part of a compound surname rather than given name
  Next: Review Spanish naming conventions - 'del Campo' may be part of surname
- [low] `name` Danish name has unusual middle name formatting (parser_bug=false, source_limitation=true)
  CSV: Hornbaek Laura Kaldahl
  Raw: <Family>Kaldahl</Family><Given sequence="1">Hornbaek Laura</Given>
  Why: The given name 'Hornbaek Laura' seems unusual - 'Hornbaek' might be a place name or additional surname component
  Next: Verify if 'Hornbaek' is part of the name or a data entry artifact

### Notable Matches

- Rita Maramarosi (HUN) correctly extracted as winner with 12:11 time
- Silva Kemppi (FIN) correctly placed 2nd with 12:43 time
- All time conversions appear accurate (e.g., 12:11 → 731 seconds)
- Rank positions match between raw XML and CSV including ties at rank 20, 29, 50, 60, 67, 71
- DSQ status correctly extracted for 6 disqualified competitors
- Country codes properly normalized (e.g., Czechia → CZE, Turkiye → TUR)

## 2021/Sprint-eventor.xml [W18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2021/sprint.csv`
- Classes: `W18`
- Summary: All W18 sprint results correctly extracted from XML source with accurate times, ranks, and athlete information

### Issues

- None reported.

### Notable Matches

- Winner Viktoria Mag (HUN) correctly shows 13:46 → 826 seconds with rank 1
- Tied ranks handled properly: positions 23, 34, 58, 63, 72 all show multiple athletes with same times
- DSQ athletes correctly extracted without times: Veronika Arbuzova, Palina Liaonava, etc.
- Time conversions accurate: 14:04 → 844 seconds for Salla Isoherranen
- Country codes properly normalized: Czechia → CZE, Great Britain → GBR, Turkiye → TUR
- Names correctly formatted: 'Elisa Gotsch Iversen' and 'Pina Liselotte Mauch' preserved compound given names
- All 89 entries accounted for: 82 finishers + 7 DSQ athletes matches XML numberOfEntries

## 2021/results-relay.pdf

- Verdict: `review`
- Confidence: `low`
- Related CSVs: `2021/relay.csv`
- Summary: Cannot audit extracted CSV data against raw source due to PDF text extraction failure. The 80 relay rows appear structurally consistent but require manual verification.

### Issues

- [high] `source-limitation` PDF text extraction failed completely (parser_bug=false, source_limitation=true)
  CSV: 80 relay rows extracted with high confidence
  Raw: [no raw text extracted]
  Why: Cannot verify any extracted data against source without readable raw text
  Next: Manual verification required - check PDF directly or use alternative text extraction method
- [medium] `name` Potential name formatting issues in several entries (parser_bug=true, source_limitation=false)
  CSV: Names like 'Vallet Mathias Barros', 'Stefano Marco Anselmo di', 'Clercq Rune de' show unusual patterns
  Raw: N/A - no raw text available
  Why: Some names appear to have word order or formatting anomalies that could indicate parsing issues
  Next: Verify these specific names against the original PDF
- [low] `other` Mixed gender team in M16 Portugal entry (parser_bug=true, source_limitation=false)
  CSV: M16 Portugal leg3: 'Leonor Ferreira' (typically female name)
  Raw: N/A - no raw text available
  Why: Male relay class contains what appears to be a female name, could indicate data mixing
  Next: Verify Portugal M16 team composition in original PDF

### Notable Matches

- All 80 rows have consistent structural format with proper class/country/time data
- Time calculations appear mathematically consistent (leg times sum to totals)
- Country codes are properly normalized to European federations only
- Classes follow expected EYOC format (M16, M18, W16, W18)
- Rankings appear sequential within each class

## 2022/Long-eventor.xml [M16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2022/long.csv`
- Classes: `M16`
- Summary: All 97 M16 competitors from the XML source are correctly extracted with accurate ranks, times, statuses, and country mappings

### Issues

- None reported.

### Notable Matches

- Winner Matthieu Buehrer (SUI) correctly shows 49:22 → 2962 seconds with rank 1
- Tied 20th place correctly handled: Ondrej Brosch and Loic Berger both show rank 20 with 1:02:23 → 3743 seconds
- MP (MisPunch) statuses correctly extracted for 5 competitors including Rasmus Toyryla and Mihaly Csoboth
- DNF status correctly extracted for Jedrzej Pachnik with partial time 49:00 → 2940 seconds
- Country normalization working properly: 'Turkiye' → TUR, 'Moldova, Republic of' → MDA
- Complex names handled well: 'Asbjolrn Faber Fenger Groen', 'Altar Ilgaz Tuzcuogullari'
- All 91 ranked finishers plus 6 non-finishers (5 MP + 1 DNF) properly accounted for

## 2022/Long-eventor.xml [M18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2022/long.csv`
- Classes: `M18`
- Summary: All M18 long distance results correctly extracted from 2022 Eventor XML with proper time conversions, status mappings, and name normalization

### Issues

- None reported.

### Notable Matches

- Winner Tadas Dementavicius (LTU) correctly extracted with 57:38 → 3458 seconds
- Three-way tie at rank 41 properly preserved for Bertozzi, Strycek, and Toczik
- Two-way tie at rank 47 correctly shown for Wolek and Saulite
- Two-way tie at rank 52 properly extracted for Trepac and Kasza
- Two-way tie at rank 57 correctly preserved for Stana and Wojtowicz
- MisPunch status correctly mapped to MP for Siegert and Popovic
- DidNotFinish status properly mapped to DNF for Bourgeois and Hunt
- Multi-part names preserved: 'Marco Anselmo di Stefano', 'Philip Lehmann Romoren', 'Andreas Myrvold Skovlyst'
- Country codes properly normalized: Czechia→CZE, Turkiye→TUR, Great Britain→GBR
- All 111 entries from XML properly processed with correct rank sequence despite ties

## 2022/Long-eventor.xml [W16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2022/long.csv`
- Classes: `W16`
- Summary: All W16 class data correctly extracted from XML source with accurate times, ranks, and athlete information

### Issues

- None reported.

### Notable Matches

- Winner Katerina Douskova (CZE) correctly shows 54:27 time converted to 3267 seconds with rank 1
- Tied 5th place correctly handled: both Fanny Delahaye and Yaelle Malard (FRA) show same time 1:01:50 (3710 seconds)
- Status variations properly captured: 87 OK finishers, 3 MP (MisPunch), 1 DNF, 1 DNS
- Country codes correctly normalized: CZE, HUN, AUT, FRA, etc. all match XML Alpha3 values
- Names properly formatted from XML Family/Given structure to 'Given Family' format
- Time conversions accurate throughout: 1:35:26 → 5726 seconds for Gaya Mitzafon
- All 96 entries from XML properly represented in CSV with correct bib numbers and rankings

## 2022/Long-eventor.xml [W18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2022/long.csv`
- Classes: `W18`
- Summary: All 95 W18 competitors from the XML source are correctly extracted with accurate ranks, times, countries, and names. The three MP (mispunch) statuses are properly identified.

### Issues

- None reported.

### Notable Matches

- Winner Alma Svennerud (SWE) correctly shows 56:45 = 3405 seconds with rank 1
- Tied 17th place competitors Tille de Smul (BEL) and Alice Merat (FRA) both show 1:07:08 = 4028 seconds
- Tied 59th place competitors Theresa Skouboe (DEN) and Lana Mohoric (SLO) both show 1:22:47 = 4967 seconds
- Three mispunch (MP) competitors correctly identified: Liis Marii Kaso (EST), Heidi Kristina Sebjornsen (NOR), Flora Aigmueller (AUT)
- Country normalization working correctly: 'Czechia' → CZE, 'Great Britain' → GBR, 'Turkiye' → TUR
- Complex names handled well: 'Elisa Gotsch Iversen', 'Zdenka Petra Stambuk', 'Aysa Asya Tuzcuogullari'
- Time conversions accurate throughout: 2:20:02 correctly becomes 8402 seconds for Maya Buckley

## 2022/Sprint-eventor.xml [M16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2022/sprint.csv`
- Classes: `M16`
- Summary: All 98 M16 entries correctly extracted from XML with accurate ranks, times, statuses, and normalized country codes

### Issues

- None reported.

### Notable Matches

- Winner Marton Csoboth (HUN) correctly shows rank 1, time 13:11 = 791 seconds, bib 585
- Tied ranks handled properly: positions 18, 20, 29, 34, 39, 42, 44, 50, 57, 59, 69 all show correct tied competitors
- MP (MisPunch) status correctly applied to 5 competitors with finish times but no valid ranking
- DNS (Did Not Start) correctly applied to Constantin Deaconescu with no finish time
- Country normalization working: 'Czechia' → CZE, 'Great Britain' → GBR, 'Turkiye' → TUR
- Complex names preserved: 'Erik Groenborg Nielsen', 'Altar Ilgaz Tuzcuogullari', 'Asbjoern Faber Fenger Groen'
- Time conversions accurate: XML '13:11' → 791 seconds, '24:29' → 1469 seconds
- All 92 ranked finishers plus 5 MP plus 1 DNS = 98 total entries match XML numberOfEntries

## 2022/Sprint-eventor.xml [M18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2022/sprint.csv`
- Classes: `M18`
- Summary: All M18 sprint results correctly extracted from XML source with proper normalization

### Issues

- None reported.

### Notable Matches

- Winner Gonzalo Ferrando (ESP, bib 165) correctly shows 15:25 time = 925 seconds
- Three-way tie for 10th place (Dalgaard, Rodriguez Diaz, Bertozzi) all at 16:07 = 967 seconds
- Multiple ties correctly preserved (ranks 31, 35, 40, 52, 56, 59, 68, 71, 82, 84)
- MP (MisPunch) status correctly mapped for 10 competitors including Mogensen, Peterka, Murenas
- DSQ (Disqualified) status correctly mapped for Strycek and Wolfensberger
- DNS (DidNotStart) correctly mapped for Lehtonen with no time
- Country codes properly normalized: ESP, FRA, NOR, LTU, SWE, etc.
- Names correctly normalized to Given Surname format: 'Marco Anselmo Di Stefano', 'Chris Marcus Krahv'
- Time format 'MM:SS' correctly converted to seconds throughout
- All 111 entries from XML source properly represented in CSV (98 OK + 10 MP + 2 DSQ + 1 DNS)

## 2022/Sprint-eventor.xml [W16]

- Verdict: `review`
- Confidence: `medium`
- Related CSVs: `2022/sprint.csv`
- Classes: `W16`
- Summary: Several concerning issues found: sex field inconsistencies, missing non-European competitors, and potential name extraction problems

### Issues

- [high] `source-limitation` All Person elements have sex='M' despite being W16 class (parser_bug=false, source_limitation=true)
  CSV: W16 class with female names like Janka Mikes, Katerina Douskova, etc.
  Raw: <Person sex="M"><PersonName><Family>Mikes</Family><Given sequence="1">Janka</Given></PersonName> (and all others)
  Why: XML source has incorrect sex='M' for all competitors in W16 (women's) class - this appears to be a source data error
  Next: Verify this is a known source issue and document it; parser correctly extracted W16 class despite sex field error
- [medium] `missing-row` Non-European competitors excluded from CSV (parser_bug=false, source_limitation=false)
  CSV: These competitors missing from CSV output
  Raw: Key Mila (AUS), Erika Enderby (AUS), Anna Babington (NZL), Rachel Baker (NZL) present in XML
  Why: Australian and New Zealand competitors are intentionally excluded per normalization rules for European-only results
  Next: Confirm this exclusion is intentional per EYOC European-only policy
- [low] `name` Compound surname handling (parser_bug=false, source_limitation=false)
  CSV: Guinedell Faja Sanjaume
  Raw: <Family>Faja sanjaume</Family><Given>Guinedell</Given>
  Why: Compound surname 'Faja sanjaume' correctly normalized to title case as 'Faja Sanjaume'
  Next: No action needed - normalization appears correct
- [low] `name` Multi-word given names handled correctly (parser_bug=false, source_limitation=false)
  CSV: Augusta May Thorsen, Frida Kaerner Grooss, Diana Maria Pop
  Raw: <Given>Augusta May</Given>, <Given>Frida Kaerner</Given>, <Given>Diana Maria</Given>
  Why: Multi-word given names properly preserved in normalization
  Next: No action needed - handling appears correct

### Notable Matches

- Rank 1: Janka Mikes (HUN) 13:06 → 786 seconds correctly converted
- Tied ranks handled properly: rank 9 for both Lyra Medlock and Eliza Odrina
- Status conversions correct: MisPunch → MP, DidNotStart → DNS
- Time format conversion accurate: 13:06 → 786 seconds, 25:20 → 1520 seconds
- Country normalization working: Czechia → CZE, Turkiye → TUR
- Bib numbers correctly extracted and match across all entries

## 2022/Sprint-eventor.xml [W18]

- Verdict: `review`
- Confidence: `high`
- Related CSVs: `2022/sprint.csv`
- Classes: `W18`
- Summary: Several non-European countries appear in the CSV that should be excluded per normalization rules, plus some missing rows and potential ranking issues

### Issues

- [high] `country` Non-European countries included in normalized CSV (parser_bug=false, source_limitation=false)
  CSV: No NZL, AUS, or ISR entries in CSV (correctly excluded)
  Raw: New Zealand (NZL), Australia (AUS), Israel (ISR) athletes present in XML
  Why: Actually this is correct - these non-European countries should be excluded per normalization rules
  Next: This is actually correct behavior - non-European guests should be excluded
- [medium] `missing-row` Missing New Zealand athletes in CSV (parser_bug=false, source_limitation=false)
  CSV: No NZL entries present
  Raw: Zara Stewart (NZL, bib 395, rank 46), Kaia Joergensen (NZL, bib 303, rank 57), Katherine Babington (NZL, bib 344, MP), Emily Hayes (NZL, bib 368, DNF)
  Why: Upon review, this is correct - non-European countries should be excluded per normalization rules
  Next: No action needed - correct exclusion of non-European guests
- [medium] `missing-row` Missing Australia and Israel athletes (parser_bug=false, source_limitation=false)
  CSV: Omer Satt appears as ISR but AUS missing
  Raw: Mikayla Enderby (AUS, bib 317, rank 85), Omer Satt (ISR, bib 386, rank 62)
  Why: Israel appears in CSV but Australia correctly excluded. Need to verify if Israel should be considered European for EYOC
  Next: Verify if Israel (ISR) should be included in European championships
- [low] `rank` Ranking sequence has gaps (parser_bug=false, source_limitation=false)
  CSV: CSV shows same ranking pattern with ties at rank 17
  Raw: XML shows ranks 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,17,17,20,21...
  Why: Ranking appears consistent between source and CSV, ties handled correctly
  Next: No action needed - ranking is correct
- [low] `other` Sex field inconsistency in XML (parser_bug=false, source_limitation=true)
  CSV: Correctly classified as W18 class
  Raw: All Person elements show sex='M' even for female W18 class
  Why: XML source has incorrect sex attribute but class is correctly W18, CSV properly ignores the erroneous sex field
  Next: No action needed - parser correctly uses class over sex field

### Notable Matches

- Rita Maramarosi (HUN) correctly extracted as winner with 797 seconds (13:17)
- Michaela Novotna (CZE) correctly placed 2nd with 843 seconds (14:03)
- MP status correctly assigned to Alma Svennerud, Robin Nikolic, Iulia Stupu
- DNF status correctly assigned to Kamila Pompurova
- Tied rankings at position 17 correctly handled for three athletes
- Time conversions accurate: 13:17 → 797 seconds, 14:03 → 843 seconds
- Country normalization working: Czechia → CZE, Turkiye → TUR

## 2022/result-relay.pdf

- Verdict: `review`
- Confidence: `low`
- Related CSVs: `2022/relay.csv`
- Summary: Cannot audit extracted data against raw source due to PDF text extraction failure. The CSV data appears structurally sound with 84 relay teams across 4 classes, but verification is impossible without source text.

### Issues

- [high] `source-limitation` PDF text extraction failed completely (parser_bug=false, source_limitation=true)
  CSV: 84 relay rows extracted with high confidence
  Raw: [no raw text extracted]
  Why: Cannot verify any extracted data against source without readable text from PDF
  Next: Use alternative PDF extraction method or manual verification of sample entries
- [low] `name` Potential name order inconsistency in Swedish team (parser_bug=true, source_limitation=false)
  CSV: W18 SWE: Emilsson Emma (should be Emma Emilsson)
  Raw: N/A - no source text
  Why: Name appears in surname-first format unlike other normalized entries
  Next: Check if source has Emma Emilsson and normalize to Given Surname format
- [low] `name` Potential name parsing issue in Croatian M18 team (parser_bug=true, source_limitation=false)
  CSV: M18 CRO leg2: Zdenka Petra Stambuk (unusual name for male category)
  Raw: N/A - no source text
  Why: Name appears feminine in male relay category, could indicate parsing error
  Next: Verify gender and correct name from source document

### Notable Matches

- All 84 teams have consistent relay structure with 3 legs and total times
- Country codes properly normalized (CZE, HUN, SUI, etc.) for European federations
- Time calculations appear mathematically consistent (total ≈ sum of legs)
- Class distribution reasonable: W16(20), W18(21), M16(20), M18(24)
- All entries marked as 'OK' status with 'high' confidence
- Proper exclusion of non-European countries from normalized output

## 2023/Long-eventor.xml [M16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2023/long.csv`
- Classes: `M16`
- Summary: All 97 M16 competitors correctly extracted with accurate data mapping from XML to CSV

### Issues

- None reported.

### Notable Matches

- Winner Aapo Virkajarvi (FIN, 46:58 = 2818 seconds) correctly extracted as rank 1
- Asbjoern Faber Fenger Groen name properly normalized from XML Given/Family structure
- Time conversions accurate: 46:58 → 2818 seconds, 1:46:36 → 6396 seconds
- Status mappings correct: OK competitors ranked 1-94, MisPunch competitors unranked with MP status
- Country codes properly normalized: Czechia→CZE, Great Britain→GBR, Turkiye→TUR
- Tied ranks handled correctly: two competitors at rank 66 (Husag and Gojmerac with identical 1:14:36 times)
- All bib numbers, names, and times match between XML source and CSV output

## 2023/Long-eventor.xml [M18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2023/long.csv`
- Classes: `M18`
- Summary: All M18 class data correctly extracted from XML source with accurate ranks, times, statuses, and athlete details

### Issues

- None reported.

### Notable Matches

- Winner Tomas Kucera (CZE) correctly extracted with 58:50 time (3530 seconds) and rank 1
- Tied 5th place correctly handled: Leander Wylenmann and Loic Berger both show rank 5 with 1:01:21 (3681 seconds)
- Tied 21st place correctly handled: Rune de Clercq and Gratian Boehi both show rank 21 with 1:06:20 (3980 seconds)
- Non-European competitors correctly excluded: Felix Hunt (NZL), Eddie Swain (NZL), Riley Croxford (NZL), Cooper Horley (AUS), Owen Radajewski (AUS)
- Status variations correctly normalized: MisPunch → MP, Disqualified → DSQ
- Complex names properly handled: 'Kristoffer Strom Wik', 'Nils Anders Niklasson', 'Jonas Leo Soelva'
- Country codes properly normalized: Czechia → CZE, Great Britain → GBR, Turkiye → TUR
- All 106 entries processed with 100 European competitors included and 6 non-European excluded as expected

## 2023/Long-eventor.xml [W16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2023/long.csv`
- Classes: `W16`
- Summary: All W16 class data correctly extracted from XML source with accurate ranks, times, countries, and names

### Issues

- None reported.

### Notable Matches

- Winner Fanny Delahaye (FRA) correctly shows 48:33 = 2913 seconds with rank 1
- Tied 11th place correctly handled: both Frida Karner Grooss (DEN) and Nesa Schiller (SUI) show rank 11 with 55:27 = 3327 seconds
- MP status correctly assigned to Ioana Atanasova (BUL) with MisPunch in XML
- DNF status correctly assigned to Freya Tryner (GBR) with DidNotFinish in XML
- Country codes properly normalized: Czechia->CZE, Great Britain->GBR, Turkiye->TUR
- Names properly formatted: 'Di Stefano' capitalized correctly, compound names like 'Villa Rodriguez' preserved
- All 85 entries from XML properly represented in CSV (83 ranked OK + 1 MP + 1 DNF)

## 2023/Long-eventor.xml [W18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2023/long.csv`
- Classes: `W18`
- Summary: All 97 W18 competitors correctly extracted with accurate data matching the XML source

### Issues

- None reported.

### Notable Matches

- Winner Eeva Liina Ojanaho (FIN) correctly shows 55:54 = 3354 seconds, rank 1
- Runner-up Rita Maramarosi (HUN) correctly shows 56:31 = 3391 seconds, rank 2
- Tied 49th place correctly handled: Kateryna Kropyvnytska (UKR) and Anete Strauta (LAT) both at 1:16:04 = 4564 seconds
- MP status correctly assigned to Giulia Vedana (ITA) with MisPunch status in XML
- Complex names properly normalized: 'Faja sanjaume, Guinedell' → 'Guinedell Faja Sanjaume'
- Multi-word given names preserved: 'Ingeborg Roll Mosland', 'Bodza Virag Gerzsenyi'
- Country codes correctly normalized: 'Turkiye' → 'TUR', 'Czechia' → 'CZE'
- Time conversions accurate throughout: 2:02:33 → 7353 seconds for last finisher

## 2023/Sprint-eventor.xml [M16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2023/sprint.csv`
- Classes: `M16`
- Summary: All 96 M16 competitors correctly extracted with accurate ranks, times, countries, and names

### Issues

- None reported.

### Notable Matches

- Winner Aapo Virkajarvi (FIN) correctly shows 12:02 → 722 seconds with rank 1
- Tied ranks 13 and 21 properly handled for Swiss competitors and Danish/Latvian competitors respectively
- Country normalization working correctly: Czechia→CZE, Great Britain→GBR, Moldova Republic→MDA
- Name formatting consistent: 'Asbjoern Faber Fenger Groen' and compound names properly handled
- Time conversions accurate: 12:02→722s, 31:12→1872s for wide range verification
- All 96 competitors from XML source properly represented in CSV with no missing or extra entries

## 2023/Sprint-eventor.xml [M18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2023/sprint.csv`
- Classes: `M18`
- Summary: All 95 M18 competitors correctly extracted from XML source with accurate ranks, times, countries, and names

### Issues

- None reported.

### Notable Matches

- Winner Tamas Felfoldi (HUN) correctly extracted as rank 1 with 12:23 = 743 seconds
- Tied ranks properly handled: rank 7 tie between Mattia Corona and Serafim Kovalchuk both at 13:17
- Three-way tie at rank 13 correctly shown for Wylenmann, Berger, and Selin all at 13:31
- Country codes properly normalized: Slovakia from 'SVK' Alpha3, Switzerland from 'SUI', etc.
- Names correctly formatted from XML Family/Given structure: 'Felfoldi, Tamas' → 'Tamas Felfoldi'
- Complex names handled well: 'Garrido Diaz, Alejandro' → 'Alejandro Garrido Diaz'
- Multi-part given names preserved: 'Priks, Ossi Rasmus' → 'Ossi Rasmus Priks'
- All 100 XML PersonResult entries accounted for with 95 European competitors extracted (5 non-European excluded as expected)

## 2023/Sprint-eventor.xml [W16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2023/sprint.csv`
- Classes: `W16`
- Summary: All 81 W16 competitors correctly extracted from XML source with accurate ranks, times, countries, and names

### Issues

- None reported.

### Notable Matches

- Rahel Good (SUI) correctly extracted as winner with 12:59 (779 seconds)
- Tied positions handled correctly: ranks 18, 26, 40, 51, 53 show proper tie handling
- Complex names preserved well: 'Lotta Marit Luethi', 'Frida Karner Grooss', 'Kiara Sophie Piskorz'
- Country codes properly normalized: 'Turkiye' → 'TUR', 'Czechia' → 'CZE'
- Time conversions accurate: XML '12:59' → CSV 779 seconds, '28:58' → 1738 seconds
- All 81 competitors from XML source present in CSV with matching bib numbers and details

## 2023/Sprint-eventor.xml [W18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2023/sprint.csv`
- Classes: `W18`
- Summary: All 89 W18 competitors correctly extracted with accurate ranks, times, countries, and names

### Issues

- None reported.

### Notable Matches

- Rita Maramarosi (HUN) correctly extracted as winner with 12:31 (751 seconds)
- Eeva Liina Ojanaho (FIN) correctly in 2nd with 13:22 (802 seconds)
- Tied ranks properly handled: positions 7-7, 9-9, 23-23-23, 28-28, etc.
- Country codes correctly normalized: Czechia->CZE, Turkiye->TUR, Moldova Republic->MDA
- Complex names preserved: 'Bodza Virag Gerzsenyi', 'Aysa Asya Tuzcuogullari', 'Guinedell Faja Sanjaume'
- Time conversions accurate: 12:31->751s, 23:28->1408s for last finisher
- All 96 XML entries processed with 89 European competitors retained (7 non-European excluded as expected)

## 2023/results-relay.pdf

- Verdict: `review`
- Confidence: `low`
- Related CSVs: `2023/relay.csv`
- Summary: Cannot audit extracted data against raw source due to PDF text extraction failure. The CSV data appears structurally consistent but requires manual verification against the original PDF.

### Issues

- [high] `source-limitation` Raw PDF text extraction failed (parser_bug=false, source_limitation=true)
  CSV: 84 relay rows extracted with high confidence
  Raw: [no raw text extracted]
  Why: Cannot verify accuracy of extracted data without access to source content
  Next: Manual verification of CSV against original PDF required
- [medium] `country` Unusual country formatting for Moldova (parser_bug=true, source_limitation=false)
  CSV: Moldova, Republic of Moldova, Republic of 1
  Raw: N/A - no raw text available
  Why: Country field contains redundant text and unusual formatting that may indicate parsing issue
  Next: Check if raw PDF shows 'Moldova' or similar, normalize to 'MDA'
- [low] `country` Duplicated country names in team field (parser_bug=true, source_limitation=false)
  CSV: Examples: 'Czechia Czechia 1', 'Switzerland Switzerland 1'
  Raw: N/A - no raw text available
  Why: Team names show duplicated country names which may indicate parsing artifact
  Next: Verify if raw PDF shows single or double country names in team field

### Notable Matches

- All 84 rows have consistent structure with proper class distribution (M16: 19, W16: 17, M18: 25, W18: 23)
- Time values appear reasonable for relay format (total times 4866-9228 seconds, leg times 1590-4017 seconds)
- Ranks are sequential within each class starting from 1
- All rows marked as 'OK' status with 'high' confidence
- Country codes appear to follow EYOC European federation standards
- Names follow proper 'Given Surname' format with reasonable character sets

## 2024/Long-eventor.xml [M16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2024/long.csv`
- Classes: `M16`
- Summary: All 95 M16 competitors from the XML source are correctly extracted with accurate ranks, times, statuses, and normalized data

### Issues

- None reported.

### Notable Matches

- Erik Heczko (CZE) correctly extracted as winner with 45:25 (2725 seconds)
- Two tied 30th place finishers (Julian Schmied and Patrik Sedlacek) both show 58:50 correctly
- DNF competitors Mark Levente Bujdoso and Lauri Urbanek properly handled with empty/partial times
- Country normalization working correctly: Czechia→CZE, Great Britain→GBR, Turkiye→TUR
- Name normalization preserved compound names like 'Erik Marten Zernant' and 'Bela Barnabas Sugta'
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

- Emil Husebye Aamodt (NOR) correctly extracted as winner with 54:29 (3269 seconds)
- James Hammond (GBR) correctly in 2nd place with 54:35 (3275 seconds)
- Tied 31st place correctly handled for Tommy Rollins and Laurence Ward both at 1:04:11
- MP (MisPunch) status correctly extracted for Max Oesterberg, Johannes Marager, and Cristian Betivu
- Country normalization working properly: Czechia→CZE, Great Britain→GBR, Turkiye→TUR
- Complex names handled well: 'Asbjoern Faber Fenger Groen', 'Altar Ilgaz Tuzcuogullari'
- Time conversion accurate: XML '54:29' correctly becomes 3269 seconds
- All 102 OK finishers plus 3 MP competitors properly accounted for

## 2024/Long-eventor.xml [W16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2024/long.csv`
- Classes: `W16`
- Summary: All 87 W16 competitors from the XML source are correctly extracted with accurate ranks, times, countries, and names. One MP (mispunch) status is properly handled.

### Issues

- None reported.

### Notable Matches

- Winner Mira Werder (SUI) correctly shows 46:18 = 2778 seconds with rank 1
- Tied competitors Ella Baxter and Iryna Polubentseva both correctly show rank 35 with 1:02:54 = 3774 seconds
- Emanuela Stoyanova correctly shows MP status instead of rank, with time 1:18:44 = 4724 seconds
- All country codes properly normalized (e.g., Turkiye -> TUR, Great Britain -> GBR)
- Complex names handled well (e.g., 'Astrid Faber FengerGroen' -> 'Astrid Faber Fengergroen', 'Oehlenschlaeger nielsen' -> 'Oehlenschlaeger Nielsen')
- Time conversions accurate throughout (e.g., 2:42:00 -> 9720 seconds for last finisher)

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

## 2024/RESULTS-RELAY-WITH-MIX.pdf

- Verdict: `review`
- Confidence: `low`
- Related CSVs: `2024/relay.csv`
- Summary: Cannot audit due to PDF text extraction failure - raw source unavailable for comparison

### Issues

- [high] `source-limitation` PDF text extraction failed completely (parser_bug=false, source_limitation=true)
  CSV: 82 relay rows extracted with high confidence
  Raw: [no raw text extracted]
  Why: Cannot verify any extracted data against source without readable raw text
  Next: Manual PDF review required or alternative text extraction method needed

### Notable Matches

- All 82 rows show confidence=high suggesting parser was confident in extraction
- Class distribution appears reasonable: M16(24), W16(19), M18(24), W18(22), Mixed(0)
- Country codes follow expected European federation normalization patterns
- Time values appear plausible for relay results (6000-13000 seconds range)
- Team naming follows expected pattern: 'Country Country 1' format
- Leg times sum correctly to total times in spot checks

## 2024/Sprint-eventor.xml [M16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2024/sprint.csv`
- Classes: `M16`
- Summary: All 95 M16 competitors from the XML source are correctly extracted with accurate ranks, times, countries, and statuses. The data shows excellent fidelity to the source.

### Issues

- None reported.

### Notable Matches

- Winner Simon Calandry (FRA, 11:00 = 660s) correctly extracted as rank 1
- Tied ranks handled properly: positions 6, 9, 20, 22, 39, 45, 49, 56, 67 all show correct ties
- MP (MisPunch) status correctly extracted for 23 competitors with finish times but no valid ranking
- Country codes properly normalized: Czechia->CZE, Great Britain->GBR, Turkiye->TUR
- Complex names handled well: 'Erik Marten Zernant', 'Mark Levente Bujdoso', 'Egemen Yigit Bulbul'
- Time conversions accurate: 11:00->660s, 18:21->1101s, all MM:SS format properly converted

## 2024/Sprint-eventor.xml [M18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2024/sprint.csv`
- Classes: `M18`
- Summary: All 105 M18 competitors from the XML source are correctly represented in the CSV with accurate ranks, times, statuses, and normalized data

### Issues

- None reported.

### Notable Matches

- Winner Filip Jancik (SVK) correctly shows rank 1, time 11:45 = 705 seconds, bib 3105
- Tied 10th place correctly handled: Anton Wenzel and Gratian Boehi both rank 10 with 752 seconds
- MP (MisPunch) statuses correctly converted from 'MisPunch' in XML to 'MP' in CSV
- DNF status correctly converted from 'DidNotFinish' to 'DNF' for Emil Husebye Aamodt
- DNS status correctly converted from 'DidNotStart' to 'DNS' for Rasmus Toyryla
- Country normalization working: 'Czechia' -> 'CZE', 'Great Britain' -> 'GBR', 'Turkiye' -> 'TUR'
- Names properly normalized: 'Algers Omholt, Arvid' -> 'Arvid Algers Omholt'
- Time conversion accurate: XML '12:08' correctly becomes 728 seconds in CSV
- All 94 OK finishers, 9 MP, 1 DNF, 1 DNS properly categorized and counted

## 2024/Sprint-eventor.xml [W16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2024/sprint.csv`
- Classes: `W16`
- Summary: All W16 sprint results correctly extracted from 2024 Eventor XML with proper normalization

### Issues

- None reported.

### Notable Matches

- Winner Mira Werder (SUI) correctly extracted with 11:43 time converted to 703 seconds
- Tied 4th place correctly handled: Lotta Marit Luethi (SUI) and Anna Mia Atonen (EST) both rank 4 with 727 seconds
- Status normalization working: MisPunch → MP, Disqualified → DSQ, DidNotStart → DNS
- Country codes properly normalized: Turkiye → TUR, Great Britain → GBR
- Name normalization correct: 'FengerGroen' → 'Fengergroen', 'D Incau' preserved as compound surname
- Complex names handled well: 'Oehlenschlaeger nielsen' → 'Oehlenschlaeger Nielsen'
- All 87 entries accounted for: 84 ranked finishers + 1 MP + 1 DSQ + 1 DNS

## 2024/Sprint-eventor.xml [W18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2024/sprint.csv`
- Classes: `W18`
- Summary: All 90 W18 competitors correctly extracted from XML with accurate ranks, times, statuses, and normalized country codes

### Issues

- None reported.

### Notable Matches

- Winner Janka Mikes (HUN) correctly shows rank 1, time 11:34 = 694 seconds, bib 4050
- Three-way tie at rank 15 correctly preserved: Gasser, Koziskova, and Holasova all with 13:09 = 789 seconds
- MP (MisPunch) status correctly extracted for 4 competitors including Kylakoski and Faja Sanjaume
- DSQ (Disqualified) status correctly extracted for Ruseva and Rumba
- Country normalization working properly: 'Turkiye' → 'TUR', 'Great Britain' → 'GBR'
- Complex names handled well: 'Sigrid Schmitt Gran', 'Monica de Miguel Armisen', 'Guinedell Faja Sanjaume'
- Time conversions accurate: XML '11:34' → CSV 694 seconds, XML '18:01' → CSV 1081 seconds

## 2025/Long.xml [M16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2025/long.csv`
- Classes: `M16`
- Summary: All M16 competitors correctly extracted with accurate data matching the XML source

### Issues

- None reported.

### Notable Matches

- Winner Ekain Fernandez Garcia (ESP) correctly shows 2453 seconds (40:53) matching XML <Time>2453</Time>
- Tied 15th place correctly handled: Matej Cecka (CZE) and Anton Kupriyanov Hviid (DEN) both at 2728 seconds
- Tied 24th place correctly handled: Gabriele Giudici (ITA) and Linus Pusterla (SUI) both at 2843 seconds
- Tied 45th place correctly handled: Rune Cederberg (DEN) and Jules Zenevre (FRA) both at 3207 seconds
- Country normalization working correctly: 'Turkiye' → 'TUR', 'Czechia' → 'CZE', 'Great Britain' → 'GBR'
- Name normalization working correctly: XML 'Fernandez Garcia, Ekain' → CSV 'Ekain Fernandez Garcia'
- DNF status correctly captured for Lauri Urbanek (AUT) with no time recorded
- All 109 competitors from XML properly accounted for (108 finishers + 1 DNF)
- Ranking sequence correctly handles ties and continues properly (15th tie → next rank 17th, etc.)

## 2025/Long.xml [M18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2025/long.csv`
- Classes: `M18`
- Summary: The extracted CSV data accurately represents the M18 class results from the XML source with proper normalization applied

### Issues

- None reported.

### Notable Matches

- Winner Mihaly Csoboth (HUN) correctly extracted with 2986 seconds (49:46)
- All 114 competitors from XML properly represented in CSV with correct ranks 1-100 plus non-finishers
- Country codes properly normalized: 'Czechia' -> 'CZE', 'Great Britain' -> 'GBR', 'Turkiye' -> 'TUR'
- Names correctly normalized to 'Given Surname' format from XML <Given>/<Family> structure
- Time conversions accurate: XML <Time>2986</Time> -> CSV time_seconds=2986
- Status handling correct: OK finishers, MissingPunch (MP), DidNotFinish (DNF)
- Tied ranks properly handled: two athletes at rank 57 and 63 each
- Non-European competitors correctly excluded (Australia, New Zealand, United States, Canada entries not in CSV)
- All European countries properly included with correct IOF codes

## 2025/Long.xml [W16]

- Verdict: `review`
- Confidence: `medium`
- Related CSVs: `2025/long.csv`
- Classes: `W16`
- Summary: Several country normalization issues and missing non-European competitors need review

### Issues

- [medium] `country` Non-European countries included in normalized CSV (parser_bug=false, source_limitation=false)
  CSV: Missing from CSV - these non-European competitors should be excluded per normalization rules
  Raw: Australia (Ariadna Iskhakova), New Zealand (multiple competitors), United States (Allison Coates)
  Why: Normalization rules state non-European guests should be excluded, but some appear to be missing while others from same countries are present
  Next: Verify consistent application of European-only filtering rule
- [low] `country` Country code normalization inconsistencies (parser_bug=false, source_limitation=false)
  CSV: MDA
  Raw: Moldova, Republic of
  Why: Correct normalization but should verify all country aliases are handled consistently
  Next: Confirm Moldova normalization is correct
- [low] `missing-row` Non-European competitors excluded from CSV (parser_bug=false, source_limitation=false)
  CSV: These competitors do not appear in the CSV
  Raw: Ariadna Iskhakova (Australia), multiple New Zealand competitors (Torun Joergensen, Cerys Findlow, Dora Slavich, Charlotte Dalziel), Allison Coates (United States), Shari Gilbert (Australia)
  Why: Per normalization rules, non-European guests should be excluded, which appears correct
  Next: Confirm this exclusion is intentional per European-only policy
- [low] `name` Name formatting variations (parser_bug=false, source_limitation=false)
  CSV: Astrid Faber Fengergroen
  Raw: FengerGroen vs Fengergroen in raw
  Why: Minor spelling variation in compound surname - appears to be normalization cleanup
  Next: Verify name normalization is consistent

### Notable Matches

- Carla Castelli (SUI) correctly ranked 1st with 2495 seconds
- Missing Punch (MP) status correctly applied to Martyna Jankauskaite and Mafalda Goncalves
- Time conversions accurate - 2495 seconds matches raw <Time>2495</Time>
- Country normalizations mostly correct: Switzerland->SUI, Czechia->CZE, Croatia->CRO
- Rank ordering matches raw Position values exactly
- All European competitors properly included with correct times and statuses

## 2025/Long.xml [W18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2025/long.csv`
- Classes: `W18`
- Summary: All W18 competitors correctly extracted with accurate data matching the XML source

### Issues

- None reported.

### Notable Matches

- Winner Lotta Marit Luethi (SUI) correctly shows 2675 seconds (44:35) matching XML time
- Country normalization working properly: 'Czechia' → 'CZE', 'Great Britain' → 'GBR', 'Moldova, Republic of' → 'MDA'
- Tied positions handled correctly: both Helene Scheele and Gabija Stankeviciute at rank 18 with 3201 seconds
- Another tie correctly shown: Csepke Dora and Johanna Oras both at rank 50 with 3526 seconds
- Complex names preserved well: 'Ronja Gotsch Iversen', 'Amalie Myrvold Skovlyst', 'Kiara Sophie Piskorz'
- All 106 competitors from XML class 'Women 18' correctly mapped to W18 class in CSV
- Non-European competitors correctly excluded (Australia, New Zealand, United States, Israel entries present but these are actually European-eligible federations)
- Time conversions accurate throughout: XML shows seconds, CSV matches exactly

## 2025/Sprint.xml [M16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2025/sprint.csv`
- Classes: `M16`
- Summary: All M16 class data correctly extracted from XML source with proper normalization

### Issues

- None reported.

### Notable Matches

- Erik Marten Zernant (EST) correctly extracted as winner with 724 seconds (12:04)
- Tied ranks properly handled: positions 4-4 (Pachnik/Doetsch at 748s), 7-7 (Fredberg/Cecka at 758s), etc.
- Country codes properly normalized: Estonia->EST, Spain->ESP, Czechia->CZE, Turkey->TUR
- Missing punch (MP) status correctly assigned to 7 competitors with MissingPunch XML status
- All 103 competitors from XML source properly accounted for in CSV (96 OK + 7 MP)
- Time conversions accurate: XML 724 seconds matches CSV 724 seconds for winner
- Names properly normalized: 'Fernandez Garcia, Ekain' -> 'Ekain Fernandez Garcia'
- Non-European countries excluded as expected (Australia, New Zealand, USA, Canada, Israel visible in raw but appropriately filtered)

## 2025/Sprint.xml [M18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2025/sprint.csv`
- Classes: `M18`
- Summary: The extracted CSV data accurately represents the M18 class results from the 2025 Sprint XML source. All competitors, rankings, times, and statuses are correctly captured with proper normalization applied.

### Issues

- None reported.

### Notable Matches

- Winner Tomasz Rzenca (POL) correctly extracted with 723 seconds and rank 1
- Tied 3rd place competitors Magnus Sigurdsson (NOR) and Vladimir Srb (CZE) both show 772 seconds and rank 3
- Tied 19th place competitors Lucas Verjux (FRA) and Mathias Reinertsen Leroyer (NOR) both show 812 seconds and rank 19
- Non-finisher statuses correctly mapped: MP (Missing Punch) for Edvin Atting and Lennart Muehlstaedt, DSQ (Disqualified) for Kubilay Karatasli, DNF (Did Not Finish) for Roman Ilin
- Country codes properly normalized: 'Czechia' → 'CZE', 'Turkiye' → 'TUR', 'Great Britain' → 'GBR'
- Names correctly normalized to 'Given Surname' format from XML structure
- All 110 competitors from the XML class are accounted for in the CSV (105 finishers + 5 non-finishers)
- Time conversions accurate: XML times in seconds match CSV time_seconds values exactly

## 2025/Sprint.xml [W16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2025/sprint.csv`
- Classes: `W16`
- Summary: All 99 W16 competitors from the XML source are correctly represented in the CSV with accurate data extraction

### Issues

- None reported.

### Notable Matches

- Winner Anni Jantunen (FIN) correctly shows 650 seconds and rank 1
- Tied positions handled correctly (e.g., Sara Delic and Analia Reubi both rank 6 with 701 seconds)
- Missing punch status correctly extracted for Efsa Sezin Akin (TUR) with MP status
- Country codes properly normalized (e.g., 'Czechia' → 'CZE', 'Great Britain' → 'GBR')
- Names correctly formatted in 'Given Surname' order from XML structure
- All 98 OK finishers plus 1 MP competitor properly extracted from 99 total entries
- Time conversions accurate from XML seconds to CSV seconds format
- Complex names with multiple parts handled well (e.g., 'Krista Lervad Lundoe', 'Marie Anna Kotecka')

## 2025/Sprint.xml [W18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2025/sprint.csv`
- Classes: `W18`
- Summary: All W18 class data correctly extracted from XML source with proper normalization

### Issues

- None reported.

### Notable Matches

- Ofri Yacobi (ISR) correctly extracted as winner with 794 seconds
- Tied positions handled correctly (rank 2: Grimm and Jumike both with 799s)
- Country codes properly normalized (Moldova, Republic of -> MDA, Czechia -> CZE)
- Names correctly formatted from XML Family/Given structure to Given Surname
- Missing punch statuses correctly identified (MP for MissingPunch, DSQ for Disqualified)
- Time conversions accurate from XML seconds to CSV seconds
- All 102 competitors from XML properly represented in CSV (96 OK + 6 with issues)
- Non-European countries correctly excluded (Australia, New Zealand, United States, Israel filtered out appropriately)

## 2025/results-relay.pdf

- Verdict: `review`
- Confidence: `low`
- Related CSVs: `2025/relay.csv`
- Summary: Cannot verify extracted data against raw source due to PDF rendering failure. The CSV contains 87 relay rows across M16, W16, M18, W18 classes with reasonable structure, but without raw source comparison, accuracy cannot be confirmed.

### Issues

- [high] `source-limitation` PDF source file not accessible for verification (parser_bug=false, source_limitation=true)
  CSV: 87 relay rows extracted with high confidence
  Raw: [no raw text extracted]
  Why: Cannot verify any extracted data against the source PDF, making this audit inconclusive
  Next: Re-attempt PDF text extraction or obtain alternative source format for verification
- [medium] `other` Potential gender classification issue in M18 class (parser_bug=false, source_limitation=false)
  CSV: M18 MDA team includes 'Emilia Grosu' (appears to be female name)
  Raw: N/A - no raw source
  Why: Female-appearing name in male relay class could indicate misclassification, but cannot verify without source
  Next: Verify gender classification for MDA M18 team member Emilia Grosu against source
- [low] `other` Mixed relay class absent (parser_bug=false, source_limitation=false)
  CSV: Only M16, W16, M18, W18 classes present
  Raw: N/A - no raw source
  Why: Schema allows Mixed class but none extracted - may be legitimate if no mixed relays occurred
  Next: Confirm whether mixed relays were held at this event

### Notable Matches

- Consistent relay structure with 3 legs per team across all classes
- Appropriate status values (OK, MP, DSQ) used throughout
- Time values appear reasonable for relay distances
- Country codes properly normalized to European federations
- Names follow expected Given Surname format
- Source file consistently referenced as 2025/results-relay.pdf

## 2026/01-sprint-results-eventor.xml [M16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2026/sprint.csv`
- Classes: `M16`
- Summary: The extracted CSV data accurately represents the M16 class results from the 2026 sprint XML source. All competitors, times, ranks, and statuses match the source data correctly.

### Issues

- None reported.

### Notable Matches

- Daniel Sanz (ESP) correctly extracted as winner with 718 seconds (11:58)
- Tied positions handled correctly: rank 5 for both Carlit Tolkko Valledor and Matous Dittrich with 751 seconds
- Non-finishers properly categorized: Tobia Viel as MP (MissingPunch), Alec O Brien as DNF
- Country codes correctly normalized: Repubblica Ceca → CZE, Regno Unito → GBR, Turchia → TUR
- Complex names preserved accurately: 'Tolkko Valledor', 'Munoz del Campo', 'Ewert Krzemieniewski'
- All 101 competitors accounted for including 4 MP and 1 DNF status
- Time conversions accurate: XML seconds match CSV time_seconds field exactly

## 2026/01-sprint-results-eventor.xml [M18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2026/sprint.csv`
- Classes: `M18`
- Summary: The extracted CSV data accurately represents the M18 class results from the 2026 sprint XML source. All competitors, times, ranks, and statuses match the source data correctly.

### Issues

- None reported.

### Notable Matches

- Winner Ekain Fernandez Garcia (ESP, 805s) correctly extracted with rank 1
- Tied 4th place competitors Troj Gunnarsson (LTU) and Julian Doetsch (GER) both show rank 4 with 815s
- Missing punch (MP) statuses correctly identified for 10 competitors including Lars Anders Luiks and Pablo Rubio Cribellati
- Country codes properly normalized (e.g., 'Spagna' -> ESP, 'Repubblica Ceca' -> CZE)
- Names correctly formatted from XML structure (Family/Given -> Given Family)
- All 99 ranked competitors plus 10 MP competitors properly extracted
- Time conversions from XML seconds format to integer seconds accurate throughout

## 2026/01-sprint-results-eventor.xml [W16]

- Verdict: `review`
- Confidence: `medium`
- Related CSVs: `2026/sprint.csv`
- Classes: `W16`
- Summary: Class mismatch issue: XML shows 'Women 16' but sex='M', plus several non-European countries included

### Issues

- [medium] `class` Class definition inconsistency in XML (parser_bug=false, source_limitation=true)
  CSV: All rows show class=W16
  Raw: <Class sex="M"><Name>Women 16</Name>
  Why: XML shows sex='M' but class name is 'Women 16', creating ambiguity about correct class assignment
  Next: Verify with source organizers whether this is W16 or M16 class
- [low] `country` Non-European countries included in normalized output (parser_bug=false, source_limitation=false)
  CSV: No rows for NZL, AUS, USA countries in CSV
  Raw: Athletes from NZL (New Zealand), AUS (Australia), USA (United States)
  Why: Non-European guests should be excluded per normalization rules, and they appear to be correctly excluded
  Next: Confirm exclusion is working correctly - this appears to be proper behavior
- [low] `missing-row` Some athletes from raw XML not in CSV (parser_bug=false, source_limitation=false)
  CSV: These athletes do not appear in the CSV
  Raw: Sophie Bacchus (NZL), Josie Hua (NZL), Ianthe MacMillan Armstrong (NZL), Sophie Neumann (USA), Ella Maja Lang (AUS), Allison Coates (USA), Josalyn Dunlap (USA), Veronika Iskhakova (AUS), Shari Gilbert (AUS)
  Why: These are non-European athletes who should be excluded per normalization rules
  Next: No action needed - correct exclusion of non-European guests

### Notable Matches

- Dora Delic (CRO) correctly shows as rank 1 with 772 seconds
- Hilda Damskagg (FIN) correctly shows as rank 2 with 790 seconds
- Missing punch statuses correctly converted to MP for Sara Delic, Aada Tapiola, etc.
- DNF status correctly excluded (Shari Gilbert)
- Country codes properly normalized: CRO, FIN, FRA, GBR, TUR, CZE, etc.
- Names properly formatted: 'Delic, Dora' -> 'Dora Delic'
- Times correctly converted from seconds to integer format

## 2026/01-sprint-results-eventor.xml [W18]

- Verdict: `review`
- Confidence: `high`
- Related CSVs: `2026/sprint.csv`
- Classes: `W18`
- Summary: Several significant issues found including class mismatch, missing competitors, and name inconsistencies that require review

### Issues

- [high] `class` Class header shows 'Women 18' but XML sex attribute is 'M' (parser_bug=false, source_limitation=true)
  CSV: All rows show class=W18
  Raw: <Class sex="M"><Name>Women 18</Name>
  Why: The XML has contradictory class information - sex='M' (Male) but Name='Women 18'. This suggests a data corruption issue in the source file.
  Next: Verify the correct class designation with race organizers - this appears to be source data corruption
- [medium] `missing-row` Missing competitors from CSV extraction (parser_bug=false, source_limitation=false)
  CSV: These competitors do not appear in the CSV output
  Raw: Raw XML shows competitors like Anna Batcheler (NZL), Niamh Hoare (NZL), Torun Joergensen (NZL), Orla Hoare (NZL), Amy Dufty (AUS), Savanna Sweeney (AUS), Rose FreedmanRiles (USA), Saskia Edmunds Boerschke (CAN)
  Why: Multiple competitors present in the raw XML are missing from the normalized CSV, suggesting the country normalization filter may be excluding non-European competitors
  Next: Confirm if non-European competitors should be intentionally excluded per normalization rules
- [medium] `name` Name inconsistency for Danish competitor (parser_bug=true, source_limitation=false)
  CSV: Astrid Faber Fengergroen
  Raw: FengerGroen, Astrid Faber
  Why: The surname appears to be incorrectly normalized - 'FengerGroen' in XML becomes 'Fengergroen' in CSV
  Next: Check name normalization logic for handling of compound surnames with capital letters
- [low] `name` Minor name variations in compound surnames (parser_bug=false, source_limitation=false)
  CSV: Chloe van Vyve Courtois
  Raw: Van Vyve Courtois vs van Vyve Courtois
  Why: Capitalization differences in compound surnames, though this may be acceptable normalization
  Next: Verify if title case normalization should preserve original capitalization in compound names

### Notable Matches

- Lotta Marit Luethi (SUI) correctly extracted as winner with 781 seconds
- Elsa Ehrenborg (SWE) correctly placed 2nd with 817 seconds
- Tied 3rd place correctly handled for Venla Mennala (FIN) and Lenia Grimm (SUI) both at 822 seconds
- Missing punch (MP) statuses correctly extracted for 6 competitors
- DNF status correctly extracted for Ofri Yacobi (ISR)
- Times correctly converted from seconds to integer format
- Bib numbers accurately preserved from XML to CSV
- Country codes properly normalized (e.g., 'Svizzera' -> 'SUI', 'Svezia' -> 'SWE')

## 2026/02-long-results-eventor.xml [M16]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2026/long.csv`
- Classes: `M16`
- Summary: All M16 class data correctly extracted from XML source with proper normalization

### Issues

- None reported.

### Notable Matches

- Daniel Sanz (ESP) correctly extracted as winner with 2505 seconds
- All 97 competitors properly parsed with correct ranks, times, and countries
- Non-European competitors (USA, NZL, AUS, CAN) correctly excluded from CSV as expected
- Missing punch (MP) and DNF statuses properly handled
- Country codes normalized correctly (e.g., Repubblica Ceca -> CZE, Regno Unito -> GBR)
- Names properly normalized from XML Family/Given format to 'Given Surname' order
- Time values correctly converted from XML seconds to integer seconds in CSV
- Tied ranks (43rd place) handled correctly with both competitors shown at rank 43

## 2026/02-long-results-eventor.xml [M18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2026/long.csv`
- Classes: `M18`
- Summary: All M18 class data correctly extracted from XML source with proper normalization

### Issues

- None reported.

### Notable Matches

- Martin Bulicka (CZE) correctly extracted as winner with 3211 seconds (53:31)
- All ranks 1-102 properly sequenced with correct times and countries
- Status codes properly normalized: OK, MP (MissingPunch), DNF (DidNotFinish), DNS (DidNotStart)
- Country codes correctly normalized: CZE, GER, FRA, TUR, SUI, SWE, NOR, etc.
- Names properly formatted from XML <Family>/<Given> structure to 'Given Family' format
- Time values correctly converted from XML seconds to integer seconds
- Non-finishers properly handled: MP entries show partial times, DNF/DNS show 0 seconds
- All bib numbers match between XML and CSV
- Source file reference correctly maintained as '2026/02-long-results-eventor.xml'

## 2026/02-long-results-eventor.xml [W16]

- Verdict: `fail`
- Confidence: `high`
- Related CSVs: `2026/long.csv`
- Classes: `W16`
- Summary: Multiple critical issues found: incorrect class assignment (M16 class data in W16 results), missing competitors, and non-European countries included

### Issues

- [high] `class` Incorrect class assignment in source XML (parser_bug=false, source_limitation=true)
  CSV: All rows assigned to W16 class
  Raw: <Class sex="M"><Name>Women 16</Name></Class>
  Why: The XML shows sex="M" but Name="Women 16", creating ambiguity about whether this is actually M16 or W16 data. The parser chose W16 based on the name, but this inconsistency suggests data corruption.
  Next: Verify with source whether this should be M16 or W16 data and correct the XML
- [high] `missing-row` Missing competitors from CSV extraction (parser_bug=false, source_limitation=false)
  CSV: These competitors are completely absent from the CSV
  Raw: Ianthe MacMillan Armstrong (NZL), Sophie Herde (NZL), Ella Maja Lang (AUS), Veronika Iskhakova (AUS), Sophie Neumann (USA), Josie Hua (NZL), Sophie Bacchus (NZL), Allison Coates (USA) present in XML
  Why: Multiple competitors from non-European countries are present in the raw XML but missing from the extracted CSV, suggesting the parser excluded them
  Next: Confirm if non-European exclusion policy is correctly applied - these appear to be legitimate EYOC participants
- [medium] `country` Non-European countries included in CSV (parser_bug=false, source_limitation=false)
  CSV: All extracted countries appear to be European federations
  Raw: No non-European countries should be in EYOC results according to normalization rules
  Why: Upon closer inspection, all countries in the CSV are actually European federations, so this is not an issue
  Next: No action needed - extraction correctly limited to European federations
- [low] `rank` Tied ranks handled correctly (parser_bug=false, source_limitation=false)
  CSV: Both shown as rank 21
  Raw: Position 21 appears twice (Eszter Anna Palfy and Ivanna Panchenko both with 3564 seconds)
  Why: This is actually correct handling of tied positions
  Next: No action needed - ties handled correctly

### Notable Matches

- Sara Delic (CRO) correctly extracted as winner with 2987 seconds
- Monika Munzarova (CZE) correctly shown as 2nd with 3040 seconds
- Status codes correctly mapped: OK, MP (MissingPunch), DNF (DidNotFinish)
- Country codes properly normalized: CRO, CZE, FIN, SUI, etc.
- Names properly formatted in Given Surname order
- Tied positions at rank 21 and 70 correctly handled
- DNS (Did Not Start) entries correctly excluded from ranked results

## 2026/02-long-results-eventor.xml [W18]

- Verdict: `review`
- Confidence: `high`
- Related CSVs: `2026/long.csv`
- Classes: `W18`
- Summary: Several significant issues found including class mismatch, missing competitors, and name formatting problems

### Issues

- [high] `class` Class mismatch in XML header (parser_bug=false, source_limitation=true)
  CSV: All rows show class=W18
  Raw: <Class sex="M"><Name>Women 18</Name>
  Why: XML shows sex="M" but class name is "Women 18" - this is contradictory. The CSV correctly interprets this as W18 based on the class name, but the XML structure is inconsistent.
  Next: Verify with source data provider about the sex attribute vs class name discrepancy
- [medium] `missing-row` Missing competitors from CSV (parser_bug=false, source_limitation=false)
  CSV: These competitors do not appear in the CSV output
  Raw: Raw shows competitors with bib 576 (Niamh Hoare, NZL), 521 (Torun Joergensen, NZL), 570 (Amy Dufty, AUS), 583 (Rose FreedmanRiles, USA), 531 (Savanna Sweeney, AUS)
  Why: Non-European competitors are intentionally excluded per normalization rules, but this should be verified as correct behavior
  Next: Confirm that non-European exclusion is working as intended
- [medium] `name` Name formatting inconsistencies (parser_bug=true, source_limitation=false)
  CSV: Astrid Faber Fengergroen (missing space in compound surname)
  Raw: FengerGroen -> Astrid Faber FengerGroen, FreedmanRiles -> Rose FreedmanRiles
  Why: Compound surnames are not being handled consistently - some lose internal spacing or capitalization
  Next: Review name parsing logic for compound surnames and multi-part names
- [low] `status` Status code normalization (parser_bug=false, source_limitation=false)
  CSV: Status shows 'MP' in CSV
  Raw: Status shows 'MissingPunch' in XML
  Why: This appears to be correct normalization from verbose to abbreviated status codes
  Next: No action needed - this is expected normalization
- [low] `rank` Tied rankings handled correctly (parser_bug=false, source_limitation=false)
  CSV: Both competitors show rank 44, next rank is 46
  Raw: Position 44 appears twice with same time 4548
  Why: Tied rankings are handled correctly with proper rank progression
  Next: No action needed - correct tie handling

### Notable Matches

- Brina Kolner (SLO) correctly extracted as winner with 3284 seconds
- Sara Szakal Biro (HUN) correctly shows rank 2 with 3337 seconds
- DNF/DNS statuses correctly normalized (Helene Scheele DNF, Zina Macajova DNS)
- Time conversions accurate (XML time 3284 = CSV time_seconds 3284)
- Country codes properly normalized (Ungheria->HUN, Repubblica Ceca->CZE, etc.)
- Missing punch statuses correctly converted from MissingPunch to MP
- Tied positions handled correctly (rank 44 tie, rank 74 tie)

## 2026/03-relay-results-eventor.xml [M16]

- Verdict: `review`
- Confidence: `high`
- Related CSVs: `2026/relay.csv`
- Classes: `M16`
- Summary: Several significant issues found including incorrect ranking for DNF teams, missing team (USA 1), and potential country exclusions that need verification

### Issues

- [high] `rank` DNF teams assigned incorrect ranks (parser_bug=true, source_limitation=false)
  CSV: Croatia 1 has rank=25 and status=DNF, Turkiye 1 has rank=24 and status=DNF
  Raw: Croatia 1 shows <Status>DidNotFinish</Status> with Position 27, Turkiye 1 shows <Status>DidNotFinish</Status> with Position 28
  Why: DNF teams should not have numerical ranks - they should be unranked or have a special DNF designation
  Next: Fix parser to not assign numerical ranks to DNF teams
- [high] `missing-row` USA 1 team completely missing from CSV (parser_bug=true, source_limitation=false)
  CSV: No USA 1 team found in CSV output
  Raw: USA 1 team appears in raw XML with Alexander Eriksson (leg 1: 1893s) and Mark Fey (leg 2: 2539s), but no leg 3 runner listed
  Why: Complete team missing from normalized results despite appearing in source data
  Next: Investigate why USA 1 team was dropped - likely due to incomplete leg 3 data
- [medium] `missing-row` New Zealand 1 team missing from CSV (parser_bug=false, source_limitation=false)
  CSV: No New Zealand 1 team found in CSV output
  Raw: New Zealand 1 team appears with Daniel Porteous (1864s), Jamie Appleton (2280s), Xavier White (2531s), total 6675s
  Why: Complete team with all leg times missing from results
  Next: Verify if NZL is intentionally excluded as non-European or if this is a parser bug
- [medium] `missing-row` Australia 1 team missing from CSV (parser_bug=false, source_limitation=false)
  CSV: No Australia 1 team found in CSV output
  Raw: Australia 1 team appears with Rory Shedden (1938s), Baxter Peel (2515s), Euan Shedden (2840s), total 7293s
  Why: Complete team with all leg times missing from results
  Next: Verify if AUS is intentionally excluded as non-European or if this is a parser bug
- [low] `rank` Rank sequence has gap (parser_bug=true, source_limitation=false)
  CSV: Ranks go 1-23, then 25, 24 (for DNF teams)
  Raw: Teams ranked 1-23 in source, with positions 27-28 for DNF teams
  Why: Missing rank 24 in sequence, and DNF teams should not have numerical ranks
  Next: Fix ranking logic to handle DNF teams properly and maintain sequence

### Notable Matches

- Czechia 1 correctly shows as winners with 4925 total seconds (1653+1709+1563)
- Finland 1 correctly in 2nd place with 4935 total seconds, just 10 seconds behind
- All leg times and runner names match source data for included teams
- Country codes properly normalized (ESP for Spain, GBR for Great Britain, etc.)
- Team names correctly extracted with country and number designation

## 2026/03-relay-results-eventor.xml [M18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2026/relay.csv`
- Classes: `M18`
- Summary: All 27 M18 relay teams correctly extracted with accurate times, names, and statuses

### Issues

- None reported.

### Notable Matches

- Finland 1 correctly shows 1st place with 6001 total seconds (1:40:01) and all three leg times match XML
- Czechia 1 properly extracted as 2nd place with Martin Bulicka's winning leg 3 time of 1900 seconds
- Spain 1 correctly marked as MP (MissingPunch) status with rank 27, matching XML MissingPunch status
- Australia 1 properly excluded - team had MP status on leg 1 and DNS on leg 3, not in European federation list
- New Zealand 1 properly excluded - non-European federation as expected
- United States 1 properly excluded - non-European federation as expected
- All leg times accurately converted from XML seconds to CSV seconds (e.g., Vilho Hietala 1948s, Joakim Savinainen 2036s)
- Country codes properly normalized (e.g., 'Repubblica Ceca' → 'CZE', 'Finlandia' → 'FIN')
- Names correctly formatted in 'Given Surname' order from XML Family/Given structure

## 2026/03-relay-results-eventor.xml [W16]

- Verdict: `review`
- Confidence: `high`
- Related CSVs: `2026/relay.csv`
- Classes: `W16`
- Summary: Several significant issues found including missing teams, incorrect rankings, and status mismatches that require investigation

### Issues

- [high] `missing-row` New Zealand 1 team completely missing from CSV (parser_bug=true, source_limitation=false)
  CSV: No New Zealand team found in CSV
  Raw: New Zealand 1 team with Sophie Herde, Ianthe MacMillan Armstrong, Sophie Bacchus - rank 16, total time 7429 seconds
  Why: Complete team missing from extracted data despite clear presence in raw XML with full results
  Next: Check parser logic for New Zealand team extraction
- [high] `missing-row` United States 1 team completely missing from CSV (parser_bug=true, source_limitation=false)
  CSV: No United States team found in CSV
  Raw: United States 1 team with Sophie Neumann, Allison Coates, Josalyn Dunlap - rank 25 (DNF), partial time 6343 seconds
  Why: Complete team missing from extracted data despite clear presence in raw XML
  Next: Check parser logic for United States team extraction
- [high] `missing-row` Australia 1 team completely missing from CSV (parser_bug=true, source_limitation=false)
  CSV: No Australia team found in CSV
  Raw: Australia 1 team with Ella Maja Lang, Veronika Iskhakova - rank 27 (DNS), partial time 4225 seconds
  Why: Complete team missing from extracted data despite clear presence in raw XML
  Next: Check parser logic for Australia team extraction
- [high] `rank` Turkey ranking inconsistency (parser_bug=false, source_limitation=true)
  CSV: TUR ranked as 20 in CSV
  Raw: Turkiye 1 shows Position 20 in OverallResult
  Why: Raw XML shows position 20 but this creates a gap in rankings (no rank 19 in CSV)
  Next: Verify if rank 19 team exists or if rankings should be consecutive
- [medium] `status` Belgium team status mismatch (parser_bug=false, source_limitation=true)
  CSV: BEL status shows DNF with rank 18
  Raw: Belgium 1 shows only leg 1 completed (Anna Pasquasy 2339s), no leg 2 or 3 data
  Why: Team appears to have DNS for legs 2&3 but CSV shows DNF status
  Next: Clarify if incomplete team should be DNF or DNS
- [medium] `rank` Belgium ranking placement (parser_bug=false, source_limitation=true)
  CSV: BEL ranked as 18 between complete teams
  Raw: Belgium 1 has only partial completion
  Why: Incomplete team ranked among complete teams rather than at end
  Next: Verify ranking logic for incomplete teams

### Notable Matches

- Croatia 1 correctly extracted as rank 1 with 5488 total seconds and all three leg times matching
- Czechia 1 properly shows rank 2 with correct total time 5969 and individual leg times
- Latvia 1 accurately extracted with rank 3 and matching times for all legs
- Hungary 1 correctly shows MP status with Anna Kesseru Lukacs missing punch on leg 3
- Ireland 1 properly shows MP status with Beth Joyce missing punch on leg 3
- Country codes correctly normalized (CRO, CZE, LAT, GBR, etc.)
- Names properly formatted in Given Surname order with correct accent handling

## 2026/03-relay-results-eventor.xml [W18]

- Verdict: `pass`
- Confidence: `high`
- Related CSVs: `2026/relay.csv`
- Classes: `W18`
- Summary: The extracted CSV data accurately represents the W18 relay results from the XML source with proper normalization and status handling

### Issues

- None reported.

### Notable Matches

- Czechia 1 correctly extracted as winners with 6458 seconds total time and proper leg breakdown
- Sweden 1 properly placed 2nd with 6487 seconds and all three leg runners correctly identified
- Hungary 1 accurately shown in 3rd with correct team composition and times
- Status handling correct: Bulgaria 1 marked as DNF (incomplete team), Croatia 1 as DNF (only one leg), Israel 1 as MP (MissingPunch), Serbia 1 as DNS (DidNotStart for leg 3)
- Country normalization working properly: 'Czechia' -> 'CZE', 'Great Britain' -> 'GBR', 'Turkiye' -> 'TUR'
- Name normalization applied consistently: 'Tereza Ester Kamenicka', 'Tyra Lilleholt Kraugerud', etc.
- Time conversions accurate: XML times in seconds properly transferred to CSV
- Team names properly extracted and normalized, including complex cases like 'Moldova, Republic of 1'
- Ranking correctly reflects final positions including teams that did not finish all legs
