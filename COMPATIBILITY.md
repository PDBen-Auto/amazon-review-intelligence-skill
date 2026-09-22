# Compatibility

| Surface | Supported | Notes |
| --- | --- | --- |
| Codex / Agent Skills | Yes | Install with `npx skills add` or copy the Skill directory. |
| Python | 3.10+ | Python 3.12 is covered by CI. |
| Input evidence | JSON, CSV, XLSX | Analysis-only mode accepts existing sanitized evidence. |
| Output | JSON, XLSX, standalone HTML | Reports open locally without a server. |
| Amazon login | Not required for the public written-review path | Stop when a login wall, CAPTCHA, Robot Check, or account warning appears. |
| Windows / Linux | Supported | Use a virtual environment for optional Python packages. |

Unsupported or incomplete inputs must produce a bounded partial result rather than invented review coverage.
