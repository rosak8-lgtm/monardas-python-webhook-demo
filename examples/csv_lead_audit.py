#!/usr/bin/env python3
"""Offline CSV lead quality audit. No API requests, writes or personal-data logging."""
import argparse
import csv
import json
from pathlib import Path

REQUIRED = ('name', 'email', 'service')
MAX_ISSUES = 25


def _clean(value):
    if not isinstance(value, str):
        return ''
    return ' '.join(value.strip().split())


def _email_ok(email):
    if len(email) > 254 or email.count('@') != 1 or any(ch.isspace() for ch in email):
        return False
    local, domain = email.split('@')
    return bool(local and domain and '.' in domain and not domain.startswith('.') and not domain.endswith('.'))


def audit_csv(path):
    """Return only counts and row-level issue codes; never include source values."""
    result = {'rows': 0, 'accepted': 0, 'duplicates': 0, 'rejected': 0, 'issues': [], 'issues_truncated': False}
    seen = set()
    with Path(path).open('r', encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        columns = reader.fieldnames
        if not columns or len(columns) != len(set(columns)) or any(not col for col in columns):
            raise ValueError('missing, empty or duplicate CSV headers')
        if any(name not in columns for name in REQUIRED):
            raise ValueError('missing required columns: name, email, service')
        for line, raw in enumerate(reader, start=2):
            result['rows'] += 1
            reason = None
            if None in raw or any(value is None for value in raw.values()):
                reason = 'malformed_row'
            else:
                values = {key: _clean(raw[key]) for key in REQUIRED}
                if any(not values[key] for key in REQUIRED):
                    reason = 'missing_field'
                elif not _email_ok(values['email']):
                    reason = 'invalid_email'
                elif any(len(values[key]) > 200 for key in REQUIRED):
                    reason = 'oversized_field'
                else:
                    fingerprint = (values['email'].casefold(), values['service'].casefold())
                    if fingerprint in seen:
                        reason = 'duplicate'
                    else:
                        seen.add(fingerprint)
            if reason == 'duplicate':
                result['duplicates'] += 1
            elif reason:
                result['rejected'] += 1
            else:
                result['accepted'] += 1
            if reason:
                if len(result['issues']) < MAX_ISSUES:
                    result['issues'].append({'row': line, 'code': reason})
                else:
                    result['issues_truncated'] = True
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description='Offline synthetic/authorized lead CSV audit; no data leaves this computer.')
    parser.add_argument('csv_path', help='Path to UTF-8 CSV (header: name,email,service)')
    args = parser.parse_args(argv)
    try:
        report = audit_csv(args.csv_path)
    except (OSError, UnicodeError, csv.Error, ValueError):
        # Never print filesystem paths or source values; generic, safe error.
        print(json.dumps({'ok': False, 'error': 'csv_unreadable_or_invalid'}))
        return 2
    print(json.dumps({'ok': report['rejected'] == 0, **report}, sort_keys=True))
    return 0 if report['rejected'] == 0 else 1


if __name__ == '__main__':
    raise SystemExit(main())
