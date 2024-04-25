#7-9 ユーザーが自分のプロフィールを変更できるようにする url.pyも新たにファイルを作る
from django.urls import path
from .views import ProfileUpdateView

urlpatterns = [
    #...,
    path("<int:pk>/", ProfileUpdateView.as_view(), name="profile-update"),
]