
from django.contrib import admin
from django.urls import path, include

#4-5　画像を表示するためにsettingとstaticをインポート
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("nippo/", include('nippo.urls')),#nippoアプリのurlsへへ
    path('accounts/', include('allauth.urls')),#これによってallauthのそれぞれのページへアクセスすることができるようになります。
    path("profile/", include("accounts.urls")),#7-9 ユーザーが自分でprofileを更新できるようにする　紐づけ
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#4-5 画像を表示するファイルにアクセスするための記述、media_local の中に保存していくフォルダは、
# media/でアクセスできる。settingがDEBUG　true→　ローカル環境のとき実行