from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as accounts_views
from django.urls import path, include

urlpatterns = [
    path('', lambda request: redirect('login')),
    path('admin/', admin.site.urls),
    path('register/', accounts_views.register, name='register'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', accounts_views.profile, name='profile'),
    path('audit-log/', accounts_views.audit_log, name='audit_log'),
    path('inventory/', include('inventory.urls')),
    path('cart/', include('cart.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)