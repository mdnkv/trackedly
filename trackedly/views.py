from django.http import request
from django.shortcuts import redirect

def home_view(request):
    if request.user.is_authenticated:
        return redirect('entries:entries_list_view')
    else:
        return redirect('users:login_view')