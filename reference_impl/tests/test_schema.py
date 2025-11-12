"""Tests for OHSDM schema validation."""

import json
from pathlib import Path

from jsonschema import Draft202012Validator

SCHEMA_PATH = Path("schema/ohsdm.schema.v1_0.json")


def test_schema_is_valid():
    """Test that the OHSDM schema itself is valid."""
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)
    Draft202012Validator.check_schema(schema)
