from django.db import models

class Student(models.Model):
    roll = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)

    tamil = models.IntegerField()
    english = models.IntegerField()
    maths = models.IntegerField()
    science = models.IntegerField()
    social = models.IntegerField()

    def total(self):
        return self.tamil + self.english + self.maths + self.science + self.social

    def percentage(self):
        return self.total() / 5

    def status(self):
        marks = [self.tamil, self.english, self.maths, self.science, self.social]
        return "FAIL" if any(m < 35 for m in marks) else "PASS"

    def grade(self):
        p = self.percentage()
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
