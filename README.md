# MONARDAS — Lead Webhook & Duplicate Protection (technical demo)

**Status:** self-contained local demonstration, not production software or a completed client engagement.

Python 3 standard library only. Receives JSON leads at `POST /webhooks/lead`, validates required fields, normalizes email/name/service, deduplicates by normalized email + service, stores leads in SQLite, and returns an idempotent result. Includes `/health` and six unit tests. No third-party APIs, no email sending, no CRM sync, no AI scoring, and **no n8n runtime**; these are integration extension points, not claimed features.

## Run tests

```bash
python3 -B -m unittest -v test_lead_demo.py
```

## Try locally

```bash
python3 -B lead_demo.py --db demo_leads.sqlite --port 8765
```

In another terminal:

```bash
curl -sS -X POST http://127.0.0.1:8765/webhooks/lead \
  -H 'Content-Type: application/json' \
  -d '{"name":"Ada","email":"ada@example.com","service":"automation","message":"Need an API integration"}'
```

Repeat the same request: `duplicate` changes from `false` to `true`. Stop with Ctrl+C.

## Design limitations

- Binds only to `127.0.0.1`; not deployed publicly.
- Inadequate for public production exposure without authentication, rate limits, TLS termination and retention/privacy controls.
- Deduplication key is scoped to normalized email + service: legitimate repeat inquiries may be classified as duplicates.
- SQLite is suitable for a local proof of concept, not inherently horizontally scalable.
- No integration with MONARDAS production databases, HVAC, Gmail, or scheduled jobs.
- Test results should be independently reproduced before sharing as evidence.

## Honest portfolio description

> Built a local Python HTTP webhook demo with JSON input validation, SQLite persistence, duplicate detection and unit tests. This is an independent engineering sample, not prior paid client work. Available to extend to n8n and a CRM after defining acceptance criteria.


## Small paid engineering pilots

MONARDAS is available to discuss **small, paid, clearly scoped Python/API tasks**. The repository above is a technical demo, not evidence of production deployments or prior paid client work.

Possible first projects include:

- Validate incoming HTTP/JSON payloads and document failure cases.
- Add or improve Python unit tests for an existing API/webhook handler.
- Diagnose duplicate records, normalize data, or prototype safe SQLite persistence.
- Build a small, reproducible data-mapping script when sample input/output and access terms are provided.

**Before any engagement:** agree in writing on exact deliverables, acceptance tests, schedule, price, access/security limitations, and handover. Production deployment, CRM/n8n integrations, and data-security guarantees are **not** part of this demo and would require separate review and scope.

For employer-direct inquiries: **rosak8@gmail.com** (subject: `MONARDAS — paid Python/API pilot`). If you found this work through Upwork or another hiring marketplace, **use that platform's approved messaging and contracting process instead of contacting off-platform**.
