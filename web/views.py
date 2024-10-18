import json

from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse
from web.functions import generate_form_errors

from .forms import ContactForm, JobApplyForm
from .models import (
    About,
    Career,
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
    News,
    Spotlight,
    Team,
    Testimonial,
)


def index(request):
    spotlight = Spotlight.objects.filter(is_deleted=False)
    about_us = About.objects.filter(is_deleted=False).first()
    institution = Institution.objects.filter(is_deleted=False)
    gallery = Gallery.objects.filter(is_deleted=False)[:3]
    news = News.objects.filter(is_deleted=False)[:3]
    testimonials = Testimonial.objects.filter(is_deleted=False)
    contact_us = ContactUs.objects.filter(is_deleted=False).first()

    context = {
        "title": "Home",
        "is_index": True,
        "spotlight": spotlight,
        "about_us": about_us,
        "contact_us": contact_us,
        "institution": institution,
        "gallery": gallery,
        "news": news,
        "testimonials": testimonials,
    }

    return render(request, "web/index.html", context)


def about(request):
    about_us = About.objects.filter(is_deleted=False).first()
    team = Team.objects.filter(is_deleted=False)
    contact_us = ContactUs.objects.filter(is_deleted=False).first()

    context = {
        "title": "About Us",
        "is_about": True,
        "about_us": about_us,
        "contact_us": contact_us,
        "team": team,
    }

    return render(request, "web/about.html", context)


def gallery(request):
    gallery = Gallery.objects.filter(is_deleted=False)
    context = {
        "title": "Gallery",
        "gallery": gallery,
        "is_gallery": True,
    }

    return render(request, "web/gallery.html", context)


def techies_park(request):
    testimonials = Testimonial.objects.filter(is_deleted=False)

    context = {
        "title": "Talrop Techies Park, Edavanna",
        "is_techies_park": True,
        "testimonials": testimonials,
    }

    return render(request, "web/techies_park.html", context)


def jne_about(request):
    testimonials = Testimonial.objects.filter(is_deleted=False)

    context = {
        "title": "ABOUT JNE",
        "is_jne_about": True,
        "testimonials": testimonials,
    }

    return render(request, "web/jne-about.html", context)


def institution(request):
    institution = Institution.objects.filter(is_deleted=False)
    contact_us = ContactUs.objects.filter(is_deleted=False).first()

    institution_type = request.GET.get("institution-type", None)
    if institution_type:
        institution = institution.filter(institution_type=institution_type)

    context = {
        "title": "Institutions",
        "contact_us": contact_us,
        "is_institution": True,
        "institution": institution,
    }

    return render(request, "web/institutions.html", context)


def institution_single(request, slug):
    instance = get_object_or_404(Institution, slug=slug)
    contact_us = ContactUs.objects.filter(is_deleted=False).first()
    institution_team = InstitutionTeam.objects.filter(
        is_deleted=False, institution=instance
    )
    department = Department.objects.filter(is_deleted=False, institution=instance)
    course = Corse.objects.filter(is_deleted=False, institution=instance)
    facilities = Facilities.objects.filter(is_deleted=False, institution=instance)
    institution_gallery = InstitutionGallery.objects.filter(
        is_deleted=False, institution=instance
    ).first()
    event = Event.objects.filter(is_deleted=False, institution=instance)
    institute_testimonial = InstituteTestimonial.objects.filter(
        is_deleted=False, institution=instance
    )
    contact_form = ContactForm()

    context = {
        "title": "Institution",
        "contact_us": contact_us,
        "page_name": instance.name,
        "institution_team": institution_team,
        "department": department,
        "instance": instance,
        "course": course,
        "facilities": facilities,
        "institution_gallery": institution_gallery,
        "event": event,
        "institute_testimonial": institute_testimonial,
        "is_institution_single": True,
        "contact_form": contact_form,
        "institution_single_url": reverse(
            "web:institution_single", kwargs={"slug": instance.slug}
        ),
    }

    return render(request, "web/institution-single.html", context)


def department(request, slug):
    department = Department.objects.get(slug=slug)
    instance = department.institution
    contact_us = ContactUs.objects.filter(is_deleted=False).first()

    facilities = Facilities.objects.filter(is_deleted=False, institution=instance)
    activities = DepartmentActivity.objects.filter(
        is_deleted=False, institution=instance
    )

    faculties = DepartmentFaculties.objects.filter(is_deleted=False)
    department_contact = DepartmentContact.objects.filter(is_deleted=False).first()
    departments = Department.objects.filter(is_deleted=False).exclude(
        slug=department.slug
    )

    context = {
        "title": "Department",
        "page_name": department.name,
        "instance": instance,
        "contact_us": contact_us,
        "department": department,
        "activities": activities,
        "departments": departments,
        "facilities": facilities,
        "faculties": faculties,
        "department_contact": department_contact,
        "is_department": True,
    }

    return render(request, "web/department.html", context)


def career(request):
    career = Career.objects.filter(is_deleted=False, job_type="5")
    contact_us = ContactUs.objects.filter(is_deleted=False).first()
    apply_form = JobApplyForm()

    context = {
        "title": "Careers",
        "contact_us": contact_us,
        "apply_form": apply_form,
        "career": career,
        "is_career": True,
    }

    return render(request, "web/career.html", context)


def news(request):
    news = News.objects.filter(is_deleted=False)
    latest_three = news[0:3]
    news = news[3:]

    contact_us = ContactUs.objects.filter(is_deleted=False).first()

    context = {
        "title": "Latest News",
        "news": news,
        "news_single": news_single,
        "latest_three": latest_three,
        "contact_us": contact_us,
        "is_news": True,
    }

    return render(request, "web/news.html", context)


def news_single(request, pk):
    news = News.objects.get(is_deleted=False, pk=pk)

    context = {
        "title": "News",
        "news": news,
        "is_news": True,
    }

    return render(request, "web/news-single.html", context)


def contact(request):
    contact_form = ContactForm()
    contact_us = ContactUs.objects.filter(is_deleted=False).first()

    context = {
        "title": "Contact Us",
        "contact_form": contact_form,
        "contact_us": contact_us,
        "is_contact": True,
    }

    return render(request, "web/contact.html", context)


def save_message(request):
    if request.method == "POST":
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()

            response_data = {
                "status": "true",
                "redirect": "true",
                "title": "Successfully Submitted.",
                "message": "Message Successfully Created.",
                "redirect_url": reverse("web:index"),
            }

        else:
            message = generate_form_errors(form, formset=False)

            response_data = {
                "status": "false",
                "stable": "true",
                "title": "Form validation error",
                "message": message,
            }

    else:
        response_data = {
            "status": "false",
            "message": "Invalid Request",
        }

    return HttpResponse(
        json.dumps(response_data), content_type="application/javascript"
    )


def get_careers(request):
    instances = Career.objects.filter()
    job_type = request.GET.get("job_type")

    if job_type:
        instances = instances.filter(job_type=job_type)

    context = {
        "instances": instances,
    }

    html_content = render_to_string(
        "web/includes/career-cards.html", context, request=request
    )

    response_data = {
        "status": "true",
        "html_content": html_content,
    }

    return HttpResponse(
        json.dumps(response_data), content_type="application/javascript"
    )


def get_gallery(request):
    instances = Gallery.objects.filter()
    institution_pk = request.GET.get("institution_pk")

    if institution_pk and institution_pk != "all":
        instances = instances.filter(institution__pk=institution_pk)
    print(instances, "test hello")
    context = {
        "gallery": instances,
    }

    html_content = render_to_string(
        "web/includes/gallery-cards.html", context, request=request
    )

    response_data = {
        "status": "true",
        "html_content": html_content,
    }

    return HttpResponse(
        json.dumps(response_data), content_type="application/javascript"
    )


def job_apply(request, slug):
    career = get_object_or_404(Career.objects.filter(pk=slug))
    print(career, "---care")
    if request.method == "POST":
        form = JobApplyForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.career = career
            data.save()

            response_data = {
                "status": "true",
                "redirect": "true",
                "title": "Successfully Submitted.",
                "message": "Job Apply Successfully Created.",
                "redirect_url": reverse("web:career"),
            }

        else:
            message = generate_form_errors(form, formset=False)

            response_data = {
                "status": "false",
                "stable": "true",
                "title": "Form validation error",
                "message": message,
            }

    else:
        response_data = {
            "status": "false",
            "message": "Invalid Request",
        }

    return HttpResponse(
        json.dumps(response_data), content_type="application/javascript"
    )
