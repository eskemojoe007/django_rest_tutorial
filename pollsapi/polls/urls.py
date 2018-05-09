from django.urls import path, include
# from .apiviews import PollList, PollDetail, ChoiceList, CreateVote, PollViewSet
from .apiviews import  ChoiceList, CreateVote, PollViewSet, UserCreate, LoginView
from rest_framework.routers import DefaultRouter

# For view sets the default router attaches the proper function to the methods
router = DefaultRouter()
router.register('polls',PollViewSet,base_name='poll')
router.register('users',UserCreate,base_name='users')


urlpatterns = [
    path('login/',LoginView.as_view(),name='login'),
    # path('polls/',PollList.as_view(),name='polls_list'),
    # path('polls/<int:pk>/',PollDetail.as_view(),name='polls_detail'),
    path('polls/<int:pk>/choices/',ChoiceList.as_view(),name='choice_list'),
    path('polls/<int:pk>/choices/<int:choice_pk>/vote/',CreateVote.as_view(),name='create_vote'),
    # path('users/',UserCreate.as_view(),name='user_create'),
]

urlpatterns += router.urls
