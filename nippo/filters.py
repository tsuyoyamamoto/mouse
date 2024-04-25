#8-7　アプリフォルダの中にfilters.py ファイルを作りそこにクラスを作成する

import django_filters
from nippo.models import NippoModel
from django.forms.widgets import Select#selectフォームにするためにwidgetからインポート

public_choices = ((0, "全て"), (1, "公開済のみ"), (2, "ドラフトのみ"))

class NippoModelFilter(django_filters.FilterSet):#8-7 検索機能 NippoModelfilterという新しいクラスを作る
    #公開・非公開を入力
    #新しいフィールドに上書き
    public = django_filters.TypedChoiceFilter(
                        choices=public_choices, 
                        method="public_chosen", #下のメソッドを実行qsが返す値
                        label="公開済み・下書き", 
                        widget=Select(attrs={#attarsは属性の略
                                "class":"form-select"
                                    }))
    #年月日によるもの
    date = django_filters.TypedChoiceFilter(
                method="timestamp_checker", 
                label="作成月", 
                widget=Select(attrs={
                    "class":"form-select"
                }))
    
    profile = django_filters.NumberFilter(method="get_profile_nippo")
    #8-8 リストビューでアーカイブページを作成
    
    class Meta:
        model = NippoModel
        fields = ["date", "public"]

    def __init__(self, *args, **kwargs):
        qs = kwargs["queryset"]#クエリセットを取り出す
        choice_option = [(obj.date.year, obj.date.month) for obj in qs]#内包表記
        choice_option = list(set(choice_option))#重複している分を取り出さない
        choice_option.sort(reverse=True)
        DATE_OPTIONS = [
            ((year, month), f"{year}年{month}月") for year, month in choice_option
            ]#受け取る値と表示される値
        DATE_OPTIONS.insert(0, (None, "---"))#ここまでが選択肢を作る記述
        #↓作った選択肢をフィールドに入れていくself.base_filters["date"]でDATE_OPTIONSを入れる
        self.base_filters["date"].extra["choices"] = DATE_OPTIONS
        super().__init__(*args, **kwargs)#superで継承元の設定を読み込む

    def timestamp_checker(self, queryset, name, value):
        qs = queryset
        if value is not None:
            year, month = eval(value)
            print(year, month)
            qs = queryset.filter(date__year=year).filter(date__month=month)#field lookupを使って取り出している
        return qs

    def public_chosen(self, queryset, name, value):#valueはpublic_choicesの数字
        qs = queryset
        if value == "1":
            qs = qs.filter(public=True)
        elif value == "2":
            qs = qs.filter(public=False)
        return qs
    
    #8-8アーカイブページの作成
    def get_profile_nippo(self, queryset, name, value):
        from accounts.models import Profile#関数の中でprofileクラスをインポート
        qs = queryset
        if Profile.objects.filter(id=value).exists():
            qs = qs.filter(user__profile__id=value)
        else:
            qs = qs.none()
        return qs