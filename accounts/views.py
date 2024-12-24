from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from core import mixins

from . import tables
from .models import User


class UserListView(mixins.HybridListView):
    model = User
    table_class = tables.UserTable
    filterset_fields = ("is_active", "is_staff", "usertype")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Users"
        context["is_master"] = True
        context["is_user"] = True
        context["can_add"] = True
        context["new_link"] = reverse_lazy("accounts:user_create")
        return context


class UserDetailView(mixins.HybridDetailView):
    model = User
    permissions = ("Superadmin", "Admin", "Staff",)


class UserCreateView(mixins.HybridCreateView):
    model = User
    fields = ("username", "password", "usertype")
    permissions = ("Superadmin", "Admin",)

    def get_template_names(self):
        if "pk" in self.kwargs:
            return "employees/employee_form.html"
        return super().get_template_names()

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data["password"])
        user = form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Employee'
        context['subtitle'] = 'Account Details'
        context['is_account'] = True
        return context

    def get_success_url(self):
        return reverse_lazy("employees:employee_list")

    def get_success_message(self, cleaned_data):
        message = "Employee created successfully"
        return message


class UserUpdateView(mixins.HybridUpdateView):
    model = User
    fields = ("username",'first_name','last_name', "password", "usertype")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Employee'
        context['subtitle'] = 'Account Details'
        context['is_account'] = True
        return context

    def get_success_url(self):
        return reverse_lazy("accounts:user_list")

    def get_success_message(self, cleaned_data):
        message = "Employee Updated successfully"
        return message

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data["password"])
        return super().form_valid(form)


class UserDeleteView(mixins.HybridDeleteView):
    model = User
    permissions = ("Superadmin",)
