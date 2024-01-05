from django.urls import path
from myapp import views

urlpatterns = [
    path('import_login_details', views.import_login_details, name='import_login_details'),
    path('', views.view_login_datas, name='view_login_datas'),
    path('export_to_excel/', views.export_to_excel, name='export_to_excel'),
    path('export_filter/', views.export_filter, name='export_filter'),

  
    # path('export_by_name/', views.export_by_name, name='export_by_name'),
    # path('export_by_date/', views.export_by_date, name='export_by_date'),




]