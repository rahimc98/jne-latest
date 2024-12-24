import django_filters
from django.db import models

from .models import Batch, ExamStudentMark
import django_filters
from .models import ExamStudentMark

class ExamStudentMarkFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method="filter_name", label="Student Name")
    reg_no = django_filters.CharFilter(method="filter_reg_no", label="Register Number")
    batch = django_filters.ModelChoiceFilter(
        queryset=Batch.objects.filter(is_active=True),  # Assuming you have a Batch model
        method="filter_batch",
        label="Batch"
    )
    def filter_name(self, queryset, name, value):
        if value:
            return queryset.filter(student__student__name__icontains=value)
        return queryset
    
    def filter_batch(self, queryset, name, value):
        
        if value:
            return queryset.filter(subject__batch__id__exact=value.pk)
        return queryset
    
    def filter_reg_no(self, queryset, name, value):
        if value:
            return queryset.filter(student__student__reg_no__icontains=value)
        return queryset
    
    class Meta:
        model = ExamStudentMark
        fields = {
            "subject": ["exact"],
        }
