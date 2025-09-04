from fastapi import FastAPI, UploadFile, File, HTTPException
import json
from jsonschema import Draft202012Validator

app = FastAPI(title="OHSDM API v1.0")
SCHEMA = json.load(open("schema/ohsdm.schema.v1_0.json"))
V = Draft202012Validator(SCHEMA)

@app.get("/health")
def health(): return {"status":"ok"}

@app.get("/schema")
def schema(): return SCHEMA

@app.post("/validate")
async def validate(file: UploadFile = File(...)):
    data = (await file.read()).decode("utf-8")
    try:
        obj = json.loads(data)
    except Exception as ex:
        raise HTTPException(400, f"Invalid JSON: {ex}")
    errors = [{"message": e.message, "path": "/" + "/".join(map(str,e.path))} for e in V.iter_errors(obj)]
    return {"valid": not errors, "errors": errors}

@app.post("/submit")
async def submit(file: UploadFile = File(...)):
    res = await validate(file)
    if not res["valid"]:
        raise HTTPException(422, res)
    return {"accepted": True}
