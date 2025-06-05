import unittest
import uuid
from hashlib import sha256

from app.config import ConfigDatabase, set_config
from app.db.db import Database
from app.pseudonym.service import PseudonymService
from tests.test_config import get_test_config


class TestService(unittest.TestCase):
    def setUp(self) -> None:
        set_config(get_test_config())

    def test_health(self) -> None:
        db = Database(ConfigDatabase(dsn="sqlite://"))
        db.generate_tables()
        service = PseudonymService(db)

        provider1 = str(uuid.uuid4())
        provider2 = str(uuid.uuid4())
        provider3 = str(uuid.uuid4())
        bsnhash1 = sha256(b"1234").hexdigest()
        bsnhash2 = sha256(b"4567").hexdigest()

        entry1 = service.register(bsnhash1, provider1)
        self.assertIsNotNone(entry1)
        self.assertEqual(entry1.hashed_bsn, bsnhash1)
        self.assertEqual(entry1.provider, provider1)

        entry2 = service.exchange(entry1.pseudonym, provider2)
        if entry2 is None:
            self.fail("Entry2 is None")
        self.assertEqual(entry2.hashed_bsn, bsnhash1)
        self.assertEqual(entry2.provider, provider2)
        self.assertNotEqual(entry2.pseudonym, entry1.pseudonym)

        entry3 = service.exchange(entry2.pseudonym, provider1)
        if entry3 is None:
            self.fail("Entry3 is None")
        self.assertEqual(entry3.hashed_bsn, bsnhash1)
        self.assertEqual(entry3.provider, provider1)
        self.assertEqual(entry3.pseudonym, entry1.pseudonym)

        entry4 = service.register(bsnhash1, provider2)
        if entry4 is None:
            self.fail("Entry4 is None")
        self.assertEqual(entry4.hashed_bsn, bsnhash1)
        self.assertEqual(entry4.provider, provider2)
        self.assertEqual(entry4.pseudonym, entry2.pseudonym)

        # Register second hash in provider3 and exchange to provider1. It should be a different pseudonym than in entry1
        entry5 = service.register(bsnhash2, provider3)
        if entry5 is None:
            self.fail("Entry5 is None")

        entry6 = service.exchange(entry5.pseudonym, provider1)
        if entry6 is None:
            self.fail("Entry6 is None")
        self.assertEqual(entry1.provider, entry6.provider)
        self.assertNotEqual(entry1.provider, entry5.provider)
        self.assertNotEqual(entry6.provider, entry5.provider)

        self.assertNotEqual(entry1.hashed_bsn, entry5.hashed_bsn)
        self.assertNotEqual(entry1.hashed_bsn, entry6.hashed_bsn)
        self.assertEqual(entry5.hashed_bsn, entry6.hashed_bsn)

        self.assertNotEqual(entry1.pseudonym, entry5.pseudonym)
        self.assertNotEqual(entry5.pseudonym, entry6.pseudonym)
        self.assertNotEqual(entry6.pseudonym, entry1.pseudonym)
