from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from .forms import LoginDetailsForm
from .models import LoginDetails
import pandas as pd
import csv 
from django.utils import timezone
# from django.core.exceptions import ValidationError
from django.contrib import messages
# from django.utils.timezone import make_aware
from django.utils.text import slugify
from datetime import datetime
from io import BytesIO
from django.db.models.functions import TruncDate
from django.db.models import Q
# Create your views here.


def import_login_details(request):
    if request.method == 'POST':
        form = LoginDetailsForm(request.POST, request.FILES)
        # print(form)
        if form.is_valid():
            file = request.FILES['File']
            if file.name.endswith('.xlsx') or file.name.endswith('.xls'):
                # df = pd.read_excel(file)
                try:
                    df = pd.read_excel(file, parse_dates=['Log Date'], date_parser=lambda x: timezone.make_aware(pd.to_datetime(x), timezone=timezone.get_default_timezone()))
                # df = pd.read_excel(file, parse_dates=['Log Date'], date_parser=lambda x: pd.to_datetime(x, format='%d-%b-%Y %H:%M:%S'))
                except:
                    return HttpResponse("<script>alert('Data does not match');history.back();</script>")


                # print(df)
                csv_data = df.to_csv(index=False)
                # print(csv_data)

                # Save CSV data to a temporary file

                try:
                    with open('temp_data.csv', 'x') as temp_file_path:
                        temp_file_path.write('This file will only be created if it does not exist.')
                except FileExistsError:
                    print('The file already exists. Choose a different filename or open it in a different mode.')
                
                temp_file_path = 'temp_data.csv'
            
                with open(temp_file_path, 'w') as temp_file:
                    temp_file.write(csv_data)
                     

                # Read the CSV file into a Pandas DataFrame
                df_csv = pd.read_csv(temp_file_path)
                # print(df_csv)
                success=0
                duplicate=0
                # Iterate over the DataFrame rows and create or update LoginDetails objects
                for index, row in df_csv.iterrows():
                    login_date = row['Log Date']
                    emp_code = row['Employee Code']
                    emp_name = row['Employee Name']
                    company = row['Company']
                    department = row['Department']

                    # Attempt to get the object, create if it doesn't exist
                    login_details, created = LoginDetails.objects.get_or_create(
                        login_date=login_date,
                        defaults={
                            'Emp_code': 'IND-'+str(emp_code),
                            'emp_name': emp_name,
                            'company': company,
                            'department': department,
                        }
                    )
                    
                    # print(created)
                    

                    # If the object already exists, update the fields
                    if not created:
                        duplicate+=1
                        login_details.Emp_code = 'IND-'+str(emp_code)
                        login_details.emp_name = emp_name
                        login_details.company = company
                        login_details.department = department
                        login_details.save()
                        data = False
                        
                    else:
                        success+=1
                        data=True

                import os

                # Save the DataFrame to an Excel file in a folder
                folder_path = 'F:\Assignment_new\Work\myproject\Login_data'
                os.makedirs(folder_path, exist_ok=True)
                file_name = f"LoginData_{slugify(datetime.now())}.xlsx"

                excel_file_path = os.path.join(folder_path, file_name)
                df['Log Date'] = df['Log Date'].dt.tz_localize(None)

                df.to_excel(excel_file_path, index=False)


                # Clean up: remove the temporary CSV file
                os.remove(temp_file_path)
                # print('success',success)
                # print('dup',duplicate)
                if data==True:
                    messages.success(request, 'Uploaded Successfully')
                    return redirect(view_login_datas)
                else:
                    messages.success(request, f'Uploaded Successfully.{duplicate} Duplicates entries have not been inserted')
                    return redirect(view_login_datas)
            else:
                return HttpResponse("<script>alert('Only support .xls and .xlsx files');history.back();</script>")
                
                
    # else:
    #     form = LoginDetailsForm()
    #     return render(request, 'import_login_details.html', {'form': form})
    


def view_login_datas(request):
    log_data=LoginDetails.objects.all()
    form = LoginDetailsForm()
    return render(request,'view_login_details.html',{'log_datas':log_data,'form': form})


def export_to_excel(request):
        try:
            data = LoginDetails.objects.values('login_date', 'Emp_code','emp_name','company','department')
            if not data:
                raise
        except:
            return HttpResponse("<script>alert('No data to export');history.back();</script>")

        # print(data)
        df = pd.DataFrame(data)
        # Make datetimes timezone-unaware (assuming they are in the timezone-aware format)
        # df['login_date'] = df['login_date'].apply(lambda x: make_aware(x).astimezone(timezone.utc).replace(tzinfo=None) if x else None)
        df['login_date'] = df['login_date'].dt.tz_localize(None)
        # print(df)
        
        # Use slugify to generate a filename from the model name and current timestamp
        file_name = f"LoginData_{slugify(datetime.now())}.xlsx"

        # print(file_name)

        # saving the excel
        response = HttpResponse(content_type = 'application/xlsx')
        response['Content-Disposition'] = f'attachment; filename={file_name}'

        df.to_excel(response)

        return response



def export_filter(request):
    if request.method == 'POST':
        log_date = request.POST.get('log_date')
        name = request.POST.get('emp_name')
      
        # Start with an empty Q object
        conditions = Q()

        # Add date condition if log_date is provided
        if log_date:
            conditions &= Q(login_date__date=datetime.strptime(log_date, '%Y-%m-%d').date())

        # Add name condition if name is provided
        if name:
            conditions &= Q(emp_name=name)

        try:
            # Filter objects based on dynamic conditions
            data = LoginDetails.objects.annotate(date_only=TruncDate('login_date')).filter(conditions).values('login_date', 'Emp_code', 'emp_name', 'company', 'department')

            if not data:
                raise
        except:
            return HttpResponse("<script>alert('No Data');history.back();</script>")

        # print(data)

        df = pd.DataFrame(data)
        df['login_date'] = df['login_date'].dt.tz_localize(None)
        # print(df)
        
        # # Use slugify to generate a filename from the model name and current timestamp
        file_name = f"LoginData_{slugify(datetime.now())}.xlsx"

        # print(file_name)
  
        # saving the excel
        response = HttpResponse(content_type = 'application/xlsx')
        response['Content-Disposition'] = f'attachment; filename={file_name}'

        df.to_excel(response)

        return response
        