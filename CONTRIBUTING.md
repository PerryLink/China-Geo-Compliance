# Contributing to china-geo-compliance

## Project Status

This is a **personal project** currently maintained solely by [PerryLink](https://github.com/PerryLink). While contributions are welcome, please note that review and merge timelines depend on the maintainer's availability.

---

## Reporting Issues

Found a bug or have a suggestion? Please open an [Issue](https://github.com/PerryLink/china-geo-compliance/issues) with the following information:

- **Bug reports**: Steps to reproduce, expected behavior, actual behavior, your Python version and OS
- **Feature requests**: Describe the use case and why it would benefit the project
- **Questions**: Check existing issues first; if not answered, open a new one

---

## Development Setup

### Prerequisites

- Python 3.8+
- [Poetry](https://python-poetry.org/) (recommended)

### Steps

```bash
# 1. Fork and clone the repository
git clone https://github.com/PerryLink/china-geo-compliance.git
cd china-geo-compliance

# 2. Install dependencies
poetry install

# 3. Verify setup by running tests
poetry run pytest
```

---

## Code Standards

This project follows [PEP 8](https://peps.python.org/pep-0008/) with the following toolchain:

```bash
# Format code
poetry run black src/

# Lint
poetry run ruff check src/

# Run tests
poetry run pytest
```

Please ensure all checks pass before submitting a pull request.

---

## Submitting a Pull Request

1. **Fork** the repository and create a branch from `main`:
   ```bash
   git checkout -b feat/your-feature-name
   ```

2. **Make your changes** — keep commits focused and atomic.

3. **Run checks locally**:
   ```bash
   poetry run black src/
   poetry run ruff check src/
   poetry run pytest
   ```

4. **Write a clear PR description** explaining:
   - What problem this solves
   - How you tested it
   - Any related issues (e.g., `Closes #42`)

5. **Open the PR** against the `main` branch.

---

## License

By contributing, you agree that your contributions will be licensed under the [Apache License 2.0](LICENSE).

Copyright 2026 Chance Dean (novelnexusai@outlook.com)
