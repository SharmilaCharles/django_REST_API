from django.db import models

class Employee(models.Model):
    emp_id= models.CharField(max_length=50)
    emp_name = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.emp_name