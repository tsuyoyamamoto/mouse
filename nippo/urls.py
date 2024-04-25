#1-3　nippoの下にurls.pyを作成する
#nippo/でアクセスされたら、nippoアプリのurls.pyを見に行くという意味

from django.urls import path
from .views import (
                    NippoDeleteView,
                    NippoListView,
                    NippoDetailView,
                    NippoCreateModelFormView,
                    NippoUpdateModelFormView,
                    NippoCreateFormView,
                    nippoListView,
                    nippoDetailView, 
                    nippoCreateView,
                    nippoUpdateFormView,
                    nippoDeleteView
                    )#同一の系列にあるviewからインポートして。。


urlpatterns = [
  path("", NippoListView.as_view(), name="nippo-list"),#5-1viewクラスとurlを紐づける as_viewがないと展開されない
  path("detail/<slug:slug>/", NippoDetailView.as_view(), name="nippo-detail"),
  path("create/", NippoCreateModelFormView.as_view(), name="nippo-create"),
  path("update/<slug:slug>/", NippoUpdateModelFormView.as_view(), name="nippo-update"),
  path("delete/<slug:slug>/", NippoDeleteView.as_view(), name="nippo-delete"),
  #path("create/", NippoCreateFormView.as_view(), name="nippo-create"),
  #path("", nippoListView, name="nippo-list"),#インポートした関数を呼びだすview関数
  #path("detail/",nippoDetailView),#2-2
  #path("detail/<int:pk>/", nippoDetailView, name="nippo-detail"),#3-1　pkでプライマリーキーを受け取る
  #path("create/", nippoCreateView, name="nippo-create"),#2-5formから値を受け取る
  #path("update/<int:pk>/", nippoUpdateFormView, name="nippo-update"),#3-5
  #path("delete/<int:pk>/", nippoDeleteView, name="nippo-delete"),
]    
#2-6リンク先をページ名にする
    