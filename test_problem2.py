"""
Unit tests for Problem 2: BankAccount

Instructions:
Complete the unit test methods below using Python's unittest framework.
Your test methods must assert MULTIPLE ATTRIBUTES on the BankAccount object
(e.g., balance, status, transaction_history, summary) to verify state consistency.

Running tests:
    python -m unittest test_problem2.py -v
"""
import unittest
from problem2 import BankAccount


class TestBankAccount(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.account_empty = BankAccount("ACC001", "Alice", initial_balance=0.0, overdraft_limit=100.0)
        self.account_funded = BankAccount("ACC002", "Bob", initial_balance=200.0, overdraft_limit=50.0)

    def test_initial_state_multi_attributes(self):
        """
        Verify that a newly created account initializes all attributes correctly.
        Check balance, owner, status, overdraft_limit, transaction_history, and summary.
        """
       # Test empty account
        self.assertEqual(self.account_empty.account_id, "ACC001")
        self.assertEqual(self.account_empty.owner, "Alice")
        self.assertEqual(self.account_empty.balance, 0.0)
        self.assertEqual(self.account_empty.overdraft_limit, 100.0)
        self.assertEqual(self.account_empty.status, "ACTIVE")
        self.assertEqual(len(self.account_empty.transaction_history), 0)

        # Test funded account
        self.assertEqual(self.account_funded.account_id, "ACC002")
        self.assertEqual(self.account_funded.owner, "Bob")
        self.assertEqual(self.account_funded.balance, 200.0)
        self.assertEqual(self.account_funded.overdraft_limit, 50.0)
        self.assertEqual(self.account_funded.status, "ACTIVE")
        self.assertEqual(len(self.account_funded.transaction_history), 1)
        
        summary = self.account_funded.get_summary()
        self.assertEqual(summary["balance"], 200.0)
        self.assertEqual(summary["transaction_count"], 1)

    def test_deposit_updates_multiple_attributes(self):
        """
        Test that deposit correctly updates balance, transaction_history, and summary.
        """
        result = self.account_empty.deposit(150.0)
        self.assertTrue(result)
        self.assertEqual(self.account_empty.balance, 150.0)
        self.assertEqual(len(self.account_empty.transaction_history), 1)
        self.assertEqual(self.account_empty.transaction_history[0]["type"], "DEPOSIT")
        self.assertEqual(self.account_empty.get_summary()["balance"], 150.0)

    def test_withdrawal_within_balance_multi_attributes(self):
        """
        Test withdrawal when sufficient positive balance exists.
        """
        result = self.account_funded.withdraw(50.0, fee=2.50)
        self.assertTrue(result)
        self.assertEqual(self.account_funded.balance, 147.50)
        self.assertEqual(self.account_funded.status, "ACTIVE")
        self.assertEqual(len(self.account_funded.transaction_history), 2)

    def test_overdraft_withdrawal_and_status_transition(self):
        """
        Test withdrawal that uses overdraft protection (balance becomes negative but >= -overdraft_limit).
        """
        result = self.account_empty.withdraw(50.0)
        self.assertTrue(result)
        self.assertEqual(self.account_empty.balance, -50.0)
        self.assertEqual(self.account_empty.status, "OVERDRAWN")

    def test_deposit_recovering_from_overdrawn_status(self):
        """
        Test that depositing enough money to bring balance >= 0 transitions status from OVERDRAWN to ACTIVE.
        """
        self.account_empty.withdraw(50.0)
        self.assertEqual(self.account_empty.status, "OVERDRAWN")
        
        self.account_empty.deposit(100.0)
        self.assertEqual(self.account_empty.balance, 50.0)
        self.assertEqual(self.account_empty.status, "ACTIVE")

    def test_transfer_between_accounts_multi_attributes(self):
        """
        Test fund transfer between two accounts.
        """
        result = self.account_funded.transfer_to(self.account_empty, 50.0, transfer_fee=5.0)
        self.assertTrue(result)
        self.assertEqual(self.account_funded.balance, 145.0)  # 200 - 50 - 5
        self.assertEqual(self.account_empty.balance, 50.0)

    def test_frozen_account_restrictions(self):
        """
        Test that a FROZEN account rejects deposits, withdrawals, and transfers with RuntimeError.
        """
        self.account_funded.freeze()
        self.assertEqual(self.account_funded.status, "FROZEN")

        with self.assertRaises(RuntimeError):
            self.account_funded.deposit(50.0)

        with self.assertRaises(RuntimeError):
            self.account_funded.withdraw(50.0)

        with self.assertRaises(RuntimeError):
            self.account_funded.transfer_to(self.account_empty, 50.0)

    def test_invalid_operations_raise_exceptions(self):
        """
        Test exception handling
        """
        # Negative initial balance
        with self.assertRaises(ValueError):
            BankAccount("ACC003", "Charlie", initial_balance=-10.0)

        # Invalid deposit
        with self.assertRaises(ValueError):
            self.account_funded.deposit(-50.0)

        # Exceed overdraft limit
        with self.assertRaises(ValueError):
            self.account_empty.withdraw(200.0)  # Limit is 100

        # Transfer to invalid target
        with self.assertRaises(TypeError):
            self.account_funded.transfer_to("not_a_bank_account", 50.0)


if __name__ == "__main__":
    unittest.main()