"""MONARDAS demo: safe lead webhook processing (standard library only)."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Lock
import json, re

seen = set()
lock = Lock()


def process(payload):
    if not isinstance(payload, dict):
        return 400, {"error": "Expected JSON object"}
    lead_id = payload.get("lead_id")
    email = payload.get("email")
    if not isinstance(lead_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", lead_id):
        return 422, {"error": "Invalid lead_id"}
    if not isinstance(email, str) or len(email) > 254 or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
        return 422, {"error": "Invalid email"}
    with lock:
        if lead_id in seen:
            return 200, {"status": "duplicate", "lead_id": lead_id}
        seen.add(lead_id)
    return 201, {"status": "accepted", "lead_id": lead_id, "email": email.strip().lower()}


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/lead":
            return self.respond(404, {"error": "Not found"})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not (0 < length <= 8192):
                return self.respond(413, {"error": "Invalid body size"})
            payload = json.loads(self.rfile.read(length))
        except (ValueError, json.JSONDecodeError):
            return self.respond(400, {"error": "Invalid JSON"})
        status, body = process(payload)
        self.respond(status, body)

    def respond(self, status, body):
        data = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    print("Demo only: http://127.0.0.1:8765/lead")
    ThreadingHTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
