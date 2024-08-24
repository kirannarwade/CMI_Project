from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UploadFileDataForm
from django.contrib.auth import logout
from django.contrib import messages
from django.views import View
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .models import CompanyData
import csv
import chardet
import pandas as pd
import io

# Create your views here.


@login_required(login_url='/login/')
def index(request):
    return render(request, 'index.html')

@login_required(login_url='/login/')
def upload_data(request):
    form = UploadFileDataForm()
    return render(request, 'upload_data.html', {'form':form})


def detect_encoding(file):
    # Read the first few bytes to detect encoding
    file.seek(0)
    result = chardet.detect(file.read(10000))  # Read first 10KB to detect encoding
    file.seek(0)
    return result['encoding']

class UploadFileData(View):
    def get(self, request):
        form = UploadFileDataForm()
        return render(request, 'upload_data.html', {'form':form})
    
    def post(self, request):
        form = UploadFileDataForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']

            file_content = uploaded_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(file_content)


            # df = pd.read_csv(uploaded_file, encoding='utf-8')
            for row in reader:
                CompanyData.objects.update_or_create(
                    name=row['name'],
                    defaults={
                        'domain': row['domain'],
                        'year_founded': int(row['year founded']),
                        'industry': row['industry'],
                        'size_range': row['size range'],
                        'locality': row['locality'],
                        'country': row['country'],
                        'linkedin_url': row['linkedin url'],
                        'current_employee_estimate': int(row['current employee estimate']),
                        'total_employee_estimate': int(row['total employee estimate']),
                    }
                )
            return render(request, 'index.html')

        else:
            form.add_error('file', 'Invalid file format or file size exceeds limit.')
        return render(request, 'upload_data.html', {'form': form})

@login_required(login_url='/login/')
def query_builder(request):
    return render(request, 'query_builder.html')

@login_required(login_url='/login/')
def users_info(request):
    return render(request, 'users_info.html')



class CustomerRegistrationView(View):
    def get(self, request):
        try:
            form = UserRegistrationForm()
            return render(request, 'signup.html', {'form':form})
        except Exception as err:
            print(err)

    def post(self, request):
        try:
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                messages.success(request, "Account Register Successfully!")
                form.save()
            return render(request, 'signup.html', {'form':form})
        except Exception as err:
            print(err)


@login_required(login_url='/login/')
def logoutUser(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('/login')
