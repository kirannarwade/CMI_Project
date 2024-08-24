from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm

urlpatterns = [
    path('', views.index, name='home'),
    path('upload-data/', views.UploadFileData.as_view(), name='upload_data'),
    path('query-builder/', views.query_builder, name='query_builder'),
    path('users-info/', views.users_info, name='users_info'),

    path('login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    path('signup/', views.CustomerRegistrationView.as_view(), name="signup"),
    path('logout/', views.logoutUser, name="logout"),
]