from django.db import models
from django.conf import settings
from routine import helpers


class Routine(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, max_length=110)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        created = self.id is None

        # Generate a slug if the routine is being created
        if created:
            self.slug = helpers.generate_slug_for_routine(self.name, Routine)

        super().save(*args, **kwargs)


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
    subject = models.CharField(max_length=30)
    teacher_short_name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.subject} on {self.day} in {self.routine.name}"
