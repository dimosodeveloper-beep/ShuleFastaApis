from django.shortcuts import render

# Create your views here.
def home(request):
    my_users = "My name is dimoso"

    context= {
        'my_users':my_users,
    }

    return render(request, 'MyTemplatesApp/home.html', context)