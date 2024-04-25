from django.db import models
#7-1foreignkeyの使い方　User = get_user_model()で認証で使うUserを取得する
#AUTH_USER_MODEL = 'accounts.User'を取得
from django.contrib.auth import get_user, get_user_model
from utils.random_string import random_string_generator#8-5
User = get_user_model()

from django.db.models import Q #インポート
#8-3検索機能の追加 独自のクエリセットを定義
from django.utils import timezone#8-6
#8-5
def slug_maker():
    repeat = True
    while repeat:
        new_slug = random_string_generator()
        counter = NippoModel.objects.filter(slug=new_slug).count()
        if counter == 0:
            repeat = False
    return new_slug


class NippoModelQuerySet(models.QuerySet):#継承すると、新たなメソッドを追加できる
    def search(self, query=None):#searchメソッドを追加する query=Noneで検索している引数を受け取る
        qs = self#全てのオブジェクト all
        #qs = qs.filter(public=True) #公開済みの日報のみでQuerySetを作成しています
        if query is not None:
            or_lookup = (
                Q(title__icontains=query)|
                Q(content__icontains=query)            
            )
            qs = qs.filter(or_lookup).distinct()#distinctは重複しているものを省く
        return qs.order_by("-date") #新しい順に並び替えてます#8-6修正
'''
 DjangoのORMでは、QuerySetのサブクラスを作成することができます。サブクラスを作成することで、オリジナルのQuerySetに独自のメソッドを追加することができます   
'''

class NippoModelManager(models.Manager):
    def get_queryset(self):
        return NippoModelQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)
#self.get_queryset().search(query=query)で全てのクエリを受け取り、searchメソッドを実行
'''
Djangoのモデルマネージャーとは何ですか？
マネージャ (Manager) とは、Django のモデルに対するデータベースクエリの操作を提供するインターフェイスです。 Django アプリケーション内の1つのモデルに対して、Manager は最低でも1つは存在します。
インターフェイスとは、複数の異なる者同士を接続するという意味
'''  

    
class NippoModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)#7-1foreignkeyで紐づけ
    title = models.CharField(max_length=100, verbose_name="タイトル")#5-6変更したらマイグレーションする
    content = models.TextField(max_length=1000, verbose_name="内容")
    public = models.BooleanField(default=False, verbose_name="公開する")
    #9-1クエリセット」を動的に変更する公開非公開を追加 データベースをいじったら、必ずマイグレーションする
    date = models.DateField(default=timezone.now)
    slug = models.SlugField(max_length=20, unique=True, default=slug_maker)#8-4「slug」は、IT用語の一つで、URLの一部として使用される短い文字列を指す。
    #8-5 default=slug_makerで作成した関数が自動で実行される
    timestamp = models.DateTimeField(auto_now_add=True)#8-6 カレンダー表示
    
    objects = NippoModelManager()#8-3検索機能の実装
    #モデルマネジャーとモデルクラスの紐づけ
    
    class Meta:
        verbose_name_plural ="日報" #任意のモデルクラス名5-6
    
    def __str__(self):
        return self.title#1-7modelに独自の名前を付ける
    
    def get_profile_page_url(self):
        from django.urls import reverse_lazy
        return reverse_lazy("nippo-list") + f"?profile={self.user.profile.id}"#nippo/?profile=intがパラメータ
    #8-8 urlを取得するためのメソッドをmodelクラス内で作成する
    #model内でメソッドを作ることによって、object.メソッド名でurlを取得できるようになる。
#データベースはdb.sqliteに保存される

    
