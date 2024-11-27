from django.contrib import admin
from django.shortcuts import redirect
from import_export.admin import ImportExportModelAdmin
from django.contrib import messages
from django.utils.translation import ngettext
from . models import *
# Register your models here.

def mark_inactive(self, request, queryset):
    updated = queryset.update(is_active=False)
    self.message_user(request, ngettext("%d item was successfully marked as deleted.", "%d items were successfully marked as deleted.", updated) % updated, messages.SUCCESS)


def mark_active(self, request, queryset):
    updated = queryset.update(is_active=True)
    self.message_user(request, ngettext("%d item was successfully marked as active.", "%d items were successfully marked as active.", updated) % updated, messages.SUCCESS)


def export_to_halticket(modeladmin, request, queryset):
    selected_ids = list(queryset.values_list('id', flat=True))
    request.session['selected_ids'] = selected_ids
    messages.success(request, f"{len(selected_ids)} objects selected.")
    return redirect('examination:halticket')

def export_to_gradecard(modeladmin, request, queryset):
    selected_ids = list(queryset.values_list('student__id', flat=True))
    request.session['selected_ids'] = selected_ids
    messages.success(request, f"{len(selected_ids)} objects selected.")
    return redirect('examination:gradecard')


def export_to_exam_applied(modeladmin, request, queryset):
    selected_ids = list(queryset.values_list('id', flat=True))
    request.session['selected_ids'] = selected_ids
    messages.success(request, f"{len(selected_ids)} objects selected.")
    return redirect('examination:exam_applied')

def export_to_exam_applied_batch_based(modeladmin, request, queryset):
    selected_ids = list(queryset.values_list('id', flat=True))
    request.session['selected_ids'] = selected_ids
    messages.success(request, f"{len(selected_ids)} objects selected.")
    return redirect('examination:exam_applied_batch_based')

class BaseAdmin(ImportExportModelAdmin):
    list_display = ("__str__","is_active")
    list_filter = ("is_active",)
    actions = [mark_active, mark_inactive]
    readonly_fields = ( "pk",)
    search_fields = ("pk",)

    def render_change_form(self, request, context, add=False, change=False, form_url="", obj=None):
        context.update({"show_save_and_continue": False, "show_save_and_add_another": True})
        return super().render_change_form(request, context, add, change, form_url, obj)

    class Media:
        css = {"all": ("extra_admin/css/admin.css",)}

@admin.register(College)
class CollegeAdmin(BaseAdmin):
    pass

@admin.register(GradingSystem)
class GradingSystemAdmin(BaseAdmin):
    list_filter = ("interpretation",)
    list_display = ("id","marks_range_from",'marks_range_to','grade','interpretation')


@admin.register(Batch)
class BatchAdmin(BaseAdmin):
    list_filter = ("is_active",'course','course__type')
    list_display = ("__str__","course",'name')

    def get_actions(self, request):
        actions = super().get_actions(request)
        if request.user.is_superuser:
            actions['export_to_exam_applied_batch_based'] = (export_to_exam_applied_batch_based, 'export_to_exam_applied_batch_based', 'Export to Exam Applied List')
        else:
            # Remove actions for non-superusers
            actions.pop('export_to_exam_applied_batch_based', None)
        return actions

@admin.register(Course)
class CourseAdmin(BaseAdmin):
    list_filter = ("is_active",'college','type')
    list_display = ("id","college",'name','code','type')


@admin.register(Examination)
class ExaminationAdmin(BaseAdmin):
    list_filter = ("is_active",'batch')
    list_display = ("id","batch",'name')


@admin.register(Student)
class StudentAdmin(BaseAdmin):
    list_filter = ("is_active",'course')
    list_display = ("id","course",'reg_no','name','dob')
    search_fields = ("reg_no","name")


@admin.register(Subject)
class SubjectAdmin(BaseAdmin):
    list_filter = ("is_active",'batch')
    list_display = ("id","batch",'name','course_code','credit_score')


@admin.register(ExamStudentMark)
class ExamStudentMarkAdmin(BaseAdmin):
    list_filter = ("is_active",'subject__batch','subject')
    list_display = ("id","student",'subject','te_mark','ce_mark')
    list_per_page = 500
    search_fields = ("student__student__reg_no","student__student__name")
    list_editable = ('subject','ce_mark','te_mark')

@admin.register(ExamStudent)
class ExamStudentAdmin(BaseAdmin):
    list_filter = ("is_active",'student__course','exam__batch')
    list_display = ("id","student",'exam')

    def get_actions(self, request):
        actions = super().get_actions(request)
        if request.user.is_superuser:
            actions['export_to_halticket'] = (export_to_halticket, 'export_to_halticket', 'Export to Hallticket')
            actions['export_to_gradecard'] = (export_to_gradecard, 'export_to_gradecard', 'Export to Grade Card')
        else:
            # Remove actions for non-superusers
            actions.pop('export_to_halticket', None)
            actions.pop('export_to_gradecard', None)
        return actions

@admin.register(ExamApply)
class ExamApplyAdmin(BaseAdmin):
    list_filter = ("is_active",'exam_type','subject__batch','subject')
    list_display = ("get_student_reg_no","get_student_name",'subject','exam_type','amount')

    def get_student_name(self, obj):
        return obj.student.student.name if obj.student and obj.student.student else None
    def get_student_reg_no(self, obj):
        return obj.student.student.reg_no if obj.student and obj.student.student else None
    get_student_reg_no.short_description = "Register Number"
    get_student_name.short_description = "Student"

    def get_actions(self, request):
        actions = super().get_actions(request)
        if request.user.is_superuser:
            actions['export_to_exam_applied'] = (export_to_exam_applied, 'export_to_exam_applied', 'Export to Exam Applied List')
        else:
            # Remove actions for non-superusers
            actions.pop('export_to_exam_applied', None)
        return actions

