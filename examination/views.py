from django.shortcuts import render
from .create_pdf import PDFView
from . models import ExamStudent

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