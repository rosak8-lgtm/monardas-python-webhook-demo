#!/usr/bin/env python3
"""MONARDAS lead workflow demo. Localhost-only, no outbound calls, stdlib only."""
import argparse
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

MAX_BODY = 16384
REQUIRED = ('name', 'email', 'service')

def clean(value, maxlen=200):
    if not isinstance(value, str):
        raise ValueError('fields must be strings')
    value = ' '.join(value.strip().split())
    if not value or len(value) > maxlen:
        raise ValueError('missing/oversized field')
    return value

def normalize(payload):
    if not isinstance(payload, dict):
        raise ValueError('expected JSON object')
    fields = {k: clean(payload.get(k)) for k in REQUIRED}
    fields['email'] = fields['email'].lower()
    if fields['email'].count('@') != 1 or '.' not in fields['email'].split('@')[1]:
        raise ValueError('invalid email')
    fields['message'] = clean(payload.get('message', ''), 3000) if payload.get('message') else ''
    return fields

def fingerprint(lead):
    return hashlib.sha256((lead['email'] + '\0' + lead['service'].lower()).encode()).hexdigest()

def init_db(db):
    db.execute('PRAGMA busy_timeout=3000')
    db.execute('CREATE TABLE IF NOT EXISTS leads (fingerprint TEXT PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL, service TEXT NOT NULL, message TEXT NOT NULL, created_at TEXT NOT NULL)')
    db.commit()

def store(db, payload):
    lead = normalize(payload)
    key = fingerprint(lead)
    with db:
        inserted = db.execute('INSERT OR IGNORE INTO leads VALUES (?,?,?,?,?,?)', (key, lead['name'], lead['email'], lead['service'], lead['message'], datetime.now(timezone.utc).isoformat())).rowcount == 1
    return {'accepted': True, 'duplicate': not inserted, 'reference': key[:12]}

def handler_factory(db_path):
    class Handler(BaseHTTPRequestHandler):
        def send_json(self, status, payload):
            body = json.dumps(payload).encode()
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        def do_GET(self):
            if urlsplit(self.path).path != '/health':
                return self.send_json(404, {'error': 'not found'})
            self.send_json(200, {'status': 'ok', 'demo': True})
        def do_POST(self):
            if urlsplit(self.path).path != '/webhooks/lead':
                return self.send_json(404, {'error': 'not found'})
            try:
                length = int(self.headers.get('Content-Length', '-1'))
                if length < 1 or length > MAX_BODY:
                    return self.send_json(413, {'error': 'body size invalid'})
                raw = self.rfile.read(length)
                payload = json.loads(raw)
                with sqlite3.connect(db_path) as db:
                    init_db(db)
                    result = store(db, payload)
                self.send_json(200, result)
            except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                self.send_json(400, {'error': 'invalid input'})
            except sqlite3.Error:
                self.send_json(500, {'error': 'storage error'})
        def log_message(self, fmt, *args):
            return  # Avoid request PII in logs
    return Handler

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', default='demo_leads.sqlite')
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    if not (1024 <= args.port <= 65535):
        raise SystemExit('invalid port')
    db_path = str(Path(args.db).resolve())
    with sqlite3.connect(db_path) as db:
        init_db(db)
    server = ThreadingHTTPServer(('127.0.0.1', args.port), handler_factory(db_path))
    print(f'Demo listening on http://127.0.0.1:{args.port}', flush=True)
    server.serve_forever()

if __name__ == '__main__':
    main()
