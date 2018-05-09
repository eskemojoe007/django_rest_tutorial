from django.urls import path, include

# OLD WITH OLD VIEWS
# from .views import polls_list, polls_detail

# urlpatterns = [
#     path("",polls_list,name='Polls_list'),
#     path("<int:pk>/",polls_detail,name='polls_detail'),
# ]

# NEW WITH REST VIEWS
from .apiviews import PollList, PollDetail, ChoiceList, CreateVote

urlpatterns = [
    path('polls/',PollList.as_view(),name='polls_list'),
    path('choices/',ChoiceList.as_view(),name='choice_list'),
    path('vote/',CreateVote.as_view(),name='create_vote'),
    path('polls/<int:pk>/',PollDetail.as_view(),name='polls_detail'),
]
