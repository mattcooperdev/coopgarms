from django.shortcuts import render
from django.contrib import messages


def subscription(request):
    '''Newsletter subscription'''
    template = 'marketing/index.html'
    if request.method == "POST":
        email = request.POST['email']
        print(email)
        messages.success(request, "Subscription received. Thank You! ")
    return render(request, template)
