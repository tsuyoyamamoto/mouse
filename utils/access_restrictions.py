
#8-2自作のパッケージやモジュールをインポートする方法
# プロジェクトフォルダの中にutilsフォルダを作り、中にaccess_restrictions.pyを作成する

from django.contrib.auth.mixins import UserPassesTestMixin#7-2 7-3　インポート
from django.contrib import messages#7-47-4メッセージフレームワークの使い方 特定の状態でメッセージが出るようにする
from django.shortcuts import redirect

#自分の日報のときだけアクセスできる
class OwnerOnly(UserPassesTestMixin):
    def test_func(self):
        #アクセス制限を行う関数
        nippo_instance = self.get_object()
        return nippo_instance.user == self.request.user
        #true falseが返る
    
    def handle_no_permission(self):
        messages.error(self.request, "ご自身の日報でのみ編集・削除可能です。")
        return redirect("nippo-detail", slug=self.kwargs["slug"])
    #from django.contrib import messagesをインポートしてメッセージを使えるようにする
    #falseだったときのリダイレクト先を指定
    #7-4 エラータグmessages.errorを追記
#自分のプロフィールだけ見れるようにする
class OwnProfileOnly(UserPassesTestMixin):
    def test_func(self):
        profile_obj = self.get_object()
        try:
            return profile_obj == self.request.user.profile
        except:
            return False


