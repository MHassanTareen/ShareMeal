from django import forms
from .models import bill, user2cal

class BillForm(forms.ModelForm):
    class Meta:
        model = bill
        fields = ['name', 'category', 'paidby', 'billed_amount', 'note', 'dateofBill']

    name = forms.ModelMultipleChoiceField(
        queryset=user2cal.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
class UserForm(forms.ModelForm):
    class Meta:
        model = user2cal
        fields = ['name', 'total_balance']