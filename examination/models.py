from django.db import models
from django.urls import reverse_lazy
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
    
    def get_exam_student(self):
        return ExamStudent.objects.filter(student=self).last()
    
    def get_print_grade_card(self):
        return reverse_lazy("examination:grademark", kwargs={"pk": self.pk})
    

    

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
        return self.name
    

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
        return f'{self.exam} - {self.student.reg_no}'
    
    def get_exam_marks(self):
        return ExamStudentMark.objects.filter(student=self)
    

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
    