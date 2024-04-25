
#6-2管理画面をカスタマイズ　表示を変える UserAdminクラスを継承し、新たなクラスを作成
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
#UserAdminクラスというユーザー管理画面を変更するモデルを継承し、新たなクラスを作成することによって、管理画面をカスタマイズすることができる

from .models import User, Profile #7-7インポート
from .forms import CustomAdminChangeForm#7-8複数のモデルを同一の編集ページで編集する formをインポート

class UserAdmin(BaseUserAdmin):#UserAdminをインポートして新たにクラスを作成し、カスタマイズする
    form = CustomAdminChangeForm# 7-8 formが完成したら、formを管理画面に表示する
    #一覧ページ用
    list_display = (
        "email",
        "active",
        "staff",
        "admin",
    )
    list_filter = (
        "admin",
        "active",
    )
    ordering = ("email",)
    filter_horizontal = ()
    
    search_fields = ('email',)
    
    #新規登録用
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
            }
        ),
    )
    
    #編集ページ 7-8で追記 
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('プロフィール', {'fields': (
            'username',
            'department',
            'phone_number',
            'gender',
            'birthday',
        )}),
        ('権限', {'fields': ('staff','admin',)}),
    )

admin.site.register(User, UserAdmin)
#登録する。Userはモデル名、UserAdminはカスタマイズしたクラス
#Profileクラスは不要になったのでコメントアウト
admin.site.register(Profile)
#7-7 onetoonefieldを管理画面で表示できるようにする

"""
search_fields = ('email',)#/admin/accounts/user/ の FieldError   キーワード「ユーザー名」をフィールドに解決できません。
    #選択肢は次のとおりです: アクティブ、管理者、電子メール、ID、last_login、logentry、パスワード、スタッフここを入れないと検索でfieldエラーになる
    # search_fields = ("name",)継承元がnameになっているからfieldがないとエラーになる
    #6-2/admin/accounts/user/add/ の FieldError
    #ユーザーに不明なフィールド (ユーザー名) が指定されました。UserAdmin クラスのフィールド/フィールドセット/除外属性を確認します。
    # add_fieldsetsで'email'に指定しないとエラーになる
"""
