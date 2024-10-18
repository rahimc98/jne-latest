from web.models import ContactUs, Institution, News


def main_context(request):

    latest_news = News.objects.filter(is_deleted=False).order_by("date").last()
    institution = Institution.objects.filter(is_deleted=False)
    contact_us = ContactUs.objects.filter(is_deleted=False).first()

    return {
        "latest_news": latest_news,
        "institution": institution,
        "contact_us": contact_us,
    }
