#!/usr/bin/env python3
"""Command-line validator for OHSDM JSON files."""
import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

from jsonschema import Draft202012Validator, ValidationError

# Configuration
DEFAULT_SCHEMA_PATH_STR = "schema/ohsdm.schema.v1_0.json"


def load_schema(schema_path: Path | None = None) -> Dict[str, Any]:
    """
    Load and return the OHSDM schema.

    Args:
        schema_path: Optional path to the schema file. If not provided, uses
                     the default path or OHSDM_SCHEMA_PATH environment variable.

    Returns:
        The OHSDM schema as a dictionary

    Raises:
        FileNotFoundError: If the schema file is not found
        json.JSONDecodeError: If the schema file contains invalid JSON
    """
    if schema_path is None:
        schema_path_str = os.getenv("OHSDM_SCHEMA_PATH", DEFAULT_SCHEMA_PATH_STR)
        schema_path = Path(schema_path_str)
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_json_file(file_path: str) -> Dict[str, Any]:
    """
    Load and return JSON from a file.

    Args:
        file_path: Path to the JSON file

    Returns:
        The JSON data as a dictionary

    Raises:
        FileNotFoundError: If the file does not exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File '{file_path}' not found.")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def format_validation_errors(errors: List[ValidationError]) -> List[Dict[str, str]]:
    """
    Format validation errors into a list of dictionaries.

    Args:
        errors: List of ValidationError objects from jsonschema

    Returns:
        List of dictionaries with 'message' and 'path' keys
    """
    return [
        {"message": error.message, "path": "/" + "/".join(map(str, error.path))} for error in errors
    ]


def main() -> None:
    """Main entry point for the validator CLI."""
    parser = argparse.ArgumentParser(description="Validate OHSDM JSON files against the schema")
    parser.add_argument("json_file", help="Path to the JSON file to validate")
    parser.add_argument(
        "--schema",
        help="Path to the schema file (default: schema/ohsdm.schema.v1_0.json)",
        default=None,
    )
    args = parser.parse_args()

    # Determine schema path
    schema_path = Path(args.schema) if args.schema else None

    try:
        schema = load_schema(schema_path)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        used_path = (
            schema_path
            if schema_path
            else Path(os.getenv("OHSDM_SCHEMA_PATH", DEFAULT_SCHEMA_PATH_STR))
        )
        print(f"Error: Invalid schema file '{used_path}': {e}", file=sys.stderr)
        sys.exit(1)

    validator = Draft202012Validator(schema)

    try:
        obj = load_json_file(args.json_file)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file '{args.json_file}': {e}", file=sys.stderr)
        sys.exit(1)

    errors = list(validator.iter_errors(obj))
    formatted_errors = format_validation_errors(errors)

    if not formatted_errors:
        print("OK")
        sys.exit(0)
    else:
        print("ERRORS", file=sys.stderr)
        for error in formatted_errors:
            print(f"{error['path']}: {error['message']}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
