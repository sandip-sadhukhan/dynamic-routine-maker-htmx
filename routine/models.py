from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Routine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.id is None:
            self.slug = slugify(self.name)

        super(Routine, self).save(*args, **kwargs)
    

class Class(models.Model):
    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6

    day_choices = (
        (SUNDAY, "Sunday"),
        (MONDAY, "Monday"),
        (TUESDAY, "Tuesday"),
        (WEDNESDAY, "Wednesday"),
        (THURSDAY, "Thursday"),
        (FRIDAY, "Friday"),
        (SATURDAY, "Saturday"),
    )

    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
    day = models.PositiveIntegerField(choices=day_choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject = models.CharField(max_length=100)
    teacher_short_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.subject} on {self.day} in {self.routine.name}"
