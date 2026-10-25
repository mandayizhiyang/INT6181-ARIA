"""
Unit tests for Problem 4: MeetingRoom

Instructions:
Complete the unit test methods below using Python's unittest framework.
Your test methods must assert MULTIPLE ATTRIBUTES on the MeetingRoom object
(e.g., bookings list, total_hours_booked, free slots, utilization rate)
to verify room state and conflict management.

Running tests:
    python -m unittest test_problem4.py -v
"""
import unittest
from problem4 import MeetingRoom


class TestMeetingRoom(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.room = MeetingRoom("Conference-A", capacity=10)

    def test_initial_state_multi_attributes(self):
        """
        Verify initial state of an empty meeting room.
        """
        self.assertEqual(self.room.room_id, "Conference-A")
        self.assertEqual(self.room.capacity, 10)
        self.assertEqual(self.room.total_hours_booked, 0)
        self.assertFalse(self.room.is_maintenance)
        self.assertEqual(len(self.room.bookings), 0)
        self.assertEqual(self.room.get_utilization_rate(10), 0.0)

    def test_single_booking_multi_attributes(self):
        """
        Test making a single valid booking.
        Verify bookings list, total_hours_booked, utilization rate, and free slots.
        """
        result = self.room.book("B01", "Design Review", 10, 12, 5)
        self.assertTrue(result)
        self.assertEqual(self.room.total_hours_booked, 2)
        self.assertEqual(len(self.room.bookings), 1)
        self.assertEqual(self.room.get_utilization_rate(10), 0.2)
        # Free slots between 8 and 18 -> [(8, 10), (12, 18)]
        self.assertEqual(self.room.get_free_slots(8, 18), [(8, 10), (12, 18)])

    def test_back_to_back_meetings_allowed(self):
        """
        Test that valid consecutive / back-to-back meetings (e.g. 9-10 and 10-12)
        are permitted without raising conflict errors.
        Verify multi-attribute state after both bookings succeed.
        """
        self.assertTrue(self.room.book("B01", "Morning Sync", 9, 10, 4))
        self.assertTrue(self.room.book("B02", "Planning", 10, 12, 6))
        self.assertEqual(len(self.room.bookings), 2)
        self.assertEqual(self.room.total_hours_booked, 3)

    def test_overlapping_booking_rejected(self):
        """
        Test that overlapping bookings (e.g. 9-11 and 10-12, or completely inside 9-12 and 10-11)
        raise ValueError and leave room state unchanged.
        """
        self.room.book("B01", "Meeting 1", 9, 11, 4)
        with self.assertRaises(ValueError):
            self.room.book("B02", "Meeting 2", 10, 12, 4)
        
        # State should be unchanged
        self.assertEqual(len(self.room.bookings), 1)
        self.assertEqual(self.room.total_hours_booked, 2)

    def test_cancel_booking_updates_all_attributes(self):
        """
        Test that cancelling a booking correctly removes it from bookings,
        decrements total_hours_booked, and restores free slots.
        """
        self.room.book("B01", "Meeting 1", 9, 11, 4)
        self.room.book("B02", "Meeting 2", 13, 15, 4)
        self.assertEqual(self.room.total_hours_booked, 4)

        # Cancel B01
        self.assertTrue(self.room.cancel("B01"))
        self.assertEqual(len(self.room.bookings), 1)
        self.assertEqual(self.room.total_hours_booked, 2)
        self.assertEqual(self.room.bookings[0]["booking_id"], "B02")

    def test_capacity_and_validation_exceptions(self):
        """
        Test edge cases and exceptions:
        - Attendees exceeding capacity (ValueError)
        - Start time >= End time (ValueError)
        - Duplicate booking ID (ValueError)
        - Booking when room is under maintenance (RuntimeError)
        - Cancelling non-existent booking (KeyError)
        """
        # Capacity exceeded
        with self.assertRaises(ValueError):
            self.room.book("B01", "Big Event", 9, 10, 15)

        # Invalid time range
        with self.assertRaises(ValueError):
            self.room.book("B02", "Invalid Time", 10, 10, 5)

        # Duplicate ID
        self.room.book("B03", "Sync", 9, 10, 3)
        with self.assertRaises(ValueError):
            self.room.book("B03", "Duplicate ID Sync", 11, 12, 3)

        # Maintenance mode
        self.room.is_maintenance = True
        with self.assertRaises(RuntimeError):
            self.room.book("B04", "Maintenance Booking", 14, 15, 2)

        # Cancel non-existent booking
        with self.assertRaises(KeyError):
            self.room.cancel("NON_EXISTENT")


if __name__ == "__main__":
    unittest.main()