from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f'{self.name}'


class Lesson(models.Model):
    date = models.DateTimeField()
    is_remote = models.BooleanField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey("User.User", on_delete=models.PROTECT, limit_choices_to={'user_type': 'Teacher'})
    number = models.IntegerField()
    homework_url = models.URLField(max_length=300) # this is url, maybe use another type
    homework_deadline = models.DateTimeField()


class Homework_submission(models.Model):
    student = models.ForeignKey("User.User", on_delete=models.CASCADE, limit_choices_to={'user_type': 'Student'})
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    submission_datetime = models.DateTimeField(auto_now_add=True)
    result = models.PositiveIntegerField()
    feedback = models.TextField(null=False, blank=True)
    submission_datetime = models.DateTimeField(auto_now_add=True)

class Atachments(models.Model):
    type = models.CharField(max_length=100)
    url = models.URLField(max_length=200) # this is url, maybe use another type
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)




