from django.shortcuts import get_object_or_404, render
from .create_pdf import PDFView
from django.db.models import Sum
from . models import ExamApply, ExamStudent, GradingSystem, Student

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
        return context