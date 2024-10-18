from django import forms
from django.forms.widgets import FileInput, Select, TextInput
from django.utils.translation import gettext_lazy as _

from .models import (
    About,
    Career,
    Contact,
    ContactUs,
    Corse,
    Department,
    DepartmentActivity,
    DepartmentContact,
    DepartmentFaculties,
    Event,
    Facilities,
    Gallery,
    InstituteTestimonial,
    Institution,
    InstitutionGallery,
    InstitutionTeam,
    JobApply,
    News,
    Spotlight,
    Team,
    Testimonial,
)


class SpotlightForm(forms.ModelForm):
    class Meta:
        model = Spotlight
        exclude = ["is_deleted"]

        widgets = {
            "title": TextInput(attrs={"class": "required form-control"}),
            "description": TextInput(attrs={"class": "required form-control"}),
            "admission_year": TextInput(attrs={"class": "required form-control"}),
            "whatsapp_number": TextInput(attrs={"class": "required form-control"}),
        }

        error_messages = {
            "title": {
                "required": _("Title field is required."),
            },
            "description": {
                "required": _("Description field is required."),
            },
            "admission_year": {
                "required": _("Admission year field is required."),
            },
        }


class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        exclude = ["is_deleted"]

        widgets = {
            "title": TextInput(attrs={"class": "required form-control"}),
            "description": TextInput(attrs={"class": "required form-control"}),
            "our_mission": TextInput(attrs={"class": "required form-control"}),
            "our_vision": TextInput(attrs={"class": "required form-control"}),
        }

        error_messages = {
            "description": {
                "required": _("Our Vision field is required."),
            }
        }


class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        exclude = ["is_deleted"]

        widgets = {
            "name": TextInput(attrs={"class": "required form-control"}),
            "location": TextInput(attrs={"class": "required form-control"}),
            "content": TextInput(attrs={"class": "required form-control"}),
            # 'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }

        error_messages = {
            "name": {
                "required": _("Name field is required."),
            },
            "location": {
                "required": _("Location field is required."),
            },
            "content": {
                "required": _("Content field is required."),
            },
        }


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        exclude = ["is_deleted", "institution"]

        widgets = {}

        error_messages = {
            "location": {
                "required": _("Location field is required."),
            },
            "content": {
                "required": _("Content field is required."),
            },
        }


class InstitutionGalleryForm(forms.ModelForm):
    class Meta:
        model = InstitutionGallery
        exclude = ["is_deleted", "institution"]

        widgets = {}

        error_messages = {
            "location": {
                "required": _("Location field is required."),
            },
            "content": {
                "required": _("Content field is required."),
            },
        }


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        exclude = ["is_deleted"]

        widgets = {
            "title": TextInput(attrs={"class": "required form-control"}),
            "reporter": TextInput(attrs={"class": "required form-control"}),
            "date": TextInput(
                attrs={
                    "class": "required form-control fc-datepicker",
                    "placeholder": "Date",
                }
            ),
            "content": TextInput(attrs={"class": "required form-control"}),
        }

        error_messages = {
            "title": {
                "required": _("Title field is required."),
            },
            "date": {
                "required": _("Date field is required."),
            },
            "content": {
                "required": _("Content field is required."),
            },
        }


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        exclude = ["is_deleted"]

        widgets = {
            "name": TextInput(attrs={"class": "required form-control"}),
            "description": TextInput(attrs={"class": "required form-control"}),
        }

        error_messages = {
            "name": {
                "required": _("Name field is required."),
            },
            "description": {
                "required": _("Description field is required."),
            },
        }


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        exclude = ["is_deleted"]

        widgets = {
            "name": TextInput(attrs={"class": "required form-control"}),
            "designation": TextInput(attrs={"class": "required form-control"}),
            "description": TextInput(attrs={"class": "required form-control"}),
            "instagram_url": TextInput(
                attrs={"class": "form-control", "placeholder": "Instagram url"}
            ),
            "facebook_url": TextInput(
                attrs={"class": "form-control", "placeholder": "Facebook url"}
            ),
            "twitter_url": TextInput(
                attrs={"class": "form-control", "placeholder": "Twitter url"}
            ),
            "linkedin_url": TextInput(
                attrs={"class": "form-control", "placeholder": "Linkedin url"}
            ),
        }

        error_messages = {
            "name": {
                "required": _("Name field is required."),
            },
            "designation": {
                "required": _("Designation field is required."),
            },
            "description": {
                "required": _("Description field is required."),
            },
        }


class InstitutionTeamForm(forms.ModelForm):
    class Meta:
        model = InstitutionTeam
        exclude = ["is_deleted", "institution"]

        widgets = {
            "name": TextInput(attrs={"class": "required form-control"}),
            "designation": TextInput(attrs={"class": "required form-control"}),
            "description": TextInput(attrs={"class": "required form-control"}),
            "instagram_url": TextInput(
                attrs={"class": "form-control", "placeholder": "Instagram url"}
            ),
            "facebook_url": TextInput(
                attrs={"class": "form-control", "placeholder": "Facebook url"}
            ),
            "twitter_url": TextInput(
                attrs={"class": "form-control", "placeholder": "Twitter url"}
            ),
            "linkedin_url": TextInput(
                attrs={"class": "form-control", "placeholder": "Linkedin url"}
            ),
        }

        error_messages = {
            "name": {
                "required": _("Name field is required."),
            },
            "designation": {
                "required": _("Designation field is required."),
            },
            "description": {
                "required": _("Description field is required."),
            },
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        exclude = ["is_deleted", "institution"]

        widgets = {
            "name": TextInput(attrs={"class": "required form-control"}),
            "description": TextInput(attrs={"class": "required form-control"}),
        }

        error_messages = {
            "name": {
                "required": _("Name field is required."),
            },
            "description": {
                "required": _("Description field is required."),
            },
        }


class DepartmentActivityForm(forms.ModelForm):
    class Meta:
        model = DepartmentActivity
        exclude = ["is_deleted", "institution"]

        widgets = {
            "name": TextInput(attrs={"class": "required form-control"}),
            "description": TextInput(attrs={"class": "required form-control"}),
            "date": TextInput(attrs={"class": "required form-control"}),
        }

        error_messages = {
            "name": {
                "required": _("Name field is required."),
            },
            "description": {
                "required": _("Description field is required."),
            },
        }


class DepartmentFacultiesForm(forms.ModelForm):
    class Meta:
        model = DepartmentFaculties
        exclude = ["is_deleted", "institution", "department"]

        widgets = {
            "name": TextInput(attrs={"class": "required form-control"}),
            "designation": TextInput(attrs={"class": "required form-control"}),
            "instagram_url": TextInput(
                attrs={"class": "form-control", "placeholder": "Instagram url"}
            ),
            "facebook_url": TextInput(
                attrs={"class": "form-control", "placeholder": "Facebook url"}
            ),
            "twitter_url": TextInput(
                attrs={"class": "form-control", "placeholder": "Twitter url"}
            ),
            "linkedin_url": TextInput(
                attrs={"class": "form-control", "placeholder": "Linkedin url"}
            ),
        }

        error_messages = {
            "name": {
                "required": _("Name field is required."),
            },
            "designation": {
                "required": _("Designation field is required."),
            },
        }


class DepartmentContactForm(forms.ModelForm):
    class Meta:
        model = DepartmentContact
        exclude = ["is_deleted", "institution", "department"]

        widgets = {
            "phone": TextInput(
                attrs={
                    "class": "required form-control",
                    "type": "number",
                    "placeholder": "Phone",
                }
            ),
            "second_phone": TextInput(
                attrs={
                    "class": "required form-control",
                    "type": "number",
                    "placeholder": "Second Phone",
                }
            ),
            "email": TextInput(
                attrs={"class": "required form-control", "placeholder": "Email"}
            ),
            "second_email": TextInput(
                attrs={"class": "required form-control", "placeholder": "Second Email"}
            ),
            "location": TextInput(
                attrs={"class": "required form-control", "placeholder": "Location"}
            ),
        }

        error_messages = {
            "location": {
                "required": _("Location field is required."),
            }
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Corse
        exclude = ["is_deleted", "institution"]

        widgets = {
            "name": TextInput(attrs={"class": "required form-control"}),
            "description": TextInput(attrs={"class": "required form-control"}),
        }

        error_messages = {
            "name": {
                "required": _("Name field is required."),
            },
            "description": {
                "required": _("Description field is required."),
            },
        }


class FacilitiesForm(forms.ModelForm):
    class Meta:
        model = Facilities
        exclude = ["is_deleted", "institution", "department"]

        widgets = {
            "name": TextInput(attrs={"class": "required form-control"}),
            "description": TextInput(attrs={"class": "required form-control"}),
        }

        error_messages = {
            "name": {
                "required": _("Name field is required."),
            },
            "description": {
                "required": _("Description field is required."),
            },
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ["is_deleted", "institution"]

        widgets = {
            "name": TextInput(attrs={"class": "required form-control"}),
            "description": TextInput(attrs={"class": "required form-control"}),
            "date": TextInput(attrs={"class": "required form-control"}),
        }

        error_messages = {
            "name": {
                "required": _("Name field is required."),
            },
            "description": {
                "required": _("Description field is required."),
            },
            "date": {
                "required": _("Date field is required."),
            },
        }


class InstituteTestimonialForm(forms.ModelForm):
    class Meta:
        model = InstituteTestimonial
        exclude = ["is_deleted"]

        widgets = {
            "name": TextInput(attrs={"class": "required form-control"}),
            "description": TextInput(attrs={"class": "required form-control"}),
        }

        error_messages = {
            "name": {
                "required": _("Name field is required."),
            },
            "description": {
                "required": _("Description field is required."),
            },
        }


class CareerForm(forms.ModelForm):
    class Meta:
        model = Career
        exclude = ["is_deleted", "id", "date_added"]

        widgets = {
            "job_type": Select(
                attrs={"class": "required form-control", "placeholder": "Job Type"}
            ),
            "designation": TextInput(
                attrs={"class": "required form-control", "placeholder": "Designation"}
            ),
            "location": TextInput(
                attrs={"class": "required form-control", "placeholder": "Location"}
            ),
            "description": TextInput(
                attrs={"class": "required form-control", "placeholder": "Description"}
            ),
        }

        error_messages = {
            "designation": {
                "required": _("Designation field is required."),
            },
            "location": {
                "required": _("Location field is required."),
            },
            "description": {
                "required": _("Description field is required."),
            },
        }


class JobApplyForm(forms.ModelForm):
    class Meta:
        model = JobApply
        exclude = ["is_deleted", "id", "date_added", "career"]

        widgets = {
            "name": TextInput(
                attrs={
                    "class": "required form-control",
                    "placeholder": "Enter Your Name",
                }
            ),
            "phone": TextInput(
                attrs={
                    "class": "required form-control",
                    "type": "number",
                    "placeholder": "Enter Your Number",
                }
            ),
            "email": TextInput(
                attrs={
                    "class": "required form-control",
                    "placeholder": "Enter Your Email",
                    "type": "email",
                }
            ),
            "cv": FileInput(
                attrs={
                    "class": "required form-control FileInput FileUpload1",
                    "name": "booking_attachment",
                }
            ),
        }

        error_messages = {
            "name": {
                "required": _("Name field is required."),
            },
            "phone": {
                "required": _("Phone field is required."),
            },
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ["is_deleted", "id", "date_added"]

        widgets = {
            "name": TextInput(
                attrs={"class": "required form-control", "placeholder": "Name"}
            ),
            "phone": TextInput(
                attrs={
                    "class": "required form-control",
                    "type": "number",
                    "placeholder": "Phone",
                }
            ),
            "email": TextInput(
                attrs={"class": "required form-control", "placeholder": "Email"}
            ),
            "message": TextInput(
                attrs={"class": "required form-control", "placeholder": "Message"}
            ),
        }

        error_messages = {
            "name": {
                "required": _("Name field is required."),
            },
            "phone": {
                "required": _("Phone field is required."),
            },
        }


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        exclude = ["is_deleted"]

        widgets = {
            "phone": TextInput(
                attrs={
                    "class": "required form-control",
                    "type": "number",
                    "placeholder": "Phone",
                }
            ),
            "email": TextInput(
                attrs={"class": "required form-control", "placeholder": "Email"}
            ),
            "location": TextInput(
                attrs={"class": "required form-control", "placeholder": "Location"}
            ),
            "instagram_url": TextInput(
                attrs={"class": "form-control", "placeholder": "Instagram url"}
            ),
            "facebook_url": TextInput(
                attrs={"class": "form-control", "placeholder": "Facebook url"}
            ),
            "twitter_url": TextInput(
                attrs={"class": "form-control", "placeholder": "Twitter url"}
            ),
            "linkedin_url": TextInput(
                attrs={"class": "form-control", "placeholder": "Linkedin url"}
            ),
        }

        error_messages = {
            "location": {
                "required": _("Location field is required."),
            }
        }
