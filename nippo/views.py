from typing import Any
from django.db.models.query import QuerySet

from random import randint
from .models import NippoModel
from .forms import  NippoModelForm,NippoFormClass#5-5フォームを使うためにインポート
#NippoModelから値を取得するためには、view.pyでNippoModelをインポートする
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse, reverse_lazy

from django.views.generic import FormView,ListView,DetailView #5-1djangoクラスのLISTVIEW,DetailViewをインポート
from django.views.generic.edit import DeleteView,CreateView,UpdateView#5-5modelformを使ってみようでインポート
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin#7-2 7-3　インポート

from django.db.models import Q#8-1 Qオブジェクトをインポート
from utils.access_restrictions import OwnerOnly#8-2パッケージ化

from .filters import NippoModelFilter#8-7フィルターの実装

from accounts.models import Profile#8-8

    
#5-3 Formviewを使ってみよう
class NippoListView(ListView): #5-1ListViewクラスを継承
    template_name = "nippo/nippo-list.html" #変数「template_name」には使用するHTMLテンプレートのパス
    model = NippoModel #変数「model」にはデータを取得する元のモデルクラス名
#1 modelで指定したデータベーステーブルからQuerySetを取得する
#2 「object_list」という変数にQuerySetを格納する
#3 HTMLテンプレートへコンテキストとしてQuerySetを渡す ということをすべてやってくれる
    def get_queryset(self):#8-3検索機能の実装
        q = self.request.GET.get("search")#searchを受け取る
        qs =  NippoModel.objects.search(query=q)#searchメソッド
        if self.request.user.is_authenticated:
           qs = qs.filter(Q(public=True)|Q(user=self.request.user))
        else:
            qs = qs.filter(public=True)
        return qs 
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["filter"] = NippoModelFilter(self.request.GET, queryset=self.get_queryset())
        #8-8 get_context_dataの中に、profileというコンテキストを渡す
        profile_id = self.request.GET.get("profile")#パラメータからprofile_idを受け取る
        q = Profile.objects.filter(id=profile_id)#pk
        if q.exists():
            ctx["profile"] = q.first()
        #8-7 get_context_dataでデータを受け取り、NippoModelFilterインスタンスを作成
        return ctx#if の場合、templateにはprofileという属性が入っている
        #views.pyでは、プロフィールパラメータがあるときだけ、profileコンテキストを渡します。
"""
    def get_queryset(self):
         qs = NippoModel.objects.none()#何も表示されない
         return qs #何も表示されないobjectをtemplateに返している
     
    def get_queryset(self):
        qs = NippoModel.objects.none()
        if self.request.user.is_authenticated:
            qs = NippoModel.objects.all()
        return qs
    
    def get_context_data(self):
        ctx = super().get_context_data()
        ctx["site_name"] = "itc.tokyo"#{{site_name}}を埋め込むと動的に変更できる
        return ctx
"""

class NippoDetailView(DetailView):
    template_name = "nippo/nippo-detail.html"
    model = NippoModel
"""
    DetailViewクラスの記述は、3ステップで完了します

    1 DetailViewクラスのインポート
    2 DetailViewクラスの継承
    3「template_name」「model」変数へ値を格納
  この3ステップさえ守れば、
    ブラウザから「pk」を受け取る
    データベースから「pk」が一致するデータを取り出す
    コンテキストとしてHTMLテンプレートへ渡す
  ことが自動的に行われます
"""

#5-5モデルフォームクラスを作る　from django.views.generic.edit import CreateViewをインポート
#CreateViewはform_validで保存しなくても保存してくれる
#7-2 LoginRequiredMixinをインポートしてログインしている人間しかアクセスできないようにする
class NippoCreateModelFormView(LoginRequiredMixin,CreateView):
    template_name = "nippo/nippo-form.html"
    form_class = NippoModelForm #紐づけるモデルクラス
    success_url = reverse_lazy("nippo-list")
    
  
    def get_form_kwargs(self):
        kwgs = super().get_form_kwargs()
        kwgs["user"] = self.request.user
        return kwgs
#7-1 user_id にobjectがありません。エラーが出るのでアクセスしたユーザー情報を#formに送る。formに送って登録、保存 
#kwgs = super().get_form_kwargs()で親クラスから全ての情報を取得
#kwgs["user"] = self.request.userにはアクセスしたユーザー情報が格納されている
#return kwags でformに送る
    
#5-5from django.views.generic.edit import CreateView,UpdateView#5-5modelformを使ってみようでインポート   
class NippoUpdateModelFormView(OwnerOnly,UpdateView):
    template_name = "nippo/nippo-form.html"
    model = NippoModel
    form_class = NippoModelForm
    success_url = reverse_lazy("nippo-list")    
    

class NippoDeleteView(OwnerOnly,DeleteView):
    template_name = "nippo/nippo-delete.html"
    model = NippoModel
    success_url = reverse_lazy("nippo-list")

#5-6以降使わない
#from django.views.generic import FormView#5-3 でインポート
#from django.urls import reverse, reverse_lazyをインポート
class NippoCreateFormView(FormView):
    template_name = "nippo/nippo-form.html"
    form_class = NippoFormClass
    success_url = reverse_lazy("nippo-list")
    
    def form_valid(self, form):#保存方法
        data = form.cleaned_data
        obj = NippoModel(**data)
        obj.save()
        return super().form_valid(form)
        """FormViewのインポートし、継承したクラスを作成する
           template_nameでHTMLテンプレートを指定する
           form_classで使用するFormクラスを指定する
           success_urlでフォーム送信後のリダイレクト先を指定する 
           form_validメソッドは、フォームがエラーなく送信された際に実行される関数
           引数として、「self」以外に「form」を受け取る
          「return super().form_valid(form)」で終わること
        """
        

def nippoListView(request):
    template_name = "nippo/nippo-list.html"
    ctx = {}
    qs = NippoModel.objects.all()
    ctx["object_list"] = qs
    return render(request, template_name, ctx)
#from .models import NippoModelでmodelClassもインポートする
#ctxコンテキストの辞書を作り、取得したデータはコンテキストに入れる
#ctx["object_list"] = qsでctxコンテキストをnippo-list.htmlに送る
#<QuerySet [<NippoModel: テストタイトル>, <NippoModel: ラスト>, <NippoModel: マウス>,<NippoModel: みさきちゃん>]>=object_list
#object_listをnippo-list.htmlで受け取る
#2-1
#関数では、下記を返す（return）ことで指定のtemplateファイルを読み込めます
#def nippoListView(request):
#	return render(request, "nippo/nippo-list.html")#templates以下のパスを必ず記載
"""
 python manage.py shell
 from nippo.models import NippoModel
 qs = NippoModel.object.all()
 qs →<QuerySet [<NippoModel: テストタイトル>, <NippoModel: ラスト>, <NippoModel: マウス>,<NippoModel: みさきちゃん>]>
 とデータベースから値を受け取れる
"""

"""2-2
def nippoDetailView(request):
    template_name="nippo/nippo-detail.html"
    random_int = randint(1,10)
    ctx = {
        "random_number": random_int,
    }
    return render(request, template_name, ctx)
"""
"""2-3
def nippoDetailView(request, number): #numberを引数としてで値を受け取る
    template_name="nippo/nippo-detail.html"
    random_int = randint(1,10)
    ctx = {
        "random_number": random_int,
        "number": number,
    }
    return render(request, template_name, ctx)
"""

#3-1
def nippoDetailView(request, pk):
     template_name = "nippo/nippo-detail.html"
     ctx = {}
     #q = NippoModel.objects.get(pk=pk)
     q = get_object_or_404(NippoModel, pk=pk)
     ctx["object"] = q
     return render(request, template_name, ctx)
#pkで値を受け取るpkはプライマリーキー、主キー
#q = NippoModel.objects.get(pk=pk)で単一のオブジェクトを受け取る
#objectをnippo-detail.htmlに送る

"""2-5
def nippoCreateView(request):#ここでrequestで情報を受け取っている
    template_name = "nippo/nippo-form.html"
    if request.POST:
        print(request)
        print(request.POST)
        title = request.POST.get("title")
        content = request.POST.get("content")
        #受け取った値で必要な処理を行います
        obj = NippoModel(title=title, content=content)#3-2
        obj.save()
    return render(request, template_name)
"""
#3-3
def nippoCreateView(request):#from .forms import  NippoFormClassしてフォームクラスを使えるようにする
    template_name="nippo/nippo-form.html"
    form = NippoFormClass(request.POST or None) #大事　NippoFormClassを実行してインスタンスを作る
    #大事　ここではNippoFormClassインスタンスを作る
    #request.POSTでformのデータを受け取る
    ctx = {"form":form} #作ったインスタンスをコンテキストに格納　新規ページにはobjえお渡さないupdateでは渡す
    if form.is_valid():#送信時にエラーがないかチェック
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
        obj = NippoModel(title=title,content=content)
        #ここでNippoModel（データ）のインスタンスを作る
        obj.save()
        return redirect("nippo-list")
    return render(request, template_name, ctx) #コンテキストを送る

#3-4
def nippoUpdateFormView(request, pk):
    template_name = "nippo/nippo-form.html"
    obj = get_object_or_404(NippoModel, pk=pk)
    #obj = NippoModel.objects.get(pk=pk)#pkで値を受け取るpkはプライマリーキー、主キー
    #NippoModelはデータベースへのアクセス
    #q = NippoModel.objects.get(pk=pk)で単一のオブジェクトを受け取る
    initial_values = {"title": obj.title, "content":obj.content}#pkのオブジェクトを受け取る
    form = NippoFormClass(request.POST or initial_values)#フォームインスタンスを作成
    ctx = {"form": form}
    ctx["objects"] = obj#日報オブジェクトを変数「object」としてHTMLテンプレートへ渡す。新規ページにはない#3-5
    if form.is_valid():
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
        obj.title = title
        obj.content = content
        obj.save()
        if request.POST:
            return redirect("nippo-list")#3-8
    return render(request, template_name, ctx)

def nippoDeleteView(request, pk):
    template_name = "nippo/nippo-delete.html"
    obj = get_object_or_404(NippoModel, pk=pk)
    #et_object_or_404ない場合は、404エラー。ある場合は、objectを取り出す
    ctx = {"object": obj}#削除対象となるpk
    if request.POST:
        obj.delete()
        return redirect("nippo-list")
    return render(request, template_name, ctx) 
    