from django.shortcuts import render

from sponsorships.models import CustomUserModel


def home_view(request):
    try:
        phone_number = request.session.get('user_phone_number')
        user = CustomUserModel.objects.get(phone_number=phone_number)
    except CustomUserModel.DoesNotExist:
        user = request.user
        print(user)
    context = {
        'user': user,
    }
    return render(request, 'pages/home.html', context=context)



