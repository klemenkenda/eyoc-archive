# Independent Data Audit

`openrouter_data_audit.py` runs an LLM-based audit over the repository's normalized CSVs.

It groups rows by `source_file`, sends:
- the raw source file rendered as text
- the matching extracted CSV rows
- a detailed normalization/audit prompt

to OpenRouter, then writes one combined Markdown report.

Usage:

```sh
python scripts/independent_data_audit/openrouter_data_audit.py --model <openrouter-model-id>
```

Useful options:
- `--max-sources 5` for a small pilot run
- `--source-filter 2024/Long-eventor.xml` to retry one source
- `--max-completion-tokens 4000` to keep more room for input context

Debugging:
- Set `OPENROUTER_AUDIT_DEBUG_PDF=1` to print which PDF extractor was tried, whether it failed, and how many characters it returned.

Environment:
- Put `OPENROUTER_API_KEY=...` in `.env`
- You can also set `OPENROUTER_MODEL=...` instead of passing `--model`

Outputs:
- Full Markdown report: `results/raw/OPENROUTER-DATA-AUDIT.md`
- Concise issues-first report: `results/raw/OPENROUTER-DATA-AUDIT-SUMMARY.md`
- Cached per-source JSON responses: `scripts/independent_data_audit/cache/`

Notes:
- The report is only as good as the model and prompt. Treat it as an independent review layer, not ground truth.
- For HTML/XML/text files, the raw file is sent as text.
- Large XML sources are automatically split into smaller per-class audit tasks to avoid model context-limit failures.
- For PDFs, the script now tries multiple extractors in order: PyMuPDF (`fitz`), `pdftotext -layout`, `pypdf`/`PyPDF2`, and `pdfplumber`. If none work, PDF raw text may still be blank and the report will note reduced confidence.
- Cache keys include an internal version marker, so extraction-logic changes can invalidate old cached audit responses automatically.
- The concise report keeps the global summary, then shows one compact heading per audit task with verdict, confidence, related CSVs, classes, a brief task summary, and only the issues section.
