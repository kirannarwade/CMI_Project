from django.db import models

# Create your models here.


class CompanyData(models.Model):
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)
    year_founded = models.IntegerField()
    industry = models.CharField(max_length=100)
    size_range = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    linkedin_url = models.URLField()
    current_employee_estimate = models.IntegerField()
    total_employee_estimate = models.IntegerField()

    def __str__(self) -> str:
        return f'Company name is {self.name}'