# MONARDAS — Small Paid Python / Data QA Projects

**Contact for employer-direct projects:** rosak8@gmail.com

**Location:** Kutaisi, Georgia (UTC+4). Written, asynchronous communication preferred. Basic English. Remote work only.

These are **proposed paid service scopes**, not evidence of completed commercial engagements. A client's actual scope, price, dates and payment milestones must be agreed in writing before work begins.

## Pilot A — CSV / JSON Data Quality Report

**Proposed starter fixed price: $75**, subject to reviewing a sanitized sample and agreeing on the scope.

**Client provides:** one documented CSV or JSON input format; up to three validation rules beyond required-field checks; synthetic or legally shared test data; expected output definition.

**What I deliver:** a Python 3 standard-library CLI script for a single input format; count of accepted, invalid and duplicate records; reproducible issue-code report without printing personal fields; automated tests; setup and run instructions; one correction pass for an agreed acceptance-test failure.

**Acceptance:** script processes the supplied sample, reports the agreed fields/rules, produces documented status codes, and included tests pass in a clean Python 3 environment.

**Independent technical example:** [offline CSV auditor](examples/csv_lead_audit.py), [13 tests](examples/test_csv_lead_audit.py), and [synthetic sample](examples/sample_leads.csv).

**Out of scope:** arbitrary large file throughput guarantees, third-party API access, production deployment, personal-data hosting, data-enrichment scraping, general-purpose email verification, and unapproved use of sensitive datasets.

## Pilot B — Python Webhook / API Validation Tests

**Proposed starter fixed price: $125**, subject to reviewing the implementation, inputs, and acceptance criteria.

**Client provides:** one isolated Python handler or synthetic HTTP/JSON interface, a reproducible bug or test requirement, expected behavior, a safe local test environment, and permission to review the code.

**What I deliver:** targeted failure-case/replay/duplicate tests for one agreed handler; small scoped code correction if feasible without infrastructure changes; a test report explaining what passes, fails or remains unverified; README/run instructions; one acceptance-related correction pass.

**Acceptance:** specified tests reproduce the original defect when possible, documented tests pass after the agreed change, and unresolved limitations are disclosed.

**Independent technical example:** [local webhook handler](lead_demo.py) and [six associated unit tests](test_lead_demo.py).

**Out of scope:** internet-facing deployment, live CRM/WhatsApp/n8n production integration, authentication and privacy guarantees, ongoing monitoring, open-ended incident response, third-party secrets or database credentials.

## Collaboration / safety

1. Before quoting a binding price, send a short task description, sanitized input/output, acceptance tests, deadline, and environment constraints.
2. Agree in writing on the fixed fee, deliverables, milestones, refund/dispute rules and usage rights.
3. Start only once funding is verified through the selected platform's escrow or other mutually agreed protected payment mechanism.
4. Do not provide real customer data, live tokens, account passwords or privileged access during an initial unpaid discussion. Prefer synthetic data.
5. Work and communicate **inside Upwork, Contra, Freelancer or another marketplace** if the customer originated there. Do not move such conversations or payments off-platform.

**Truthful experience statement:** MONARDAS currently showcases independent reproducible technical samples. These are **not** paid-client references or deployed production systems.
