# Technology Stack

## Core Development
- **Language:** Python (>=3.12) - Utilizing modern features and strict type hinting.
- **Data Validation:** [Pydantic v2](https://docs.pydantic.dev/latest/) - For robust data modeling and API response validation.
- **HTTP Client:** [httpx](https://www.python-httpx.org/) - Supporting both synchronous and asynchronous request handling.

## Development & Tooling
- **Package Manager:** [uv](https://github.com/astral-sh/uv) - For fast dependency management and environment synchronization.
- **Linting & Formatting:** [Ruff](https://beta.ruff.rs/docs/) - Ensuring code quality and consistent style across the codebase.
- **Build Backend:** [hatchling](https://hatch.pypa.io/latest/) with `hatch-vcs` for dynamic versioning from Git tags.

## Testing & Quality Assurance
- **Test Framework:** [pytest](https://docs.pytest.org/) - Comprehensive testing suite.
- **Testing Plugins:**
    - `pytest-asyncio`: For testing asynchronous functionality.
    - `pytest-httpx`: For mocking API responses during unit tests.
    - `pytest-cov`: For monitoring and reporting code coverage.
- **CI/CD:** GitHub Actions with [tox](https://tox.wiki/) for multi-version Python testing.
