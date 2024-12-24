from datetime import datetime

from django.conf import settings
from django.db.models import Q
from django.urls import reverse_lazy
from django.db.models import Sum

from core import mixins
from examination.models import Student

class HomeView(mixins.HybridListView):
    model = Student
    
    template_name = "core/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        
        

        context["is_dashboard"] = True
        return context
