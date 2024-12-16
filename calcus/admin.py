from django.contrib import admin
from .models import Category,user2cal,bill,Expense,Summary
# Register your models here.
admin.site.register(Category)
admin.site.register(user2cal)
admin.site.register(bill)
admin.site.register(Expense)
admin.site.register(Summary)