from django.shortcuts import render
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    """registration flow
    based off the model"""
    if request.method == 'POST':
        # Registration form
        errors = User.objects.user_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
