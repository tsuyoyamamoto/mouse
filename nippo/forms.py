# 3-3 appフォルダ「nippo」 > forms.pyを作成　views.py と並列に→　その中にFormクラスを作成する(継承) →　フィールドの作成

from django import forms
#5-5モデルフォーム
from .models import NippoModel
#8-6カレンダー表示
from bootstrap_datepicker_plus.widgets import DatePickerInput

class NippoModelForm(forms.ModelForm):
    date = forms.DateField(
        label="作成日",
        widget=DatePickerInput(format='%Y-%m-%d')
    )
    #8-6 dateフィールドは備わっているが、上書きする。（継承しているから上書きできる）
    class Meta:
        model = NippoModel
        exclude = ["user"]#7-1userを外す
        #fields = "__all__"

    def __init__(self, user=None,*args, **kwargs):#ここでuserを受け取り、
        for key, field in self.base_fields.items():#8-1 必要な処理
            if key != "public":
                field.widget.attrs["class"] = "form-control"#入力エリア
            else:
                field.widget.attrs["class"] = "form-check-input"#チェックボックスを適用
                
        #for field in self.base_fields.values(): #必要な処理をして、
        #   field.widget.attrs["class"] = "form-control"
            self.user = user
        super().__init__(*args, **kwargs)#super、**kwargsで全てのインスタンス、情報を引き継ぐ
#7-1 user=Noneで引数を受け取る
#super().__init__(*args, **kwargs) で親クラスの全てのインスタンス（情報も）を受け取る

    def save(self, commit=True):
        nippo_obj = super().save(commit=False)
        if self.user:
            nippo_obj.user = self.user
        if commit:
            nippo_obj.save()
        return nippo_obj
        
#使用したいモデルをインポート、こっちは使わない
#model変数に紐づける
class NippoFormClass(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'タイトル...'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'内容...'}))
    #TExtareaに変更、placeholder、labelを日本語表記にする3-3
    #4-7 フォームクラスで作成したフォームに一括でクラスを追加する
    def __init__(self, *args, **kwargs):
        for field in self.base_fields.values():
            #print(field)でfields.Charfield を取り出す
            field.widget.attrs.update({"class":"form-control"})
        super().__init__(*args, **kwargs)
        
    #4-7 formにCSSを適用する
    #forでfieldを取り出し、各々のfieldにform-classを適用している
   
"""
#3-5      
    def __init__(self,*args,**kwargs):#親classをすべて引っ張ってくる
        print(**kwargs)
        print(self.base_fields["title"].initial) #表示はNone
        print(self.base_fields["content"].initial)#表示はNone
         #新しい処理をして値を格納
        self.base_fields["title"].initial="testmouse"
        self.base_fields["content"].initial="testmouse-content"
        super().__init__(*args,**kwargs) #処理をした後の新しいデータとインスタンスを受け取る
        print("---",**kwargs)
        print(self.base_fields["title"].initial)#表示はtestmouse
        print(self.base_fields["content"].initial)#表示はtestmouse-content
        #super().__init__(*args,**kwargs)で新しく処理したデータとインスタンスを受け取る。だから
        #formのtitleはtestmouse、contentはtestmouse-content
"""
#5-5formはformを表示するためだけのもの、modelformは保存の機能も備わっている

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

補足
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