# Template Validator

This folder contains a GitHub Actions workflow and a validation script for the templates repository. It validates every `data.json` file with `@liten/template-validator` (Template V2 schema) and produces a full report.

## Files

- `.github/workflows/validate-templates.yml`: CI workflow.
- `scripts/validate-templates.js`: Validation script.
- Output:
  - `validation-report.json`
  - `validation-report.md`

## Local usage

```bash
npm init -y
npm install @liten/template-validator
node scripts/validate-templates.js
```

The process exits with code `1` if any template fails validation.
