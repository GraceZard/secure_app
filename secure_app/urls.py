from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect   # <-- add this import
from accounts import views as accounts_views

urlpatterns = [
    path('', lambda request: redirect('login')),   # <-- redirects root to login page
    path('admin/', admin.site.urls),
    path('register/', accounts_views.register, name='register'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', accounts_views.profile, name='profile'),
    path('audit-log/', accounts_views.audit_log, name='audit_log'),
    path('inventory/', include('inventory.urls')),
]