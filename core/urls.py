from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Resume upload and results
    path('upload/', views.upload_resume, name='upload_resume'),
    path('results/', views.matched_results, name='matched_results'),

    # Job management
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/create/', views.create_job, name='create_job'),

    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # For built-in Django login redirection fallback
    path('accounts/login/', views.login_view),
]
