from django import forms
from .models import College, Course, Batch

class BatchFilterForm(forms.Form):
    college = forms.ModelChoiceField(queryset=College.objects.filter(is_active=True), widget=forms.Select(attrs={"class": "form-control"}))
    course = forms.ModelChoiceField(queryset=Course.objects.filter(is_active=True), widget=forms.Select(attrs={"class": "form-control"}))
    batch = forms.ModelChoiceField(queryset=Batch.objects.filter(is_active=True), widget=forms.Select(attrs={"class": "form-control"})) 
