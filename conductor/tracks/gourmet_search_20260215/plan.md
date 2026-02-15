# Implementation Plan - Gourmet Search Parameter Mapping

## Phase 1: Preparation and Analysis
- [x] Task: Audit existing `Option` and `Shop` models against the official Hotpepper API documentation.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Preparation and Analysis' (Protocol in workflow.md)

## Phase 2: Model Updates
- [x] Task: Update `pygourmet/option.py` with missing parameters.
    - [x] Add missing fields to `Option` Pydantic model.
    - [x] Update docstrings for new fields.
- [x] Task: Update `pygourmet/shop.py` if missing response fields are identified.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Model Updates' (Protocol in workflow.md)

## Phase 3: Testing and Verification
- [x] Task: Write unit tests for new `Option` parameters.
- [x] Task: Implement updated parameter handling in `Api.search` if necessary.
- [x] Task: Run `uv run prek` to ensure linting and type checks pass.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Testing and Verification' (Protocol in workflow.md)
