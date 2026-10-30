"""Tests use only synthetic names and example.com email addresses."""
import csv
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from csv_lead_audit import audit_csv, main, MAX_ISSUES


class CSVAuditTests(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.TemporaryDirectory()
        self.addCleanup(self.work.cleanup)
        self.path = Path(self.work.name) / 'synthetic.csv'

    def write(self, rows, headers=('name', 'email', 'service')):
        with self.path.open('w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

    def test_two_valid_rows(self):
        self.write([['Ada', 'ada@example.com', 'Heating'], ['Bo', 'bo@example.com', 'Heating']])
        self.assertEqual(audit_csv(self.path)['accepted'], 2)

    def test_duplicate_normalization(self):
        self.write([['Ada', 'ADA@EXAMPLE.COM', 'Heating'], ['A', 'ada@example.com ', ' heating ']])
        x = audit_csv(self.path)
        self.assertEqual((x['accepted'], x['duplicates']), (1, 1))
        self.assertEqual(x['issues'][0]['code'], 'duplicate')

    def test_different_service_is_not_duplicate(self):
        self.write([['Ada', 'ada@example.com', 'Heating'], ['Ada', 'ada@example.com', 'Plumbing']])
        self.assertEqual(audit_csv(self.path)['accepted'], 2)

    def test_missing_field(self):
        self.write([['Ada', 'ada@example.com', '']])
        self.assertEqual(audit_csv(self.path)['issues'][0]['code'], 'missing_field')

    def test_invalid_email(self):
        self.write([['Ada', 'bad-address', 'Heating']])
        self.assertEqual(audit_csv(self.path)['issues'][0]['code'], 'invalid_email')

    def test_extra_csv_cell(self):
        self.write([['Ada', 'ada@example.com', 'Heating', 'unexpected']])
        self.assertEqual(audit_csv(self.path)['issues'][0]['code'], 'malformed_row')

    def test_duplicate_headers_fail(self):
        self.write([], headers=('name', 'email', 'service', 'email'))
        with self.assertRaises(ValueError):
            audit_csv(self.path)

    def test_missing_required_header_fails(self):
        self.write([], headers=('name', 'email'))
        with self.assertRaises(ValueError):
            audit_csv(self.path)

    def test_bom_header_supported(self):
        self.path.write_text('\ufeffname,email,service\nAda,ada@example.com,Heating\n', encoding='utf-8')
        self.assertEqual(audit_csv(self.path)['accepted'], 1)

    def test_no_personal_values_in_report(self):
        self.write([['Ada', 'ADA@EXAMPLE.COM', 'Heating'], ['Ada', 'ADA@EXAMPLE.COM', 'Heating']])
        report_text = json.dumps(audit_csv(self.path))
        for secret in ('Ada', 'ADA@EXAMPLE.COM', 'Heating'):
            self.assertNotIn(secret, report_text)

    def test_issue_cap(self):
        self.write([['Ada', 'bad', 'Heating']] * (MAX_ISSUES + 5))
        x = audit_csv(self.path)
        self.assertEqual(len(x['issues']), MAX_ISSUES)
        self.assertTrue(x['issues_truncated'])
        self.assertEqual(x['rejected'], MAX_ISSUES + 5)

    def test_command_exit_and_report(self):
        self.write([['Ada', 'ada@example.com', 'Heating'], ['Bo', 'broken', 'Heating']])
        output = StringIO()
        with redirect_stdout(output):
            code = main([str(self.path)])
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(output.getvalue())['rejected'], 1)

    def test_no_file_reports_generic_error(self):
        output = StringIO()
        with redirect_stdout(output):
            code = main([str(self.path)])
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(output.getvalue())['error'], 'csv_unreadable_or_invalid')


if __name__ == '__main__':
    unittest.main(verbosity=2)
