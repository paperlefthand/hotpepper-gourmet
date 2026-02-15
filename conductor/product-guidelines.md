# Product Guidelines

## Code Philosophy
- **Explicit over Implicit:** Prioritize descriptive naming and explicit type hints. The code should be self-documenting and easy to navigate for any Python developer.
- **Strict Typing:** Leverage Pydantic v2 to ensure all data entering or leaving the library is validated and correctly typed. Avoid `Any` at all costs.
- **Consistency with API:** Align the library's models and parameter names with the official Hotpepper Gourmet API documentation to reduce cognitive load for users familiar with the service.

## Documentation Standards
- **Google Style Docstrings:** Maintain comprehensive docstrings for all public interfaces. Include parameter descriptions, return types, and usage examples.
- **Self-Documenting Code:** Choose clear variable and function names that describe their purpose without needing excessive comments.

## Quality Standards
- **Test-Driven Reliability:** Maintain high test coverage (>80%). Use mocks for unit tests and strictly separate integration tests that interact with the live API.
- **Linting & Formatting:** Adhere strictly to the project's Ruff configuration (4-space indent, double quotes).
- **Conventional Commits:** Use structured commit messages to maintain a clean and readable project history.

## Visual Identity & Prose
- **Professional & Technical:** Maintain a clear, professional tone in all documentation and communications.
- **Instructional Clarity:** Ensure that READMEs and guides provide direct, actionable instructions for developers.
