from django.contrib import admin

from .models import (
    About,
    Career,
    Contact,
    ContactUs,
    Corse,
    Department,
    DepartmentActivity,
    DepartmentContact,
    DepartmentFaculties,
    Event,
    Facilities,
    Gallery,
    Institution,
    InstitutionGallery,
    InstitutionTeam,
    JobApply,
    News,
    Spotlight,
    Team,
    Testimonial,
)

admin.site.register(Spotlight)
admin.site.register(About)
admin.site.register(Institution)
admin.site.register(Gallery)
admin.site.register(InstitutionGallery)
admin.site.register(News)
admin.site.register(Testimonial)
admin.site.register(Team)
admin.site.register(InstitutionTeam)
admin.site.register(Department)
admin.site.register(Corse)
admin.site.register(Facilities)
admin.site.register(Event)
admin.site.register(Contact)
admin.site.register(ContactUs)
# admin.site.register(JobApply)


class JobApplyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "career", "phone", "date_added", "email")


admin.site.register(JobApply, JobApplyAdmin)

admin.site.register(Career)
admin.site.register(DepartmentFaculties)
admin.site.register(DepartmentContact)
admin.site.register(DepartmentActivity)
