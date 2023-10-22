# In attendance/forms.py
from django import forms

class DateSelectionForm(forms.Form):
    selected_date = forms.DateField(widget=forms.SelectDateWidget)
