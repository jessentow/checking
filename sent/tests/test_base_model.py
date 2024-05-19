#!/usr/bin/python3
"""Define class TestBase class"""
import unittest
from time import sleep
from datetime import datetime
from models.base_model import BaseModel


class TestBase(unittest.TestCase):
    """Define unittests for TestBase calss."""

    def test_unique_id(self):
        """Check for id uniquenti."""
        b1 = BaseModel()
        b2 = BaseModel()
        self.assertNotEqual(b1.id, b2.id)

    def test_id_type(self):
        """Check for id type."""
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_type(self):
        """Check for created_at type."""
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_type(self):
        """Check for updated_at type."""
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_save(self):
        """Check for save method."""
        self.assertTrue(hasattr(BaseModel, "save"))
        old = BaseModel().updated_at
        sleep(0.05)
        BaseModel().save()
        self.assertLess(old, BaseModel().updated_at)

    def test_str(self):
        """Check for save method."""
        dt = datetime.today()
        dt_repr = repr(dt)
        bm = BaseModel()
        bm.id = "123"
        bm.created_at = bm.updated_at = dt
        bmstr = bm.__str__()
        self.assertIn("[BaseModel] (123)", bmstr)
        self.assertIn("'id': '123'", bmstr)
        self.assertIn("'created_at': " + dt_repr, bmstr)
        self.assertIn("'updated_at': " + dt_repr, bmstr)


if __name__ == '__main__':
    unittest.main()
