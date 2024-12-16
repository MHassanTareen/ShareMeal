import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # Replace 'config.settings' with your project's settings module
django.setup()

# Use absolute imports for models
from django.test import TestCase
from .models import user2cal, bill, Category
from datetime import date

class BillModelTestCase(TestCase):
    def setUp(self):
        """Set up the data for testing."""
        # Create users
        self.user1 = user2cal.objects.create(name="Ali Aqdas", total_balance=0)
        self.user2 = user2cal.objects.create(name="Muhammad Hassan Khan", total_balance=0)
        self.user3 = user2cal.objects.create(name="Zohair", total_balance=0)
        self.user4 = user2cal.objects.create(name="Muhammad Ali", total_balance=0)

        # Create a category
        self.category = Category.objects.create(name="Travel")

        # Create a bill
        self.bill = bill.objects.create(
            category=self.category,
            paidby=self.user3,  # Assume Zohair paid the bill
            billed_amount=1600.00,
            dateofBill=date.today(),
        )
        # Add users to the bill
        self.bill.name.add(self.user1, self.user2, self.user3, self.user4)

    def test_calculate_per_head(self):
        """Test the per-head calculation."""
        self.bill.calculate_per_head()
        self.assertEqual(self.bill.per_head_amount, 400.00)  # 1600 divided by 4 users

    def test_update_balances(self):
        """Test the update_balances method."""
        self.bill.process_bill()
        
        self.user1.refresh_from_db()
        self.user2.refresh_from_db()
        self.user3.refresh_from_db()
        self.user4.refresh_from_db()

        self.assertEqual(self.user1.total_balance, 400.00)
        self.assertEqual(self.user2.total_balance, 400.00)
        self.assertEqual(self.user3.total_balance, -1200.00)  # Paid the bill
        self.assertEqual(self.user4.total_balance, 400.00)

try:
    # Fetch the bill with id=1
    bills = bill.objects.get(id=1)
    print(f"Bill Details: {bills}")

    # Fetch all users and print their balances
    allUsers = user2cal.objects.all()
    for user in allUsers:
        print(f"{user.name}: {user.total_balance}")
except bill.DoesNotExist:
    print("No bill with id=1 found.")
except Exception as e:
    print(f"An error occurred: {e}")