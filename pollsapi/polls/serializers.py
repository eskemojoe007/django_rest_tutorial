from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Poll, Choice, Vote
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','username','email','password')
        read_only_fields = ('id',)
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        user = User(email=validated_data['email'],
            username=validated_data['username'])

        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
class ChoiceSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True,required=False,read_only=True)
    class Meta:
        model = Choice
        fields = '__all__'


class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Poll
        fields = '__all__'

# From https://stackoverflow.com/questions/41312558/django-rest-framework-post-nested-objects
class PollReadSerializer(PollSerializer):
    created_by = UserSerializer(read_only=True)
    # def create(self, validated_data):
    #     created_by_data = validated_data.pop('created_by')
