import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from lead_demo import init_db, store, normalize, fingerprint

class LeadTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = sqlite3.connect(str(Path(self.temp.name) / 'test.sqlite'))
        init_db(self.db)
        self.payload = {'name':'Ada', 'email':'ADA@EXAMPLE.COM', 'service':'HVAC repair', 'message':'Please call'}
    def tearDown(self):
        self.db.close()
        self.temp.cleanup()
    def test_first_lead_accepted(self):
        self.assertEqual(store(self.db, self.payload)['duplicate'], False)
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM leads').fetchone()[0], 1)
    def test_duplicate_is_not_inserted(self):
        store(self.db, self.payload)
        self.assertTrue(store(self.db, dict(self.payload, email=' ada@example.com '))['duplicate'])
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM leads').fetchone()[0], 1)
    def test_invalid_email_rejected(self):
        with self.assertRaises(ValueError):
            store(self.db, dict(self.payload, email='invalid'))
    def test_missing_required_field_rejected(self):
        with self.assertRaises(ValueError):
            store(self.db, {'email':'a@b.com', 'name':'A'})
    def test_different_service_new_lead(self):
        store(self.db, self.payload)
        self.assertFalse(store(self.db, dict(self.payload, service='Plumbing'))['duplicate'])
    def test_no_sensitive_content_in_receipt(self):
        result = store(self.db, self.payload)
        self.assertNotIn('email', result)
        self.assertNotIn('name', result)

if __name__ == '__main__':
    unittest.main(verbosity=2)
