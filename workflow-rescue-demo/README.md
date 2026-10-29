# MONARDAS Workflow Rescue Demo

Standalone **engineering demonstration**, not a delivered client project or production service.

This Python 3 standard-library demo implements `POST /lead` with input validation, single-process in-memory duplicate suppression and JSON responses. Includes five automated unit tests.

## Run locally

```sh
cd workflow-rescue-demo
python3 -B -m unittest -v test_demo.py
python3 -B webhook_demo.py
```

From a second terminal:

```sh
curl -i -X POST http://127.0.0.1:8765/lead -H 'Content-Type: application/json' -d '{"lead_id":"demo-001","email":"person@example.com"}'
```

## Limitations

No authentication, persistent deduplication, external CRM or email sending, rate limits, replay protection after restart, distributed locking or retry queue. Localhost-only server. No n8n runtime integration and no claims of previous paid client deployment. Production work requires separate scoping and security review.

## MONARDAS paid pilot

Workflow Rescue Sprint: review and fix one clearly scoped Python/webhook/API automation defect, add agreed tests, and provide handover notes. Indicative small milestone **USD $150–300**, subject to requirements and confirmed access.

Contact for *direct* inquiries: rosak8@gmail.com. If work originates on Upwork or another marketplace, keep communication and contracts on that platform in accordance with its rules.
