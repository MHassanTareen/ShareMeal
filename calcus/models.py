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
        
class Contribution(models.Model):
    user = models.ForeignKey(user2cal,on_delete=models.DO_NOTHING,related_name="user_make_contribution")
    amount = models.DecimalField(max_digits=100000,decimal_places=2,blank=True,null=True)
    ToBill = models.ForeignKey(bill , on_delete=models.DO_NOTHING,related_name="make_contibuation_to_bill")
    entrydate = models.DateTimeField(auto_now_add=True,editable=False)

    def __str__(self):
        return f"{self.user} make contribution  - : {self.amount}"
    
    def update_balance(self):
            """Update the balance of the user who made the contribution."""
            if self.amount:
                user = self.user
                user.total_balance -= Decimal(self.amount)
                user.save()
                return f"{user} balance updated, new balance: {user.total_balance}"
            else:
                raise ValueError("Contribution amount must be specified.")


class Recived(models.Model):
    PayedBy = models.ForeignKey(user2cal,on_delete=models.DO_NOTHING,related_name="pay_bill_to_him")
    RecivedBy = models.ForeignKey(user2cal,on_delete=models.DO_NOTHING,related_name="recided_bill_by")
    amount = models.DecimalField(max_digits=100000,decimal_places=2,blank=True,null=True)
    ToBill = models.ForeignKey(bill,on_delete=models.DO_NOTHING,blank=True, null=True,related_name="pay_back_to_bill")
    entrydate = models.DateTimeField(auto_now_add=True,editable=False)

    def __str__(self):
        return f"Payed by {self.PayedBy} - Recived by {self.RecivedBy} : {self.amount}"
    
    def update_balance(self):
        """Update the balance of the user who received the payment and the user who paid."""
        if self.amount:
            # Update the balance for the user who paid the amount
            payer = self.PayedBy
            payer.total_balance -= Decimal(self.amount)
            payer.save()

            # Update the balance for the user who received the payment
            receiver = self.RecivedBy
            receiver.total_balance += Decimal(self.amount)
            receiver.save()

            return (
                f"{payer} balance updated, new balance: {payer.total_balance}, "
                f"{receiver} balance updated, new balance: {receiver.total_balance}"
            )
        else:
            raise ValueError("Amount must be specified for the payment received.")

class Expense(models.Model):
    friend = models.ManyToManyField(user2cal, related_name='expenses')
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    


class Summary(models.Model):
    total_out = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='summaries')

    def __str__(self):
        return f"{self.category.name} - {self.total_out}"
