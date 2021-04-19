from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers


class Message(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('url', 'subject', 'body', 'pk')


class UserProfile(models.Model):
 
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
 
    org = models.CharField(
        'Organization', max_length=128, blank=True)
 
    telephone = models.CharField(
        'Telephone', max_length=50, blank=True)
 
    mod_date = models.DateTimeField('Last modified', auto_now=True)
 
    class Meta:
        verbose_name = 'User Profile'
 
    def __str__(self):
        return "{}'s profile".format(self.user.__str__())


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"