
#8-2パッケージ化
from django import forms
from django.utils.translation import gettext, gettext_lazy as _

from accounts.models import User, Profile, GENDER_CHOICE
#7-9  ユーザーが自分のプロフィールを変更したい。Profoleをインポート
#8-2並列にならないので、書き換えるaccounts.models

#7-9  ユーザーが自分のプロフィールを変更したい。
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["user"]
        
#7-12 フォームにバリデーションを実装する方法バリデーション：検証
#usernameにemailが入っていた場合、バリデーション機能が働く
    def clean_username(self):
        username = self.cleaned_data.get("username")
        user_email = self.instance.user.email
        if username == user_email:
            raise forms.ValidationError("ユーザー名を変更してください")
        elif "@" in username:
            raise forms.ValidationError("ユーザー名にEメールアドレスは使用できません")
        return username


