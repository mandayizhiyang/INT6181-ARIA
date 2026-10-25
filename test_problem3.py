"""
Unit tests for Problem 3: Order

Instructions:
Complete the unit test methods below using Python's unittest framework.
Your test methods must assert MULTIPLE ATTRIBUTES on the Order object
(e.g., subtotal, discount_amount, tax_amount, shipping_fee, final_total, status)
to verify state consistency under various conditions.

Running tests:
    python -m unittest test_problem3.py -v
"""
import unittest
from problem3 import Order


class TestOrder(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.regular_order = Order("ORD100", customer_tier="regular")
        self.silver_order = Order("ORD200", customer_tier="silver")
        self.gold_order = Order("ORD300", customer_tier="gold")

    # TODO: develop 5 test methods for Order class
    def test_add_item_and_financial_recalculation(self):
        """
        Test adding items recalculates subtotal, tax (excluding grocery), shipping fee, and final total.
        """
        # Add general item $40 (shipping applies since < $50)
        self.regular_order.add_item("Book", 40.0, 1, category="general")
        self.assertEqual(self.regular_order.subtotal, 40.0)
        self.assertEqual(self.regular_order.discount_amount, 0.0)
        self.assertEqual(self.regular_order.shipping_fee, 5.99)
        self.assertEqual(self.regular_order.tax_amount, 3.20)  # 40 * 0.08
        self.assertEqual(self.regular_order.final_total, 49.19)  # 40 + 3.20 + 5.99

        # Add grocery item $20 (tax-exempt) -> Total net subtotal $60 >= $50 -> Free shipping
        self.regular_order.add_item("Apple", 20.0, 1, category="grocery")
        self.assertEqual(self.regular_order.subtotal, 60.0)
        self.assertEqual(self.regular_order.shipping_fee, 0.0)
        self.assertEqual(self.regular_order.tax_amount, 3.20)  # Tax stays 3.20 (only on Book)
        self.assertEqual(self.regular_order.final_total, 63.20)

    def test_membership_tier_and_coupon_discounts(self):
        """
        Test membership discounts (Gold = 10%) and coupon application (SAVE10 = 10% on remaining).
        """
        self.gold_order.add_item("Laptop Sleeve", 100.0, 1, category="electronics")
        # Subtotal: 100. Tier discount (10%): 10.0
        self.assertEqual(self.gold_order.discount_amount, 10.0)

        # Apply coupon SAVE10 -> 10% off remaining 90.0 = 9.0 -> Total discount = 19.0
        self.gold_order.apply_coupon("SAVE10")
        self.assertEqual(self.gold_order.discount_amount, 19.0)
        self.assertEqual(self.gold_order.subtotal, 100.0)
        # Net subtotal = 81.0 -> Free shipping (>= 50)
        self.assertEqual(self.gold_order.shipping_fee, 0.0)
        self.assertEqual(self.gold_order.tax_amount, 6.48)  # 81 * 0.08
        self.assertEqual(self.gold_order.final_total, 87.48)

    def test_remove_item_updates_all_totals(self):
        """
        Test removing items updates quantity, subtotal, tax, and shipping status.
        """
        self.silver_order.add_item("Shirt", 30.0, 2, category="general")  # Subtotal 60.0
        self.assertEqual(self.silver_order.shipping_fee, 0.0)

        # Remove 1 shirt -> Subtotal 30.0 (< 50 threshold) -> Standard shipping charged
        self.silver_order.remove_item("Shirt", 1)
        self.assertEqual(self.silver_order.items["Shirt"]["quantity"], 1)
        self.assertEqual(self.silver_order.subtotal, 30.0)
        self.assertEqual(self.silver_order.shipping_fee, 5.99)

    def test_checkout_and_status_restrictions(self):
        """
        Test status transition to PAID on checkout, and ensure non-PENDING orders reject modifications.
        """
        self.regular_order.add_item("Headphones", 50.0, 1)
        self.assertTrue(self.regular_order.checkout())
        self.assertEqual(self.regular_order.status, "PAID")

        # Modifying a PAID order must raise RuntimeError
        with self.assertRaises(RuntimeError):
            self.regular_order.add_item("Cable", 10.0, 1)

        with self.assertRaises(RuntimeError):
            self.regular_order.apply_coupon("FLAT15")

    def test_invalid_operations_and_exceptions(self):
        """
        Test edge cases like invalid tier, negative price/quantity, bad coupon, and empty checkout.
        """
        with self.assertRaises(ValueError):
            Order("ORD999", customer_tier="diamond")

        with self.assertRaises(ValueError):
            self.regular_order.add_item("Item", -5.0, 1)

        with self.assertRaises(ValueError):
            self.regular_order.apply_coupon("INVALID_CODE")

        # Checkout empty order raises ValueError
        with self.assertRaises(ValueError):
            self.regular_order.checkout()


if __name__ == "__main__":
    unittest.main() 




