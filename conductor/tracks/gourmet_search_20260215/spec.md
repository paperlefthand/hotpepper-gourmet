# Specification - Gourmet Search Parameter Mapping

## Overview
This track aims to ensure full compatibility with the [Hotpepper Gourmet Search API](https://webservice.recruit.co.jp/doc/hotpepper/reference.html) by mapping all available request parameters and ensuring the response models are complete.

## Requirements
- Update `Option` class in `pygourmet/option.py` to include all missing parameters from the official documentation (e.g., `special`, `special_or`, `special_category`, `wifi`, `wedding`, etc.).
- Ensure all parameters have correct type hints and Pydantic validation.
- Verify that the `Shop` model in `pygourmet/shop.py` correctly captures all relevant fields returned by the Gourmet Search API.
- Update the `Api.search` and `Api.search_async` methods to correctly pass these parameters to the API.

## Acceptance Criteria
- All Gourmet Search API parameters are represented in the `Option` class.
- Unit tests verify that `Option` objects are correctly serialized into query parameters.
- Integration tests (mocked) verify that complex queries return correctly parsed `Shop` objects.
- `uv run prek` passes without errors.
