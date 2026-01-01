## Config Drift Checker (V1 – Stable)

A lightweight Python CLI utility for detecting configuration drift between two JSON configuration files.

Designed for **automation, diagnostics, and compliance checks**, this tool compares a baseline
configuration against a target configuration and reports structural or value differences in a
deterministic, machine-friendly way.

---
## Features

* Compare two JSON configuration files (baseline vs target)
* Detect:
  * Missing keys
  * New keys
  * Modified values
* Human-readable console output (optional)
* CSV and JSON export for automation pipelines
* Deterministic exit codes for scripting and CI/CD use
* Schema-safe comparison (no assumptions beyond JSON validity)

---
## Usage

```bash
python config_drift_checker_v1_stable.py \
  --baseline baseline.json \
  --target target.json
```
### Optional flags

```bash
--csv output.csv        Export drift results to CSV
--json output.json      Export drift results to JSON
--quiet                 Suppress console output
```
---
## Exit Codes

| Code | Meaning                          |
| ---- | -------------------------------- |
| 0    | No drift detected                |
| 1    | Drift detected                   |
| 2    | Invalid input or execution error |

This makes the tool safe for use in:

* Automation scripts
* CI/CD pipelines
* Scheduled integrity checks

---

## Example Output

### Console
Drift detected:
- Modified value: logging.level
- Missing key: security.timeout

### CSV / JSON
Each drift entry includes:
* Key path
* Change type
* Baseline value
* Target value

---
## Test Data
Sample baseline and target JSON files are included for demonstration and validation purposes.

---
## Limitations (By Design)
* JSON-only (no YAML/XML)
* No recursive directory scanning
* No automatic remediation

These are intentional to keep V1:
* Predictable
* Safe
* Extensible

---
## Roadmap (Future Versions)
* Threshold-based alerts
* Recursive directory comparison
* YAML support
* Policy enforcement mode
* Remediation suggestions

---
## License
MIT License — free to use, modify, and integrate.

---

## 👤 Author

Darren Williamson
Python Utility Development * Automation * Data Analysis * AI-assisted tooling
Uk Citizen / Spain-based / Remote
LinkedIn: https://www.linkedin.com/in/darren-williamson3/
