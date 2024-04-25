#7-5 アプリフォルダの中にtemplatestags を作り　__init.py　を作ってモジュール化する
from django import template
register = template.Library()

@register.filter
def user_display(user):
    user_display = "ゲスト"
    if user.is_authenticated:
        user_display = user.profile.username
    return user_display

#templateをインポートしtemplate.Library()でクラスを作り、registerに格納
#@register.filterでデコレータを作り、userを引数で受け取る  return user_displayで返す