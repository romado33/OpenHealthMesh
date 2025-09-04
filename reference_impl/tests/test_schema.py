import json
from jsonschema import Draft202012Validator

def test_schema_is_valid():
    s=json.load(open('schema/ohsdm.schema.v1_0.json'))
    Draft202012Validator.check_schema(s)
