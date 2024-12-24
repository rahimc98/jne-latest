from web.models import ContactUs, Institution, News
from django.conf import settings

def main_context(request):

    latest_news = News.objects.filter(is_deleted=False).order_by("date").last()
    institution = Institution.objects.filter(is_deleted=False)
    contact_us = ContactUs.objects.filter(is_deleted=False).first()
    current_employee = None
    name = None
    
    app_settings = settings.APP_SETTINGS
   
    if request.user.is_authenticated:
        current_employee = request.user
        name = current_employee.username
        
    return {
        "latest_news": latest_news,
        "institution": institution,
        "contact_us": contact_us,
        "current_employee": current_employee,
        "default_user_avatar": f"https://ui-avatars.com/api/?name={name}&background=fdc010&color=fff&size=128",
        "app_settings": app_settings,
    }
