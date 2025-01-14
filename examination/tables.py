from core.base import BaseTable
from django_tables2 import columns

from .models import Certificate, ExamStudentMark


class  CertificateTable(BaseTable):
    action = columns.TemplateColumn(
        """
        <div class="btn-group">
        
        <a class="btn btn-default mx-1 btn-sm" title='Print' target="_blank" href="{{record.get_print_certificate}}"> <i class="fa fa-file-pdf-o"></i></a>
        <a class="btn btn-default mx-1 btn-sm" title='View' href="{{record.get_absolute_url}}"><i class="fa fa-eye"></i> </a>
        <a class="btn btn-default mx-1 btn-sm" title='Edit' href="{{record.get_update_url}}"><i class="fa fa-edit"></i> </a>
        <a class="btn btn-default mx-1 btn-sm" title='Delete' href="{{record.get_delete_url}}"><i class="fa fa-trash"></i> </a>
        
        </div>
        """,
        orderable=False,
    )
    class Meta:
        model = Certificate
        fields = ('reg_no_en',"name_en", "dob_en",'vrfcn_no','gender')
        attrs = {"class": "table border-0 table-hover table-striped "}

class  ExamStudentMarkTable(BaseTable):
    subject  = columns.TemplateColumn("""{{ record.subject.name }}""", orderable=False)
    student  = columns.TemplateColumn("""{{ record.student.student.name }}""", orderable=False)
    reg_no  = columns.TemplateColumn("""{{ record.student.student.reg_no }}""", orderable=False)
    t_mark = columns.TemplateColumn(
    """
    {% if record.te_mark is not None %}
    
        <span class="{% if record.te_mark >= '32' %}text-dark{% else %}text-danger{% endif %}" 
              style="font-weight: bold;">
            {{ record.te_mark }}
        </span>
    {% else %}
        N/A
    {% endif %}
    """,
    orderable=False
)

    class Meta:
        model = ExamStudentMark
        fields = ('reg_no',"student", "subject",'t_mark','ce_mark',)
        attrs = {"class": "table border-0 table-hover table-striped "}


