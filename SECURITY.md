# Security Policy

## Supported surface

Report issues in the public review collector, evidence normalization, offline report generation, accidental data disclosure, or release-boundary checks.

The collector must stop when Amazon presents CAPTCHA, Robot Check, a sign-in wall, or an account warning. Do not report a bypass request as a bug.

## Reporting

Use GitHub private vulnerability reporting when available. Otherwise contact the repository owner through a private channel listed in the profile. Never include credentials, cookies, customer names, private ASIN research, or production exports.

## Operational rules

- Remove secrets and personal data from issue bodies, logs, screenshots, and fixtures.
- Rotate a token or cookie immediately if it appears in logs or commits.
- Treat synthetic examples as the default for reproduction.
- Do not claim that a release is official unless its manifest and provenance signature verify.
- This project is not affiliated with Amazon and does not authorize access that the source platform does not permit.
