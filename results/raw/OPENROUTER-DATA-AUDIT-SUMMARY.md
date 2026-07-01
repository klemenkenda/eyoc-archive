# OpenRouter Independent Data Audit Summary

Generated: 2026-07-01T12:20:01.506636+00:00
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

## Year/Discipline Matrix

Legend: `✅` clean, `⚠️` review/low-medium issues, `❌` high-severity issue, `⛔` request failure

| Year | Sprint | Long | Relay |
|---|---|---|---|
| 2002 | ✅ | ✅ | ✅ |
| 2003 | ⚠️ name | ⚠️ name | ⚠️ name |
| 2004 | ✅ | ✅ | ✅ |
| 2005 | ✅ | ✅ | ✅ |
| 2006 | ✅ | ✅ | ⚠️ name, country |
| 2007 | ✅ | ✅ | ✅ |
| 2008 | ⚠️ name | ⚠️ name | ⚠️ name |
| 2009 | ✅ | ✅ | ✅ |
| 2010 | ✅ | ✅ | ✅ |
| 2011 | ✅ | ✅ | ✅ |
| 2012 | ✅ | ✅ | ✅ |
| 2013 | ⚠️ name | ⚠️ name | ⚠️ name |
| 2014 | ❌ missing-row, rank | ✅ | ❌ source-limitation, rank |
| 2015 | ✅ | ✅ | ✅ |
| 2016 | ⚠️ name, other | ❌ status, missing-row | ✅ |
| 2017 | ❌ time, missing-row | ❌ time, missing-row | ❌ name, missing-row |
| 2018 | ✅ | ✅ | ❌ missing-row, name |
| 2019 | ✅ | ✅ | ⚠️ missing-row, name |
| 2021 | ✅ | ✅ | ✅ |
| 2022 | ⚠️ missing-row, name | ❌ country, name | ✅ |
| 2023 | ❌ missing-row, rank | ⚠️ missing-row, name | ⚠️ missing-row, name |
| 2024 | ✅ | ✅ | ✅ |
| 2025 | ❌ country, missing-row | ❌ missing-row, country | ✅ |
| 2026 | ⚠️ other, missing-row | ✅ | ❌ missing-row, status |

## 2002/eyoc2002.htm | verdict=`pass` | confidence=`high` | csv=`2002/long.csv`, `2002/relay.csv`, `2002/sprint.csv` | classes=`(all)`

- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All classes, ranks, times, names, and countries match the source data after...

### Issues

- None reported.

## 2003/eyoc2003.htm | verdict=`pass` | confidence=`high` | csv=`2003/long.csv`, `2003/relay.csv`, `2003/sprint.csv` | classes=`(all)`

- Summary: The CSV extraction accurately represents the raw source data with proper normalization applied. All major data points match correctly across sprint, long distance, and relay...

### Issues

- [low] `name` Minor name variations in relay teams
  CSV: Both spellings appear consistently within their respective contexts
  Raw: Struhalova Olena vs Srtuhalova Olena in individual events
  Why: The raw source shows slight spelling variations between individual and relay sections, which the CSV preserves accurately
  Next: No action needed - this reflects source inconsistencies
- [low] `name` Abbreviated names in relay results
  CSV: CSV preserves the abbreviated forms as they appear in relay sections
  Raw: Nin Oleynichenkova, Karin D´Harreville in relay vs full names in individual
  Why: Raw source uses abbreviated names in relay results, CSV correctly preserves these
  Next: No action needed - accurately reflects source formatting

## 2004/eyoc2004.htm | verdict=`pass` | confidence=`high` | csv=`2004/long.csv`, `2004/relay.csv`, `2004/sprint.csv` | classes=`(all)`

- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All major data points match correctly.

### Issues

- None reported.

## 2005/eyoc2005.htm | verdict=`pass` | confidence=`high` | csv=`2005/long.csv`, `2005/relay.csv`, `2005/sprint.csv` | classes=`(all)`

- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All individual and relay results are correctly parsed with appropriate class,...

### Issues

- None reported.

## 2006/2006_relay_m16.txt | verdict=`pass` | confidence=`high` | csv=`2006/relay.csv` | classes=`(all)`

- Summary: CSV accurately represents the raw relay results with proper normalization applied

### Issues

- None reported.

## 2006/2006_relay_m18.txt | verdict=`review` | confidence=`medium` | csv=`2006/relay.csv` | classes=`(all)`

- Summary: Most data matches well, but several issues need review: incorrect country code (ROU vs ROM), problematic relay leg composition with female athlete in male class, and some name...

### Issues

- [medium] `country` Country code mismatch for Romania
  CSV: ROU,Team ROM 62
  Raw: Team ROM 62
  Why: Raw source shows 'ROM' but CSV normalized to 'ROU'. Need to verify if ROM->ROU normalization is correct for 2006 EYOC
  Next: Verify correct country code for Romania in 2006 EYOC context
- [medium] `relay-composition` Female athlete in male relay team
  CSV: (Jerica (Ak)) (Bernik) - normalized as leg2 runner in M18 class
  Raw: (Bernik), (Jerica (AK)) (0) - appears to be female name Jerica
  Why: While female athletes can appear in male teams when incomplete, the parentheses and formatting suggest this may be a placeholder or substitution that needs verification
  Next: Verify if this relay composition accurately reflects the raw source intent
- [low] `name` Name normalization concerns
  CSV: Matij Klusacek vs Kaspar Hagler vs Bjorseth
  Raw: Klusácek, Matìj vs Hägler, Kaspar vs Bjørseth
  Why: Accent removal and diacritic handling appears inconsistent - some preserved, others removed
  Next: Review accent handling consistency in name normalization
- [low] `name` Unusual name formatting in SLO team
  CSV: (Jerica (Ak)) (Bernik)
  Raw: (Bernik), (Jerica (AK)) (0)
  Why: Parentheses and formatting preserved in normalized name, which seems unusual for standard name normalization
  Next: Clean up parentheses and formatting artifacts in name normalization

## 2006/2006_relay_w16.txt | verdict=`pass` | confidence=`high` | csv=`2006/relay.csv` | classes=`(all)`

- Summary: CSV accurately represents the raw relay results with proper normalization applied

### Issues

- None reported.

## 2006/2006_relay_w18.txt | verdict=`pass` | confidence=`high` | csv=`2006/relay.csv` | classes=`(all)`

- Summary: CSV accurately represents the raw relay results with proper normalization applied

### Issues

- None reported.

## 2006/eyoc2006.htm | verdict=`pass` | confidence=`high` | csv=`2006/long.csv`, `2006/sprint.csv` | classes=`(all)`

- Summary: The CSV extraction accurately represents the raw source data with proper normalization applied. All individual results match the source with correct class normalization, time...

### Issues

- None reported.

## 2007/eyoc2007.htm | verdict=`pass` | confidence=`high` | csv=`2007/long.csv`, `2007/relay.csv`, `2007/sprint.csv` | classes=`(all)`

- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All individual and relay results match the source data with appropriate class,...

### Issues

- None reported.

## 2008/eyoc2008.htm | verdict=`pass` | confidence=`high` | csv=`2008/long.csv`, `2008/relay.csv`, `2008/sprint.csv` | classes=`(all)`

- Summary: The extracted CSV data accurately represents the raw source with proper normalization applied. All major data points match correctly.

### Issues

- [low] `name` Minor name variations in sprint results
  CSV: Klingenberg (missing first name), Rafols (missing first name)
  Raw: Klingenberg, Ita (W16 rank 30), Pol Rafols (M18 rank 55)
  Why: Some names appear abbreviated in sprint results, likely due to space constraints in original formatting
  Next: Accept as source limitation - sprint results appear to have abbreviated some names

## 2009/eyoc2009.htm | verdict=`pass` | confidence=`high` | csv=`2009/long.csv`, `2009/relay.csv`, `2009/sprint.csv` | classes=`(all)`

- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All major data points match correctly across sprint, long, and relay events.

### Issues

- None reported.

## 2010/eyoc2010.htm | verdict=`pass` | confidence=`high` | csv=`2010/long.csv`, `2010/relay.csv`, `2010/sprint.csv` | classes=`(all)`

- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All major data points match correctly including names, times, countries, and...

### Issues

- None reported.

## 2011/eyoc2011.htm | verdict=`pass` | confidence=`high` | csv=`2011/long.csv`, `2011/relay.csv`, `2011/sprint.csv` | classes=`(all)`

- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All major elements including names, times, countries, classes, and rankings...

### Issues

- None reported.

## 2012/eyoc2012.htm | verdict=`pass` | confidence=`high` | csv=`2012/long.csv`, `2012/relay.csv`, `2012/sprint.csv` | classes=`(all)`

- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All major data points match correctly.

### Issues

- None reported.

## 2013/eyoc2013.htm | verdict=`pass` | confidence=`high` | csv=`2013/long.csv`, `2013/relay.csv`, `2013/sprint.csv` | classes=`(all)`

- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All major data points match correctly.

### Issues

- [low] `name` Potential name parsing issue for Netherlands athletes
  CSV: Nina Roothans 96 The, Paul Roothans 95 The
  Raw: Nina Roothans 96 THE NETHERLANDS, Paul Roothans 95 THE NETHERLANDS
  Why: The country name 'THE NETHERLANDS' appears to be partially included in the athlete name field, showing as 'Nina Roothans 96 The' instead of just 'Nina Roothans'
  Next: Review name parsing logic for athletes from 'THE NETHERLANDS' to ensure country text is properly separated from names

## 2014/results-long.pdf | verdict=`pass` | confidence=`high` | csv=`2014/long.csv` | classes=`(all)`

- Summary: The CSV data accurately represents the raw PDF source with proper normalization applied. All entries match the source data with expected class normalization, country code...

### Issues

- None reported.

## 2014/results-relay.pdf | verdict=`review` | confidence=`low` | csv=`2014/relay.csv` | classes=`(all)`

- Summary: Cannot perform meaningful audit due to missing raw source text from PDF. Several potential issues identified in CSV data including duplicate ranks, missing leg times, and unusual...

### Issues

- [high] `source-limitation` Raw PDF text unavailable for comparison
  CSV: 85 relay team entries across all classes
  Raw: [no raw text extracted]
  Why: Cannot verify CSV accuracy against source without readable raw text
  Next: Re-extract PDF text or obtain alternative source format for proper audit
- [medium] `rank` Duplicate and missing ranks in multiple classes
  CSV: M16 has rank 6 twice (DEN and AUT), M18 has rank 6 twice (FRA and ITA), several teams missing ranks
  Raw: Cannot verify from source
  Why: Ranking inconsistencies suggest potential parsing errors
  Next: Verify ranking sequence against original PDF
- [medium] `time` Missing leg times in multiple entries
  CSV: Examples: TUR W16 leg2 missing, EST M16 leg1 missing, LAT W18 leg3 missing
  Raw: Cannot verify from source
  Why: Missing times could indicate parsing issues or source data problems
  Next: Check if times are present in original PDF but not extracted
- [low] `country` Unusual country formatting
  CSV: MDA shows as 'Moldova Moldova', IRL shows as 'lreland' (lowercase L)
  Raw: Cannot verify from source
  Why: Formatting suggests potential OCR or parsing artifacts
  Next: Verify country names in original PDF and normalize properly

## 2014/results-sprint.pdf | verdict=`fail` | confidence=`high` | csv=`2014/sprint.csv` | classes=`(all)`

- Summary: Missing winner Ricardo Esteves (POR) from M16 class and several other Portuguese athletes, plus systematic exclusion of Portuguese results

### Issues

- [high] `missing-row` Missing M16 winner Ricardo Esteves
  CSV: CSV starts with rank 1 as Tuomas Heikkila (FIN)
  Raw: 1 39 Ricardo Esteves 98 PO 11:51 0:00
  Why: The actual winner of M16 class (Ricardo Esteves from Portugal) is completely missing from the CSV, causing all subsequent ranks to be shifted down by one position
  Next: Fix parser to include Portuguese (PO/POR) athletes - they appear to be systematically excluded
- [high] `missing-row` Missing Portuguese athletes across all classes
  CSV: No Portuguese athletes found in any class
  Raw: Multiple PO entries: 98 Joăo Bernandino, 71 António Ferreira, 14 Joăo Casal, 169 Beatriz Sanguino, 217 Joăo Novo, 272 Daniel Catarino, 242 André Esteves, 281 Bernardo Pereira, 344 Beatriz Moreira, 366 Catarina Reis
  Why: All Portuguese (PO) athletes are systematically missing from the normalized CSV, suggesting the parser doesn't recognize 'PO' as a valid country code
  Next: Add 'PO' as an alias for Portugal (POR) in the country normalization logic
- [medium] `rank` Rank sequence errors due to missing winner
  CSV: M16 ranks: 1 Tuomas Heikkila (FIN), 2 Vojtech Sykora (CZE), 3 Antonie Guenin (FRA)
  Raw: M16 ranks: 1 Ricardo Esteves (PO), 2 Tuomas Heikkilä (FIN), 3 Vojtěch Sýkora (CZE)
  Why: Due to missing Portuguese winner, all M16 ranks are shifted incorrectly - what should be rank 2 appears as rank 1, etc.
  Next: Fix Portuguese country recognition to restore correct ranking sequence
- [medium] `country` GE vs GER country code inconsistency
  CSV: CSV shows 'GER' for same athletes: Veit Slodowski GER, Ole Hennseler GER
  Raw: Raw shows 'GE' for German athletes: 82 Veit Slodowski 98 GE, 35 Ole Hennseler 98 GE
  Why: Country normalization from 'GE' to 'GER' is correct but should be verified as intentional
  Next: Confirm 'GE' -> 'GER' normalization is working as intended

## 2015/results-lf.pdf | verdict=`pass` | confidence=`high` | csv=`2015/long.csv` | classes=`(all)`

- Summary: CSV data accurately matches the raw PDF source with proper normalization applied

### Issues

- None reported.

## 2015/results-relay.pdf | verdict=`pass` | confidence=`high` | csv=`2015/relay.csv` | classes=`(all)`

- Summary: CSV data accurately matches the raw PDF source with proper normalization applied

### Issues

- None reported.

## 2015/results-sf.pdf | verdict=`pass` | confidence=`high` | csv=`2015/sprint.csv` | classes=`(all)`

- Summary: The CSV data accurately represents the raw PDF source with proper normalization applied. All entries, ranks, times, countries, and statuses match the source data correctly.

### Issues

- None reported.

## 2016/results-long.pdf | verdict=`fail` | confidence=`high` | csv=`2016/long.csv` | classes=`(all)`

- Summary: Multiple athletes incorrectly assigned times and ranks when they should have MISPUNCH, OVERTIME, or DISQ status

### Issues

- [high] `status` M16 DNF athletes incorrectly given finishing times
  CSV: These athletes appear with ranks 81-85 and specific times like 6131, 6155 seconds
  Raw: GARRIDO CORRAL Miguel shows 'MISPUNCH', ALLMANN Hando shows 'MISPUNCH', etc.
  Why: Athletes with MISPUNCH/OVERTIME/DISQ status should not have finishing times or numerical ranks
  Next: Fix parser to correctly handle non-OK statuses and not assign times to MISPUNCH/OVERTIME/DISQ athletes
- [medium] `missing-row` Multiple MISPUNCH/OVERTIME athletes missing from CSV
  CSV: These athletes are completely absent from the CSV
  Raw: Many athletes listed with MISPUNCH, OVERTIME, DISQ status in all classes
  Why: Non-finishing athletes should still appear in results with appropriate status codes
  Next: Include all athletes from raw results with correct status codes (MP, DNS, DNF, DSQ)
- [low] `time` Some time conversions may be incorrect for DNF entries
  CSV: Converted to seconds like 6131, 6339
  Raw: Times like '102.11', '105.39' for athletes who should be MISPUNCH
  Why: These times should not exist for non-finishing athletes
  Next: Ensure time conversion only applies to athletes with OK status

## 2016/results-relay.pdf | verdict=`pass` | confidence=`high` | csv=`2016/relay.csv` | classes=`(all)`

- Summary: The CSV data accurately represents the relay results from the 2016 PDF source with proper normalization applied

### Issues

- None reported.

## 2016/results-sprint.pdf | verdict=`review` | confidence=`low` | csv=`2016/sprint.csv` | classes=`(all)`

- Summary: Cannot verify accuracy due to missing raw source text, but CSV shows concerning patterns including corrupted names, suspicious bib numbers, and potential OCR artifacts that need...

### Issues

- [medium] `name` Multiple corrupted or incomplete names
  CSV: Names like 'Spektorsfricis', 'Repsysadomas', 'Lorenztimon', 'Dzalbsedijs', 'Upitisuldis', 'Hirsotakar', 'Iinkfvichigor', 'Wolzaymeric', 'Szocsattila', 'Eerolalotta', 'Smulems de', 'Korvellorely', 'Georgievaniya', 'Myroniukalina', 'Gokculsumeyra', 'Leenukka Hanhijarvi', 'Indolalinda', 'Emilijaanna Stage'
  Raw: [no raw text available]
  Why: Many names appear corrupted, incomplete, or contain OCR artifacts that seem unlikely to be real names
  Next: Manual verification against original PDF to determine if these are OCR errors or parsing issues
- [medium] `other` Suspicious bib number
  CSV: M18 row with bib '3481' for 'Iinkfvichigor' from RUS
  Raw: [no raw text available]
  Why: Bib number 3481 is unusually high compared to other bib numbers in 200-400 range, suggesting possible OCR error
  Next: Verify this bib number against the original PDF
- [low] `rank` Rank sequence anomaly in W18
  CSV: W18 shows rank 69, then 71, then 69 again: 'Lucia Matejickova' rank 69, 'Minati Alessandra' rank 71, 'Sandrine Defraigne' rank 69
  Raw: [no raw text available]
  Why: Duplicate rank 69 with rank 71 in between suggests possible parsing error or tie handling issue
  Next: Check original PDF for correct ranking sequence in W18 class
- [low] `source-limitation` All confidence marked as 'approx'
  CSV: Every row has confidence=approx
  Raw: [no raw text available]
  Why: Consistent 'approx' confidence suggests OCR-derived data which explains name corruption issues
  Next: Accept as expected for OCR-derived results, but verify critical data points

## 2017/result-sprint.pdf | verdict=`review` | confidence=`high` | csv=`2017/sprint.csv` | classes=`(all)`

- Summary: Several significant issues found including incorrect time conversions, missing competitors, and potential data corruption

### Issues

- [high] `time` Incorrect time conversion for M16 rank 78 Timo Tantanini
  CSV: M16,78,OK,0113,SUI,Timo Tantanini,1353,high
  Raw: 78. Timo Tantanini SUI0113 C Switzerland 17.05 + 4.23
  Why: Raw shows 17.05 (17 minutes 5 seconds = 1025 seconds) but CSV shows 1353 seconds (22 minutes 33 seconds)
  Next: Fix time conversion logic - 17.05 should be 1025 seconds, not 1353
- [high] `missing-row` Missing M16 competitors with times converted to status changes
  CSV: M16,78,DNF,0219,POR,Vasco Amorim Ramos Mendes,,high, M16,80,DNF,0246,UKR,Teremetskyi Tymofii,,high
  Raw: 78. Vasco Amorim Ramos Mendes POR0219 C Portugal 17.05 + 4.23, 80. Teremetskyi Tymofii UKR0246 C Ukraine 17.10 + 4.28, etc.
  Why: Multiple competitors with valid times in raw source appear as DNF with no times in CSV
  Next: Review parser logic for handling times after rank 78 in M16 class
- [high] `time` Multiple M18 competitors missing times despite having them in raw
  CSV: M18,81,DNF,9946,EST,Kiur Erik Eensaar,,high, M18,82,DNF,0044,ESP,Alvaro Casado Gomez,,high
  Raw: 81. Kiur Erik Eensaar EST9946 C Estonia 17.29 + 4.24, 82. Alvaro Casado Gomez ESP0044 C Spain 17.36 + 4.31, etc.
  Why: Raw source shows valid finishing times but CSV shows DNF status with no times
  Next: Fix parser to correctly extract times for M18 competitors after rank 80
- [medium] `missing-row` Guest nations excluded as expected
  CSV: No corresponding rows found
  Raw: 34. Katie Cory-Wright NZL9989 C New Zealand 14.26 + 2.08, 56. Aston Key AUS0002 C Australia 16.01 + 2.56, 62. Danielle Goodall NZL9990 C New Zealand 15.48 + 3.30, 77. Jenna Tidswell NZL0091 C New Zealand 16.40 + 4.22
  Why: Non-EYOC countries (NZL, AUS) correctly excluded from normalized CSV per policy
  Next: No action needed - this is correct normalization behavior
- [low] `name` Minor name normalization differences
  CSV: Morten Ornhagen Jorgensen, Szuromi Ron
  Raw: Morten Örnhagen Jorgensen, Szuromi Áron
  Why: Accent removal and possible OCR artifacts in name processing
  Next: Review name normalization for accent handling consistency

## 2017/results-long.pdf | verdict=`review` | confidence=`high` | csv=`2017/long.csv` | classes=`(all)`

- Summary: Several significant discrepancies found between raw source and CSV, including incorrect time conversions, missing entries, wrong status assignments, and name formatting issues

### Issues

- [high] `time` Incorrect time conversion for M16 rank 72 Peles Vlad
  CSV: M16,72,OK,0130,ROU,Peles Vlad,4788,high
  Raw: 72. Peles Vlad ROU0130 C Romania 68.57 +22.30
  Why: Raw shows 68.57 (4137 seconds) but CSV shows 4788 seconds - significant discrepancy
  Next: Check time parsing logic for this entry
- [high] `time` Incorrect time conversion for W16 rank 78 Ghit Denisa
  CSV: W16,78,OK,0183,ROU,Ghit Denisa,9255,high
  Raw: 78. Ghit Denisa ROU0183 C Romania 73.49 +35.24
  Why: Raw shows 73.49 (4429 seconds) but CSV shows 9255 seconds - major discrepancy
  Next: Check time parsing logic for this entry
- [medium] `missing-row` Missing entries with times in raw source
  CSV: M16,81,DNF,0219,POR,Vasco Amorim Ramos Mendes,,high
  Raw: 81. Vasco Amorim Ramos Mendes POR0219 C Portugal 73.15 +26.48
  Why: Raw source shows time 73.15 but CSV marks as DNF with no time
  Next: Review status determination logic for entries with times
- [medium] `status` Multiple entries with times marked as DNF instead of OK
  CSV: Various M16 entries marked DNF with empty time_seconds
  Raw: Multiple entries like ranks 82-98 in M16 show times but are marked DNF in CSV
  Why: Raw source shows actual finish times but CSV incorrectly assigns DNF status
  Next: Review status assignment logic for entries with valid times
- [medium] `name` Name truncation in CSV
  CSV: M16,37,OK,0210,HUN,Szuromi Ron,3437,high
  Raw: 37. Szuromi Áron HUN0210 C Hungary 57.17 +10.50
  Why: Name appears truncated from 'Szuromi Áron' to 'Szuromi Ron'
  Next: Check name parsing for accent handling and truncation
- [medium] `missing-row` Missing MP entries in CSV
  CSV: No corresponding entry found
  Raw: Timo Tantanini SUI0113 C Switzerland MP
  Why: Raw source shows MP (mispunch) entries that are missing from CSV
  Next: Include MP status entries in CSV output
- [low] `country` Guest nations correctly excluded
  CSV: No entry for Australia
  Raw: 92. Jensen Key AUS0201 C Australia 87.03 +40.36
  Why: Australia is correctly excluded as non-EYOC nation per normalization rules
  Next: No action needed - correct exclusion

## 2017/results-relay.pdf | verdict=`review` | confidence=`high` | csv=`2017/relay.csv` | classes=`(all)`

- Summary: Several significant issues found including missing NZL team, incorrect country codes, and potential name/time mismatches

### Issues

- [high] `missing-row` New Zealand team missing from W18 class
  CSV: No NZL team found in W18 class CSV rows
  Raw: 14. NZL 1 New Zealand 128.08 - Danielle Goodall 42.46 (19) Jenna Tidswell 47.31 (20) Katie Cory-Wright 37.51 (7)
  Why: NZL team appears in raw source at rank 14 in W18 class but is completely missing from CSV
  Next: Check if NZL should be excluded per EYOC-COUNTRIES.md allowlist or if this is a parser error
- [medium] `country` Romania country code inconsistency
  CSV: ROU (appears in CSV rows)
  Raw: ROM 1 (appears multiple times in raw source)
  Why: Raw source consistently shows 'ROM 1' but CSV uses 'ROU' - need to verify correct normalization
  Next: Verify if ROM->ROU normalization is correct per EYOC-COUNTRIES.md
- [medium] `name` Potential name corruption in M18 SLO team
  CSV: Aan Ravnikar
  Raw: Äan Ravnikar
  Why: Special character 'Ä' appears to be converted to 'A' - may indicate encoding issue
  Next: Check character encoding handling for special characters
- [low] `name` Name normalization inconsistencies
  CSV: van Lommel Jens, de Smul Ems
  Raw: Van Lommel Jens, De Smul Ems
  Why: Inconsistent capitalization of particles 'Van/van' and 'De/de'
  Next: Standardize particle capitalization rules
- [low] `other` Unranked teams with times in raw source
  CSV: Both teams appear with empty rank field
  Raw: POR 1 Portugal 181.54, SRB 1 Serbia 198.34 (both appear without rank numbers)
  Why: Teams have completion times but no official ranking in source - CSV correctly reflects this
  Next: Verify this is correct interpretation of unranked but timed teams

## 2018/results-long.pdf | verdict=`pass` | confidence=`high` | csv=`2018/long.csv` | classes=`(all)`

- Summary: CSV extraction accurately represents the PDF source with proper normalization applied

### Issues

- None reported.

## 2018/results-relay.pdf | verdict=`fail` | confidence=`high` | csv=`2018/relay.csv` | classes=`(all)`

- Summary: Multiple critical data extraction errors including corrupted names, incorrect time assignments, and missing athletes

### Issues

- [high] `name` Corrupted athlete names replaced with header text
  CSV: All three replaced with '2018 Relay Mon 02-Jul-18 Eyoc' in CSV
  Raw: Matan Ivri (M16 Israel leg 3), Amir Zur (M18 Israel leg 3), Laura Fidalgo Casares (W16 Spain leg 3)
  Why: Parser appears to have replaced legitimate athlete names with document header text, creating completely incorrect data
  Next: Fix parser to correctly extract athlete names from leg 3 positions, especially when they span page breaks
- [high] `time` Incorrect time assignment for corrupted names
  CSV: All assigned 1308 seconds (21:48) in CSV
  Raw: Matan Ivri: 30:40, Amir Zur: 32:54, Laura Fidalgo Casares: 31:48
  Why: The corrupted names are also assigned an incorrect time that appears to be derived from the document timestamp
  Next: Ensure correct time extraction for all leg positions, particularly when names are corrupted
- [medium] `missing-row` Australia team excluded from M18 results
  CSV: No Australia entry in M18 class
  Raw: 21 169 Australia Australia 1:44:49 +20:05 with Aston Key, Angus Haines, Alastair George
  Why: Australia (AUS) is not in the EYOC countries allowlist, so exclusion is expected per normalization rules
  Next: No action needed - this is correct normalization behavior
- [medium] `missing-row` New Zealand team excluded from W18 results
  CSV: No New Zealand entry in W18 class
  Raw: 14 66 New Zealand New Zealand 1:39:11 +15:23 with Jenna Tidswell, Marisol Hunter, Briana Steven
  Why: New Zealand (NZL) is not in the EYOC countries allowlist, so exclusion is expected per normalization rules
  Next: No action needed - this is correct normalization behavior
- [low] `country` Country name truncation in team field
  CSV: Correctly normalized to RUS in country field but team field shows truncated version
  Raw: Russian Federati Russian Feder appears multiple times
  Why: Team field preserves source formatting while country field is properly normalized - this is acceptable
  Next: Consider whether team field should also be normalized or if source preservation is preferred

## 2018/results-sprint.pdf | verdict=`pass` | confidence=`high` | csv=`2018/sprint.csv` | classes=`(all)`

- Summary: The CSV extraction accurately represents the raw PDF source with proper normalization applied. All competitors, times, ranks, and statuses match the source data. Guest nations...

### Issues

- None reported.

## 2019/Long-eventor.xml [M16] | verdict=`pass` | confidence=`high` | csv=`2019/long.csv` | classes=`M16`

- Summary: All 102 M16 entries from the XML source are correctly extracted and normalized in the CSV. Times, ranks, names, countries, and statuses all match accurately.

### Issues

- None reported.

## 2019/Long-eventor.xml [M18] | verdict=`pass` | confidence=`high` | csv=`2019/long.csv` | classes=`M18`

- Summary: All M18 class entries from the XML source are correctly extracted and normalized in the CSV, with proper handling of times, statuses, and country codes

### Issues

- None reported.

## 2019/Long-eventor.xml [W16] | verdict=`pass` | confidence=`high` | csv=`2019/long.csv` | classes=`W16`

- Summary: CSV data accurately matches the raw XML source with proper normalization applied

### Issues

- None reported.

## 2019/Long-eventor.xml [W18] | verdict=`pass` | confidence=`high` | csv=`2019/long.csv` | classes=`W18`

- Summary: CSV data accurately matches the raw XML source with proper normalization applied

### Issues

- None reported.

## 2019/Sprint-eventor.xml [M16] | verdict=`pass` | confidence=`high` | csv=`2019/sprint.csv` | classes=`M16`

- Summary: CSV data accurately matches the raw XML source with proper normalization applied

### Issues

- None reported.

## 2019/Sprint-eventor.xml [M18] | verdict=`pass` | confidence=`high` | csv=`2019/sprint.csv` | classes=`M18`

- Summary: All 106 M18 competitors from the XML source are correctly represented in the CSV with accurate ranks, times, countries, and statuses

### Issues

- None reported.

## 2019/Sprint-eventor.xml [W16] | verdict=`pass` | confidence=`high` | csv=`2019/sprint.csv` | classes=`W16`

- Summary: CSV extraction correctly matches the raw XML source with proper normalization applied

### Issues

- None reported.

## 2019/Sprint-eventor.xml [W18] | verdict=`pass` | confidence=`high` | csv=`2019/sprint.csv` | classes=`W18`

- Summary: All 98 W18 competitors from the XML source are correctly extracted and normalized in the CSV with accurate ranks, times, countries, and names

### Issues

- None reported.

## 2019/result-relay.pdf | verdict=`review` | confidence=`medium` | csv=`2019/relay.csv` | classes=`(all)`

- Summary: The CSV extraction appears largely accurate but has several issues requiring review: missing teams with MP status, a potential name normalization error, and exclusion of non-EYOC...

### Issues

- [medium] `missing-row` Missing MP status teams from CSV
  CSV: These teams are completely absent from the CSV
  Raw: Teams 324 Moldova (W16), 322 Serbia (W16), 207 Spain (M16), 121 Turkey (W18), 112 Romania (W18), 12 Great Britain (M18), 28 Serbia (M18), 23 Spain (M18) all show 'mp' status
  Why: Teams with MP status should be included in normalized results with status=MP, not excluded entirely
  Next: Include MP status teams in CSV with appropriate status field
- [low] `name` Potential name normalization inconsistency
  CSV: Marco Anselmo di Stefano
  Raw: Marco Anselmo Di Stefano (M16 Italy leg 1)
  Why: Capitalization of 'Di' vs 'di' - minor but worth checking normalization consistency
  Next: Verify name capitalization normalization rules are consistently applied
- [low] `missing-row` New Zealand team excluded from CSV
  CSV: New Zealand team is absent from CSV
  Raw: 323 New Zealand team appears in W16 results with rank 23 and complete times
  Why: Expected exclusion as NZL is not in EYOC-COUNTRIES allowlist, but worth confirming this is intentional
  Next: Confirm New Zealand exclusion is correct per EYOC country policy
- [low] `missing-row` Mixed relay teams with MP status missing
  CSV: These Mixed teams are absent from CSV
  Raw: Teams 420, 417, 410, 411 in MIX class show 'mp' status with partial results
  Why: Mixed relay MP teams should likely be included with status=MP
  Next: Include Mixed MP teams in CSV if Mixed class is supported

## 2021/Long-eventor.xml [M16] | verdict=`pass` | confidence=`high` | csv=`2021/long.csv` | classes=`M16`

- Summary: CSV data accurately matches the raw XML source with proper normalization applied

### Issues

- None reported.

## 2021/Long-eventor.xml [M18] | verdict=`pass` | confidence=`high` | csv=`2021/long.csv` | classes=`M18`

- Summary: CSV extraction accurately represents the XML source data with proper normalization applied

### Issues

- None reported.

## 2021/Long-eventor.xml [W16] | verdict=`pass` | confidence=`high` | csv=`2021/long.csv` | classes=`W16`

- Summary: The CSV extraction accurately represents the W16 class results from the 2021 Long XML source. All 88 competitors are correctly captured with proper normalization of class names,...

### Issues

- None reported.

## 2021/Long-eventor.xml [W18] | verdict=`pass` | confidence=`high` | csv=`2021/long.csv` | classes=`W18`

- Summary: The CSV extraction accurately represents the W18 class results from the 2021 Long-eventor.xml source file. All 89 entries are correctly processed with proper normalization of...

### Issues

- None reported.

## 2021/Sprint-eventor.xml [M16] | verdict=`pass` | confidence=`high` | csv=`2021/sprint.csv` | classes=`M16`

- Summary: CSV data accurately matches the XML source with proper normalization applied

### Issues

- None reported.

## 2021/Sprint-eventor.xml [M18] | verdict=`pass` | confidence=`high` | csv=`2021/sprint.csv` | classes=`M18`

- Summary: The CSV accurately represents the M18 class results from the 2021 Sprint XML source. All 104 entries are correctly extracted with proper normalization of class names, countries,...

### Issues

- None reported.

## 2021/Sprint-eventor.xml [W16] | verdict=`pass` | confidence=`high` | csv=`2021/sprint.csv` | classes=`W16`

- Summary: CSV extraction accurately represents the W16 class results from the 2021 Sprint XML source with proper normalization

### Issues

- None reported.

## 2021/Sprint-eventor.xml [W18] | verdict=`pass` | confidence=`high` | csv=`2021/sprint.csv` | classes=`W18`

- Summary: All CSV rows accurately match the raw XML source data with proper normalization applied

### Issues

- None reported.

## 2021/results-relay.pdf | verdict=`pass` | confidence=`high` | csv=`2021/relay.csv` | classes=`(all)`

- Summary: The CSV data accurately represents the relay results from the 2021 PDF source. All teams, times, and placements match the raw source after proper normalization.

### Issues

- None reported.

## 2022/Long-eventor.xml [M16] | verdict=`pass` | confidence=`high` | csv=`2022/long.csv` | classes=`M16`

- Summary: The CSV accurately represents the M16 class results from the 2022 Long XML source. All 97 entries are correctly extracted with proper normalization of class names, countries,...

### Issues

- None reported.

## 2022/Long-eventor.xml [M18] | verdict=`pass` | confidence=`high` | csv=`2022/long.csv` | classes=`M18`

- Summary: CSV data accurately matches the XML source with proper normalization applied

### Issues

- None reported.

## 2022/Long-eventor.xml [W16] | verdict=`review` | confidence=`medium` | csv=`2022/long.csv` | classes=`W16`

- Summary: Several guest nations (NZL, AUS) appear in raw source but are correctly excluded from CSV per normalization rules. However, there are potential issues with sex field mismatches...

### Issues

- [medium] `source-limitation` Sex field shows 'M' for all W16 competitors
  CSV: All entries correctly appear in W16 class
  Raw: All PersonResult entries show <Person sex="M"> despite being in W16 class
  Why: Raw XML shows sex='M' for all competitors in W16 class, which appears to be a source data error rather than parser issue
  Next: Verify this is a known source limitation in the XML data format
- [low] `name` Name normalization variations
  CSV: Normalized to 'Monica de Miguel Armisen', 'Guinedell Faja Sanjaume'
  Raw: Names like 'de MIguel Armisen' (with capital I), 'Faja sanjaume' (lowercase s)
  Why: Parser correctly normalizes case inconsistencies in raw source names
  Next: No action needed - proper normalization
- [low] `country` Guest nations correctly excluded
  CSV: These competitors do not appear in CSV
  Raw: Rachel Baker (NZL), Anna Babington (NZL), Erika Enderby (AUS), Milla Key (AUS) appear in raw
  Why: Non-EYOC allowlisted countries are intentionally excluded per normalization rules
  Next: No action needed - correct exclusion per policy

## 2022/Long-eventor.xml [W18] | verdict=`review` | confidence=`high` | csv=`2022/long.csv` | classes=`W18`

- Summary: Several non-EYOC countries appear in CSV that should be excluded per normalization rules

### Issues

- [high] `country` New Zealand athletes included despite non-allowlisted status
  CSV: No NZL entries found in CSV
  Raw: Multiple NZL athletes: Stewart (bib 361), Hayes (bib 317), Babington (bib 342), Joergensen (bib 386)
  Why: NZL is not in the EYOC allowlist and should be excluded from normalized CSV, but appears to be correctly excluded
  Next: Verify this is actually correct - NZL should be excluded
- [high] `country` Australia athlete included despite non-allowlisted status
  CSV: No AUS entries found in CSV
  Raw: Enderby, Mikayla from AUS (bib 325) with time 1:43:52
  Why: AUS is not in the EYOC allowlist and should be excluded from normalized CSV, appears correctly excluded
  Next: Verify this is correct - AUS should be excluded
- [medium] `missing-row` Several athletes from raw source missing from CSV
  CSV: CSV shows 90 entries (87 OK + 3 MP)
  Raw: Raw shows 95 entries total, including NZL and AUS athletes
  Why: Missing entries likely due to intentional exclusion of non-allowlisted countries NZL and AUS
  Next: Confirm that exactly 5 non-EYOC athletes (4 NZL + 1 AUS) were correctly excluded
- [low] `name` Minor name variations in normalization
  CSV: CSV shows 'Tille de Smul', 'Ingeborg Roll Mosland'
  Raw: Raw shows 'De Smul' (bib 379), 'Roll Mosland' (bib 371)
  Why: Name formatting appears consistent with normalization rules for title case and given/surname order
  Next: No action needed - normal name normalization

## 2022/Sprint-eventor.xml [M16] | verdict=`pass` | confidence=`high` | csv=`2022/sprint.csv` | classes=`M16`

- Summary: The CSV data accurately represents the M16 class results from the 2022 Sprint XML source. All 98 entries are correctly extracted with proper normalization of class names,...

### Issues

- None reported.

## 2022/Sprint-eventor.xml [M18] | verdict=`review` | confidence=`high` | csv=`2022/sprint.csv` | classes=`M18`

- Summary: CSV correctly excludes non-EYOC guest nations (AUS, NZL, CAN) but includes all EYOC-allowlisted countries. All times, ranks, and statuses match the XML source accurately.

### Issues

- [low] `missing-row` Guest nations excluded from CSV as expected
  CSV: These competitors do not appear in the CSV
  Raw: Sam Woolford (AUS), Felix Hunt (NZL), Toby Cazzolato (AUS), Alec Le Helloco (CAN) appear in XML with OK status
  Why: This is expected behavior - non-EYOC guest nations are intentionally excluded from normalized CSVs
  Next: No action needed - this is correct normalization behavior

## 2022/Sprint-eventor.xml [W16] | verdict=`review` | confidence=`medium` | csv=`2022/sprint.csv` | classes=`W16`

- Summary: Several guest nations (AUS, NZL) appear in raw source but are correctly excluded from CSV per normalization rules. However, there are some potential issues with name formatting...

### Issues

- [low] `missing-row` Australia competitors excluded from CSV
  CSV: No AUS entries in CSV
  Raw: Key Mila (AUS, bib 701, rank 16) and Erika Enderby (AUS, bib 704, rank 27) appear in raw XML
  Why: Guest nations like AUS are intentionally excluded per normalization rules, but flagging for confirmation
  Next: Confirm AUS is not in EYOC-COUNTRIES.md allowlist
- [low] `missing-row` New Zealand competitors excluded from CSV
  CSV: No NZL entries in CSV
  Raw: Anna Babington (NZL, bib 730, rank 43) and Rachel Baker (NZL, bib 748, rank 50) appear in raw XML
  Why: Guest nations like NZL are intentionally excluded per normalization rules, but flagging for confirmation
  Next: Confirm NZL is not in EYOC-COUNTRIES.md allowlist
- [low] `name` Compound surname formatting inconsistency
  CSV: Guinedell Faja Sanjaume in CSV
  Raw: Faja sanjaume -> Guinedell in raw XML
  Why: Raw shows family name as 'Faja sanjaume' but CSV shows 'Guinedell Faja Sanjaume' - may be correct normalization but worth verifying
  Next: Verify name normalization logic for compound surnames
- [low] `name` Name capitalization in compound surname
  CSV: Monica de Miguel Armise in CSV
  Raw: de Miguel Armise -> Monica in raw XML
  Why: Raw shows family name as 'de Miguel Armise' which appears correctly normalized in CSV
  Next: Verify this is correct title case normalization

## 2022/Sprint-eventor.xml [W18] | verdict=`review` | confidence=`medium` | csv=`2022/sprint.csv` | classes=`W18`

- Summary: CSV correctly excludes non-allowlisted guest nations (NZL, AUS) but includes some competitors that appear to be missing from the normalized output

### Issues

- [medium] `missing-row` Missing New Zealand competitors from CSV
  CSV: No NZL entries present in CSV
  Raw: Zara Stewart (NZL, bib 395, rank 46), Kaia Joergensen (NZL, bib 303, rank 57), Katherine Babington (NZL, bib 344, MP), Emily Hayes (NZL, bib 368, DNF)
  Why: Four NZL competitors appear in raw XML but are absent from CSV. This is expected behavior per normalization rules since NZL is not in the EYOC allowlist, but should be confirmed as intentional exclusion rather than parser error
  Next: Confirm this is intentional exclusion of non-allowlisted guest nation NZL
- [medium] `missing-row` Missing Australia competitor from CSV
  CSV: No AUS entries present in CSV
  Raw: Mikayla Enderby (AUS, bib 317, rank 85)
  Why: One AUS competitor appears in raw XML but is absent from CSV. This is expected behavior per normalization rules since AUS is not in the EYOC allowlist, but should be confirmed as intentional exclusion rather than parser error
  Next: Confirm this is intentional exclusion of non-allowlisted guest nation AUS
- [low] `other` Rank sequence gap in CSV
  CSV: CSV shows ranks 1-87 with gap after rank 17 (jumps to 20)
  Raw: Raw shows ranks 1-90 with some ties
  Why: The CSV rank sequence has a gap, but this appears to be due to the intentional exclusion of guest nations that held ranks 18-19 in the original results
  Next: Verify that rank gaps are due to excluded guest nations rather than missing data

## 2022/result-relay.pdf | verdict=`pass` | confidence=`high` | csv=`2022/relay.csv` | classes=`(all)`

- Summary: The CSV accurately represents the relay results from the 2022 PDF source. All ranked teams are correctly extracted with proper normalization of class names, country codes, and...

### Issues

- None reported.

## 2023/Long-eventor.xml [M16] | verdict=`pass` | confidence=`high` | csv=`2023/long.csv` | classes=`M16`

- Summary: The CSV data accurately represents the M16 class results from the XML source with proper normalization applied

### Issues

- None reported.

## 2023/Long-eventor.xml [M18] | verdict=`review` | confidence=`medium` | csv=`2023/long.csv` | classes=`M18`

- Summary: The CSV correctly extracts most data from the XML source, but excludes guest nations (NZL, AUS) as expected. However, there are some notable exclusions that need verification.

### Issues

- [medium] `missing-row` Felix Hunt (NZL) missing from CSV
  CSV: No corresponding row found
  Raw: Felix Hunt, bib 3033, NZL, rank 31, time 1:09:23
  Why: NZL (New Zealand) is not in the EYOC allowlist, so exclusion is expected and correct
  Next: Verify NZL is intentionally excluded per EYOC-COUNTRIES.md
- [medium] `missing-row` Eddie Swain (NZL) missing from CSV
  CSV: No corresponding row found
  Raw: Eddie Swain, bib 3087, NZL, rank 66, time 1:20:06
  Why: NZL (New Zealand) is not in the EYOC allowlist, so exclusion is expected and correct
  Next: Verify NZL is intentionally excluded per EYOC-COUNTRIES.md
- [medium] `missing-row` Riley Croxford (NZL) missing from CSV
  CSV: No corresponding row found
  Raw: Riley Croxford, bib 3073, NZL, rank 71, time 1:22:20
  Why: NZL (New Zealand) is not in the EYOC allowlist, so exclusion is expected and correct
  Next: Verify NZL is intentionally excluded per EYOC-COUNTRIES.md
- [medium] `missing-row` Cooper Horley (AUS) missing from CSV
  CSV: No corresponding row found
  Raw: Cooper Horley, bib 3063, AUS, rank 73, time 1:22:37
  Why: AUS (Australia) is not in the EYOC allowlist, so exclusion is expected and correct
  Next: Verify AUS is intentionally excluded per EYOC-COUNTRIES.md
- [medium] `missing-row` Owen Radajewski (AUS) missing from CSV
  CSV: No corresponding row found
  Raw: Owen Radajewski, bib 3103, AUS, rank 79, time 1:25:27
  Why: AUS (Australia) is not in the EYOC allowlist, so exclusion is expected and correct
  Next: Verify AUS is intentionally excluded per EYOC-COUNTRIES.md
- [medium] `missing-row` Jacob Knoef (NZL) missing from CSV
  CSV: No corresponding row found
  Raw: Jacob Knoef, bib 3009, NZL, rank 93, time 1:37:31
  Why: NZL (New Zealand) is not in the EYOC allowlist, so exclusion is expected and correct
  Next: Verify NZL is intentionally excluded per EYOC-COUNTRIES.md

## 2023/Long-eventor.xml [W16] | verdict=`pass` | confidence=`high` | csv=`2023/long.csv` | classes=`W16`

- Summary: CSV data accurately matches the raw XML source with proper normalization applied

### Issues

- None reported.

## 2023/Long-eventor.xml [W18] | verdict=`review` | confidence=`medium` | csv=`2023/long.csv` | classes=`W18`

- Summary: The CSV correctly extracts most data from the XML source, but excludes guest nations (NZL, AUS) as expected. However, there's a potential issue with one competitor's name...

### Issues

- [low] `name` Name normalization inconsistency for Spanish competitor
  CSV: Guinedell Faja Sanjaume
  Raw: <Family>Faja sanjaume</Family><Given sequence="1">Guinedell</Given>
  Why: The raw XML shows 'Faja sanjaume' (lowercase 's') but CSV shows 'Faja Sanjaume' (title case). This appears to be proper title-case normalization, but worth noting the case change.
  Next: Verify that title-case normalization is consistently applied to family names
- [low] `country` Guest nations excluded as expected
  CSV: These competitors do not appear in the CSV
  Raw: Rachel Baker (NZL), Katherine Babington (NZL), Anna Babington (NZL), Molly McGowan (NZL), Nea Shingler (AUS), Milla Key (AUS), Erika Enderby (AUS)
  Why: Guest nations NZL and AUS are intentionally excluded from normalized CSV as they are not in the EYOC allowlist. This is correct behavior.
  Next: No action needed - this is expected normalization behavior

## 2023/Sprint-eventor.xml [M16] | verdict=`review` | confidence=`high` | csv=`2023/sprint.csv` | classes=`M16`

- Summary: One significant issue found: Leo Croxford (NZL) appears in raw source but is missing from CSV, which contradicts the expected normalization behavior for non-allowlisted countries

### Issues

- [high] `missing-row` Leo Croxford (NZL) missing from CSV despite appearing in raw source
  CSV: No corresponding row found in CSV for Leo Croxford
  Raw: PersonResult for Leo Croxford, bib 1001, NZL, rank 94, time 20:14
  Why: The raw XML clearly shows Leo Croxford from New Zealand (NZL) finishing 94th with time 20:14, but he does not appear in the normalized CSV. While NZL is not in the EYOC allowlist and should be excluded, the CSV shows 95 rows ending with Maksym Barchuk at rank 96, suggesting a gap at rank 94.
  Next: Verify parser logic for handling non-allowlisted countries and ensure consistent exclusion without creating rank gaps

## 2023/Sprint-eventor.xml [M18] | verdict=`review` | confidence=`medium` | csv=`2023/sprint.csv` | classes=`M18`

- Summary: CSV correctly excludes non-EYOC guest nations (AUS, NZL) but includes all EYOC-allowlisted countries. Some athletes appear missing from CSV despite being in raw source.

### Issues

- [medium] `missing-row` Cooper Horley (AUS) missing from CSV
  CSV: No corresponding row found
  Raw: Cooper Horley, rank 11, bib 3050, AUS, time 13:20
  Why: Australian athlete appears in raw source at rank 11 but is missing from CSV. This is expected behavior as AUS is not in EYOC allowlist.
  Next: Confirm AUS is intentionally excluded per EYOC-COUNTRIES.md allowlist
- [medium] `missing-row` Felix Hunt (NZL) missing from CSV
  CSV: No corresponding row found
  Raw: Felix Hunt, rank 51, bib 3017, NZL, time 14:37
  Why: New Zealand athlete appears in raw source at rank 51 but is missing from CSV. This is expected behavior as NZL is not in EYOC allowlist.
  Next: Confirm NZL is intentionally excluded per EYOC-COUNTRIES.md allowlist
- [medium] `missing-row` Jacob Knoef (NZL) missing from CSV
  CSV: No corresponding row found
  Raw: Jacob Knoef, rank 53, bib 3067, NZL, time 14:42
  Why: New Zealand athlete appears in raw source at rank 53 but is missing from CSV. This is expected behavior as NZL is not in EYOC allowlist.
  Next: Confirm NZL is intentionally excluded per EYOC-COUNTRIES.md allowlist
- [medium] `missing-row` Riley Croxford (NZL) missing from CSV
  CSV: No corresponding row found
  Raw: Riley Croxford, rank 61, bib 3042, NZL, time 14:58
  Why: New Zealand athlete appears in raw source at rank 61 but is missing from CSV. This is expected behavior as NZL is not in EYOC allowlist.
  Next: Confirm NZL is intentionally excluded per EYOC-COUNTRIES.md allowlist
- [medium] `missing-row` Owen Radajewski (AUS) missing from CSV
  CSV: No corresponding row found
  Raw: Owen Radajewski, rank 75, bib 3060, AUS, time 15:37
  Why: Australian athlete appears in raw source at rank 75 but is missing from CSV. This is expected behavior as AUS is not in EYOC allowlist.
  Next: Confirm AUS is intentionally excluded per EYOC-COUNTRIES.md allowlist
- [low] `rank` Rank sequence adjustment after guest exclusions
  CSV: CSV shows consecutive ranks without gaps
  Raw: Raw ranks include gaps where guest nations were removed
  Why: After excluding AUS/NZL athletes, ranks appear to be renumbered consecutively, which may be correct normalization
  Next: Verify if rank renumbering after guest exclusion is intended behavior

## 2023/Sprint-eventor.xml [W16] | verdict=`pass` | confidence=`high` | csv=`2023/sprint.csv` | classes=`W16`

- Summary: All 81 W16 competitors correctly extracted from XML source with accurate ranks, times, countries, and names

### Issues

- None reported.

## 2023/Sprint-eventor.xml [W18] | verdict=`review` | confidence=`medium` | csv=`2023/sprint.csv` | classes=`W18`

- Summary: The CSV correctly extracts most data but excludes guest nations (AUS, NZL) as expected. However, there are some ranking inconsistencies that need review.

### Issues

- [medium] `rank` Missing rank 29 in CSV extraction
  CSV: Anna Taksdal appears as rank 28, but should be rank 29 since Enderby (AUS) at rank 29 was excluded
  Raw: Erika Enderby (AUS) has ResultPosition 29, Anna Taksdal (NOR) has ResultPosition 30
  Why: When guest nations are excluded, subsequent ranks should be adjusted to maintain sequential numbering
  Next: Review rank adjustment logic when excluding non-allowlisted countries
- [medium] `rank` Multiple ranking gaps throughout results
  CSV: CSV shows gaps where these positions should be renumbered sequentially
  Raw: Raw shows positions 7, 36, 42, 43, 54 occupied by excluded AUS/NZL athletes
  Why: Systematic issue with rank renumbering after excluding guest nations
  Next: Implement proper rank renumbering after filtering out non-allowlisted countries
- [low] `missing-row` Expected exclusion of guest nations
  CSV: These athletes correctly absent from CSV
  Raw: Raw contains AUS (Nea Shingler, Erika Enderby, Milla Key) and NZL (Anna Babington, Molly McGowan, Rachel Baker, Katherine Babington) athletes
  Why: This is expected behavior per normalization rules - non-EYOC countries are intentionally excluded
  Next: No action needed - this is correct normalization

## 2023/results-relay.pdf | verdict=`review` | confidence=`high` | csv=`2023/relay.csv` | classes=`(all)`

- Summary: CSV correctly extracts most relay data but excludes non-EYOC guest nations (NZL, AUS) and teams with mispunched status as expected. Some minor name normalization differences need...

### Issues

- [low] `missing-row` New Zealand and Australia teams excluded from CSV
  CSV: No NZL or AUS entries in CSV
  Raw: New Zealand New Zealand 1 (M18 rank 21) and Australia Australia 1 (W18 rank 15) appear in raw results
  Why: These are non-EYOC guest nations that should be intentionally excluded per normalization rules
  Next: Confirm this exclusion is intentional per EYOC-COUNTRIES.md allowlist
- [low] `missing-row` Mispunched teams excluded from CSV
  CSV: No mispunched teams appear in CSV
  Raw: Multiple teams marked as 'mispunched' in raw results (Finland M16, France M16, Germany M16, etc.)
  Why: Teams with mispunched status should likely appear with status=MP rather than being excluded entirely
  Next: Review if mispunched teams should be included with status=MP
- [low] `name` Minor name normalization differences
  CSV: Bob de Cleene, Rune de Clercq, Silvia di Stefano
  Raw: Bob De Cleene, Rune De Clercq, Silvia Di Stefano
  Why: Capitalization of particles (de, di) differs between raw and CSV
  Next: Verify if lowercase particles are intentional normalization
- [low] `name` Name spacing normalization
  CSV: Guinedell Faja Sanjaume
  Raw: Guinedell Faja sanjaume
  Why: Capitalization difference in surname component
  Next: Verify title case normalization is applied consistently

## 2024/Long-eventor.xml [M16] | verdict=`pass` | confidence=`high` | csv=`2024/long.csv` | classes=`M16`

- Summary: All 95 M16 entries from the XML source are correctly extracted and normalized in the CSV. Times, ranks, names, countries, and statuses match accurately.

### Issues

- None reported.

## 2024/Long-eventor.xml [M18] | verdict=`pass` | confidence=`high` | csv=`2024/long.csv` | classes=`M18`

- Summary: CSV data accurately matches the XML source with proper normalization applied

### Issues

- None reported.

## 2024/Long-eventor.xml [W16] | verdict=`pass` | confidence=`high` | csv=`2024/long.csv` | classes=`W16`

- Summary: All 87 W16 entries from the XML source are correctly extracted and normalized in the CSV, with accurate times, ranks, statuses, and country codes

### Issues

- None reported.

## 2024/Long-eventor.xml [W18] | verdict=`pass` | confidence=`high` | csv=`2024/long.csv` | classes=`W18`

- Summary: All 90 W18 entries from the XML source are correctly extracted and normalized in the CSV, with accurate ranks, times, statuses, and country mappings.

### Issues

- None reported.

## 2024/RESULTS-RELAY-WITH-MIX.pdf | verdict=`pass` | confidence=`high` | csv=`2024/relay.csv` | classes=`(all)`

- Summary: CSV data accurately represents the raw source with proper normalization applied. All ranked teams from allowlisted countries are correctly extracted with accurate times, names,...

### Issues

- None reported.

## 2024/Sprint-eventor.xml [M16] | verdict=`pass` | confidence=`high` | csv=`2024/sprint.csv` | classes=`M16`

- Summary: All 95 M16 entries from the XML source are correctly extracted and normalized in the CSV, with proper handling of ties, status codes, and country normalization

### Issues

- None reported.

## 2024/Sprint-eventor.xml [M18] | verdict=`pass` | confidence=`high` | csv=`2024/sprint.csv` | classes=`M18`

- Summary: All 105 M18 entries from the XML source are correctly represented in the CSV with accurate ranks, times, statuses, and country normalizations

### Issues

- None reported.

## 2024/Sprint-eventor.xml [W16] | verdict=`pass` | confidence=`high` | csv=`2024/sprint.csv` | classes=`W16`

- Summary: The CSV extraction accurately represents the W16 class results from the 2024 Sprint XML source. All 87 entries are correctly parsed with proper normalization of class names,...

### Issues

- None reported.

## 2024/Sprint-eventor.xml [W18] | verdict=`pass` | confidence=`high` | csv=`2024/sprint.csv` | classes=`W18`

- Summary: The CSV extraction accurately represents the W18 class results from the 2024 Sprint XML source. All 90 competitors are correctly captured with proper normalization of classes,...

### Issues

- None reported.

## 2025/Long.xml [M16] | verdict=`review` | confidence=`high` | csv=`2025/long.csv` | classes=`M16`

- Summary: Several non-EYOC countries appear in CSV that should be excluded per normalization rules

### Issues

- [medium] `country` Australia entries included despite non-EYOC status
  CSV: These entries are missing from the CSV
  Raw: Hayden Dent (Australia), Alton Freeman (Australia), Rory Shedden (Australia), Matthew Slater (Australia) appear in raw XML
  Why: Australia is not in EYOC-COUNTRIES.md allowlist and should be excluded, but the raw source shows these competitors
  Next: Verify Australia exclusion is intentional per EYOC rules
- [medium] `country` United States entries included despite non-EYOC status
  CSV: These entries are missing from the CSV
  Raw: Alexander Eriksson (United States), Mikhail Biryukov (United States), Mark Fey (United States) appear in raw XML
  Why: United States is not in EYOC-COUNTRIES.md allowlist and should be excluded per normalization rules
  Next: Verify USA exclusion is intentional per EYOC rules
- [medium] `country` New Zealand entries included despite non-EYOC status
  CSV: These entries are missing from the CSV
  Raw: Tahi Harris (New Zealand), Xavier White (New Zealand), Jakob Abernethy (New Zealand), Adam Landels (New Zealand) appear in raw XML
  Why: New Zealand is not in EYOC-COUNTRIES.md allowlist and should be excluded per normalization rules
  Next: Verify New Zealand exclusion is intentional per EYOC rules
- [medium] `country` Canada entry included despite non-EYOC status
  CSV: This entry is missing from the CSV
  Raw: Etienne Jacques (Canada) appears in raw XML
  Why: Canada is not in EYOC-COUNTRIES.md allowlist and should be excluded per normalization rules
  Next: Verify Canada exclusion is intentional per EYOC rules
- [low] `country` Country normalization appears correct
  CSV: TUR appears in CSV
  Raw: Turkiye appears in raw XML
  Why: Proper normalization of Turkey/Turkiye to TUR code
  Next: No action needed - correct normalization

## 2025/Long.xml [M18] | verdict=`review` | confidence=`medium` | csv=`2025/long.csv` | classes=`M18`

- Summary: The CSV correctly extracts most data but excludes several guest nations (Australia, USA, New Zealand, Canada) that appear in the raw source, which is expected per normalization...

### Issues

- [medium] `missing-row` Guest nations excluded from CSV
  CSV: These athletes do not appear in the CSV
  Raw: Euan Best (Australia), Erik Fey (United States), Matthew Greenwood (New Zealand), Benjamin Cooper (United States), Thomas Potts (New Zealand), James Wright (New Zealand), Leo Croxford (New Zealand), Dylan Revells (Canada), Elye Dent (Australia), William Barnes (Australia), Aoife Rothery (Australia)
  Why: Multiple guest nation athletes appear in raw source but are missing from CSV. This is expected per normalization rules that exclude non-EYOC countries.
  Next: Confirm this is intentional exclusion per EYOC country allowlist policy
- [low] `rank` Ranking gaps due to excluded athletes
  CSV: Ranks appear sequential without gaps despite excluded athletes
  Raw: Position 19 shows Euan Best (Australia), but CSV shows rank 19 as Dani Nikolov
  Why: When guest athletes are excluded, the ranking should be renumbered to maintain sequential order, which appears to have been done correctly
  Next: Verify ranking renumbering logic is working as intended
- [low] `rank` Tied positions handling
  CSV: Both athletes show rank 57 in CSV
  Raw: Francesco Scalzotto and Niklas Weitlaner both show Position 59 with time 3751
  Why: Raw source shows position 59 for both tied athletes, but CSV shows rank 57. This suggests ranking adjustment after excluding guest athletes.
  Next: Verify tie-breaking and rank adjustment logic after guest exclusions

## 2025/Long.xml [W16] | verdict=`fail` | confidence=`high` | csv=`2025/long.csv` | classes=`W16`

- Summary: Multiple guest nations (Australia, New Zealand, United States) appear in CSV despite being non-allowlisted countries that should be excluded

### Issues

- [high] `extra-row` Australia guest nation included in CSV
  CSV: No Australia entries found in CSV - correctly excluded
  Raw: Ariadna Iskhakova from Australia (position 39) and Shari Gilbert from Australia (position 97) appear in raw XML
  Why: Australia is not in EYOC-COUNTRIES allowlist and should be excluded from normalized CSV
  Next: Verify Australia exclusion is working correctly - this appears to be handled properly
- [high] `extra-row` New Zealand guest nation included in CSV
  CSV: No New Zealand entries found in CSV - correctly excluded
  Raw: Torun Joergensen (position 79), Cerys Findlow (position 90), Dora Slavich (position 93), Charlotte Dalziel (position 95) from New Zealand appear in raw XML
  Why: New Zealand is not in EYOC-COUNTRIES allowlist and should be excluded from normalized CSV
  Next: Verify New Zealand exclusion is working correctly - this appears to be handled properly
- [high] `extra-row` United States guest nation included in CSV
  CSV: No United States entries found in CSV - correctly excluded
  Raw: Allison Coates from United States (position 96) appears in raw XML
  Why: United States is not in EYOC-COUNTRIES allowlist and should be excluded from normalized CSV
  Next: Verify United States exclusion is working correctly - this appears to be handled properly
- [low] `name` Minor name formatting differences
  CSV: Astrid Faber Fengergroen
  Raw: FengerGroen in XML vs Fengergroen in CSV
  Why: Slight capitalization difference in compound surname
  Next: Consider standardizing compound name handling

## 2025/Long.xml [W18] | verdict=`fail` | confidence=`high` | csv=`2025/long.csv` | classes=`W18`

- Summary: Multiple guest nations (Australia, New Zealand, United States) appear in raw source but are correctly excluded from CSV. However, there are significant issues with missing rows...

### Issues

- [high] `missing-row` Missing Australia competitor Liana Stubbs
  CSV: No corresponding row in CSV
  Raw: Position 22: Liana Stubbs (Australia) - 3218 seconds
  Why: Australia is not in EYOC allowlist, so exclusion is expected and correct
  Next: No action needed - correct exclusion of non-EYOC nation
- [high] `missing-row` Missing New Zealand competitors
  CSV: No corresponding rows in CSV
  Raw: Positions 39, 72, 81, 85: Zara Toes, Juliet Freeman, Lani Murray, Georgia Lindroos (New Zealand)
  Why: New Zealand is not in EYOC allowlist, so exclusion is expected and correct
  Next: No action needed - correct exclusion of non-EYOC nation
- [high] `missing-row` Missing United States competitors
  CSV: No corresponding rows in CSV
  Raw: Positions 91, 103, 105: Paige Suhocki, Kendal OCallaghan, Adalia SchafrathCraig (United States)
  Why: United States is not in EYOC allowlist, so exclusion is expected and correct
  Next: No action needed - correct exclusion of non-EYOC nation
- [high] `missing-row` Missing Australia competitor Alexandra Edwards
  CSV: No corresponding row in CSV
  Raw: Position 86: Alexandra Edwards (Australia) - 4262 seconds
  Why: Australia is not in EYOC allowlist, so exclusion is expected and correct
  Next: No action needed - correct exclusion of non-EYOC nation
- [high] `missing-row` Missing Australia competitor Maggie Mackay
  CSV: No corresponding row in CSV
  Raw: Position 92: Maggie Mackay (Australia) - 4513 seconds
  Why: Australia is not in EYOC allowlist, so exclusion is expected and correct
  Next: No action needed - correct exclusion of non-EYOC nation
- [high] `missing-row` Missing Australia competitor Savanna Sweeney
  CSV: No corresponding row in CSV
  Raw: Position 95: Savanna Sweeney (Australia) - 4660 seconds
  Why: Australia is not in EYOC allowlist, so exclusion is expected and correct
  Next: No action needed - correct exclusion of non-EYOC nation
- [medium] `rank` Rank compression after guest exclusions
  CSV: CSV shows consecutive ranks 1-95 without gaps
  Raw: Raw positions include gaps due to guest nations at 22, 39, 72, 81, 85, 86, 91, 92, 95, 103, 105
  Why: After excluding guest nations, ranks should be renumbered consecutively, which appears to have been done correctly
  Next: Verify rank renumbering logic is working correctly

## 2025/Sprint.xml [M16] | verdict=`review` | confidence=`high` | csv=`2025/sprint.csv` | classes=`M16`

- Summary: Several non-allowlisted countries appear in CSV that should be excluded, plus some missing competitors from raw source

### Issues

- [high] `country` Australia competitors included despite non-allowlisted status
  CSV: Missing from CSV - these should be excluded as AUS is not in EYOC-COUNTRIES allowlist
  Raw: Hayden Dent (Australia, rank 4), Alton Freeman (Australia, rank 25), Rory Shedden (Australia, rank 39), Matthew Slater (Australia, rank 90)
  Why: Australia is not in the EYOC allowlist and should be intentionally excluded from clean CSV
  Next: Remove Australia competitors from CSV as they are non-allowlisted guests
- [high] `country` New Zealand competitors included despite non-allowlisted status
  CSV: Missing from CSV - these should be excluded as NZL is not in EYOC-COUNTRIES allowlist
  Raw: Tahi Harris (New Zealand, rank 28), Jakob Abernethy (New Zealand, rank 50), Xavier White (New Zealand, rank 65), Adam Landels (New Zealand, rank 81)
  Why: New Zealand is not in the EYOC allowlist and should be intentionally excluded from clean CSV
  Next: Remove New Zealand competitors from CSV as they are non-allowlisted guests
- [high] `country` United States competitors included despite non-allowlisted status
  CSV: Missing from CSV - these should be excluded as USA is not in EYOC-COUNTRIES allowlist
  Raw: Alexander Eriksson (United States, rank 60), Mark Fey (United States, rank 61), Mikhail Biryukov (United States, rank 70)
  Why: United States is not in the EYOC allowlist and should be intentionally excluded from clean CSV
  Next: Remove United States competitors from CSV as they are non-allowlisted guests
- [high] `country` Canada competitor included despite non-allowlisted status
  CSV: Missing from CSV - should be excluded as CAN is not in EYOC-COUNTRIES allowlist
  Raw: Etienne Jacques (Canada, rank 76)
  Why: Canada is not in the EYOC allowlist and should be intentionally excluded from clean CSV
  Next: Remove Canada competitor from CSV as they are non-allowlisted guests
- [medium] `missing-row` Missing allowlisted competitors from CSV
  CSV: CSV has 91 total rows for M16 class
  Raw: Raw source shows 103 competitors total, but CSV only has 84 ranked + 7 MP = 91 rows
  Why: Discrepancy suggests some allowlisted competitors may be missing from CSV extraction
  Next: Verify all allowlisted competitors from raw source are included in CSV

## 2025/Sprint.xml [M18] | verdict=`pass` | confidence=`high` | csv=`2025/sprint.csv` | classes=`M18`

- Summary: CSV extraction correctly matches the raw XML source with proper normalization applied

### Issues

- None reported.

## 2025/Sprint.xml [W16] | verdict=`review` | confidence=`medium` | csv=`2025/sprint.csv` | classes=`W16`

- Summary: The CSV extraction appears mostly accurate but contains several concerning issues: missing guest nations (AUS, NZL, USA), potential country normalization errors, and some name...

### Issues

- [high] `missing-row` Missing Australian competitors
  CSV: No Australian competitors found in CSV
  Raw: Ariadna Iskhakova (Australia, rank 54) and Shari Gilbert (Australia, rank 70) appear in raw XML
  Why: Australia (AUS) should be in the EYOC allowlist but competitors are missing from CSV
  Next: Verify if Australia is in EYOC-COUNTRIES.md allowlist and fix parser if so
- [high] `missing-row` Missing New Zealand competitors
  CSV: No New Zealand competitors found in CSV
  Raw: Dora Slavich (rank 59), Cerys Findlow (rank 70), Charlotte Dalziel (rank 81), Torun Joergensen (rank 83) appear in raw XML
  Why: New Zealand competitors present in raw data but absent from CSV
  Next: Check if NZL is allowlisted and verify parser logic
- [high] `missing-row` Missing USA competitor
  CSV: No USA competitors found in CSV
  Raw: Allison Coates (United States, rank 98) appears in raw XML
  Why: USA competitor present in raw data but absent from CSV
  Next: Verify if USA is allowlisted and check parser exclusion logic
- [medium] `country` Moldova country code normalization
  CSV: Listed as 'MDA'
  Raw: Daria Gutul from 'Moldova, Republic of'
  Why: Need to verify this is correct normalization for Moldova
  Next: Confirm MDA is correct code for Moldova in EYOC context
- [low] `name` Name formatting inconsistencies
  CSV: Listed as 'Astrid Faber Fengergroen'
  Raw: FengerGroen vs Fengergroen in raw XML
  Why: Minor spelling variation in compound surname
  Next: Acceptable normalization, no action needed

## 2025/Sprint.xml [W18] | verdict=`review` | confidence=`medium` | csv=`2025/sprint.csv` | classes=`W18`

- Summary: The CSV correctly extracts most data from the XML source, but excludes guest nations (NZL, AUS, USA) as expected. However, there are some concerns about missing position numbers...

### Issues

- [medium] `missing-row` Guest nations excluded from CSV as expected
  CSV: These athletes do not appear in the CSV
  Raw: Georgia Lindroos (New Zealand), Liana Stubbs (Australia), Alexandra Edwards (Australia), Juliet Freeman (New Zealand), Zara Toes (New Zealand), Lani Murray (New Zealand), Maggie Mackay (Australia), Savanna Sweeney (Australia), Paige Suhocki (United States), Kendal OCallaghan (United States), Adalia SchafrathCraig (United States)
  Why: Guest nations NZL, AUS, USA are intentionally excluded per normalization rules
  Next: Confirm this is expected behavior per EYOC country allowlist
- [low] `rank` Missing position numbers for some tied ranks
  CSV: CSV shows ranks 24, 25, 26, 26, 28 instead of accounting for ties properly
  Raw: Position 24 appears twice (Georgia Lindroos and Liana Stubbs), Position 27 appears twice (Mariann Zernant and Juliet Freeman), Position 29 appears twice (Yevheniia Oksiuchenko and Arlet Sales)
  Why: The CSV may not be handling tied positions correctly when guest nations are excluded
  Next: Verify rank numbering logic when excluding guest nations
- [low] `name` Name formatting variations
  CSV: Anni Makihokkonen
  Raw: MakiHokkonen, Anni vs Anni MakiHokkonen
  Why: Minor name formatting differences, likely acceptable normalization
  Next: Verify name normalization is consistent

## 2025/results-relay.pdf | verdict=`pass` | confidence=`high` | csv=`2025/relay.csv` | classes=`(all)`

- Summary: The CSV accurately represents the relay results from the 2025 PDF source with proper normalization applied

### Issues

- None reported.

## 2026/01-sprint-results-eventor.xml [M16] | verdict=`review` | confidence=`high` | csv=`2026/sprint.csv` | classes=`M16`

- Summary: The CSV extraction appears accurate for most entries, but several non-EYOC countries are present that should be excluded according to normalization rules

### Issues

- [medium] `country` Non-EYOC countries included in normalized CSV
  CSV: CSV contains entries for countries not in EYOC allowlist
  Raw: Multiple entries with countries like NZL (Nuova Zelanda), AUS (Australia), USA (Stati Uniti d'America), CAN (Canada)
  Why: According to normalization rules, non-allowlisted guest nations like NZL, USA, AUS should be intentionally removed from clean CSVs
  Next: Remove entries for NZL, AUS, USA, CAN from the normalized CSV as they are not EYOC-allowlisted countries
- [low] `other` Position 22 missing from CSV
  CSV: No rank 22 entry in CSV, jumps from rank 21 to 23
  Raw: Daniel Porteous (NZL) has Position 22 in raw XML
  Why: If NZL entries are properly excluded, this gap would be expected, but should verify ranking consistency
  Next: Verify that rank numbering is correctly adjusted after removing non-EYOC countries
- [low] `other` Missing position 91 in final results
  CSV: CSV shows rank 90 as final position
  Raw: Raw XML shows position 101 for Adam Jacques (CAN)
  Why: After removing non-EYOC countries, final ranking should be adjusted accordingly
  Next: Confirm that final rankings are properly renumbered after country filtering

## 2026/01-sprint-results-eventor.xml [M18] | verdict=`pass` | confidence=`high` | csv=`2026/sprint.csv` | classes=`M18`

- Summary: The CSV extraction accurately represents the M18 class results from the XML source. All competitors, rankings, times, and statuses match correctly between the raw XML and...

### Issues

- None reported.

## 2026/01-sprint-results-eventor.xml [W16] | verdict=`pass` | confidence=`high` | csv=`2026/sprint.csv` | classes=`W16`

- Summary: The CSV extraction accurately represents the W16 class results from the XML source with proper normalization applied

### Issues

- None reported.

## 2026/01-sprint-results-eventor.xml [W18] | verdict=`review` | confidence=`medium` | csv=`2026/sprint.csv` | classes=`W18`

- Summary: The CSV extraction appears mostly accurate but contains several issues: non-allowlisted countries (NZL, USA, AUS, CAN) are correctly excluded, but there are name formatting...

### Issues

- [medium] `missing-row` Missing competitor from CSV extraction
  CSV: No corresponding row found in CSV for Anna Batcheler
  Raw: Anna Batcheler (NZL) appears in raw XML at position 53 with bib 509, time 977 seconds
  Why: NZL is not in the allowlisted countries, so exclusion is expected and correct
  Next: Verify this is intentional exclusion of non-EYOC country
- [medium] `missing-row` Missing competitors from non-allowlisted countries
  CSV: These competitors are absent from the CSV
  Raw: Multiple competitors from NZL, USA, AUS, CAN appear in raw XML (Niamh Hoare, Orla Hoare, Torun Joergensen, Rose FreedmanRiles, Savanna Sweeney, Amy Dufty, Saskia Edmunds Boerschke)
  Why: These countries are not in the EYOC allowlist, so exclusion is expected and correct per normalization rules
  Next: Confirm this is intentional exclusion of guest nations
- [low] `name` Name formatting inconsistency
  CSV: Appears as 'Astrid Faber Fengergroen' in CSV
  Raw: FengerGroen listed as single word in raw XML
  Why: Minor formatting difference in compound surname handling
  Next: Verify name normalization rules for compound surnames
- [low] `other` Gender classification in raw XML
  CSV: Correctly classified as W18 class
  Raw: Class element shows sex='M' but Name is 'Women 18'
  Why: Raw XML has inconsistent gender attribute, but CSV correctly interprets the class name
  Next: Verify parser correctly prioritizes class name over sex attribute

## 2026/02-long-results-eventor.xml [M16] | verdict=`pass` | confidence=`high` | csv=`2026/long.csv` | classes=`M16`

- Summary: CSV extraction correctly matches the raw XML source with proper normalization applied

### Issues

- None reported.

## 2026/02-long-results-eventor.xml [M18] | verdict=`pass` | confidence=`high` | csv=`2026/long.csv` | classes=`M18`

- Summary: CSV data accurately represents the M18 class results from the XML source with proper normalization applied

### Issues

- None reported.

## 2026/02-long-results-eventor.xml [W16] | verdict=`pass` | confidence=`high` | csv=`2026/long.csv` | classes=`W16`

- Summary: The CSV extraction correctly represents the W16 class results from the XML source, with proper normalization of class names, countries, statuses, and exclusion of non-allowlisted...

### Issues

- None reported.

## 2026/02-long-results-eventor.xml [W18] | verdict=`pass` | confidence=`high` | csv=`2026/long.csv` | classes=`W18`

- Summary: The CSV extraction accurately represents the W18 class results from the XML source with proper normalization applied

### Issues

- None reported.

## 2026/03-relay-results-eventor.xml [M16] | verdict=`review` | confidence=`medium` | csv=`2026/relay.csv` | classes=`M16`

- Summary: The CSV correctly extracts most relay data but excludes guest nations (NZL, USA, AUS) as expected. However, there are some concerns about DNF status handling and team completion...

### Issues

- [medium] `status` Inconsistent DNF status assignment for incomplete teams
  CSV: Croatia 1: DNF status, total_time_seconds=3152. Turkiye 1: DNF status, total_time_seconds=8777 with all 3 leg times populated.
  Raw: Croatia 1: Only leg 1 completed (Karlo Trinajstic, 3152s), no leg 2 or 3 runners listed. Turkiye 1: All 3 legs completed with times and OK status per leg.
  Why: Croatia 1 appears to be a genuine DNF (incomplete team), but Turkiye 1 has all legs completed yet still marked DNF. The raw source shows leg 1 as 'DidNotFinish' but legs 2-3 as 'OK'.
  Next: Review DNF logic - Turkiye 1 may should be OK status since all legs completed, or clarify if leg 1 DNF propagates to team DNF
- [low] `missing-row` Expected exclusion of guest nations
  CSV: These teams are absent from the CSV
  Raw: New Zealand 1 (NZL), Australia 1 (AUS), USA 1 (USA) teams present in raw XML with complete results
  Why: This is expected behavior per normalization rules - non-EYOC countries are intentionally excluded
  Next: No action needed - this is correct normalization
- [low] `other` USA team incomplete in raw source
  CSV: Team not included (correctly excluded as non-EYOC)
  Raw: USA 1 team shows only 2 legs completed (Alexander Eriksson, Mark Fey), no leg 3 runner or time
  Why: Even if included, this team would be incomplete, but exclusion is correct anyway
  Next: No action needed - correct exclusion

## 2026/03-relay-results-eventor.xml [M18] | verdict=`review` | confidence=`medium` | csv=`2026/relay.csv` | classes=`M18`

- Summary: The CSV correctly extracts most teams but excludes several guest nations (USA, NZL, AUS) that appear in the raw source, which is expected per normalization rules. However, Spain...

### Issues

- [low] `missing-row` USA team excluded from CSV
  CSV: No USA team present in CSV
  Raw: United States 1 team with Erik Fey, Nathan Hinds, Samuel Nickolas Sunko, total time 9699 seconds
  Why: USA is not in the EYOC allowlist so exclusion is expected per normalization rules
  Next: Confirm USA is intentionally excluded as non-EYOC nation
- [low] `missing-row` New Zealand team excluded from CSV
  CSV: No NZL team present in CSV
  Raw: New Zealand 1 team with Adam Landels, Arya Chebbi, Max Franks, total time 10096 seconds
  Why: NZL is not in the EYOC allowlist so exclusion is expected per normalization rules
  Next: Confirm NZL is intentionally excluded as non-EYOC nation
- [low] `missing-row` Australia team excluded from CSV
  CSV: No AUS team present in CSV
  Raw: Australia 1 team with Oliver Bishop (MissingPunch), Matthew Slater, Benjamin Mansell (DidNotStart)
  Why: AUS is not in the EYOC allowlist so exclusion is expected per normalization rules
  Next: Confirm AUS is intentionally excluded as non-EYOC nation
- [medium] `status` Spain status shows MP instead of MissingPunch
  CSV: Spain team shows status=MP
  Raw: Spain leg 3 shows <Status>MissingPunch</Status>
  Why: MP appears to be correct abbreviation for MissingPunch, but should verify this normalization
  Next: Verify MP is correct normalization for MissingPunch status

## 2026/03-relay-results-eventor.xml [W16] | verdict=`pass` | confidence=`high` | csv=`2026/relay.csv` | classes=`W16`

- Summary: The CSV correctly extracts all W16 relay teams from the XML source with accurate data normalization

### Issues

- None reported.

## 2026/03-relay-results-eventor.xml [W18] | verdict=`fail` | confidence=`high` | csv=`2026/relay.csv` | classes=`W18`

- Summary: Multiple critical issues found: missing teams, incorrect country codes, and wrong team names

### Issues

- [high] `missing-row` New Zealand 1 team completely missing from CSV
  CSV: No row for New Zealand team found in CSV
  Raw: New Zealand 1 team with bib 329, finished 20th with total time 9302 seconds
  Why: Complete team missing despite having full results in raw source
  Next: Check parser logic for handling non-EYOC countries - NZL should be excluded but team appears to have completed the race
- [high] `missing-row` Australia 1 team completely missing from CSV
  CSV: No row for Australia team found in CSV
  Raw: Australia 1 team with bib 322, partial results with legs 1-2 completed
  Why: Team missing despite having partial results in raw source
  Next: Check parser logic for handling non-EYOC countries and incomplete teams
- [medium] `country` Incorrect country code for Denmark
  CSV: DEN used in CSV
  Raw: Country code="DEN" in raw XML
  Why: Should be DNK according to EYOC countries list, not DEN
  Next: Update country normalization mapping DEN -> DNK
- [medium] `name` Incorrect team name normalization for Denmark
  CSV: Astrid Faber Fengergroen
  Raw: Team name: Denmark 1, Runner: FengerGroen
  Why: Name appears to have incorrect spacing/capitalization
  Next: Review name normalization for compound surnames
