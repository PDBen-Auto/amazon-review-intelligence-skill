# Contributing

Contributions are welcome for the public collector, evidence schemas, synthetic tests, offline reports, documentation, and release validation.

## Before opening an issue or pull request

1. Search existing issues and read the repository boundary notes.
2. Reproduce the behavior with synthetic or fully sanitized public-review data.
3. Remove credentials, cookies, account identifiers, customer data, supplier data, and private absolute paths.
4. Explain the expected behavior, observed behavior, environment, and validation performed.

## Pull requests

Keep each change focused. Run the relevant tests before submitting:

```bash
python -m unittest discover -s tests -v
python -m unittest discover -s examples/synthetic-demo -p "test_*.py" -v
```

Do not add logic that bypasses CAPTCHA, Robot Check, sign-in walls, account warnings, or platform controls. Do not add telemetry, hidden prompts, callbacks, or private customer data.

## Releases

Release metadata, public manifests, and provenance signatures are maintained by the publisher. Do not hand-edit signed release files in a feature pull request.
