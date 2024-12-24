from core.base import BaseTable
from django_tables2 import columns

from .models import ExamStudentMark


class  ExamStudentMarkTable(BaseTable):
    subject  = columns.TemplateColumn("""{{ record.subject.name }}""", orderable=False)
    student  = columns.TemplateColumn("""{{ record.student.student.name }}""", orderable=False)
    reg_no  = columns.TemplateColumn("""{{ record.student.student.reg_no }}""", orderable=False)
    class Meta:
        model = ExamStudentMark
        fields = ('reg_no',"student", "subject",'te_mark','ce_mark',)
        attrs = {"class": "table border-0 table-hover table-striped "}


