from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

# passwords
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<str:email>/', views.reset_password, name='reset_password'),

    path('logging-in/', views.logging_in, name='logging_in'),

    path('add_expense/', views.add_expense, name='add_expense'),
    path('view_expense/', views.view_expense, name='view_expense'),
    path('filter_expense/', views.filter_expense, name='filter_expense'),
    path('expense_chart/', views.expense_chart, name='expense_chart'),
    path('monthly-expense/', views.monthly_expense, name='monthly_expense'),

    path('edit_expense/<int:id>/', views.edit_expense, name='edit_expense'),
    path('delete_expense/<int:id>/', views.delete_expense, name='delete_expense'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


