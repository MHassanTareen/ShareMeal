from django.db import models
import uuid
from decimal import Decimal

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name


class user2cal(models.Model):
    name = models.CharField(max_length=100, unique=True)
    total_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

class bill(models.Model):
    name = models.ManyToManyField(user2cal,related_name="bill2fnd")
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='bill_cate')
    paidby = models.ForeignKey(user2cal, on_delete=models.DO_NOTHING,related_name="paybyfnd")
    billed_amount = models.DecimalField(max_digits=100000,decimal_places=2,blank=True,null=True)
    per_head_amount = models.DecimalField(max_digits=100000,decimal_places=2,blank=True,null=True)
    note = models.CharField(null=True,blank=True,max_length=250)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False,unique=True)
    dateofBill = models.DateField( auto_now=False, auto_now_add=False)
    entrydate = models.DateTimeField(auto_now_add=True,editable=False)

    
    def __str__(self):
        return f"Bill {self.uuid} - {self.category.name}: {self.billed_amount}"

    def calculate_per_head(self):
        """Calculate the per-head cost by dividing the bill amount among all users."""
        users_in_bill = self.name.count()
        if users_in_bill > 0:
            self.per_head_amount = Decimal(self.billed_amount) / Decimal(users_in_bill)
            self.save()
        else:
            raise ValueError("No users in this bill to calculate per-head cost.")

    def update_balances(self):
        """Update balances for all users involved in the bill."""
        if self.per_head_amount is None:
            self.calculate_per_head()

        # Deduct per-head cost for all users except the one who paid
        for user in self.name.all():
            if user == self.paidby:
                user.total_balance -= Decimal(self.billed_amount) - self.per_head_amount
            else:
                user.total_balance += self.per_head_amount
            user.save()

    def process_bill(self):
        """Run the entire bill processing logic."""
        self.calculate_per_head()
        self.update_balances()

class Expense(models.Model):
    friend = models.ManyToManyField(user2cal, related_name='expenses')
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    


class Summary(models.Model):
    total_out = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='summaries')

    def __str__(self):
        return f"{self.category.name} - {self.total_out}"
