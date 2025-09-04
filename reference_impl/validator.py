#!/usr/bin/env python3
import sys, json
from jsonschema import Draft202012Validator

S=json.load(open('schema/ohsdm.schema.v1_0.json'))
V=Draft202012Validator(S)

def main():
    if len(sys.argv) < 2:
        print("Usage: validator.py <json_file>"); sys.exit(1)
    obj=json.load(open(sys.argv[1]))
    errors=[{"message": e.message, "path": "/" + "/".join(map(str,e.path))} for e in V.iter_errors(obj)]
    print("OK" if not errors else "ERRORS\n" + "\n".join(f"{e['path']}: {e['message']}" for e in errors))

if __name__ == "__main__":
    main()
