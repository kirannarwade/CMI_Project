from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UploadFileDataForm, FilterForm
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
from io import TextIOWrapper
from django.db import transaction
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator


# Create your views here.


@login_required(login_url='/login/')
def index(request):
    try:
        return render(request, 'index.html')
    except Exception as err:
        print('err at index ', err)

@login_required(login_url='/login/')
def upload_data(request):
    try:
        form = UploadFileDataForm()
        return render(request, 'upload_data.html', {'form':form})
    except Exception as err:
        print('err at upload_data ', err)


@method_decorator(login_required, name='dispatch')
class UploadFileData(View):
    def get(self, request):
        try:
            form = UploadFileDataForm()
            return render(request, 'upload_data.html', {'form':form})
        except Exception as err:
            print('err at UploadFileData ', err)
    
    def post(self, request):
        try:
            form = UploadFileDataForm(request.POST, request.FILES)
            if form.is_valid():
                CompanyData.objects.all().delete()
                uploaded_file = form.cleaned_data['file']

                # file_content = uploaded_file.read().decode('utf-8').splitlines()
                # reader = csv.DictReader(file_content)

                file_data = TextIOWrapper(uploaded_file.file, encoding='ISO-8859-1')

                my_df = pd.read_csv(file_data)
                df = my_df.dropna()


                company_data_instances = [
                    CompanyData(
                        name=row['name'],
                        domain=row['domain'],
                        year_founded=int(row['year founded']) if pd.notnull(row['year founded']) else None,
                        industry=row['industry'],
                        size_range=row['size range'],
                        locality=row['locality'],
                        country=row['country'],
                        linkedin_url=row['linkedin url'],
                        current_employee_estimate=int(row['current employee estimate']) if pd.notnull(
                            row['current employee estimate']) else None,
                        total_employee_estimate=int(row['total employee estimate']) if pd.notnull(
                            row['total employee estimate']) else None,
                    )
                    for index, row in df.iterrows()
                ]

                with transaction.atomic():
                    CompanyData.objects.bulk_create(company_data_instances)
                
                messages.success(request, "File Uploaded Succesfully you can query filter")
                return redirect('/query-builder/')

            else:
                form.add_error('file', 'Invalid file format or file size exceeds limit.')
            return render(request, 'upload_data.html', {'form': form})
        except Exception as err:
            print('err at UploadFileData ', err)

@login_required(login_url='/login/')
def query_builder(request, my_flg=False):
    try:
        queryset = CompanyData.objects.all()

        if request.method == 'POST':
            form = FilterForm(request.POST)
            if form.is_valid():
                industry = form.cleaned_data.get('industry')
                city = form.cleaned_data.get('city')
                state = form.cleaned_data.get('state')
                country = form.cleaned_data.get('country')

                if industry:
                    queryset = queryset.filter(industry=industry)
                if city:
                    queryset = queryset.filter(locality=city)
                if state:
                    queryset = queryset.filter(state=state)
                if country:
                    queryset = queryset.filter(country=country)

                count = queryset.count()
            else:
                count = 0
            messages.success(request, f"{count} records found for the query")


        else:
            form = FilterForm()
            count = 0

        return render(request, 'query_builder.html', {
            'form': form,
            'count': count,
        })
    except Exception as err:
        print('err at query_builder ', err)




@login_required(login_url='/login/')
def users_info(request):
    try:
        user_data = User.objects.all()
        return render(request, 'users_info.html', {'user_data':user_data})
    except Exception as err:
        print('err at users_info ', err)



class CustomerRegistrationView(View):
    def get(self, request):
        try:
            form = UserRegistrationForm()
            return render(request, 'signup.html', {'form':form})
        except Exception as err:
            print('err at CustomerRegistrationView ', err)

    def post(self, request):
        try:
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                messages.success(request, "Account Register Successfully!")
                form.save()
            return render(request, 'signup.html', {'form':form})
        except Exception as err:
            print('err at CustomerRegistrationView ', err)


@login_required(login_url='/login/')
def logoutUser(request):
    try:
        logout(request)
        messages.success(request, "Logout Successfully")
        return redirect('/login')
    except Exception as err:
        print('err at logoutUser ', err)