from django.urls import path, include
# from .apiviews import PollList, PollDetail, ChoiceList, CreateVote, PollViewSet
from .apiviews import  ChoiceList, CreateVote, PollViewSet, UserCreate, LoginView
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView

# For view sets the default router attaches the proper function to the methods
router = DefaultRouter()
router.register('polls',PollViewSet,base_name='polls')
router.register('users',UserCreate,base_name='users')

app_name = 'polls'
urlpatterns = [
    path('login/',LoginView.as_view(),name='login'),
    path('polls/<int:pk>/choices/',ChoiceList.as_view(),name='choice_list'),
    path('polls/<int:pk>/choices/<int:choice_pk>/vote/',
        CreateVote.as_view(),name='create_vote'),
    path('',TemplateView.as_view(template_name='polls/index.html'),name='index'),
]
urlpatterns += router.urls
