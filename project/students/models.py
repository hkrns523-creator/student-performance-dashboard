from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Student(models.Model):
    roll = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)

    tamil = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    english = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    maths = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    science = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    social = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    @property
    def total(self):
        return self.tamil + self.english + self.maths + self.science + self.social

    @property
    def percentage(self):
        return self.total / 5

    @property
    def status(self):
        marks = [self.tamil, self.english, self.maths, self.science, self.social]
        return "FAIL" if any(m < 35 for m in marks) else "PASS"

    @property
    def grade(self):
        p = self.percentage
        if p >= 90:
            return "A+"
        elif p >= 80:
            return "A"
        elif p >= 70:
            return "B"
        elif p >= 60:
            return "C"
        elif p >= 50:
            return "D"
        elif p >= 35:
            return "E"
        else:
            return "F"
