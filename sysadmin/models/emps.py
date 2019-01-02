from django.contrib.auth.models import User
from django.db import models
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    def __str__(self):
        return "emps"
    class Meta:
        db_table = "emps"