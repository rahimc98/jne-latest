from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from core.functions import generate_fields

class College(models.Model):
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_fields(self):
        return generate_fields(self)

    @staticmethod
    def get_list_url():
        return reverse_lazy("examination:college_list")

    def get_absolute_url(self):
        return reverse_lazy("examination:college_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse_lazy("examination:college_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("examination:college_delete", kwargs={"pk": self.pk})
    
    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()
        


class Course(models.Model):
    college = models.ForeignKey(College,limit_choices_to={"is_active": True}, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    type = models.CharField(max_length=200,choices = (("pre_fadheela","pre_fadheela"),("UG","Under Graduate"),("PG","Post Graduate"),("Other","Other")),default='UG')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    def __str__(self):
        return f'{self.code}'
    
    @staticmethod
    def get_list_url():
        return reverse_lazy("examination:course_list")

    def get_absolute_url(self):
        return reverse_lazy("examination:course_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse_lazy("examination:course_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("examination:course_delete", kwargs={"pk": self.pk})

    def get_fields(self):
        return generate_fields(self)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()
    
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
        return Subject.objects.filter(is_active=True,batch=self).order_by('id')
    
    def get_examinations(self):
        return Examination.objects.filter(is_active=True)
    
    def get_exam(self):
        return Examination.objects.filter(is_active=True,batch=self).last()

    @staticmethod
    def get_list_url():
        return reverse_lazy("examination:batch_list")

    def get_absolute_url(self):
        return reverse_lazy("examination:batch_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse_lazy("examination:batch_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("examination:batch_delete", kwargs={"pk": self.pk})

    def get_fields(self):
        return generate_fields(self)
    
    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

class Examination(models.Model):
    batch = models.ForeignKey(Batch,limit_choices_to={"is_active": True}, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Examination")
        verbose_name_plural = _("Examinations")

    def __str__(self):
        return f'{self.name}'

    @staticmethod
    def get_list_url():
        return reverse_lazy("examination:examination_list")

    def get_absolute_url(self):
        return reverse_lazy("examination:examination_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse_lazy("examination:examination_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("examination:examination_delete", kwargs={"pk": self.pk})  

    def get_fields(self):
        return generate_fields(self)
    
    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()
    
class Student(models.Model):
    course = models.ForeignKey(Course,limit_choices_to={"is_active": True}, on_delete=models.CASCADE)
    reg_no = models.CharField('Register Number',max_length=200)
    name = models.CharField(max_length=200)
    dob = models.DateField('Date of Birth',default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")
        ordering = ['id']

    def __str__(self):
        return self.name
    
    def get_exam_student(self):
        return ExamStudent.objects.filter(student=self).last()
    
    def get_print_grade_card(self):
        return reverse_lazy("examination:grademark", kwargs={"pk": self.pk})

    
    @staticmethod
    def get_list_url():
        return reverse_lazy("examination:student_list")

    def get_absolute_url(self):
        return reverse_lazy("examination:student_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse_lazy("examination:student_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("examination:student_delete", kwargs={"pk": self.pk})
    
    def get_fields(self):
        return generate_fields(self)
    
    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

class Subject(models.Model):
    batch = models.ForeignKey(Batch,limit_choices_to={"is_active": True}, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    course_code = models.CharField(max_length=200,blank=True,null=True)
    credit_score = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")
        ordering = ('id',)

    def __str__(self):
        return f'{self.name}-{self.batch}'

    @staticmethod
    def get_list_url():
        return reverse_lazy("examination:subject_list")

    def get_absolute_url(self):
        return reverse_lazy("examination:subject_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse_lazy("examination:subject_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("examination:subject_delete", kwargs={"pk": self.pk})
    
    def get_fields(self):
        return generate_fields(self)
    
    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()
class ExamStudent(models.Model):
    student = models.ForeignKey(Student,limit_choices_to={"is_active": True}, on_delete=models.CASCADE)
    exam = models.ForeignKey(Examination,limit_choices_to={"is_active": True}, on_delete=models.CASCADE)
    no_of_days = models.IntegerField(default=0)
    attentence = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Exam Student")
        verbose_name_plural = _("Exam Students")

    def __str__(self):
        return f'{self.student} - {self.student.reg_no}'
    
    def get_exam_marks(self):
        return ExamStudentMark.objects.filter(student=self).order_by('subject')
    
    @staticmethod
    def get_list_url():
        return reverse_lazy("examination:examstudent_list")

    def get_absolute_url(self):
        return reverse_lazy("examination:examstudent_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse_lazy("examination:examstudent_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("examination:examstudent_delete", kwargs={"pk": self.pk})
    
    def get_fields(self):
        return generate_fields(self)
    
    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

class ExamStudentMark(models.Model):
    student = models.ForeignKey(ExamStudent,limit_choices_to={"is_active": True}, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,limit_choices_to={"is_active": True}, on_delete=models.CASCADE)
    te_mark = models.CharField(max_length=10) 
    ce_mark = models.CharField(max_length=10) 
    is_active = models.BooleanField(default=True) 
    class Meta:
        verbose_name = _("Exam Student Mark")
        verbose_name_plural = _("Exam Student Marks")

    def __str__(self):
        return f'{self.student} - {self.subject} (TE: {self.te_mark}, CE: {self.ce_mark})'
    
    def get_fields(self):
        return generate_fields(self)

    @staticmethod
    def get_list_url():
        return reverse_lazy("examination:examstudentmark_list")

    def get_absolute_url(self):
        return reverse_lazy("examination:examstudentmark_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse_lazy("examination:examstudentmark_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("examination:examstudentmark_delete", kwargs={"pk": self.pk})

    def get_fields(self):
        return generate_fields(self)
    
    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()
    
class GradingSystem(models.Model):
    COMMENT_STATUS = (
        ("Outstanding", "Outstanding"),
        ("Excellent", "Excellent"),
        ("Very Good", "Very Good"),
        ("Good", "Good"),
        ("Satisfactory", "Satisfactory"),
        ("Average", "Average"),
        ("Pass", "Pass"),
        ("Failure", "Failure"),
    )
    marks_range_from =models.IntegerField()
    marks_range_to = models.IntegerField()
    grade = models.CharField(max_length=5)
    interpretation = models.CharField(max_length=20,choices=COMMENT_STATUS)
    grade_range_from =models.FloatField(default=0)
    grade_range_to = models.FloatField(default=0) 

    def __str__(self):
        return f"{self.grade}"
    
    def get_fields(self):
        return generate_fields(self)
    
    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()
    

class ExamApply(models.Model):
    student = models.ForeignKey(ExamStudent,limit_choices_to={"is_active": True}, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,limit_choices_to={"is_active": True}, on_delete=models.CASCADE)
    exam_type = models.CharField(max_length=20,choices=(("Improvement","Improvement"),("Supplementary","Supplementary")))
    amount = models.FloatField(default=200)
    is_active = models.BooleanField(default=True) 
    class Meta:
        verbose_name = _("Exam Apply")
        verbose_name_plural = _("Exam Applies")

    def __str__(self):
        return f'{self.student} - {self.subject} - {self.exam_type}'
    
    def get_fields(self):
        return generate_fields(self)
    
    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()



class Certificate(models.Model):
    name_ar = models.CharField(max_length=200)
    dob_ar = models.CharField(max_length=200)
    ay_ar = models.CharField(max_length=200)
    eh_ar = models.CharField(max_length=200)
    reg_no_ar = models.CharField(max_length=200)
    gd_ar = models.CharField(max_length=200)
    senet_ar = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200)
    dob_en = models.CharField(max_length=200)
    ay_en = models.CharField(max_length=200)
    eh_en = models.CharField(max_length=200)
    reg_no_en = models.CharField(max_length=200)
    gd_en = models.CharField(max_length=200)
    senet_en = models.CharField(max_length=200)
    vrfcn_no = models.CharField(max_length=200)
    crtfct_no = models.CharField(max_length=200)
    gender = models.CharField(max_length=10,choices=(('male', 'Male'), ('female', 'Female')))
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name_en
    
    def get_web_url(self):
        return reverse_lazy("examination:certificate_detail", kwargs={"pk": self.pk})
    
    