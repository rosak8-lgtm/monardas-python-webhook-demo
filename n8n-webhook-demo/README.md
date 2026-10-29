# MONARDAS — Importable n8n webhook validation demo

Independent n8n workflow JSON, **not yet tested inside a live n8n runtime**. Includes POST Webhook, JavaScript Code validation and Respond to Webhook. No credentials, external service calls, emails, or storage.

## Import and test

1. Import `workflow.json` from file into your own n8n instance and inspect the nodes.
2. Enable the Webhook **Test URL** and start listening. Confirm node compatibility.
3. POST JSON: `{"email":"test@example.com","request_id":"demo_001"}`.
4. Expected JSON: `{"ok":true,"request_id":"demo_001","email":"test@example.com","status":"validated"}`.
5. Missing ID or invalid email should yield `ok:false` with `errors`.

## Limitations

Static JSON and graph checks passed offline, but **no n8n runtime test is claimed**. This demonstration uses HTTP 200 even when validation fails; production should return an appropriate 4xx status. There is no persistent duplicate protection, authentication, rate limiting, retry queue, CRM or email integration. Not a client delivery or completed paid contract.

Direct inquiries: rosak8@gmail.com. If a lead comes from a freelance marketplace, use its approved channels and contract rules.
