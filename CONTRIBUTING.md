# Contributing to OpenHealthMesh

Thanks for your interest in contributing to OpenHealthMesh (OHSDM)! This project aims to be a **community-driven schema** for unifying public health intelligence.

## Ways to Contribute

- **Schema feedback** → Open an Issue to propose field changes, new enums, or extensions.
- **Examples** → Submit PRs with new NDJSON examples from real-world sources (de-identified).
- **Crosswalks** → Add mappings to FHIR, HL7 v2, GA4GH, or other standards.
- **Tooling** → Extend the CLI validator, add ETL scripts, or improve reference API.
- **Docs** → Help clarify README, add tutorials, or draft FAQ answers.

## Process

1. Fork the repository and create a feature branch (`git checkout -b feature/my-change`).
2. Make your changes and run tests:
   ```bash
   pytest
   python reference_impl/validator.py examples/sites.ndjson
   ```
3. Submit a Pull Request with a clear description.
4. At least one maintainer review is required before merge.

## Governance

- **Versioning**: Semantic versioning (`MAJOR.MINOR.PATCH`).  
- **Backward compatibility**: Minor updates (e.g., new fields) must not break validation.  
- **Breaking changes**: Reserved for major releases (e.g., v2.0).  
- **Decisions**: Discussed in Issues/Zulip/Working Groups before merge.

## Code of Conduct

This project follows the [Contributor Covenant](https://www.contributor-covenant.org/).

## Contact

- HL7 Zulip → `#public-health` channel  
- GA4GH Slack → Genomics standards discussions  
- WHO/CDC collaborations → via working group pilots
