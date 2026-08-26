import unittest
from unittest.mock import patch

from marketplace_assignment import assign, bucket_for


class MarketplaceAssignmentTest(unittest.TestCase):
    def test_same_user_keeps_the_same_variant(self):
        with patch("marketplace_assignment.infrai.flags.get_value", return_value={"default_value": 50}):
            first = assign("user-42")
            second = assign("user-42")
        self.assertEqual(first, second)
        self.assertIn(first["variant"], {"control", "treatment"})

    def test_bucket_is_in_range(self):
        self.assertGreaterEqual(bucket_for("user-42", "marketplace-checkout"), 0)
        self.assertLess(bucket_for("user-42", "marketplace-checkout"), 100)


if __name__ == "__main__":
    unittest.main()
