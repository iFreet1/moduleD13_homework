from django.urls import path
from .views import PostList, PostCreateView, PostDetail, ResponsesList, RespopnseDelete, RespopnseAccept


urlpatterns = [
    path('', PostList.as_view()),
    path('add', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('responses', ResponsesList.as_view()),
    path('<int:pk>/accept', RespopnseAccept, name='accept'),
    path('<int:pk>/delete', RespopnseDelete, name='delete'),
]