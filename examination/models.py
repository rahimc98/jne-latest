from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class College(models.Model):
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    college = models.ForeignKey(College,limit_choices_to={"is_active": True}, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    def __str__(self):
        return f'{self.code}'



class Batch(models.Model):
    course = models.ForeignKey(Course,limit_choices_to={"is_active": True}, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Batch")
        verbose_name_plural = _("Batches")

    def __str__(self):
       return f'{self.course.code} - {self.code}'
    
    def get_subjects(self):
        return Subject.objects.filter(is_active=True,batch=self)
    
    def get_examinations(self):
        return Examination.objects.filter(is_active=True)
    


class Examination(models.Model):
    batch = models.ForeignKey(Batch,limit_choices_to={"is_active": True}, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Examination")
        verbose_name_plural = _("Examinations")

    def __str__(self):
        return f'{self.name}'
    

class Student(models.Model):
    course = models.ForeignKey(Course,limit_choices_to={"is_active": True}, on_delete=models.CASCADE)
    reg_no = models.CharField('Register Number',max_length=200)
    name = models.CharField(max_length=200)
    dob = models.DateField('Date of Birth',default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")

    def __str__(self):
        return self.name
    

class Subject(models.Model):
    batch = models.ForeignKey(Batch,limit_choices_to={"is_active": True}, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")
        ordering = ('id',)

    def __str__(self):
        return self.name
    

class ExamStudent(models.Model):
    student = models.ForeignKey(Student,limit_choices_to={"is_active": True}, on_delete=models.CASCADE)
    exam = models.ForeignKey(Examination,limit_choices_to={"is_active": True}, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Exam Student")
        verbose_name_plural = _("Exam Students")

    def __str__(self):
        return f'{self.exam} - {self.student.reg_no}'