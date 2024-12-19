from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import bill, user2cal, Category
from django.views import View
from django import forms
from .form import BillForm, UserForm

# Form for creating a new bill
class BillForm(forms.ModelForm):
    class Meta:
        model = bill
        fields = ['name', 'category', 'paidby', 'billed_amount', 'note', 'dateofBill']
        widgets = {
            'dateofBill': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'multiple': True})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['paidby'].widget.attrs.update({'class': 'form-control'})
        self.fields['billed_amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['note'].widget.attrs.update({'class': 'form-control'})
        self.fields['dateofBill'].widget.attrs.update({'class': 'form-control'})


# List all bills
class BillListView(View):
    def get(self, request):
        bills = bill.objects.all()
        return render(request, 'bills_list.html', {'bills': bills})


# # Create a new bill
class BillCreateView(View):
    template_name = 'bill_create.html'

    def get(self, request):
        form = BillForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = BillForm(request.POST)
        if form.is_valid():
            new_bill = form.save()
            new_bill.process_bill()  # Process the bill to calculate balances
            return redirect('bills-list')  # Replace with the correct name of your bills list view
        return render(request, self.template_name, {'form': form})

# View user balances
class UserBalanceView(View):
    def get(self, request):
        users = user2cal.objects.all()
        return render(request, 'user_balances.html', {'users': users})
    
class BillDetailView(View):
    def get(self, request, uuid):
        bill_obj = get_object_or_404(bill, uuid=uuid)
        users_involved = bill_obj.name.all()
        paid_user_balance = bill_obj.billed_amount - bill_obj.per_head_amount if bill_obj.per_head_amount else 0

        context = {
            'bill': bill_obj,
            'users_involved': users_involved,
            'paid_user_balance': paid_user_balance,  # Add this value
        }
        return render(request, 'bill_detail.html', context)

# View for adding a new user
class UserCreateView(View):
    def get(self, request):
        form = UserForm()
        return render(request, 'user_create.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            next_url = request.GET.get('next')  # Retrieve the 'next' parameter from the query string
            if next_url:
                return redirect(next_url)  # Redirect to the previous page
            return redirect('bills-list')  # Fallback to the user list page
        return render(request, 'user_create.html', {'form': form})

# View for user details
class UserDetailView(View):
    def get(self, request, pk):
        user = get_object_or_404(user2cal, pk=pk)
        return render(request, 'user_detail.html', {'user': user})
