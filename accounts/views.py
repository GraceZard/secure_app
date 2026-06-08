from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def audit_log(request):
    if request.user.role != 'admin':
        raise PermissionDenied

    # Try to import AuditLog, but if not available, show placeholder
    logs = []
    try:
        from audit.models import AuditLog
        logs = AuditLog.objects.all().order_by('-timestamp')
    except ImportError:
        # Model not created yet – just show empty list with message
        pass
    except Exception:
        # Any other error (e.g., table doesn't exist)
        pass
    return render(request, 'accounts/audit_log.html', {'logs': logs})
