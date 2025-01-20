from django.db import models

# Create your models here.
class Student(models.Model):
    student_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    branch = models.CharField(max_length=200)


    def __str__(self) -> str:
        return self.name
    

# The __str__ method in a Django model is used to define the 
# human-readable representation of an object. It determines 
# what will be displayed when you print an instance of the model or 
# view it in the Django admin interface or the shell.