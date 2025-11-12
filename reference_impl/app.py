import json
import os
from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI, File, HTTPException, UploadFile
from jsonschema import Draft202012Validator, ValidationError

# Configuration
DEFAULT_SCHEMA_PATH_STR = "schema/ohsdm.schema.v1_0.json"
SCHEMA_PATH = Path(os.getenv("OHSDM_SCHEMA_PATH", DEFAULT_SCHEMA_PATH_STR))

# Initialize FastAPI app
app = FastAPI(title="OHSDM API v1.0")


def load_schema() -> Dict[str, Any]:
    """
    Load and return the OHSDM schema.

    Returns:
        The OHSDM schema as a dictionary

    Raises:
        FileNotFoundError: If the schema file is not found
        json.JSONDecodeError: If the schema file contains invalid JSON
    """
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"Schema file not found: {SCHEMA_PATH}")
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
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


# Load schema and create validator at startup
try:
    SCHEMA = load_schema()
    VALIDATOR = Draft202012Validator(SCHEMA)
except (FileNotFoundError, json.JSONDecodeError) as e:
    raise RuntimeError(f"Failed to load schema: {e}") from e


@app.get("/health")
def health() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/schema")
def schema() -> Dict[str, Any]:
    """Return the OHSDM schema."""
    return SCHEMA


@app.post("/validate")
async def validate(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Validate a JSON file against the OHSDM schema.

    Args:
        file: The JSON file to validate

    Returns:
        Dictionary with 'valid' boolean and 'errors' list

    Raises:
        HTTPException: If the file cannot be read or parsed as JSON
    """
    try:
        data = (await file.read()).decode("utf-8")
    except UnicodeDecodeError as ex:
        raise HTTPException(status_code=400, detail=f"Invalid file encoding: {ex}") from ex

    try:
        obj = json.loads(data)
    except json.JSONDecodeError as ex:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {ex}") from ex

    errors = list(VALIDATOR.iter_errors(obj))
    formatted_errors = format_validation_errors(errors)
    return {"valid": len(formatted_errors) == 0, "errors": formatted_errors}


@app.post("/submit")
async def submit(file: UploadFile = File(...)) -> Dict[str, bool]:
    """
    Submit a JSON file for validation and acceptance.

    Args:
        file: The JSON file to submit

    Returns:
        Dictionary with 'accepted' boolean

    Raises:
        HTTPException: If validation fails (422 status code)
    """
    res = await validate(file)
    if not res["valid"]:
        raise HTTPException(status_code=422, detail=res)
    return {"accepted": True}
