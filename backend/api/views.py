from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from .models import Message, MessageSerializer
from .models import *

from django.shortcuts import *
from .models import UserProfile
from .forms import ProfileForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserList(APIView):
    """
    get:
        return current user
    """
    # 定义 GET 请求的方法，内部实现相同 @api_view
    def get(self, request):
        #print('================= request ================\n', type(request))
        #print('================= request ================\n', request.__dict__.keys())
        #print('================= request user ================\n', request._user)
        user = request.user
        serializer = UserSerializer(user, many=False)
        #return render(request, 'api/userlist.html', {'user': user})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 定义 POST 请求的方法
    #def post(self, request):
    #    serializer = ProjectSerializer(data=request.data)
    #    if serializer.is_valid():
    #        serializer.save()
    #        return Response(serializer.data, status=status.HTTP_201_CREATED)
    #    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
def profile(request):
    user = request.user
    print('================user email adrress: ', user.email)
    print('================sender email adrress: ', settings.EMAIL_HOST_USER)
    send_mail('EMAIL NOTIFICATION TEST',
              'HI, this is an email notification test',
              settings.EMAIL_HOST_USER,
              [user.email, 'qf31@tamu.edu'],
              fail_silently=False,)


    return render(request, 'account/profile.html', {'user': user})


@login_required
def profile_update(request):
    print('======== in profile_update view =========')
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user = user)

    if request.method == "POST":
        form = ProfileForm(request.POST)
 
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
 
            user_profile.org = form.cleaned_data['org']
            user_profile.telephone = form.cleaned_data['telephone']
            user_profile.save()
 
            return HttpResponseRedirect(reverse('profile'))
    else:
        default_data = {'first_name': user.first_name, 'last_name': user.last_name,
                        'org': user_profile.org, 'telephone': user_profile.telephone, }
        form = ProfileForm(default_data)
 
        return render(request, 'account/profile_update.html', {'form': form, 'user': user})
