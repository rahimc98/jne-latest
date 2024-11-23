import json
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse
from examination.models import Course, GradingSystem, Student
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


def exam_result(request):

    context = {
        "title": "Exam Result",
        "is_exam_rsult": True,
    }

    return render(request, "web/exam_result.html", context)

def rank_list(request):
    type = request.GET.get("type")

    students = Student.objects.filter(is_active=True,course__type=type)
    student_scores = []
    for student in students:
        exam_student = student.get_exam_student()
        marks = exam_student.get_exam_marks()
        mark_data = []
        
        for mark in marks:
            te_mark = 0
            ce_mark = 0
            total_mark = 0

            if mark.te_mark == 'Ab':
                te_mark = 0
            elif mark.te_mark == 'C':
                te_mark = 0
            else:
                te_mark = int(mark.te_mark)
                ce_mark = int(mark.ce_mark)
            total_mark = te_mark + ce_mark
            credit = mark.subject.credit_score
            grade_point = total_mark/10
            credit_point = round(credit*grade_point,2)
            mark_data.append({
                    "mark": total_mark,
                    "credit":credit,
                    'credit_point': credit_point,
                    'grade_point':grade_point,
                })
        total_credit = sum(mark['credit'] for mark in mark_data)
        total_credit_point = sum(mark['credit_point'] for mark in mark_data)
        sgpa = round(total_credit_point / total_credit, 2) if total_credit else 0
        student_scores.append({
            "student": student.name,
            "reg_no": student.reg_no,
            "course": student.course.name,
            "college": student.course.college,
            "total_mark": sum(mark['mark'] for mark in mark_data),
            "sgpa": sgpa,
        })
    top_students = sorted(student_scores, key=lambda x: x["sgpa"], reverse=True)[:50]
    
    if type == 'pre_fadheela':
        type = 'Pre Fadheela'
    context = {
        "title": str(type) + " Rank List",
        "is_rank_list": True,
        'students':top_students,

    }

    return render(request, "web/rank_list.html", context)




def find_result(request):
    hall_ticket = request.GET.get("hall_ticket")
    dob = request.GET.get("dob")
    response_data = {
        "status": "false",
        "is_data": False,
    }

    try:
        # Fetch the student object
        student = Student.objects.get(reg_no=hall_ticket, dob=dob)
        is_data = True
        name = student.name
        reg_no = student.reg_no
        program = student.course.name

        # Fetch exam student data once
        exam_student = student.get_exam_student()
        sem = exam_student.exam.batch.name
        
        download_url = student.get_print_grade_card()
        
        # Prepare response data
        response_data.update({
            "status": "true",
            "is_data": is_data,
            "name": name or "",
            "reg_no": reg_no or "",
            "program": program or "",
            "sem": sem or "",
            "download_url": download_url
        })
        print('response_data=',response_data)
    except ObjectDoesNotExist:
        response_data["status"] = "false"
    return JsonResponse(response_data)