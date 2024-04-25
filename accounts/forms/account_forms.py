
#8-2パッケージ化
#ユーザーモデルクラスのあるアプリの中にforms.py　を作成
# 7-9 formが完成したら、formを管理画面に表示する　form = CustomAdminChangeForm

from django import forms
from django.forms.fields import DateField
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import UserChangeForm#これを継承して編集ページを編集する

from accounts.models import User, Profile, GENDER_CHOICE#7-9  ユーザーが自分のプロフィールを変更したい。Profoleをインポート
#8-2並列にならないので、書き換えるaccounts.models
#GENDER_CHOICE = [(None, "--"), ("m", "男性"), ("f", "女性")]はmodels.pyで定義してます
#7-8 複数の管理ページを同一の管理ページで編集する
#ユーザーモデルクラスのカスタマイズするためのUserAdminでは、以下の変数に入れることで独自のフォームを使用できます。
#add_form変数：新規登録フォーム
#form変数：編集ページ 
# 7-8 formが完成したら、formを管理画面に表示する　adminでform = CustomAdminChangeForm
#Profileクラスのフィールドを追記します
class CustomAdminChangeForm(UserChangeForm):#これを継承して編集ページを編集する

    username = forms.CharField(max_length=100)
    department = forms.CharField(max_length=100, required=False)
    phone_number = forms.IntegerField(required=False) 
    gender = forms.ChoiceField(choices=GENDER_CHOICE, required=False)
    birthday = DateField(required=False)

    class Meta:
        model = User
        fields =('email', 'password', 'active', 'admin')

#Profileが存在する場合は、初期値にデータを格納する
    def __init__(self, *args, **kwargs):
        user_obj = kwargs["instance"]
        #番号がずれる
        
        if hasattr(user_obj, "profile"):
            profile_obj = user_obj.profile
            print(user_obj)#番号がずれる
            print(user_obj.id)
            print(profile_obj)
            print(profile_obj.id)
            self.base_fields["username"].initial = profile_obj.username
            self.base_fields["department"].initial = profile_obj.department
            self.base_fields["phone_number"].initial = profile_obj.phone_number
            self.base_fields["gender"].initial = profile_obj.gender
            self.base_fields["birthday"].initial = profile_obj.birthday
        super().__init__(*args, **kwargs)

#保存機能の定義
    def save(self, commit=True):
        user_obj = super().save(commit=False)
        username = self.cleaned_data.get("username")
        department = self.cleaned_data.get("department")
        phone_number = self.cleaned_data.get("phone_number")
        gender = self.cleaned_data.get("gender")
        birthday = self.cleaned_data.get("birthday")
        if hasattr(user_obj, "profile"):
            profile_obj = user_obj.profile
        else:
            profile_obj = Profile(user=user_obj)
        if username is not None:
            profile_obj.username = username
        if department is not None:
            profile_obj.department = department
        if phone_number is not None:
            profile_obj.phone_number = phone_number
        if gender is not None:
            profile_obj.gender=gender
        if birthday is not None:
            profile_obj.birthday = birthday
        profile_obj.save()
        if commit:
            user_obj.save()
        return user_obj
    

        
        
        
"""
「viewクラスからFormクラスへ値を渡したい！」「Formクラスで任意のオブジェクトを取得、使用したい！」
\というDjangoフレームワークでお困りの方へ向けた記事となります
当記事を通じて、
views.py ビュークラス から forms.py フォームクラスへ値を渡す方法
を解説します
特に、inputフォームなどに動的な初期値を設定したい場合やログインユーザーを自動保存としたい場合などには重宝することと思います
ビュークラスでは「get_form_kwargs」関数
フォームクラスでは「__init__」関数
へ記述をすることで値を渡すことができますので、「request.user」情報をフォームクラスで受け取ってみましょう！

get_form_kwargs関数
ビュークラスの「get_form_kwargs関数」は、FormView、CreateView、UpdateViewに用意されているメソッドです
返された辞書型の値がフォームクラスへ渡されます
ユーザー情報をフォームクラスへ渡すまでは下記のとおりです
def get_form_kwargs(self, *args, **kwargs):
    kwgs = super().get_form_kwargs(*args, **kwargs)
    kwgs["user"] = self.requst.user
    return kwgs
【解説】
kwgs = super().get_form_kwargs(*args, **kwargs)
スーパークラスからget_form_kwargsを受け取り「kwgs」変数へ格納します
kwgsは辞書型のオブジェクトになります
kwgs["user"] = self.requst.user
「kwgs」変数に{ “user”: self.request.user }を格納します
    return kwgs
辞書型変数「kwgs」を返します
返された「kwgs」をフォームクラスで受け取りましょう

__init__関数
フォームクラス「__init__関数」では、ビュークラスで設定した辞書型のキーを引数として受け取る必要があります
def __init__(self, user=None, *args, **kwargs):
    #必要な処理を行いましょう        
    super().__init__(*args, **kwargs)
まとめ
ビュークラスからフォームクラスへ値を渡す方法は下記のとおりです
【①ビュークラス：get_form_kwargs関数】
スーパークラスからの結果を受け取る
スーパークラスから受け取った結果に任意の値を追記する
【②フォームクラス：__init__関数】
ビュークラスで追加した値のキーを引数へ設定
受け取った値で必要な処理を行う
いかがでしょうか？
皆さんの「困った！」が解決できれば幸いです

"""

