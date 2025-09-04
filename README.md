# OpenHealthMesh (OHSDM v1.0)

**Open Health Mesh (OpenHealthMesh)** is an open schema for unifying diverse public health intelligence streams — OSINT/event alerts, wastewater/environmental measurements, genomic surveillance, and epidemiological events — into a single, governance-aware, analytics-ready structure.

## 🌍 Why OpenHealthMesh?

Today, epidemic intelligence is fragmented:
- **WHO-EIOS / HealthMap / ProMED** → unstructured news & event feeds
- **CDC NWSS** → wastewater/environmental signals
- **GISAID / Nextstrain** → genomic sequences and clades
- **Case counts & epi reports** → spreadsheets, PDFs, siloed feeds

These cannot be easily combined into a single operational picture for pandemic prevention.

**OpenHealthMesh provides:**
- 🧩 **One envelope** for 5 resource types: `SourceDoc`, `Site`, `Measurement`, `GenomicObservation`, `EpiEvent`
- 🔒 **Governance first-class**: provenance, license, classification, retention, redactions
- 🌐 **Geospatial + temporal precision**: ISO country codes, H3 cells, time precision flags
- 📊 **Epi metrics**: attack rates, Rt, incubation periods, stratifiers (age/sex/ethnicity/occupation)
- 🧬 **Genomics integration**: lineages, mutations, sequence accessions, coverage/QC, batches
- 🧾 **Audit trails**: lifecycle, change_reason, audit_log

## 📂 What’s in This Repository

- `schema/ohsdm.schema.v1_0.json` → JSON Schema
- `data_dictionary/` → JSON + CSV with field definitions
- `summaries/` → Markdown + PDF summaries
- `codebooks/` → PII, stratifiers, metrics (LOINC/UCUM)
- `examples/` → NDJSON examples for each resource type
- `openapi/` + `.postman/` → API spec & Postman collection
- `reference_impl/` → FastAPI server + CLI validator + Dockerfile
- `docs/` → Governance, workflows, validation rules, adoption roadmap

## 🚀 Quickstart

```bash
# Clone and run the reference FastAPI app
git clone https://github.com/your-org/openeimesh.git
cd openeimesh
python3 -m venv .venv && source .venv/bin/activate
pip install -r reference_impl/requirements.txt
uvicorn reference_impl.app:app --reload
```

Check health:
```bash
curl http://localhost:8000/health
```

Validate a sample:
```bash
python reference_impl/validator.py examples/sites.ndjson
```

## 📖 Documentation

- [Governance Notes](docs/GOVERNANCE_NOTES.md)
- [Validation Rules](docs/VALIDATION_RULES.md)
- [Example Workflows](docs/EXAMPLE_WORKFLOWS.md)
- [Adoption Roadmap](docs/ADOPTION_ROADMAP.md)
- [FHIR/HL7 Crosswalk](docs/FHIR_HL7_CROSSWALK_v1_0.md)
- [Differentiation](docs/DIFFERENTIATION_v1_0.md)

## 🔗 Interoperability

- **FHIR** → `Measurement ↔ Observation`, `Site ↔ Location`, `SourceDoc ↔ DocumentReference`, `EpiEvent ↔ Condition`
- **GA4GH** → `GenomicObservation` crosswalk with Phenopackets/variants
- **CDC NWSS** → Measurement metrics aligned with LOINC/UCUM
- **WHO EIOS** → OSINT SourceDoc normalization

## 🧑‍🤝‍🧑 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

Governance: semantic versioning, schema changes via PR + review, minor backward-compatible updates in `1.x`, breaking changes in `2.0`.

## 📅 Roadmap

- Publish HL7/FHIR profiles
- Pilot with WHO/CDC partners
- Integrate GA4GH genomics extensions
- Develop validators & migration tools
- Multilingual support (labels_i18n)

## 📜 Citation

A DOI will be minted via Zenodo. For now, cite as:

> OpenHealthMesh (OHSDM v1.0): An open schema for unified epidemic intelligence.  
> https://github.com/your-org/openeimesh
