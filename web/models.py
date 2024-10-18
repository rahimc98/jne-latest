import uuid

from django.core.validators import RegexValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from versatileimagefield.fields import VersatileImageField

JOB_CHOICES = (("5", "Full Time"), ("10", "Part Time"))

IndianPhoneRegexValidator = RegexValidator(
    regex=r"^\+91\d{10}$",
    message="Invalid indian phone number with +91",
    code="invalid_phone_number",
)

PhoneRegexValidator = RegexValidator(
    r"^((\+91|91|0)[\- ]{0,1})?[456789]\d{9}$",
    message="Please Enter 10 digit mobile number or landline as 0<std code><phone number>",
    code="invalid_mobile",
)


class Spotlight(models.Model):
    image = VersatileImageField(upload_to="Spotlight")
    title = models.TextField()
    description = models.TextField()
    admission_year = models.TextField(blank=True, null=True)
    brochure = models.FileField(
        upload_to="Spotlight/files", max_length=254, blank=True, null=True
    )
    whatsapp_number = models.TextField(
        max_length=13, blank=True, null=True, validators=[IndianPhoneRegexValidator]
    )
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "spotlight"
        verbose_name = _("Home Banner")
        verbose_name_plural = _("Home Banners")

    def __str__(self):
        return self.title


class About(models.Model):
    title = models.TextField()
    description = models.TextField()
    our_mission = models.TextField()
    our_vision = models.TextField()
    is_deleted = models.BooleanField(default=False)
    team_description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "about"
        verbose_name = _("About")
        verbose_name_plural = _("About")

    def __str__(self):
        return self.title


class Institution(models.Model):
    image = VersatileImageField(upload_to="Institution")
    name = models.TextField(max_length=200)
    location = models.TextField()
    content = models.TextField()
    slug = models.SlugField(unique=True, blank=True, null=True, editable=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "institution"
        verbose_name = _("Institution")
        verbose_name_plural = _("Institutions")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Institution, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class InstitutionGallery(models.Model):
    institution = models.ForeignKey(
        Institution, limit_choices_to={"is_deleted": False}, on_delete=models.CASCADE
    )
    image_1 = VersatileImageField(
        upload_to="Institution Gallery", blank=True, null=True
    )
    image_2 = VersatileImageField(
        upload_to="Institution Gallery", blank=True, null=True
    )
    image_3 = VersatileImageField(
        upload_to="Institution Gallery", blank=True, null=True
    )
    image_4 = VersatileImageField(
        upload_to="Institution Gallery", blank=True, null=True
    )
    image_5 = VersatileImageField(
        upload_to="Institution Gallery", blank=True, null=True
    )
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "institution_gallery"
        verbose_name = _("Institution Gallery")
        verbose_name_plural = _("Institution Gallery")

    def __str__(self):
        return str(self.institution)


class Gallery(models.Model):
    institution = models.ForeignKey(
        Institution, limit_choices_to={"is_deleted": False}, on_delete=models.CASCADE
    )
    image = VersatileImageField(upload_to="Gallery")
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "gallery"
        verbose_name = _("Gallery")
        verbose_name_plural = _("Gallery")

    def __str__(self):
        return str(self.institution)


class News(models.Model):
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)
    image = VersatileImageField(upload_to="News")
    title = models.TextField()
    reporter = models.TextField(blank=True, null=True)
    content = models.TextField()
    date = models.DateField()
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "news"
        verbose_name = _("News")
        verbose_name_plural = _("News")
        ordering = ("-date_added",)

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    image = VersatileImageField(upload_to="Testimonials")
    name = models.TextField()
    description = models.TextField()
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "testimonial"
        verbose_name = _("Testimonial")
        verbose_name_plural = _("Testimonials")

    def __str__(self):
        return self.name


class Team(models.Model):
    image = VersatileImageField(upload_to="Teams")
    name = models.TextField()
    designation = models.TextField()
    description = models.TextField()
    instagram_url = models.URLField(max_length=200, blank=True, null=True)
    facebook_url = models.URLField(max_length=200, blank=True, null=True)
    twitter_url = models.URLField(max_length=200, blank=True, null=True)
    linkedin_url = models.URLField(max_length=200, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "management_team"
        verbose_name = _("Management Team")
        verbose_name_plural = _("Management Teams")

    def __str__(self):
        return self.name


class InstitutionTeam(models.Model):
    institution = models.ForeignKey(
        Institution, limit_choices_to={"is_deleted": False}, on_delete=models.CASCADE
    )
    image = VersatileImageField(upload_to="Teams")
    name = models.TextField()
    designation = models.TextField()
    description = models.TextField()
    instagram_url = models.URLField(max_length=200, blank=True, null=True)
    facebook_url = models.URLField(max_length=200, blank=True, null=True)
    twitter_url = models.URLField(max_length=200, blank=True, null=True)
    linkedin_url = models.URLField(max_length=200, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "institution_team"
        verbose_name = _("Institution Team")
        verbose_name_plural = _("Institution Teams")

    def __str__(self):
        return self.name


class Department(models.Model):
    institution = models.ForeignKey(
        Institution, limit_choices_to={"is_deleted": False}, on_delete=models.CASCADE
    )
    image = VersatileImageField(upload_to="Department")
    name = models.TextField()
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True, null=True, editable=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "department"
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Department, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class DepartmentActivity(models.Model):
    institution = models.ForeignKey(
        Institution, limit_choices_to={"is_deleted": False}, on_delete=models.CASCADE
    )
    image = VersatileImageField(upload_to="Activity")
    date = models.DateField()
    name = models.TextField()
    description = models.TextField()
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "department_activity"
        verbose_name = _("Department Activity")
        verbose_name_plural = _("Departments Activities")

    def __str__(self):
        return self.name


class DepartmentFaculties(models.Model):
    institution = models.ForeignKey(
        Institution, limit_choices_to={"is_deleted": False}, on_delete=models.CASCADE
    )
    department = models.ForeignKey(
        Department, limit_choices_to={"is_deleted": False}, on_delete=models.CASCADE
    )
    image = VersatileImageField(upload_to="Teams")
    name = models.TextField()
    designation = models.CharField(max_length=200)

    instagram_url = models.URLField(max_length=200, blank=True, null=True)
    facebook_url = models.URLField(max_length=200, blank=True, null=True)
    twitter_url = models.URLField(max_length=200, blank=True, null=True)
    linkedin_url = models.URLField(max_length=200, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "department_faculties"
        verbose_name = _("Department Faculties")
        verbose_name_plural = _("Department Faculties")

    def __str__(self):
        return self.name


class DepartmentContact(models.Model):
    institution = models.ForeignKey(
        Institution, limit_choices_to={"is_deleted": False}, on_delete=models.CASCADE
    )
    department = models.ForeignKey(
        Department, limit_choices_to={"is_deleted": False}, on_delete=models.CASCADE
    )
    phone = models.CharField(max_length=13)
    second_phone = models.CharField(max_length=13, blank=True, null=True)
    email = models.EmailField()
    second_email = models.EmailField(blank=True, null=True)
    location = models.TextField()

    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "department_contact"
        verbose_name = _("Department Contact")
        verbose_name_plural = _("Department Contacts")

    def __str__(self):
        return self.email


class Corse(models.Model):
    institution = models.ForeignKey(
        Institution, limit_choices_to={"is_deleted": False}, on_delete=models.CASCADE
    )
    image = VersatileImageField(upload_to="Teams")
    name = models.TextField()
    description = models.TextField()
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "corse"
        verbose_name = _("Corse")
        verbose_name_plural = _("Corses")

    def __str__(self):
        return self.name


class Facilities(models.Model):
    institution = models.ForeignKey(
        Institution, limit_choices_to={"is_deleted": False}, on_delete=models.CASCADE
    )
    department = models.ForeignKey(
        Department, limit_choices_to={"is_deleted": False}, on_delete=models.CASCADE
    )
    image = VersatileImageField(upload_to="Teams")
    name = models.TextField()
    description = models.TextField()
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "facilities"
        verbose_name = _("Facilities")
        verbose_name_plural = _("Facilities")

    def __str__(self):
        return self.name


class Event(models.Model):
    institution = models.ForeignKey(
        Institution, limit_choices_to={"is_deleted": False}, on_delete=models.CASCADE
    )
    date = models.DateField()
    image = VersatileImageField(upload_to="Teams")
    name = models.TextField()
    description = models.TextField()
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "events"
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    def __str__(self):
        return self.name


class InstituteTestimonial(models.Model):
    institution = models.ForeignKey(
        Institution, limit_choices_to={"is_deleted": False}, on_delete=models.CASCADE
    )
    image = VersatileImageField(upload_to="Testimonials")
    name = models.TextField()
    description = models.TextField()
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "institute_testimonial"
        verbose_name = _("Institute Testimonial")
        verbose_name_plural = _("Institute Testimonials")

    def __str__(self):
        return self.name


class Career(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)
    job_type = models.CharField(max_length=20, choices=JOB_CHOICES)
    designation = models.CharField(max_length=200)
    location = models.CharField(max_length=20)
    description = models.TextField()

    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "career"
        verbose_name = _("Career")
        verbose_name_plural = _("Careers")
        ordering = ("-date_added",)

    def __str__(self):
        return self.designation


class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField()

    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "contact"
        verbose_name = _("Contact")
        verbose_name_plural = _("Contact")
        ordering = ("-date_added",)

    def __str__(self):
        return self.name


class ContactUs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=20, validators=[PhoneRegexValidator])
    email = models.EmailField()
    location = models.CharField(max_length=200, blank=True, null=True)
    instagram_url = models.URLField(max_length=200, blank=True, null=True)
    facebook_url = models.URLField(max_length=200, blank=True, null=True)
    twitter_url = models.URLField(max_length=200, blank=True, null=True)
    linkedin_url = models.URLField(max_length=200, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    footer_about = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "contact_us"
        verbose_name = _("Contact Us")
        verbose_name_plural = _("Contact Us")

    def __str__(self):
        return self.email


class JobApply(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    career = models.ForeignKey(
        Career, limit_choices_to={"is_deleted": False}, on_delete=models.CASCADE
    )
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    cv = models.FileField()

    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "job_apply"
        verbose_name = _("Job Apply")
        verbose_name_plural = _("Job Apply")
        ordering = ("-date_added",)

    def __str__(self):
        return self.name
