from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import viewsets

from .models import Poll, Choice
from .serializers import PollSerializer,ChoiceSerializer, VoteSerializer, UserSerializer, PollReadSerializer
from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import User
from rest_framework.permissions  import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token

# class PollList(APIView):
#     def get(self, request):
#         polls = Poll.objects.all()[:20]
#         data = PollSerializer(polls,many=True).data
#         return Response(data)
#
# class PollDetail(APIView):
#     def get(self,request,pk):
#         poll = get_object_or_404(Poll,pk=pk)
#         data = PollSerializer(poll).data
#         return Response(data)
class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def destroy(self,request,*args,**kwargs):
        poll = Poll.objects.get(pk=self.kwargs['pk'])
        if (not request.user == poll.created_by) and (not request.user.is_staff):
            raise PermissionDenied('You cannot delete this poll, only {} can'.format(poll.created_by))
        return super().destroy(request,*args,**kwargs)

    def get_serializer_class(self):
         # Define your HTTP method-to-serializer mapping freely.
         # This also works with CoreAPI and Swagger documentation,
         # which produces clean and readable API documentation,
         # so I have chosen to believe this is the way the
         # Django REST Framework author intended things to work:
         if self.request.method in ('GET', ):
             # Since the ReadSerializer does nested lookups
             # in multiple tables, only use it when necessary
             return PollReadSerializer
         return PollSerializer
# class PollList(generics.ListCreateAPIView):
#     queryset = Poll.objects.all()
#     serializer_class = PollSerializer
# class PollDetail(generics.RetrieveDestroyAPIView):
#     queryset = Poll.objects.all()
#     serializer_class = PollSerializer
class ChoiceList(generics.ListCreateAPIView):
    def get_queryset(self):
        return Choice.objects.filter(poll_id=self.kwargs["pk"])
    serializer_class = ChoiceSerializer

    def post(self,request,*args,**kwargs):
        poll = Poll.objects.get(pk=self.kwargs['pk'])
        if not request.user == poll.created_by:
            raise PermissionDenied("You can not create choice for this poll. Only {} can.".format(poll.created_by))
        return super().post(request,*args,**kwargs)
class CreateVote(APIView):

    def post(self, request,pk,choice_pk):
        voted_by = request.data.get('voted_by')
        data = {'choice': choice_pk, 'poll': pk, 'voted_by':voted_by}
        serializer = VoteSerializer(data=data)

        if serializer.is_valid():
            vote = serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#https://stackoverflow.com/questions/44533277/django-rest-framework-restrict-user-data-view-to-admins-the-very-own-user
# http://www.django-rest-framework.org/api-guide/viewsets/#introspecting-viewset-actions
class UserCreate(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # authentication_classes = () # Now quite sure why I need to comment this out

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class LoginView(APIView):
    permission_classes = ()

    def post(self,request,):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username,password=password)
        if user:
            t = Token.objects.get_or_create(user=user)
            print(t)
            return Response({'token':user.auth_token.key})
        else:
            return Response({'error':'Wrong Credentials'},status=status.HTTP_400_BAD_REQUEST)
