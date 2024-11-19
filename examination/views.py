from django.shortcuts import render
from .create_pdf import PDFView
from . models import ExamStudent, GradingSystem, Student

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
        for student in students:
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
                "mark_data": mark_data
            }
            items.append(data)
        context["items"] = items
        return context