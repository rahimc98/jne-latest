
from collections import Counter
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django_tables2 import columns
from django.views.generic import TemplateView
from django.db.models import Sum
from django.views import View

from core import mixins
from core.base import BaseTable
from examination.filter import ExamStudentMarkFilter
from .forms import BatchFilterForm
from .create_pdf import PDFView
from . models import Batch, College, Course, ExamApply, ExamStudent, ExamStudentMark, Examination, GradingSystem, Student, Subject
from . import tables

class BaseModelView:
    model = None 
    table_class = None
    exclude = ("is_active",)
    filterset_fields = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.model._meta.verbose_name_plural.title()
        context["can_add"] = mixins.check_access(self.request, self.permissions)
        context["new_link"] = reverse_lazy(f"examination:{self.model.__name__.lower()}_create")
        context[f"is_{self.model.__name__.lower()}"] = True
        context["is_master"] = True
        return context
    

def create_dynamic_table(model_class):
    excluded_fields = ["is_active",'id']

    class DynamicTable(BaseTable):
        action = columns.TemplateColumn(template_name="app/partials/table_actions_normal.html", orderable=False)

        class Meta:
            model = model_class
            fields = [field.name for field in model_class._meta.fields if field.name not in excluded_fields]
            attrs = {"class": "table key-buttons border-bottom table-striped"}
            exclude = excluded_fields

    return DynamicTable


# Create your views here.
class Halticket(PDFView):
    template_name = "web/halticket_pdf.html"
    pdfkit_options = {
        "page-height": 297,
        "page-width": 210,
        "encoding": "UTF-8",
        "margin-top": "0",
        "margin-bottom": "0",
        "margin-left": "0",
        "margin-right": "0",
    }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        selected_ids = self.request.session.get('selected_ids', [])
        items = ExamStudent.objects.filter(id__in=selected_ids,is_active=True)
        context["items"] = items
        return context
    

class GradeMarkPdfView(PDFView):
    template_name = "web/grademark_pdf.html"
    pdfkit_options = {
        "page-height": 297,
        "page-width": 210,
        "encoding": "UTF-8",
        "margin-top": "0",
        "margin-bottom": "0",
        "margin-left": "0",
        "margin-right": "0",
    }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # Fetch the student object
        student = Student.objects.get(pk=self.kwargs['pk'])

        # Fetch exam student data once
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
            grade = ""
            credit = mark.subject.credit_score
            grade_point = total_mark/10
            status = 'Pass' if te_mark >= 32 else 'Fail'
            grading_system = GradingSystem.objects.filter(
                marks_range_from__lte=total_mark,
                marks_range_to__gte=total_mark
            ).first()
            if grading_system:
                grade = grading_system.grade
            credit_point = round(credit*grade_point,2)
            if status == 'Fail':
                    credit_point = '-'
                    grade_point = '-'
                    grade = '-'
                    total_mark = te_mark

            mark_data.append({
                "subject": mark.subject.name,
                "mark": total_mark,
                "credit":credit,
                'grade':grade,
                'grade_point':grade_point,
                'credit_point': credit_point,
                'stutus':status
            })
        # Calculate total credits and credit points
        total_credit = sum(mark['credit'] for mark in mark_data)
        is_ok =True
        overall_grade = '-'
        sgpa = '-'
        total_credit_point = '-'
        for i in mark_data:
            if i['stutus'] == 'Fail':
                is_ok = False
        if is_ok :
            total_credit_point = sum(mark['credit_point'] for mark in mark_data)
            sgpa = round(total_credit_point / total_credit, 2) if total_credit else 0
            overall_grade = GradingSystem.objects.filter(
                grade_range_from__lte=sgpa,
                grade_range_to__gte=sgpa
            ).first().grade
            total_credit_point = round(total_credit_point, 2)
                

        # Prepare response data
        context["name"] = student.name
        context["reg_no"] = student.reg_no
        context["program"] = student.course.name
        context["exam"] = exam_student.exam
        context["sem"] = exam_student.exam.batch.name
        context["no_days"] = exam_student.no_of_days
        context["attentance"] = exam_student.attentence
        context["total_credit"] = round(total_credit, 2)
        context["total_credit_point"] = total_credit_point
        context["sgpa"] = sgpa
        context['overall_grade'] = overall_grade
        context["mark_data"] = mark_data
        return context
    
class GradeCard(PDFView):
    template_name = "web/grademark_pdf_admin.html"
    pdfkit_options = {
        "page-height": 297,
        "page-width": 210,
        "encoding": "UTF-8",
        "margin-top": "0",
        "margin-bottom": "0",
        "margin-left": "0",
        "margin-right": "0",
    }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        selected_ids = self.request.session.get('selected_ids', [])
        students = Student.objects.filter(id__in=selected_ids,is_active=True)
        items = []
        student_scores = []
        for student in students:
            # Fetch exam student data once
            exam_student = student.get_exam_student()
            marks = exam_student.get_exam_marks()
            is_women_college = True
            if student.course.college.pk == 1:
                is_women_college = False
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
                grade = ""
                credit = mark.subject.credit_score
                grade_point = total_mark/10
                status = 'Pass' if te_mark >= 32 else 'Fail'
                grading_system = GradingSystem.objects.filter(
                    marks_range_from__lte=total_mark,
                    marks_range_to__gte=total_mark
                ).first()
                if grading_system:
                    grade = grading_system.grade
                credit_point = round(credit*grade_point,2)
                if status == 'Fail':
                    credit_point = '-'
                    grade_point = '-'
                    grade = '-'
                    total_mark = te_mark

                mark_data.append({
                    "subject": mark.subject.name,
                    "mark": total_mark,
                    "credit":credit,
                    'grade':grade,
                    'grade_point':grade_point,
                    'credit_point': credit_point,
                    'stutus':status
                })
               
            # Calculate total credits and credit points
            total_credit = sum(mark['credit'] for mark in mark_data)
            
            
            is_ok =True
            overall_grade = '-'
            sgpa = '-'
            total_credit_point = '-'
            for i in mark_data:
                if i['stutus'] == 'Fail':
                    is_ok = False
            if is_ok :
                total_credit_point = sum(mark['credit_point'] for mark in mark_data)
                sgpa = round(total_credit_point / total_credit, 2) if total_credit else 0
                overall_grade = GradingSystem.objects.filter(
                    grade_range_from__lte=sgpa,
                    grade_range_to__gte=sgpa
                ).first().grade
                total_credit_point = round(total_credit_point, 2)
            # Prepare response data
            student_scores.append({
                    "student": student,
                    "total_mark": sum(mark['mark'] for mark in mark_data),
                    "sgpa": sgpa,
                })
            data = {
                "name": student.name,
                "reg_no": student.reg_no,
                "program": student.course.name,
                "exam": exam_student.exam,
                "sem": exam_student.exam.batch.name,
                "no_days": exam_student.no_of_days,
                "attentance": exam_student.attentence,
                "total_credit": round(total_credit, 2),
                "total_credit_point": total_credit_point,
                "sgpa": sgpa,
                'overall_grade': overall_grade,
                "mark_data": mark_data,
                'is_women_college':is_women_college
            }
            items.append(data)
        # print('student_scores=',student_scores)
        top_students = sorted(student_scores, key=lambda x: x["total_mark"], reverse=True)[:3]
        print('top_students=',top_students)
        context["items"] = items
        return context
    

class ExamApplyPdfView(PDFView):
    template_name = "web/exam_apply_pdf.html"
    pdfkit_options = {
        "page-height": 297,
        "page-width": 210,
        "encoding": "UTF-8",
        "margin-top": "0",
        "margin-bottom": "0",
        "margin-left": "0",
        "margin-right": "0",
    }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # Fetch the student object
        student = get_object_or_404(Student, pk=self.kwargs['pk'])

        exam_applies = ExamApply.objects.filter(student__student=student).select_related('subject')
        dic_data = [
            {
                "subject": exam.subject.name,
                "code": exam.subject.course_code,
                "exam_type": exam.exam_type,
                "amount": exam.amount,
            }
            for exam in exam_applies
        ]
        total_amt = exam_applies.aggregate(Sum('amount'))['amount__sum'] or 0

        context["total_amt"] = total_amt 
        context["dic_data"] = dic_data

        # Prepare response data
        context["name"] = student.name
        context["reg_no"] = student.reg_no
        context["program"] = student.course.name
        context["sem"] = student.get_exam_student().exam.batch.name
        
        return context
    
class ExamApplied(PDFView):
    template_name = "web/exam_applyed_pdf.html"
    pdfkit_options = {
        "page-height": 297,
        "page-width": 210,
        "encoding": "UTF-8",
        "margin-top": "0",
        "margin-bottom": "0",
        "margin-left": "0",
        "margin-right": "0",
    }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        selected_ids = self.request.session.get('selected_ids', [])
        students = ExamApply.objects.filter(id__in=selected_ids,is_active=True)
        instance = students.first()
        items = []
        for student in students:
            data = {
                'reg_no':student.student.student.reg_no,
                'name':student.student.student.name,
                'subject':student.subject.name,
                'exam_type':student.exam_type,
                'amount':student.amount,
                'remark':''
            }
        
            items.append(data)
        context["dic_data"] = items
        context['college'] = instance.student.student.course.college
        context['course'] = instance.student.student.course.name
        context['sem'] = instance.student.student.get_exam_student().exam.batch.name
        return 
    

class ExamAppliedBatchBased(PDFView):
    template_name = "web/exam_applyed_batch_based.html"
    pdfkit_options = {
        "page-height": 210,
        "page-width": 297,
        "encoding": "UTF-8",
        "margin-top": "0",
        "margin-bottom": "0",
        "margin-left": "0",
        "margin-right": "0",
    }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        selected_ids = self.request.session.get('selected_ids', [])
        batchs = Batch.objects.filter(id__in=selected_ids,is_active=True)
        
        dic_data = []
        total_sum = 0
        for batch in batchs:
            subjects = batch.get_subjects()
            students = ExamStudent.objects.filter(exam=batch.get_exam())
            dic_list = []
            subject_counts = {} 
            for student in students:
                sub_data = []
                total = 0
                exam_applications = ExamApply.objects.filter(student=student, subject__in=subjects)
                for subject in subjects:
                    amt = 0
                    val = ''
                    inst = exam_applications.filter(subject=subject).last()
                    if inst:
                        if inst.exam_type == 'Improvement':
                            val = 'IMP'
                        else:
                            val = 'SUP'
                        amt = inst.amount
                        subject_counts[subject.pk] = subject_counts.get(subject.pk, 0) + 1
                    total += amt
                    sb_data ={
                        'val':val,
                        'pk':subject.pk
                    }
                    sub_data.append(sb_data)
                

                st_data = {
                    'reg_no':student.student.reg_no,
                    'name': student.student.name,
                    'sub_data':sub_data,
                    'total':total
                }
                dic_list.append(st_data)
                total_sum += total

            list_data = {
                'batch':batch.name,
                'course':batch.course.name,
                'college':batch.course.college.name,
                'dic_list': dic_list,
                'subjects':subjects
            }

            dic_data.append(list_data)
            # print(dic_data)
            subject_summary = [
                {'count': subject_counts.get(subject.pk, 0)}
                for subject in subjects
            ]
        context["dic_data"] = dic_data
        context['total_sum'] = total_sum
        context['subject_summary'] = subject_summary
        return context


class BatchBasedMarkListPrint(PDFView):
    template_name = "web/batch_based_marklist_print.html"
    pdfkit_options = {
        "page-height": 210,
        "page-width": 297,
        "encoding": "UTF-8",
        "margin-top": "0",
        "margin-bottom": "0",
        "margin-left": "0",
        "margin-right": "0",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        batch = Batch.objects.get(pk=self.kwargs['pk'])
        subjects = batch.get_subjects()
        students = ExamStudent.objects.filter(exam__batch=batch)
        items = []
        for student in students:
            marks = student.get_exam_marks()
            mark_data = []
            total_credit = 0
            total_credit_point = 0
            total_mark = 0
            is_pass = True

            for mark in marks:
                te_mark = 0 if mark.te_mark in ['Ab', 'C'] else int(mark.te_mark)
                ce_mark = int(mark.ce_mark) if mark.te_mark not in ['Ab', 'C'] else 0
                total_subject_mark = te_mark + ce_mark
                credit = mark.subject.credit_score
                grade_point = total_subject_mark / 10
                credit_point = round(credit * grade_point, 2) if te_mark >= 32 else '-'
                status = 'Pass' if te_mark >= 32 else 'Fail'

                if status == 'Fail':
                    is_pass = False
                    credit_point = '-'
                    grade_point = '-'

                mark_data.append({
                    'ce_mark': ce_mark,
                    'te_mark': te_mark,
                    'total_mark': total_subject_mark,
                    'credit': credit,
                    'grade_point': grade_point,
                    'credit_point': credit_point,
                    'status': status
                })

                total_credit += credit
                total_mark += total_subject_mark
                if credit_point != '-':
                    total_credit_point += credit_point

            sgpa = round(total_credit_point / total_credit, 2) if total_credit and is_pass else '-'
            overall_grade = '-'

            if sgpa != '-':
                overall_grade = GradingSystem.objects.filter(
                    grade_range_from__lte=sgpa,
                    grade_range_to__gte=sgpa
                ).first().grade

            items.append({
                "student": student.student.name,
                "reg_no": student.student.reg_no,
                'total_mark': total_mark,
                'total_credit_point': total_credit_point if sgpa != '-' else '-',
                'sgpa': sgpa,
                'overall_grade': overall_grade,
                "subjects_data": mark_data,
            })
        
        context["is_marklist"] = True

        context['is_batch_based_mark_list'] = True
        context["items"] = sorted(items, key=lambda x: x['sgpa'] if x['sgpa'] != '-' else 0, reverse=True)
        context["subjects"] = subjects
        context["batch"] = batch
        context["title"] = f"Batch Based Mark List - {batch.course.name} - {batch.name}"
        
        return context


class CollegeListView(BaseModelView, mixins.HybridListView):
    model = College
    table_class = create_dynamic_table(College)
    filterset_fields = {"name": ["icontains"]}


class CollegeDetailView(BaseModelView, mixins.HybridDetailView):
    model = College


class CollegeCreateView(BaseModelView, mixins.HybridCreateView):
    model = College

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "New College"
        return context


class CollegeUpdateView(BaseModelView, mixins.HybridUpdateView):
    model = College

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Update {self.object} College"
        return context


class CollegeDeleteView(BaseModelView, mixins.HybridDeleteView):
    model = College

class CourseListView(BaseModelView, mixins.HybridListView):
    model = Course
    table_class = create_dynamic_table(Course)
    filterset_fields = { "college": ["exact"],}


class CourseDetailView(BaseModelView, mixins.HybridDetailView):
    model = Course


class CourseCreateView(BaseModelView, mixins.HybridCreateView):
    model = Course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "New Course"
        return context


class CourseUpdateView(BaseModelView, mixins.HybridUpdateView):
    model = Course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Update {self.object} Course"
        return context


class CourseDeleteView(BaseModelView, mixins.HybridDeleteView):
    model = Course


class BatchListView(BaseModelView, mixins.HybridListView):
    model = Batch
    table_class = create_dynamic_table(Batch)
    filterset_fields = {'course__college': ["exact"],"course": ["exact"]}


class BatchDetailView(BaseModelView, mixins.HybridDetailView):
    model = Batch


class BatchCreateView(BaseModelView, mixins.HybridCreateView):
    model = Batch

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "New Batch"
        return context


class BatchUpdateView(BaseModelView, mixins.HybridUpdateView):
    model = Batch

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Update {self.object} Batch"
        return context


class BatchDeleteView(BaseModelView, mixins.HybridDeleteView):
    model = Batch


class ExaminationListView(BaseModelView, mixins.HybridListView):
    model = Examination
    table_class = create_dynamic_table(Examination)
    filterset_fields = {"name": ["icontains"]}


class ExaminationDetailView(BaseModelView, mixins.HybridDetailView):
    model = Examination


class ExaminationCreateView(BaseModelView, mixins.HybridCreateView):
    model = Examination

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "New Examination"
        return context


class ExaminationUpdateView(BaseModelView, mixins.HybridUpdateView):
    model = Examination

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Update {self.object} Examination"
        return context


class ExaminationDeleteView(BaseModelView, mixins.HybridDeleteView):
    model = Examination



class StudentListView( mixins.HybridListView):
    model = Student
    exclude = ("is_active",)
    table_class = create_dynamic_table(Student)
    filterset_fields = {"name": ["icontains"],"reg_no": ["icontains"],"course": ["exact"]}
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.model._meta.verbose_name_plural.title()
        context["can_add"] = mixins.check_access(self.request, self.permissions)
        context["new_link"] = reverse_lazy(f"examination:{self.model.__name__.lower()}_create")
        context[f"is_{self.model.__name__.lower()}"] = True
        return context

class StudentDetailView(BaseModelView, mixins.HybridDetailView):
    model = Student


class StudentCreateView(mixins.HybridCreateView):
    model = Student
    exclude = ("is_active",)
    def get_success_url(self):
        return self.object.get_list_url()

    def form_valid(self, form): 
        response = super().form_valid(form)
        return response

    def get_success_message(self, cleaned_data):
        instance = self.object
        success_message = f"{self.model.__name__} '{instance}' was Created successfully. "
        success_message += f"<a href='{instance.get_absolute_url()}'>View {self.model.__name__}</a>."
        return success_message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "New Student"
        context['is_student'] = True
        return context


class StudentUpdateView(BaseModelView, mixins.HybridUpdateView):
    model = Student

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Update {self.object} Student"
        return context


class StudentDeleteView(BaseModelView, mixins.HybridDeleteView):
    model = Student



class SubjectListView(BaseModelView, mixins.HybridListView):
    model = Subject
    table_class = create_dynamic_table(Subject)
    filterset_fields = {"name": ["icontains"]}


class SubjectDetailView(BaseModelView, mixins.HybridDetailView):
    model = Subject


class SubjectCreateView(BaseModelView, mixins.HybridCreateView):
    model = Subject

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "New Subject"
        return context


class SubjectUpdateView(BaseModelView, mixins.HybridUpdateView):
    model = Subject

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Update {self.object} Subject"
        return context


class SubjectDeleteView(BaseModelView, mixins.HybridDeleteView):
    model = Subject


class ExamStudentListView( mixins.HybridListView):
    model = ExamStudent
    exclude = ("is_active",)
    table_class = create_dynamic_table(ExamStudent)
    filterset_fields = {"student__name": ["icontains"],"student__reg_no": ["icontains"],"exam__batch": ["exact"]}
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.model._meta.verbose_name_plural.title()
        context["can_add"] = mixins.check_access(self.request, self.permissions)
        context["new_link"] = reverse_lazy(f"examination:{self.model.__name__.lower()}_create")
        context[f"is_{self.model.__name__.lower()}"] = True
        return context

class ExamStudentDetailView(BaseModelView, mixins.HybridDetailView):
    model = ExamStudent


class ExamStudentCreateView(mixins.HybridCreateView):
    model = ExamStudent
    exclude = ("is_active",)
    def get_success_url(self):
        return self.object.get_list_url()

    def form_valid(self, form): 
        response = super().form_valid(form)
        return response

    def get_success_message(self, cleaned_data):
        instance = self.object
        success_message = f"{self.model.__name__} '{instance}' was Created successfully. "
        success_message += f"<a href='{instance.get_absolute_url()}'>View {self.model.__name__}</a>."
        return success_message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "New ExamStudent"
        context['is_examstudent'] = True
        return context


class ExamStudentUpdateView(BaseModelView, mixins.HybridUpdateView):
    model = ExamStudent

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Update {self.object} ExamStudent"
        return context


class ExamStudentDeleteView(BaseModelView, mixins.HybridDeleteView):
    model = ExamStudent


class ExamStudentMarkListView( mixins.HybridListView):
    model = ExamStudentMark
    exclude = ("is_active",)
    table_class = tables.ExamStudentMarkTable
    filterset_class = ExamStudentMarkFilter
    search_fields = ('student__student__reg_no','student__student__name')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.model._meta.verbose_name_plural.title()
        context["can_add"] = mixins.check_access(self.request, self.permissions)
        context["new_link"] = reverse_lazy(f"examination:{self.model.__name__.lower()}_create")
        context[f"is_{self.model.__name__.lower()}"] = True
        context['is_exam'] = True
        return context


class ExamStudentMarkDetailView(BaseModelView, mixins.HybridDetailView):
    model = ExamStudentMark
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.model._meta.verbose_name_plural.title()
        context["can_add"] = mixins.check_access(self.request, self.permissions)
        context["new_link"] = reverse_lazy(f"examination:{self.model.__name__.lower()}_create")
        context[f"is_{self.model.__name__.lower()}"] = True
        context['is_exam'] = True
        return context


class ExamStudentMarkCreateView(mixins.HybridCreateView):
    model = ExamStudentMark
    exclude = ("is_active",)
    def get_success_url(self):
        return self.object.get_list_url()

    def form_valid(self, form): 
        response = super().form_valid(form)
        return response

    def get_success_message(self, cleaned_data):
        instance = self.object
        success_message = f"{self.model.__name__} '{instance}' was Created successfully. "
        success_message += f"<a href='{instance.get_absolute_url()}'>View {self.model.__name__}</a>."
        return success_message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "New ExamStudentMark"
        context['is_examstudentMark'] = True
        context['is_exam'] = True
        return context


class ExamStudentMarkUpdateView(BaseModelView, mixins.HybridUpdateView):
    model = ExamStudentMark

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Update {self.object} ExamStudentMark"
        context['is_exam'] = True
        return context


class ExamStudentMarkDeleteView(BaseModelView, mixins.HybridDeleteView):
    model = ExamStudentMark


class BatchBasedMarkListView( mixins.HybridListView):
    model = ExamStudentMark
    table_class = tables.ExamStudentMarkTable
    filterset_fields = {"subject": ["exact"],}
    template_name = "examination/batch_based_mark_list.html"

    def get_queryset(self):
        qs = super().get_queryset().filter(is_active=True,subject__batch=self.kwargs['pk'])
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        batch = Batch.objects.get(pk=self.kwargs['pk'])
        subjects = batch.get_subjects()
        students = ExamStudent.objects.filter(exam__batch=batch)
        items = []
        fail_count = 0
        pass_count = 0
        marks = []
        for student in students:
            marks =student.get_exam_marks()
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
                status = 'Pass' if te_mark >= 32 else 'Fail'
                if status == 'Fail':
                    credit_point = '-'
                    grade_point = '-'
                    total_mark = te_mark
                
                mark_data.append({
                    'ce_mark':ce_mark,
                    'te_mark':int(te_mark),
                    "total_mark": total_mark,
                    "credit":credit,
                    'grade_point':grade_point,
                    'credit_point': credit_point,
                    'stutus':status
                })
                
            total_credit = sum(mark['credit'] for mark in mark_data)
            total_mark = sum(mark['total_mark'] for mark in mark_data)
            is_ok =True
            overall_grade = '-'
            sgpa = '-'
            total_credit_point = '-'
            for i in mark_data:
                if i['stutus'] == 'Fail':
                    is_ok = False
            if is_ok :
                total_credit_point = sum(mark['credit_point'] for mark in mark_data)
                sgpa = round(total_credit_point / total_credit, 2) if total_credit else 0
                overall_grade = GradingSystem.objects.filter(
                    grade_range_from__lte=sgpa,
                    grade_range_to__gte=sgpa
                ).first().grade
                total_credit_point = round(total_credit_point, 2)
            
            items.append({
                "student": student.student.name,
                "reg_no": student.student.reg_no,
                'total_mark':total_mark,
                'total_credit_point':total_credit_point,
                'sgpa':sgpa,
                'overall_grade':overall_grade,
                "subjects_data": mark_data
            })
        for item in items:
            if item['overall_grade'] == '-':
                fail_count += 1
            else :
                pass_count += 1
        grade_count = Counter(item['overall_grade'] for item in items)
        grade_list = [grade for grade, count in grade_count.items()]
        count_list = [count for grade, count in grade_count.items()]
        total_marks_list = [item['total_mark'] for item in items]
        studens_list = [item['student'] for item in items]
        context["is_marklist"] = True
        context['is_batch_based_mark_list'] = True
        context["items"] = sorted(items, key=lambda x: x['sgpa'] if x['sgpa'] != '-' else 0, reverse=True)
        context["subjects"] = subjects
        context["batch"] = batch
        context["total_marks_list"] = total_marks_list
        context["students"] = studens_list
        context["grade_list"] = grade_list
        context["count_list"] = count_list
        context["pass_count"] = pass_count
        context["fail_count"] = fail_count
        context["title"] = f"Batch Based Mark List - {batch.course.name} - {batch.name}"
        
        return context

class GetCourseView(View):
    def get(self, request, *args, **kwargs):
        college_id = request.GET.get("college_id")
        queryset = Course.objects.filter(is_active=True)
        if college_id:
            queryset = queryset.filter(college_id=college_id)
        courses = list(queryset.values("id", "name"))
        return JsonResponse({"courses": courses})
    
class GetBatchView(View):
    def get(self, request, *args, **kwargs):
        course_id = request.GET.get("course_id")
        queryset = Batch.objects.filter(is_active=True)
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        batches = [{'id': x.id, 'name': x.__str__()} for x in queryset]
        return JsonResponse({"batches": batches})
    

def get_batch_filter(request):
    if request.method == 'POST':
        page_type = request.GET.get('page_type')
        batch = request.POST.get('batch')
        if page_type == 'batch_mark_list':
            return redirect(reverse('examination:batch_based_mark_list', args=[batch]))
    context ={
        'form': BatchFilterForm,
        'title': 'Filter Form',
        'is_marklist':True
    }
    return render(request, 'examination/batch_filter.html',context)