from django.db import models
from django.conf import settings

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='course_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='lessons/videos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    date_enrolled = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"
