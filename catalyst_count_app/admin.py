from django.contrib import admin
from .models import CompanyData

# Register your models here.

@admin.register(CompanyData)
class CompanyDataAdmin(admin.ModelAdmin):
    # list_display = ['id' ,'name', 'domain', 'year_founded', 'industry']
    list_display = [field.name for field in CompanyData._meta.fields]
