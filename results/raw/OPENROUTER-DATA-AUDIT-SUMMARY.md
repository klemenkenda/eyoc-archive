# OpenRouter Independent Data Audit Summary

Generated: 2026-07-01T11:26:11.865704+00:00
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

## 2002/eyoc2002.htm | verdict=`pass` | confidence=`high` | csv=`2002/long.csv`, `2002/relay.csv`, `2002/sprint.csv` | classes=`(all)`

- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All major data points match correctly despite some expected formatting...

### Issues

- [low] `name` Minor name variations in relay data
  CSV: Sara Luscher in relay, Sara Luescher in individual
  Raw: LUSCHER Sara vs LUESCHER Sara in individual results
  Why: Slight spelling inconsistency between relay and individual sections, but both refer to the same Swiss athlete
  Next: Accept as source-level variation - common in multi-format HTML documents
- [low] `name` Accent handling variations
  CSV: Dorota Kosinska, Adrienn Csiszar without accents
  Raw: KOSIÑSKA Dorota with HTML entity, CSISZÁR Adrienn with accent
  Why: Expected normalization of accents and HTML entities as documented in normalization rules
  Next: No action needed - proper accent normalization applied

## 2003/eyoc2003.htm | verdict=`pass` | confidence=`high` | csv=`2003/long.csv`, `2003/relay.csv`, `2003/sprint.csv` | classes=`(all)`

- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All major data points match correctly.

### Issues

- [low] `name` Minor name normalization differences
  CSV: Jana Krsiakova, Sona Berzinska
  Raw: Kriaková Jana vs Krsiakova Jana, Berinská Soňa vs Berzinska Sona
  Why: Accent removal and transliteration differences are expected normalization artifacts
  Next: No action needed - this is expected normalization behavior
- [low] `country` Country code normalization
  CSV: SRB, BLR, LAT
  Raw: Serbia and Montenegr SCG, Belarusia BLR, Latvija LAT
  Why: Country names properly normalized to standard codes, including handling of truncated 'Serbia and Montenegr'
  Next: No action needed - correct normalization

## 2004/eyoc2004.htm | verdict=`pass` | confidence=`high` | csv=`2004/long.csv`, `2004/relay.csv`, `2004/sprint.csv` | classes=`(all)`

- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All major data points match correctly.

### Issues

- None reported.

## 2005/eyoc2005.htm | verdict=`pass` | confidence=`high` | csv=`2005/long.csv`, `2005/relay.csv`, `2005/sprint.csv` | classes=`(all)`

- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All major results sections (sprint, long, relay) are correctly parsed with...

### Issues

- None reported.

## 2006/2006_relay_m16.txt | verdict=`review` | confidence=`medium` | csv=`2006/relay.csv` | classes=`(all)`

- Summary: Generally accurate extraction with some normalization concerns around country codes, name formatting, and MP status handling

### Issues

- [medium] `country` SCG country code normalization to SRB
  CSV: SRB,Team SCG 69
  Raw: Team SCG 69 with STEVANOVIC, Marko etc.
  Why: Raw shows 'SCG' (Serbia and Montenegro) but CSV shows 'SRB' (Serbia). In 2006, SCG was still the official code before Montenegro independence.
  Next: Verify if SCG->SRB normalization is appropriate for 2006 data or if SCG should be preserved
- [medium] `country` ROM country code normalization to ROU
  CSV: ROU,Team ROM 61
  Raw: Team ROM 61
  Why: Raw shows 'ROM' but CSV shows 'ROU'. Both are valid codes for Romania, but should verify consistency with normalization rules.
  Next: Confirm ROM->ROU normalization is intended and consistent
- [low] `name` Accent handling in Czech names
  CSV: Stipan Zimmermann and Milos Nykodym
  Raw: Zimmermann, Štìpán and Nykodým, Miloš
  Why: Accents removed/simplified in normalization, which is expected but worth noting
  Next: Acceptable normalization artifact
- [low] `name` Name case normalization
  CSV: Tadas Vidzikauskas
  Raw: VIDZIKAUSKAS, TADAS and other all-caps names
  Why: All-caps names properly converted to title case with order flip
  Next: Acceptable normalization
- [medium] `status` MP status interpretation for incomplete teams
  CSV: Both teams have status=MP with some missing leg times
  Raw: Team ESP 21 and Team ITA 43 show MisPunch for individual legs
  Why: Teams with mispunching legs correctly marked as MP, but should verify if partial times should be preserved or blanked
  Next: Verify MP handling policy for teams with partial completion

## 2006/2006_relay_m18.txt | verdict=`review` | confidence=`medium` | csv=`2006/relay.csv` | classes=`(all)`

- Summary: Most data extracted correctly, but several issues need review including name normalization problems, potential time assignment errors, and questionable MP status handling

### Issues

- [medium] `name` Corrupted relay leg 2 name for Slovenia team
  CSV: leg2_name: (Jerica (Ak)) (Bernik)
  Raw: 2	0	(Bernik), (Jerica (AK)) (0)	1:41:58
  Why: The raw source shows a corrupted entry with ID 0 and parenthetical formatting that suggests missing or placeholder data. The CSV normalized this to a name format, but this appears to be corrupted source data rather than a real athlete name.
  Next: Verify if this represents a real athlete or if it should be handled as missing/corrupted data
- [medium] `time` Duplicate time value for Slovenia leg 2
  CSV: Slovenia leg2_time_seconds: 6118, Ireland leg2_time_seconds: 6118
  Raw: Slovenia leg 2: 1:41:58, Ireland leg 2: 1:41:58
  Why: Both Slovenia and Ireland teams show identical leg 2 times of 1:41:58 (6118 seconds). Given Slovenia's corrupted leg 2 data, this may indicate the Slovenia time was incorrectly copied or the source has data corruption.
  Next: Verify if this time duplication is legitimate or indicates source corruption
- [low] `name` Accent removal in multiple names
  CSV: Names normalized without accents
  Raw: Matìj -> Matij, Máté -> Mate, Bjørseth -> Bjorseth, Hägler -> Hagler, Jasiñski -> Jasinski, Tammemäe -> Tammemae, Röhnert -> Rohnert, Oľhava -> Olhava
  Why: Multiple names had accents removed during normalization, which is expected behavior but worth noting for completeness
  Next: No action needed - this is expected normalization
- [low] `country` ROM vs ROU country code normalization
  CSV: country: ROU
  Raw: Team ROM 62
  Why: Raw source shows 'ROM' but CSV shows 'ROU'. This appears to be correct normalization to current IOC standard, but worth confirming the mapping is intentional.
  Next: Confirm ROM->ROU mapping is correct for 2006 data

## 2006/2006_relay_w16.txt | verdict=`review` | confidence=`medium` | csv=`2006/relay.csv` | classes=`(all)`

- Summary: Data extraction is mostly accurate with proper time conversions and name normalization, but there are two country code issues that need review: SCG->SRB conversion and a...

### Issues

- [medium] `country` SCG country code converted to SRB without clear justification
  CSV: country=SRB for Team SCG 71
  Raw: Team SCG 71 - Radulovic, Cosic, Karic (Serbian names)
  Why: SCG (Serbia and Montenegro) was converted to SRB, but this needs verification as SCG was a valid country code in 2006 before Montenegro's independence
  Next: Verify if SCG->SRB conversion is appropriate for 2006 data or if SCG should be preserved
- [low] `time` Minor time discrepancy in POR team total vs leg sum
  CSV: total_time_seconds=7324 (2:02:04), leg times sum to 7323 (2:02:03)
  Raw: Place 15: 2:02:04 total, but leg 2 shows 2:02:03
  Why: 1-second difference between stated total time and sum of leg times, likely due to rounding or timing precision in source
  Next: Accept as minor timing precision issue from source data

## 2006/2006_relay_w18.txt | verdict=`review` | confidence=`medium` | csv=`2006/relay.csv` | classes=`(all)`

- Summary: Most data extracted correctly, but several issues need review: country code normalization (ROM->ROU, SCG->SRB), missing total times for MP teams, and some name accent handling...

### Issues

- [low] `country` Country code normalization ROM to ROU
  CSV: ROU,Team ROM 64
  Raw: Team ROM 64
  Why: Raw shows ROM but CSV shows ROU - need to verify if this normalization is correct for Romania
  Next: Verify ROM->ROU normalization is intended for Romania
- [low] `country` Country code normalization SCG to SRB
  CSV: SRB,Team SCG 72
  Raw: Team SCG 72
  Why: Raw shows SCG but CSV shows SRB - SCG was Serbia and Montenegro, need to verify this normalization
  Next: Verify SCG->SRB normalization is appropriate for 2006 timeframe
- [medium] `time` Missing total times for MP status teams
  CSV: total_time_seconds field is empty for MP teams
  Raw: Teams GBR, SCG, POR show individual leg times but have MP/DSQ status
  Why: MP teams should probably still show total time if calculable from leg times, or have consistent handling
  Next: Review whether MP teams should have total times calculated or consistently blank
- [low] `name` Accent handling inconsistencies
  CSV: Names show accent removal but inconsistent patterns
  Raw: Bjørgul vs Bjorgul, Péley vs Peley, Koós vs Koos
  Why: Some accents removed (ø->o, é->e, ó->o) while others preserved - should be consistent
  Next: Document accent handling policy or ensure consistent normalization
- [low] `time` Missing leg2 time for GBR team
  CSV: leg2_time_seconds is empty
  Raw: Taylor, Catherine (2112214) MisPunch
  Why: Raw shows MisPunch for leg 2, CSV correctly leaves time blank
  Next: Confirm this is correct handling for mispunch legs

## 2006/eyoc2006.htm | verdict=`pass` | confidence=`high` | csv=`2006/long.csv`, `2006/sprint.csv` | classes=`(all)`

- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All times, names, countries, and rankings match the source data.

### Issues

- None reported.

## 2007/eyoc2007.htm | verdict=`pass` | confidence=`high` | csv=`2007/long.csv`, `2007/relay.csv`, `2007/sprint.csv` | classes=`(all)`

- Summary: The extracted CSV data accurately represents the 2007 EYOC results from the raw HTML source. All individual and relay results are correctly parsed with proper time conversions,...

### Issues

- None reported.

## 2008/eyoc2008.htm | verdict=`pass` | confidence=`high` | csv=`2008/long.csv`, `2008/relay.csv`, `2008/sprint.csv` | classes=`(all)`

- Summary: The extracted CSV data accurately represents the raw source with proper normalization applied. All major data points match correctly.

### Issues

- [low] `name` Minor name variations in sprint results
  CSV: Klingenberg (missing first name), Rafols (missing first name)
  Raw: Klingenberg, Ita (W16 sprint rank 30), Pol Rafols (M18 sprint rank 55)
  Why: Some names appear abbreviated in sprint results, likely due to space constraints in original formatting
  Next: Accept as-is since source appears to have abbreviated names in these instances
- [low] `name` Accent normalization variations
  CSV: Hellmuller, Losch, Rohnert (accents removed)
  Raw: Hellmüller, Mirjam; Lösch, Susen; Röhnert, Karoline
  Why: Standard accent removal normalization applied consistently
  Next: No action needed - this is expected normalization

## 2009/eyoc2009.htm | verdict=`pass` | confidence=`high` | csv=`2009/long.csv`, `2009/relay.csv`, `2009/sprint.csv` | classes=`(all)`

- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All major results sections (sprint, long, relay) are correctly parsed with...

### Issues

- None reported.

## 2010/eyoc2010.htm | verdict=`pass` | confidence=`high` | csv=`2010/long.csv`, `2010/relay.csv`, `2010/sprint.csv` | classes=`(all)`

- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All major results sections (sprint, long, relay) are correctly parsed with...

### Issues

- None reported.

## 2011/eyoc2011.htm | verdict=`pass` | confidence=`high` | csv=`2011/long.csv`, `2011/relay.csv`, `2011/sprint.csv` | classes=`(all)`

- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All major results sections (sprint, long, relay) are correctly parsed with...

### Issues

- None reported.

## 2012/eyoc2012.htm | verdict=`pass` | confidence=`high` | csv=`2012/long.csv`, `2012/relay.csv`, `2012/sprint.csv` | classes=`(all)`

- Summary: The extracted CSV data accurately represents the 2012 EYOC results from the raw HTML source. All major data points including names, countries, times, and rankings are correctly...

### Issues

- None reported.

## 2013/eyoc2013.htm | verdict=`pass` | confidence=`high` | csv=`2013/long.csv`, `2013/relay.csv`, `2013/sprint.csv` | classes=`(all)`

- Summary: The extracted CSV data accurately represents the raw HTML source with proper normalization applied. All major results sections (sprint, long, relay) are correctly parsed with...

### Issues

- [low] `name` Inconsistent handling of 'The Netherlands' suffix
  CSV: Nina Roothans 96 The
  Raw: Nina Roothans 96 THE NETHERLANDS
  Why: The country normalization appears to have truncated part of the name when processing 'THE NETHERLANDS'
  Next: Review country extraction logic to avoid contaminating name fields with country suffixes
- [low] `name` Special character handling in Lithuanian name
  CSV: Jogvil? Susinskait?
  Raw: Jogvil? Susinskait? 96 LITHUANIA
  Why: Question marks appear to be replacement characters for accented letters, but this matches the source corruption
  Next: No action needed - source already contains replacement characters
- [low] `country` Macedonia country code normalization
  CSV: MKD
  Raw: Milovoj Velinovikj MECEDONIA
  Why: Correctly normalized misspelled 'MECEDONIA' to MKD, but worth noting the source typo
  Next: No action needed - correct normalization applied

## 2014/results-long.pdf | verdict=`review` | confidence=`low` | csv=`2014/long.csv` | classes=`(all)`

- Summary: Cannot verify extraction accuracy due to missing raw source text from PDF file

### Issues

- [high] `source-limitation` PDF source text unavailable for verification
  CSV: 404 rows extracted with high confidence from 2014/results-long.pdf
  Raw: [no raw text extracted]
  Why: The PDF file could not be rendered as text, making it impossible to verify the accuracy of the extracted data against the source
  Next: Manual verification of PDF content against CSV extraction required

## 2014/results-relay.pdf | verdict=`review` | confidence=`low` | csv=`2014/relay.csv` | classes=`(all)`

- Summary: Cannot perform meaningful audit due to missing raw source text from PDF. CSV data appears structurally sound but requires manual verification against original PDF.

### Issues

- [high] `source-limitation` Raw PDF text extraction failed
  CSV: 84 relay rows extracted with confidence=approx
  Raw: [no raw text extracted]
  Why: Cannot verify accuracy of extracted data without access to source content
  Next: Manual verification against original PDF required
- [medium] `rank` Inconsistent ranking sequences
  CSV: M16 class shows rank 6 twice (DEN and AUT), rank 8 for GER before rank 6 AUT
  Raw: N/A - no raw text
  Why: Ranking sequence appears corrupted or source may have ties/corrections
  Next: Verify ranking sequence against original PDF
- [medium] `time` Missing leg times in multiple entries
  CSV: Multiple entries missing leg2_time_seconds (e.g., TUR W16, EST M16, CRO W18, SLO M18)
  Raw: N/A - no raw text
  Why: Systematic missing times could indicate parsing issues or source data gaps
  Next: Check if source PDF has blank/missing times in these positions
- [low] `country` Potential country formatting inconsistency
  CSV: M18 MDA shows 'Moldova Moldova' as team name
  Raw: N/A - no raw text
  Why: Team name appears to duplicate country name, may indicate parsing artifact
  Next: Verify team name format in original PDF
- [low] `country` Ireland country code inconsistency
  CSV: W18 and M18 Ireland entries show 'lreland' (lowercase L) instead of 'Ireland'
  Raw: N/A - no raw text
  Why: Appears to be OCR error or typo in country field
  Next: Verify country name spelling in original PDF

## 2014/results-sprint.pdf | verdict=`review` | confidence=`low` | csv=`2014/sprint.csv` | classes=`(all)`

- Summary: Cannot verify extraction accuracy due to missing raw source text from PDF file

### Issues

- [high] `source-limitation` Raw PDF text extraction failed
  CSV: 489 rows extracted across M16, W16, M18, W18 classes
  Raw: [no raw text extracted]
  Why: Unable to audit extraction accuracy without access to source content. PDF may require OCR or specialized parsing.
  Next: Re-attempt PDF text extraction or manual verification of sample rows
- [medium] `other` High confidence claimed despite PDF extraction issues
  CSV: All rows marked confidence=high
  Raw: PDF text unavailable
  Why: If PDF required OCR or complex parsing, confidence should likely be 'approx' rather than 'high'
  Next: Verify confidence levels are appropriate for PDF extraction method used

## 2015/results-lf.pdf | verdict=`review` | confidence=`low` | csv=`2015/long.csv` | classes=`(all)`

- Summary: Cannot verify extraction accuracy due to missing raw source text from PDF file

### Issues

- [high] `source-limitation` Raw PDF source text unavailable for verification
  CSV: 384 individual long-distance results extracted with high confidence
  Raw: [no raw text extracted]
  Why: The PDF file could not be rendered as text, making it impossible to verify the accuracy of the 384 extracted results across M16, M18, W16, and W18 classes
  Next: Manual verification of PDF content against CSV extraction, or attempt alternative PDF text extraction method

## 2015/results-relay.pdf | verdict=`review` | confidence=`low` | csv=`2015/relay.csv` | classes=`(all)`

- Summary: Cannot audit extracted data against raw source due to PDF text extraction failure. The CSV contains 95 relay results across 4 classes with plausible structure, but verification...

### Issues

- [high] `source-limitation` PDF text extraction failed completely
  CSV: 95 relay results extracted with high confidence
  Raw: [no raw text extracted]
  Why: Cannot verify any extracted data against source without readable text from PDF
  Next: Use alternative PDF extraction method or manual verification of sample entries
- [medium] `other` All entries marked as high confidence despite PDF extraction failure
  CSV: All 95 rows have confidence=high
  Raw: No source text available for verification
  Why: High confidence rating seems inconsistent with complete source text extraction failure
  Next: Review confidence assignment logic for PDF parsing failures

## 2015/results-sf.pdf | verdict=`review` | confidence=`low` | csv=`2015/sprint.csv` | classes=`(all)`

- Summary: Cannot verify extraction accuracy due to missing raw source text from PDF file

### Issues

- [high] `source-limitation` PDF source text unavailable for verification
  CSV: 434 rows extracted with high confidence
  Raw: [no raw text extracted]
  Why: The PDF file could not be rendered as text, making it impossible to verify the accuracy of the extracted data against the source
  Next: Manual verification of PDF content against CSV extraction required
- [medium] `other` All extractions marked as high confidence despite PDF limitations
  CSV: All 434 rows have confidence=high
  Raw: PDF rendering failed
  Why: Given that PDF text extraction failed, it's questionable whether high confidence is appropriate for all entries
  Next: Consider marking PDF-sourced data as approx confidence when text extraction fails

## 2016/results-long.pdf | verdict=`review` | confidence=`low` | csv=`2016/long.csv` | classes=`(all)`

- Summary: Cannot perform meaningful audit due to missing raw source text from PDF file

### Issues

- [high] `source-limitation` PDF source text extraction failed
  CSV: 340 rows extracted with high confidence
  Raw: [no raw text extracted]
  Why: The PDF file could not be rendered as text, making it impossible to verify the accuracy of the extracted data against the source
  Next: Manual verification of PDF content against CSV data, or attempt alternative PDF text extraction method

## 2016/results-relay.pdf | verdict=`review` | confidence=`low` | csv=`2016/relay.csv` | classes=`(all)`

- Summary: Cannot audit extracted CSV data against raw source due to PDF text extraction failure. The CSV contains 88 relay rows across 4 classes with consistent formatting, but...

### Issues

- [high] `source-limitation` PDF text extraction failed completely
  CSV: 88 relay rows extracted with high confidence
  Raw: [no raw text extracted]
  Why: Cannot verify any extracted data against source without readable text from PDF
  Next: Use alternative PDF extraction method or manual verification of sample rows
- [medium] `name` Potentially truncated or corrupted names
  CSV: Names like 'Knobloch-Esztergar', 'O'SULLIVAN-HOURIH', 'Vmccavana Eadaoin' appear incomplete
  Raw: N/A - no source text
  Why: Some names appear truncated or contain unusual formatting that suggests extraction issues
  Next: Verify these specific names against original PDF
- [low] `name` Inconsistent name formatting patterns
  CSV: Mix of 'Given Surname' and potentially reversed names like 'Ivanow Tzwetan'
  Raw: N/A - no source text
  Why: Without source verification, cannot confirm if name order normalization was applied correctly
  Next: Spot-check name formatting against original PDF

## 2016/results-sprint.pdf | verdict=`review` | confidence=`low` | csv=`2016/sprint.csv` | classes=`(all)`

- Summary: Cannot verify extraction accuracy due to missing raw PDF text, but CSV shows concerning patterns including malformed names, suspicious bib numbers, and potential OCR artifacts...

### Issues

- [high] `name` Multiple malformed names suggest OCR corruption
  CSV: Names like 'Spektorsfricis', 'Repsysadomas', 'Lorenztimon', 'Dzalbsedijs', 'Upitisuldis', 'Ruoholaakseli', 'Hirsotakar', 'Iinkfvichigor'
  Raw: [no raw text available]
  Why: These appear to be corrupted single-word names missing spaces or proper formatting, suggesting systematic OCR issues
  Next: Verify against original PDF to confirm if these are OCR artifacts or actual name formats
- [medium] `other` Suspicious bib number in M18 class
  CSV: M18 class has bib '3481' for 'Iinkfvichigor' while others are 3-digit
  Raw: [no raw text available]
  Why: Bib number 3481 is inconsistent with the 3-digit pattern used elsewhere, may indicate OCR misread
  Next: Check original PDF for correct bib number
- [medium] `name` Names with apparent formatting issues
  CSV: Names like 'Smulems de', 'Eerolalotta', 'Korvellorely', 'Georgievaniya', 'Myroniukalina', 'Gokculsumeyra'
  Raw: [no raw text available]
  Why: These names appear to have spacing or word-order issues that may indicate OCR problems
  Next: Verify name formatting against original PDF
- [low] `rank` Potential rank sequence issue in W18
  CSV: W18 shows rank 69 followed by rank 71, then rank 69 again, then rank 72
  Raw: [no raw text available]
  Why: Rank sequence shows 69, 71, 69, 72 which may indicate a parsing or source formatting issue
  Next: Check if this reflects tied ranks or is a parsing error
- [low] `source-limitation` All confidence marked as 'approx' for PDF source
  CSV: Every row has confidence=approx
  Raw: [no raw text available]
  Why: Consistent 'approx' confidence suggests OCR-derived data which explains name formatting issues
  Next: Document that this is OCR-derived data with expected quality limitations

## 2017/result-sprint.pdf | verdict=`review` | confidence=`low` | csv=`2017/sprint.csv` | classes=`(all)`

- Summary: Cannot perform meaningful audit due to missing raw source text from PDF file

### Issues

- [high] `source-limitation` Raw PDF source text unavailable for comparison
  CSV: 391 rows extracted across M16, M18, W16, W18 classes
  Raw: [no raw text extracted]
  Why: Without the raw source text, cannot verify accuracy of extracted data, names, times, ranks, or countries
  Next: Re-extract PDF text or obtain alternative source format for proper audit

## 2017/results-long.pdf | verdict=`review` | confidence=`low` | csv=`2017/long.csv` | classes=`(all)`

- Summary: Cannot perform meaningful audit due to missing raw source text from PDF file

### Issues

- [high] `source-limitation` Raw PDF text extraction failed
  CSV: 394 rows extracted with high confidence
  Raw: [no raw text extracted]
  Why: Without the raw source text, cannot verify if extracted data matches the original PDF content
  Next: Re-attempt PDF text extraction or obtain alternative text format of source file

## 2017/results-relay.pdf | verdict=`review` | confidence=`low` | csv=`2017/relay.csv` | classes=`(all)`

- Summary: Cannot audit extracted data against raw source due to PDF text extraction failure. The CSV contains 95 relay entries across 4 classes with reasonable structure, but verification...

### Issues

- [high] `source-limitation` PDF text extraction failed completely
  CSV: 95 relay entries extracted with high confidence
  Raw: [no raw text extracted]
  Why: Cannot verify any extracted data against source without readable text
  Next: Use alternative PDF extraction method or manual verification
- [medium] `other` Suspicious ranking gaps in some classes
  CSV: M18 has rank 20 followed by unranked entries; W16 has rank 18 followed by unranked; W18 has rank 24 followed by unranked
  Raw: Cannot verify from source
  Why: Ranking sequences suggest possible missing entries or extraction issues
  Next: Verify complete extraction of all ranked teams from PDF
- [low] `name` Potential name truncation in some entries
  CSV: Names like 'Florencio Garcia Go', 'Gustav Wiren Gonzal', 'Manuele Ren' appear truncated
  Raw: Cannot verify from source
  Why: Several names end abruptly suggesting possible extraction truncation
  Next: Check PDF for complete names and verify extraction accuracy
- [low] `other` Mixed gender names in M18 Serbia entry
  CSV: M18 Serbia team has 'Olga Stanojevic' and 'Lenka Ciric' (female names) with 'Dusan Markovic'
  Raw: Cannot verify from source
  Why: Male relay class contains apparent female names, suggesting possible data corruption
  Next: Verify this is actually a Mixed relay or check for extraction error

## 2018/results-long.pdf | verdict=`review` | confidence=`low` | csv=`2018/long.csv` | classes=`(all)`

- Summary: Cannot perform meaningful audit due to missing raw source text from PDF file

### Issues

- [high] `source-limitation` Raw PDF text extraction failed
  CSV: 377 rows extracted with high confidence
  Raw: [no raw text extracted]
  Why: Without access to the raw PDF content, cannot verify accuracy of extracted data including names, times, ranks, countries, or classes
  Next: Re-attempt PDF text extraction or obtain alternative source format for verification
- [medium] `other` High confidence rating despite extraction limitations
  CSV: All 377 rows marked confidence=high
  Raw: PDF text unavailable
  Why: All extracted rows show high confidence despite PDF extraction failure, which may indicate overconfident parsing
  Next: Review confidence assignment logic for PDF sources with extraction issues

## 2018/results-relay.pdf | verdict=`review` | confidence=`low` | csv=`2018/relay.csv` | classes=`(all)`

- Summary: Cannot verify data accuracy due to unreadable PDF source, but CSV shows concerning anomalies including corrupted names and suspicious team naming patterns

### Issues

- [high] `name` Corrupted runner names containing event metadata
  CSV: Multiple rows show '2018 Relay Mon 02-Jul-18 Eyoc' as runner name (M16 rank 13 leg3, M18 rank 15 leg3, W16 rank 13 leg3)
  Raw: [no raw text extracted]
  Why: Runner names appear contaminated with event date/title information, suggesting parser confusion between data fields
  Next: Re-examine PDF parsing logic to prevent event metadata from being extracted as runner names
- [medium] `country` Duplicated country names in team field
  CSV: Team names show pattern like 'Czech Republic Czech Republic', 'Finland Finland', 'Russian Federati Russian Feder'
  Raw: [no raw text extracted]
  Why: Team field appears to duplicate country names, possibly indicating parser confusion between country and team columns
  Next: Review team name extraction logic to avoid country name duplication
- [medium] `country` Truncated country names
  CSV: 'Russian Federati Russian Feder' appears truncated compared to expected 'Russian Federation'
  Raw: [no raw text extracted]
  Why: Country names appear cut off mid-word, suggesting field width limitations or parsing boundaries
  Next: Check field extraction boundaries to ensure complete country names
- [low] `source-limitation` Cannot verify data completeness or accuracy
  CSV: 108 relay rows extracted across 4 classes
  Raw: [no raw text extracted]
  Why: PDF source unreadable prevents verification of extracted data against original
  Next: Attempt alternative PDF extraction methods or manual verification of source file

## 2018/results-sprint.pdf | verdict=`review` | confidence=`low` | csv=`2018/sprint.csv` | classes=`(all)`

- Summary: Cannot verify extraction accuracy due to missing raw PDF text, but CSV data appears structurally sound with reasonable patterns

### Issues

- [high] `source-limitation` Raw PDF text unavailable for verification
  CSV: 394 rows extracted with high confidence
  Raw: [no raw text extracted]
  Why: Cannot audit extraction accuracy without access to source content
  Next: Attempt PDF text extraction with different tools or manual verification
- [low] `other` All confidence values marked as 'high' despite PDF extraction issues
  CSV: All 394 rows have confidence=high
  Raw: PDF text extraction failed
  Why: Confidence should potentially be 'approx' if PDF parsing was problematic
  Next: Review confidence assignment logic for PDF sources

## 2019/Long-eventor.xml [M16] | verdict=`pass` | confidence=`high` | csv=`2019/long.csv` | classes=`M16`

- Summary: All 102 M16 competitors from the XML source are correctly extracted with accurate ranks, times, countries, and names. Two DNF entries are properly handled.

### Issues

- None reported.

## 2019/Long-eventor.xml [M18] | verdict=`pass` | confidence=`high` | csv=`2019/long.csv` | classes=`M18`

- Summary: All extracted CSV rows accurately match the raw XML source data with proper normalization applied

### Issues

- None reported.

## 2019/Long-eventor.xml [W16] | verdict=`pass` | confidence=`high` | csv=`2019/long.csv` | classes=`W16`

- Summary: All W16 class data correctly extracted from XML source with accurate times, ranks, and competitor details

### Issues

- None reported.

## 2019/Long-eventor.xml [W18] | verdict=`pass` | confidence=`high` | csv=`2019/long.csv` | classes=`W18`

- Summary: All 99 W18 competitors from the XML source are correctly extracted with accurate ranks, times, countries, and statuses. No material discrepancies found.

### Issues

- None reported.

## 2019/Sprint-eventor.xml [M16] | verdict=`pass` | confidence=`high` | csv=`2019/sprint.csv` | classes=`M16`

- Summary: All 101 M16 competitors from the XML source are correctly extracted with accurate ranks, times, countries, and names. One MP (MisPunch) status is properly handled.

### Issues

- None reported.

## 2019/Sprint-eventor.xml [M18] | verdict=`pass` | confidence=`high` | csv=`2019/sprint.csv` | classes=`M18`

- Summary: All 106 M18 competitors from the XML source are correctly extracted with accurate ranks, times, countries, and statuses

### Issues

- None reported.

## 2019/Sprint-eventor.xml [W16] | verdict=`pass` | confidence=`high` | csv=`2019/sprint.csv` | classes=`W16`

- Summary: All W16 competitors correctly extracted from XML source with accurate times, ranks, and statuses

### Issues

- None reported.

## 2019/Sprint-eventor.xml [W18] | verdict=`pass` | confidence=`high` | csv=`2019/sprint.csv` | classes=`W18`

- Summary: All 98 W18 competitors correctly extracted with accurate ranks, times, countries, and names

### Issues

- None reported.

## 2019/result-relay.pdf | verdict=`review` | confidence=`low` | csv=`2019/relay.csv` | classes=`(all)`

- Summary: Cannot perform meaningful audit due to missing raw source text from PDF file. The extracted CSV data appears structurally sound with 78 relay teams across 4 classes, but...

### Issues

- [high] `source-limitation` Raw PDF text extraction failed
  CSV: 78 relay rows extracted with high confidence
  Raw: [no raw text extracted]
  Why: Cannot verify any extracted data against source without readable raw text
  Next: Re-extract PDF text or obtain alternative source format for verification
- [medium] `country` Moldova country format inconsistency
  CSV: M18 rank 25: country='Moldova, Republic of'
  Raw: Cannot verify from source
  Why: Country should be normalized to 'MDA' per normalization rules, not left as full formal name
  Next: Normalize Moldova country code to 'MDA'
- [low] `other` Tied rank handling
  CSV: M18 has two teams at rank 14 (BEL and EST), then continues to rank 16
  Raw: Cannot verify from source
  Why: Need to verify if this tie and rank sequence matches the source document
  Next: Verify tie handling matches source when PDF becomes readable

## 2021/Long-eventor.xml [M16] | verdict=`pass` | confidence=`high` | csv=`2021/long.csv` | classes=`M16`

- Summary: The extracted CSV data accurately represents the M16 class results from the 2021 Long eventor.xml file. All 95 competitors are correctly captured with proper normalization of...

### Issues

- None reported.

## 2021/Long-eventor.xml [M18] | verdict=`pass` | confidence=`high` | csv=`2021/long.csv` | classes=`M18`

- Summary: All extracted CSV rows accurately match the raw XML source data with proper normalization applied

### Issues

- None reported.

## 2021/Long-eventor.xml [W16] | verdict=`pass` | confidence=`high` | csv=`2021/long.csv` | classes=`W16`

- Summary: The extracted CSV data accurately represents the W16 class results from the 2021 Long-eventor.xml source file with proper normalization applied

### Issues

- [low] `name` Minor name normalization differences
  CSV: Names appear with accents removed in CSV
  Raw: Davidavičiūtė -> Davidaviciute, Činčikaitė -> Cincikaite, Ziaziulytė -> Ziaziulyte
  Why: Expected normalization artifact - accent removal is standard practice for compatibility
  Next: No action needed - this is expected normalization
- [low] `name` Complex Spanish name handling
  CSV: Spanish names reordered to Given Surname format
  Raw: Faja sanjaume Guinedell -> Sanjaume Guinedell Faja, de MIguel Armisen Monica -> Miguel Armisen Monica de, Munoz del Campo Alba -> del Campo Alba Munoz
  Why: Parser appears to handle complex Spanish naming conventions reasonably well
  Next: No action needed - reasonable normalization of complex names

## 2021/Long-eventor.xml [W18] | verdict=`pass` | confidence=`high` | csv=`2021/long.csv` | classes=`W18`

- Summary: All W18 results correctly extracted from XML source with accurate times, ranks, names, and countries

### Issues

- None reported.

## 2021/Sprint-eventor.xml [M16] | verdict=`pass` | confidence=`high` | csv=`2021/sprint.csv` | classes=`M16`

- Summary: The extracted CSV data accurately represents the M16 class results from the 2021 Sprint XML source. All 95 competitors are correctly captured with proper ranks, times, countries,...

### Issues

- None reported.

## 2021/Sprint-eventor.xml [M18] | verdict=`pass` | confidence=`high` | csv=`2021/sprint.csv` | classes=`M18`

- Summary: All M18 sprint results correctly extracted from XML source with accurate times, ranks, statuses, and names

### Issues

- None reported.

## 2021/Sprint-eventor.xml [W16] | verdict=`review` | confidence=`medium` | csv=`2021/sprint.csv` | classes=`W16`

- Summary: Several name formatting issues detected where Spanish names appear to have incorrect word order, and one Danish name appears to have unusual formatting

### Issues

- [medium] `name` Spanish name word order appears incorrect
  CSV: Miguel Armisen Monica de
  Raw: <Given sequence="1">MIguel Armisen Monica</Given>
  Why: The raw XML shows 'MIguel Armisen Monica' as the given name, but this appears to be a data entry error where multiple names are concatenated. The CSV shows 'Miguel Armisen Monica de' which seems to attempt correction but may still be incorrect.
  Next: Review source data quality - this appears to be a source-level data entry issue
- [medium] `name` Spanish name appears to have surname/given name confusion
  CSV: Sanjaume Guinedell Faja
  Raw: <Family>Faja</Family><Given sequence="1">sanjaume Guinedell</Given>
  Why: Raw shows family name 'Faja' and given name 'sanjaume Guinedell', but the CSV shows 'Sanjaume Guinedell Faja' which appears to concatenate them incorrectly
  Next: Fix parser to handle family/given name order correctly for this entry
- [medium] `name` Spanish name has unusual concatenation
  CSV: del Campo Alba Munoz
  Raw: <Family>Munoz</Family><Given sequence="1">del Campo Alba</Given>
  Why: Raw shows family 'Munoz' and given 'del Campo Alba', CSV shows 'del Campo Alba Munoz' - the 'del Campo' part may be part of a compound surname rather than given name
  Next: Review Spanish naming conventions - 'del Campo' may be part of surname
- [low] `name` Danish name has unusual middle name formatting
  CSV: Hornbaek Laura Kaldahl
  Raw: <Family>Kaldahl</Family><Given sequence="1">Hornbaek Laura</Given>
  Why: The given name 'Hornbaek Laura' seems unusual - 'Hornbaek' might be a place name or additional surname component
  Next: Verify if 'Hornbaek' is part of the name or a data entry artifact

## 2021/Sprint-eventor.xml [W18] | verdict=`pass` | confidence=`high` | csv=`2021/sprint.csv` | classes=`W18`

- Summary: All W18 sprint results correctly extracted from XML source with accurate times, ranks, and athlete information

### Issues

- None reported.

## 2021/results-relay.pdf | verdict=`review` | confidence=`low` | csv=`2021/relay.csv` | classes=`(all)`

- Summary: Cannot audit extracted CSV data against raw source due to PDF text extraction failure. The 80 relay rows appear structurally consistent but require manual verification.

### Issues

- [high] `source-limitation` PDF text extraction failed completely
  CSV: 80 relay rows extracted with high confidence
  Raw: [no raw text extracted]
  Why: Cannot verify any extracted data against source without readable raw text
  Next: Manual verification required - check PDF directly or use alternative text extraction method
- [medium] `name` Potential name formatting issues in several entries
  CSV: Names like 'Vallet Mathias Barros', 'Stefano Marco Anselmo di', 'Clercq Rune de' show unusual patterns
  Raw: N/A - no raw text available
  Why: Some names appear to have word order or formatting anomalies that could indicate parsing issues
  Next: Verify these specific names against the original PDF
- [low] `other` Mixed gender team in M16 Portugal entry
  CSV: M16 Portugal leg3: 'Leonor Ferreira' (typically female name)
  Raw: N/A - no raw text available
  Why: Male relay class contains what appears to be a female name, could indicate data mixing
  Next: Verify Portugal M16 team composition in original PDF

## 2022/Long-eventor.xml [M16] | verdict=`pass` | confidence=`high` | csv=`2022/long.csv` | classes=`M16`

- Summary: All 97 M16 competitors from the XML source are correctly extracted with accurate ranks, times, statuses, and country mappings

### Issues

- None reported.

## 2022/Long-eventor.xml [M18] | verdict=`pass` | confidence=`high` | csv=`2022/long.csv` | classes=`M18`

- Summary: All M18 long distance results correctly extracted from 2022 Eventor XML with proper time conversions, status mappings, and name normalization

### Issues

- None reported.

## 2022/Long-eventor.xml [W16] | verdict=`pass` | confidence=`high` | csv=`2022/long.csv` | classes=`W16`

- Summary: All W16 class data correctly extracted from XML source with accurate times, ranks, and athlete information

### Issues

- None reported.

## 2022/Long-eventor.xml [W18] | verdict=`pass` | confidence=`high` | csv=`2022/long.csv` | classes=`W18`

- Summary: All 95 W18 competitors from the XML source are correctly extracted with accurate ranks, times, countries, and names. The three MP (mispunch) statuses are properly identified.

### Issues

- None reported.

## 2022/Sprint-eventor.xml [M16] | verdict=`pass` | confidence=`high` | csv=`2022/sprint.csv` | classes=`M16`

- Summary: All 98 M16 entries correctly extracted from XML with accurate ranks, times, statuses, and normalized country codes

### Issues

- None reported.

## 2022/Sprint-eventor.xml [M18] | verdict=`pass` | confidence=`high` | csv=`2022/sprint.csv` | classes=`M18`

- Summary: All M18 sprint results correctly extracted from XML source with proper normalization

### Issues

- None reported.

## 2022/Sprint-eventor.xml [W16] | verdict=`review` | confidence=`medium` | csv=`2022/sprint.csv` | classes=`W16`

- Summary: Several concerning issues found: sex field inconsistencies, missing non-European competitors, and potential name extraction problems

### Issues

- [high] `source-limitation` All Person elements have sex='M' despite being W16 class
  CSV: W16 class with female names like Janka Mikes, Katerina Douskova, etc.
  Raw: <Person sex="M"><PersonName><Family>Mikes</Family><Given sequence="1">Janka</Given></PersonName> (and all others)
  Why: XML source has incorrect sex='M' for all competitors in W16 (women's) class - this appears to be a source data error
  Next: Verify this is a known source issue and document it; parser correctly extracted W16 class despite sex field error
- [medium] `missing-row` Non-European competitors excluded from CSV
  CSV: These competitors missing from CSV output
  Raw: Key Mila (AUS), Erika Enderby (AUS), Anna Babington (NZL), Rachel Baker (NZL) present in XML
  Why: Australian and New Zealand competitors are intentionally excluded per normalization rules for European-only results
  Next: Confirm this exclusion is intentional per EYOC European-only policy
- [low] `name` Compound surname handling
  CSV: Guinedell Faja Sanjaume
  Raw: <Family>Faja sanjaume</Family><Given>Guinedell</Given>
  Why: Compound surname 'Faja sanjaume' correctly normalized to title case as 'Faja Sanjaume'
  Next: No action needed - normalization appears correct
- [low] `name` Multi-word given names handled correctly
  CSV: Augusta May Thorsen, Frida Kaerner Grooss, Diana Maria Pop
  Raw: <Given>Augusta May</Given>, <Given>Frida Kaerner</Given>, <Given>Diana Maria</Given>
  Why: Multi-word given names properly preserved in normalization
  Next: No action needed - handling appears correct

## 2022/Sprint-eventor.xml [W18] | verdict=`review` | confidence=`high` | csv=`2022/sprint.csv` | classes=`W18`

- Summary: Several non-European countries appear in the CSV that should be excluded per normalization rules, plus some missing rows and potential ranking issues

### Issues

- [high] `country` Non-European countries included in normalized CSV
  CSV: No NZL, AUS, or ISR entries in CSV (correctly excluded)
  Raw: New Zealand (NZL), Australia (AUS), Israel (ISR) athletes present in XML
  Why: Actually this is correct - these non-European countries should be excluded per normalization rules
  Next: This is actually correct behavior - non-European guests should be excluded
- [medium] `missing-row` Missing New Zealand athletes in CSV
  CSV: No NZL entries present
  Raw: Zara Stewart (NZL, bib 395, rank 46), Kaia Joergensen (NZL, bib 303, rank 57), Katherine Babington (NZL, bib 344, MP), Emily Hayes (NZL, bib 368, DNF)
  Why: Upon review, this is correct - non-European countries should be excluded per normalization rules
  Next: No action needed - correct exclusion of non-European guests
- [medium] `missing-row` Missing Australia and Israel athletes
  CSV: Omer Satt appears as ISR but AUS missing
  Raw: Mikayla Enderby (AUS, bib 317, rank 85), Omer Satt (ISR, bib 386, rank 62)
  Why: Israel appears in CSV but Australia correctly excluded. Need to verify if Israel should be considered European for EYOC
  Next: Verify if Israel (ISR) should be included in European championships
- [low] `rank` Ranking sequence has gaps
  CSV: CSV shows same ranking pattern with ties at rank 17
  Raw: XML shows ranks 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,17,17,20,21...
  Why: Ranking appears consistent between source and CSV, ties handled correctly
  Next: No action needed - ranking is correct
- [low] `other` Sex field inconsistency in XML
  CSV: Correctly classified as W18 class
  Raw: All Person elements show sex='M' even for female W18 class
  Why: XML source has incorrect sex attribute but class is correctly W18, CSV properly ignores the erroneous sex field
  Next: No action needed - parser correctly uses class over sex field

## 2022/result-relay.pdf | verdict=`review` | confidence=`low` | csv=`2022/relay.csv` | classes=`(all)`

- Summary: Cannot audit extracted data against raw source due to PDF text extraction failure. The CSV data appears structurally sound with 84 relay teams across 4 classes, but verification...

### Issues

- [high] `source-limitation` PDF text extraction failed completely
  CSV: 84 relay rows extracted with high confidence
  Raw: [no raw text extracted]
  Why: Cannot verify any extracted data against source without readable text from PDF
  Next: Use alternative PDF extraction method or manual verification of sample entries
- [low] `name` Potential name order inconsistency in Swedish team
  CSV: W18 SWE: Emilsson Emma (should be Emma Emilsson)
  Raw: N/A - no source text
  Why: Name appears in surname-first format unlike other normalized entries
  Next: Check if source has Emma Emilsson and normalize to Given Surname format
- [low] `name` Potential name parsing issue in Croatian M18 team
  CSV: M18 CRO leg2: Zdenka Petra Stambuk (unusual name for male category)
  Raw: N/A - no source text
  Why: Name appears feminine in male relay category, could indicate parsing error
  Next: Verify gender and correct name from source document

## 2023/Long-eventor.xml [M16] | verdict=`pass` | confidence=`high` | csv=`2023/long.csv` | classes=`M16`

- Summary: All 97 M16 competitors correctly extracted with accurate data mapping from XML to CSV

### Issues

- None reported.

## 2023/Long-eventor.xml [M18] | verdict=`pass` | confidence=`high` | csv=`2023/long.csv` | classes=`M18`

- Summary: All M18 class data correctly extracted from XML source with accurate ranks, times, statuses, and athlete details

### Issues

- None reported.

## 2023/Long-eventor.xml [W16] | verdict=`pass` | confidence=`high` | csv=`2023/long.csv` | classes=`W16`

- Summary: All W16 class data correctly extracted from XML source with accurate ranks, times, countries, and names

### Issues

- None reported.

## 2023/Long-eventor.xml [W18] | verdict=`pass` | confidence=`high` | csv=`2023/long.csv` | classes=`W18`

- Summary: All 97 W18 competitors correctly extracted with accurate data matching the XML source

### Issues

- None reported.

## 2023/Sprint-eventor.xml [M16] | verdict=`pass` | confidence=`high` | csv=`2023/sprint.csv` | classes=`M16`

- Summary: All 96 M16 competitors correctly extracted with accurate ranks, times, countries, and names

### Issues

- None reported.

## 2023/Sprint-eventor.xml [M18] | verdict=`pass` | confidence=`high` | csv=`2023/sprint.csv` | classes=`M18`

- Summary: All 95 M18 competitors correctly extracted from XML source with accurate ranks, times, countries, and names

### Issues

- None reported.

## 2023/Sprint-eventor.xml [W16] | verdict=`pass` | confidence=`high` | csv=`2023/sprint.csv` | classes=`W16`

- Summary: All 81 W16 competitors correctly extracted from XML source with accurate ranks, times, countries, and names

### Issues

- None reported.

## 2023/Sprint-eventor.xml [W18] | verdict=`pass` | confidence=`high` | csv=`2023/sprint.csv` | classes=`W18`

- Summary: All 89 W18 competitors correctly extracted with accurate ranks, times, countries, and names

### Issues

- None reported.

## 2023/results-relay.pdf | verdict=`review` | confidence=`low` | csv=`2023/relay.csv` | classes=`(all)`

- Summary: Cannot audit extracted data against raw source due to PDF text extraction failure. The CSV data appears structurally consistent but requires manual verification against the...

### Issues

- [high] `source-limitation` Raw PDF text extraction failed
  CSV: 84 relay rows extracted with high confidence
  Raw: [no raw text extracted]
  Why: Cannot verify accuracy of extracted data without access to source content
  Next: Manual verification of CSV against original PDF required
- [medium] `country` Unusual country formatting for Moldova
  CSV: Moldova, Republic of Moldova, Republic of 1
  Raw: N/A - no raw text available
  Why: Country field contains redundant text and unusual formatting that may indicate parsing issue
  Next: Check if raw PDF shows 'Moldova' or similar, normalize to 'MDA'
- [low] `country` Duplicated country names in team field
  CSV: Examples: 'Czechia Czechia 1', 'Switzerland Switzerland 1'
  Raw: N/A - no raw text available
  Why: Team names show duplicated country names which may indicate parsing artifact
  Next: Verify if raw PDF shows single or double country names in team field

## 2024/Long-eventor.xml [M16] | verdict=`pass` | confidence=`high` | csv=`2024/long.csv` | classes=`M16`

- Summary: All 95 M16 competitors from the XML source are correctly extracted with accurate ranks, times, statuses, and normalized data

### Issues

- None reported.

## 2024/Long-eventor.xml [M18] | verdict=`pass` | confidence=`high` | csv=`2024/long.csv` | classes=`M18`

- Summary: All 105 M18 competitors from the XML source are correctly extracted with accurate ranks, times, countries, and statuses. The data shows excellent fidelity to the source.

### Issues

- None reported.

## 2024/Long-eventor.xml [W16] | verdict=`pass` | confidence=`high` | csv=`2024/long.csv` | classes=`W16`

- Summary: All 87 W16 competitors from the XML source are correctly extracted with accurate ranks, times, countries, and names. One MP (mispunch) status is properly handled.

### Issues

- None reported.

## 2024/Long-eventor.xml [W18] | verdict=`pass` | confidence=`high` | csv=`2024/long.csv` | classes=`W18`

- Summary: All 90 W18 competitors from the XML source are correctly extracted with accurate ranks, times, countries, and statuses

### Issues

- None reported.

## 2024/RESULTS-RELAY-WITH-MIX.pdf | verdict=`review` | confidence=`low` | csv=`2024/relay.csv` | classes=`(all)`

- Summary: Cannot audit due to PDF text extraction failure - raw source unavailable for comparison

### Issues

- [high] `source-limitation` PDF text extraction failed completely
  CSV: 82 relay rows extracted with high confidence
  Raw: [no raw text extracted]
  Why: Cannot verify any extracted data against source without readable raw text
  Next: Manual PDF review required or alternative text extraction method needed

## 2024/Sprint-eventor.xml [M16] | verdict=`pass` | confidence=`high` | csv=`2024/sprint.csv` | classes=`M16`

- Summary: All 95 M16 competitors from the XML source are correctly extracted with accurate ranks, times, countries, and statuses. The data shows excellent fidelity to the source.

### Issues

- None reported.

## 2024/Sprint-eventor.xml [M18] | verdict=`pass` | confidence=`high` | csv=`2024/sprint.csv` | classes=`M18`

- Summary: All 105 M18 competitors from the XML source are correctly represented in the CSV with accurate ranks, times, statuses, and normalized data

### Issues

- None reported.

## 2024/Sprint-eventor.xml [W16] | verdict=`pass` | confidence=`high` | csv=`2024/sprint.csv` | classes=`W16`

- Summary: All W16 sprint results correctly extracted from 2024 Eventor XML with proper normalization

### Issues

- None reported.

## 2024/Sprint-eventor.xml [W18] | verdict=`pass` | confidence=`high` | csv=`2024/sprint.csv` | classes=`W18`

- Summary: All 90 W18 competitors correctly extracted from XML with accurate ranks, times, statuses, and normalized country codes

### Issues

- None reported.

## 2025/Long.xml [M16] | verdict=`pass` | confidence=`high` | csv=`2025/long.csv` | classes=`M16`

- Summary: All M16 competitors correctly extracted with accurate data matching the XML source

### Issues

- None reported.

## 2025/Long.xml [M18] | verdict=`pass` | confidence=`high` | csv=`2025/long.csv` | classes=`M18`

- Summary: The extracted CSV data accurately represents the M18 class results from the XML source with proper normalization applied

### Issues

- None reported.

## 2025/Long.xml [W16] | verdict=`review` | confidence=`medium` | csv=`2025/long.csv` | classes=`W16`

- Summary: Several country normalization issues and missing non-European competitors need review

### Issues

- [medium] `country` Non-European countries included in normalized CSV
  CSV: Missing from CSV - these non-European competitors should be excluded per normalization rules
  Raw: Australia (Ariadna Iskhakova), New Zealand (multiple competitors), United States (Allison Coates)
  Why: Normalization rules state non-European guests should be excluded, but some appear to be missing while others from same countries are present
  Next: Verify consistent application of European-only filtering rule
- [low] `country` Country code normalization inconsistencies
  CSV: MDA
  Raw: Moldova, Republic of
  Why: Correct normalization but should verify all country aliases are handled consistently
  Next: Confirm Moldova normalization is correct
- [low] `missing-row` Non-European competitors excluded from CSV
  CSV: These competitors do not appear in the CSV
  Raw: Ariadna Iskhakova (Australia), multiple New Zealand competitors (Torun Joergensen, Cerys Findlow, Dora Slavich, Charlotte Dalziel), Allison Coates (United States), Shari Gilbert (Australia)
  Why: Per normalization rules, non-European guests should be excluded, which appears correct
  Next: Confirm this exclusion is intentional per European-only policy
- [low] `name` Name formatting variations
  CSV: Astrid Faber Fengergroen
  Raw: FengerGroen vs Fengergroen in raw
  Why: Minor spelling variation in compound surname - appears to be normalization cleanup
  Next: Verify name normalization is consistent

## 2025/Long.xml [W18] | verdict=`pass` | confidence=`high` | csv=`2025/long.csv` | classes=`W18`

- Summary: All W18 competitors correctly extracted with accurate data matching the XML source

### Issues

- None reported.

## 2025/Sprint.xml [M16] | verdict=`pass` | confidence=`high` | csv=`2025/sprint.csv` | classes=`M16`

- Summary: All M16 class data correctly extracted from XML source with proper normalization

### Issues

- None reported.

## 2025/Sprint.xml [M18] | verdict=`pass` | confidence=`high` | csv=`2025/sprint.csv` | classes=`M18`

- Summary: The extracted CSV data accurately represents the M18 class results from the 2025 Sprint XML source. All competitors, rankings, times, and statuses are correctly captured with...

### Issues

- None reported.

## 2025/Sprint.xml [W16] | verdict=`pass` | confidence=`high` | csv=`2025/sprint.csv` | classes=`W16`

- Summary: All 99 W16 competitors from the XML source are correctly represented in the CSV with accurate data extraction

### Issues

- None reported.

## 2025/Sprint.xml [W18] | verdict=`pass` | confidence=`high` | csv=`2025/sprint.csv` | classes=`W18`

- Summary: All W18 class data correctly extracted from XML source with proper normalization

### Issues

- None reported.

## 2025/results-relay.pdf | verdict=`review` | confidence=`low` | csv=`2025/relay.csv` | classes=`(all)`

- Summary: Cannot verify extracted data against raw source due to PDF rendering failure. The CSV contains 87 relay rows across M16, W16, M18, W18 classes with reasonable structure, but...

### Issues

- [high] `source-limitation` PDF source file not accessible for verification
  CSV: 87 relay rows extracted with high confidence
  Raw: [no raw text extracted]
  Why: Cannot verify any extracted data against the source PDF, making this audit inconclusive
  Next: Re-attempt PDF text extraction or obtain alternative source format for verification
- [medium] `other` Potential gender classification issue in M18 class
  CSV: M18 MDA team includes 'Emilia Grosu' (appears to be female name)
  Raw: N/A - no raw source
  Why: Female-appearing name in male relay class could indicate misclassification, but cannot verify without source
  Next: Verify gender classification for MDA M18 team member Emilia Grosu against source
- [low] `other` Mixed relay class absent
  CSV: Only M16, W16, M18, W18 classes present
  Raw: N/A - no raw source
  Why: Schema allows Mixed class but none extracted - may be legitimate if no mixed relays occurred
  Next: Confirm whether mixed relays were held at this event

## 2026/01-sprint-results-eventor.xml [M16] | verdict=`pass` | confidence=`high` | csv=`2026/sprint.csv` | classes=`M16`

- Summary: The extracted CSV data accurately represents the M16 class results from the 2026 sprint XML source. All competitors, times, ranks, and statuses match the source data correctly.

### Issues

- None reported.

## 2026/01-sprint-results-eventor.xml [M18] | verdict=`pass` | confidence=`high` | csv=`2026/sprint.csv` | classes=`M18`

- Summary: The extracted CSV data accurately represents the M18 class results from the 2026 sprint XML source. All competitors, times, ranks, and statuses match the source data correctly.

### Issues

- None reported.

## 2026/01-sprint-results-eventor.xml [W16] | verdict=`review` | confidence=`medium` | csv=`2026/sprint.csv` | classes=`W16`

- Summary: Class mismatch issue: XML shows 'Women 16' but sex='M', plus several non-European countries included

### Issues

- [medium] `class` Class definition inconsistency in XML
  CSV: All rows show class=W16
  Raw: <Class sex="M"><Name>Women 16</Name>
  Why: XML shows sex='M' but class name is 'Women 16', creating ambiguity about correct class assignment
  Next: Verify with source organizers whether this is W16 or M16 class
- [low] `country` Non-European countries included in normalized output
  CSV: No rows for NZL, AUS, USA countries in CSV
  Raw: Athletes from NZL (New Zealand), AUS (Australia), USA (United States)
  Why: Non-European guests should be excluded per normalization rules, and they appear to be correctly excluded
  Next: Confirm exclusion is working correctly - this appears to be proper behavior
- [low] `missing-row` Some athletes from raw XML not in CSV
  CSV: These athletes do not appear in the CSV
  Raw: Sophie Bacchus (NZL), Josie Hua (NZL), Ianthe MacMillan Armstrong (NZL), Sophie Neumann (USA), Ella Maja Lang (AUS), Allison Coates (USA), Josalyn Dunlap (USA), Veronika Iskhakova (AUS), Shari Gilbert (AUS)
  Why: These are non-European athletes who should be excluded per normalization rules
  Next: No action needed - correct exclusion of non-European guests

## 2026/01-sprint-results-eventor.xml [W18] | verdict=`review` | confidence=`high` | csv=`2026/sprint.csv` | classes=`W18`

- Summary: Several significant issues found including class mismatch, missing competitors, and name inconsistencies that require review

### Issues

- [high] `class` Class header shows 'Women 18' but XML sex attribute is 'M'
  CSV: All rows show class=W18
  Raw: <Class sex="M"><Name>Women 18</Name>
  Why: The XML has contradictory class information - sex='M' (Male) but Name='Women 18'. This suggests a data corruption issue in the source file.
  Next: Verify the correct class designation with race organizers - this appears to be source data corruption
- [medium] `missing-row` Missing competitors from CSV extraction
  CSV: These competitors do not appear in the CSV output
  Raw: Raw XML shows competitors like Anna Batcheler (NZL), Niamh Hoare (NZL), Torun Joergensen (NZL), Orla Hoare (NZL), Amy Dufty (AUS), Savanna Sweeney (AUS), Rose FreedmanRiles (USA), Saskia Edmunds Boerschke (CAN)
  Why: Multiple competitors present in the raw XML are missing from the normalized CSV, suggesting the country normalization filter may be excluding non-European competitors
  Next: Confirm if non-European competitors should be intentionally excluded per normalization rules
- [medium] `name` Name inconsistency for Danish competitor
  CSV: Astrid Faber Fengergroen
  Raw: FengerGroen, Astrid Faber
  Why: The surname appears to be incorrectly normalized - 'FengerGroen' in XML becomes 'Fengergroen' in CSV
  Next: Check name normalization logic for handling of compound surnames with capital letters
- [low] `name` Minor name variations in compound surnames
  CSV: Chloe van Vyve Courtois
  Raw: Van Vyve Courtois vs van Vyve Courtois
  Why: Capitalization differences in compound surnames, though this may be acceptable normalization
  Next: Verify if title case normalization should preserve original capitalization in compound names

## 2026/02-long-results-eventor.xml [M16] | verdict=`pass` | confidence=`high` | csv=`2026/long.csv` | classes=`M16`

- Summary: All M16 class data correctly extracted from XML source with proper normalization

### Issues

- None reported.

## 2026/02-long-results-eventor.xml [M18] | verdict=`pass` | confidence=`high` | csv=`2026/long.csv` | classes=`M18`

- Summary: All M18 class data correctly extracted from XML source with proper normalization

### Issues

- None reported.

## 2026/02-long-results-eventor.xml [W16] | verdict=`fail` | confidence=`high` | csv=`2026/long.csv` | classes=`W16`

- Summary: Multiple critical issues found: incorrect class assignment (M16 class data in W16 results), missing competitors, and non-European countries included

### Issues

- [high] `class` Incorrect class assignment in source XML
  CSV: All rows assigned to W16 class
  Raw: <Class sex="M"><Name>Women 16</Name></Class>
  Why: The XML shows sex="M" but Name="Women 16", creating ambiguity about whether this is actually M16 or W16 data. The parser chose W16 based on the name, but this inconsistency suggests data corruption.
  Next: Verify with source whether this should be M16 or W16 data and correct the XML
- [high] `missing-row` Missing competitors from CSV extraction
  CSV: These competitors are completely absent from the CSV
  Raw: Ianthe MacMillan Armstrong (NZL), Sophie Herde (NZL), Ella Maja Lang (AUS), Veronika Iskhakova (AUS), Sophie Neumann (USA), Josie Hua (NZL), Sophie Bacchus (NZL), Allison Coates (USA) present in XML
  Why: Multiple competitors from non-European countries are present in the raw XML but missing from the extracted CSV, suggesting the parser excluded them
  Next: Confirm if non-European exclusion policy is correctly applied - these appear to be legitimate EYOC participants
- [medium] `country` Non-European countries included in CSV
  CSV: All extracted countries appear to be European federations
  Raw: No non-European countries should be in EYOC results according to normalization rules
  Why: Upon closer inspection, all countries in the CSV are actually European federations, so this is not an issue
  Next: No action needed - extraction correctly limited to European federations
- [low] `rank` Tied ranks handled correctly
  CSV: Both shown as rank 21
  Raw: Position 21 appears twice (Eszter Anna Palfy and Ivanna Panchenko both with 3564 seconds)
  Why: This is actually correct handling of tied positions
  Next: No action needed - ties handled correctly

## 2026/02-long-results-eventor.xml [W18] | verdict=`review` | confidence=`high` | csv=`2026/long.csv` | classes=`W18`

- Summary: Several significant issues found including class mismatch, missing competitors, and name formatting problems

### Issues

- [high] `class` Class mismatch in XML header
  CSV: All rows show class=W18
  Raw: <Class sex="M"><Name>Women 18</Name>
  Why: XML shows sex="M" but class name is "Women 18" - this is contradictory. The CSV correctly interprets this as W18 based on the class name, but the XML structure is inconsistent.
  Next: Verify with source data provider about the sex attribute vs class name discrepancy
- [medium] `missing-row` Missing competitors from CSV
  CSV: These competitors do not appear in the CSV output
  Raw: Raw shows competitors with bib 576 (Niamh Hoare, NZL), 521 (Torun Joergensen, NZL), 570 (Amy Dufty, AUS), 583 (Rose FreedmanRiles, USA), 531 (Savanna Sweeney, AUS)
  Why: Non-European competitors are intentionally excluded per normalization rules, but this should be verified as correct behavior
  Next: Confirm that non-European exclusion is working as intended
- [medium] `name` Name formatting inconsistencies
  CSV: Astrid Faber Fengergroen (missing space in compound surname)
  Raw: FengerGroen -> Astrid Faber FengerGroen, FreedmanRiles -> Rose FreedmanRiles
  Why: Compound surnames are not being handled consistently - some lose internal spacing or capitalization
  Next: Review name parsing logic for compound surnames and multi-part names
- [low] `status` Status code normalization
  CSV: Status shows 'MP' in CSV
  Raw: Status shows 'MissingPunch' in XML
  Why: This appears to be correct normalization from verbose to abbreviated status codes
  Next: No action needed - this is expected normalization
- [low] `rank` Tied rankings handled correctly
  CSV: Both competitors show rank 44, next rank is 46
  Raw: Position 44 appears twice with same time 4548
  Why: Tied rankings are handled correctly with proper rank progression
  Next: No action needed - correct tie handling

## 2026/03-relay-results-eventor.xml [M16] | verdict=`review` | confidence=`high` | csv=`2026/relay.csv` | classes=`M16`

- Summary: Several significant issues found including incorrect ranking for DNF teams, missing team (USA 1), and potential country exclusions that need verification

### Issues

- [high] `rank` DNF teams assigned incorrect ranks
  CSV: Croatia 1 has rank=25 and status=DNF, Turkiye 1 has rank=24 and status=DNF
  Raw: Croatia 1 shows <Status>DidNotFinish</Status> with Position 27, Turkiye 1 shows <Status>DidNotFinish</Status> with Position 28
  Why: DNF teams should not have numerical ranks - they should be unranked or have a special DNF designation
  Next: Fix parser to not assign numerical ranks to DNF teams
- [high] `missing-row` USA 1 team completely missing from CSV
  CSV: No USA 1 team found in CSV output
  Raw: USA 1 team appears in raw XML with Alexander Eriksson (leg 1: 1893s) and Mark Fey (leg 2: 2539s), but no leg 3 runner listed
  Why: Complete team missing from normalized results despite appearing in source data
  Next: Investigate why USA 1 team was dropped - likely due to incomplete leg 3 data
- [medium] `missing-row` New Zealand 1 team missing from CSV
  CSV: No New Zealand 1 team found in CSV output
  Raw: New Zealand 1 team appears with Daniel Porteous (1864s), Jamie Appleton (2280s), Xavier White (2531s), total 6675s
  Why: Complete team with all leg times missing from results
  Next: Verify if NZL is intentionally excluded as non-European or if this is a parser bug
- [medium] `missing-row` Australia 1 team missing from CSV
  CSV: No Australia 1 team found in CSV output
  Raw: Australia 1 team appears with Rory Shedden (1938s), Baxter Peel (2515s), Euan Shedden (2840s), total 7293s
  Why: Complete team with all leg times missing from results
  Next: Verify if AUS is intentionally excluded as non-European or if this is a parser bug
- [low] `rank` Rank sequence has gap
  CSV: Ranks go 1-23, then 25, 24 (for DNF teams)
  Raw: Teams ranked 1-23 in source, with positions 27-28 for DNF teams
  Why: Missing rank 24 in sequence, and DNF teams should not have numerical ranks
  Next: Fix ranking logic to handle DNF teams properly and maintain sequence

## 2026/03-relay-results-eventor.xml [M18] | verdict=`pass` | confidence=`high` | csv=`2026/relay.csv` | classes=`M18`

- Summary: All 27 M18 relay teams correctly extracted with accurate times, names, and statuses

### Issues

- None reported.

## 2026/03-relay-results-eventor.xml [W16] | verdict=`review` | confidence=`high` | csv=`2026/relay.csv` | classes=`W16`

- Summary: Several significant issues found including missing teams, incorrect rankings, and status mismatches that require investigation

### Issues

- [high] `missing-row` New Zealand 1 team completely missing from CSV
  CSV: No New Zealand team found in CSV
  Raw: New Zealand 1 team with Sophie Herde, Ianthe MacMillan Armstrong, Sophie Bacchus - rank 16, total time 7429 seconds
  Why: Complete team missing from extracted data despite clear presence in raw XML with full results
  Next: Check parser logic for New Zealand team extraction
- [high] `missing-row` United States 1 team completely missing from CSV
  CSV: No United States team found in CSV
  Raw: United States 1 team with Sophie Neumann, Allison Coates, Josalyn Dunlap - rank 25 (DNF), partial time 6343 seconds
  Why: Complete team missing from extracted data despite clear presence in raw XML
  Next: Check parser logic for United States team extraction
- [high] `missing-row` Australia 1 team completely missing from CSV
  CSV: No Australia team found in CSV
  Raw: Australia 1 team with Ella Maja Lang, Veronika Iskhakova - rank 27 (DNS), partial time 4225 seconds
  Why: Complete team missing from extracted data despite clear presence in raw XML
  Next: Check parser logic for Australia team extraction
- [high] `rank` Turkey ranking inconsistency
  CSV: TUR ranked as 20 in CSV
  Raw: Turkiye 1 shows Position 20 in OverallResult
  Why: Raw XML shows position 20 but this creates a gap in rankings (no rank 19 in CSV)
  Next: Verify if rank 19 team exists or if rankings should be consecutive
- [medium] `status` Belgium team status mismatch
  CSV: BEL status shows DNF with rank 18
  Raw: Belgium 1 shows only leg 1 completed (Anna Pasquasy 2339s), no leg 2 or 3 data
  Why: Team appears to have DNS for legs 2&3 but CSV shows DNF status
  Next: Clarify if incomplete team should be DNF or DNS
- [medium] `rank` Belgium ranking placement
  CSV: BEL ranked as 18 between complete teams
  Raw: Belgium 1 has only partial completion
  Why: Incomplete team ranked among complete teams rather than at end
  Next: Verify ranking logic for incomplete teams

## 2026/03-relay-results-eventor.xml [W18] | verdict=`pass` | confidence=`high` | csv=`2026/relay.csv` | classes=`W18`

- Summary: The extracted CSV data accurately represents the W18 relay results from the XML source with proper normalization and status handling

### Issues

- None reported.
