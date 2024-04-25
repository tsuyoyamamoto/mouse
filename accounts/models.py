#djangoのユーザーモデルとはdjangoのアプリの認証で使われるモデルのこと
#6-1独自のユーザーモデルを作成し、「Eメールアドレスによる認証方法」へ変更する方法。
#python manage.py startapp accountsでアプリを作成setting.pyに追記
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
#django/django/contrib/auth/models.py からインポート6-1
#6-1 BaseUserManageをインポートしてモデルマネジャーを作って、メソッドが使えるようにする
#UserManagerクラスを作って、ユーザーを作成するためのメソッドを作っている

#7-9 signalをインポート
from django.db.models.signals import post_save

GENDER_CHOICE = [(None, "--"), ("m", "男性"), ("f", "女性")]#7-7 onetoonefield

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):#引数でemail,passwardを受け取る
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),#インスタンスを作り、normalize_email(email)で正しい文字列にする
        )

        user.set_password(password)#userインスタンスにパスワードを入れる
        user.save(using=self._db)#データーベースの中にsave
        return user

    def create_staffuser(self, email, password):#クラス内で自分のオブジェクトを呼び出すときは、self.メソッド
        #create_userを呼び出している
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True#デフォルトがfalseなのでtrueにする
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user
    
#django/django/contrib/auth/models.py ← デフォルトのユーザーモデル
#デフォルトのユーザーモデルは、AbstractUserクラスを継承し、下記のフィールドが用意されている。
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Eメールアドレス',
        max_length=255,
        unique=True,
    )
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) 
    admin = models.BooleanField(default=False) 
    #「id」「password」「last_login」の3つは既に備わっている。
    USERNAME_FIELD = 'email'
    #usernamefirldをemailに指定すると、メールアドレスとパスワードを使って認証されるようになる。デフォルトはusername
    #ログインにはemailを使うという宣言
    objects = UserManager()
    #objects = UserManager()で上のUserManagerと紐づけている

    def __str__(self):             
        return self.email#インスタンスを作ったときの名前がemailになる

    def has_perm(self, perm, obj=None):#管理者権限があるなら、trueを返す
        return self.admin

    def has_module_perms(self, app_label):#true,falseを返す
        return self.admin

    @property
    def is_staff(self):#true,falseを返す
        return self.staff

    @property
    def is_admin(self):#true,falseを返す
        return self.admin

    @property
    def is_active(self):#true,falseを返す
        return self.active

#作成したらpython manage.py makemigrations　python manage.py migrateを実行する

#7-7onetoonefieldで新しくProfileクラスを作成する 作ったら
#python manage.py makemigrations　python manage.py migrateを実行
#OneToOneFieldに加えて、必要と思われる項目も追加し、特に必須でない項目には「blank=True, null=True」を追加しています
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)#7-7onetoonefieldで紐づけ
    username = models.CharField(max_length=100, verbose_name="ユーザー名")
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name="部署")
    phone_number = models.IntegerField(blank=True, null=True, verbose_name="携帯番号")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE, default=None, verbose_name="性別", blank=True, null=True)
    birthday = models.DateField(blank=True, null=True, verbose_name="生年月日")

    def __str__(self):
        return self.username
    
    def get_own_archive_url(self):
        from django.urls import reverse_lazy
        return reverse_lazy("nippo-list") + f"?profile={self.id}"
    #8-8
#7-9 signalを使ってprofileを自動生成する
def post_user_created(sender, instance, created, **kwargs):
    if created:
        profile_obj = Profile(user=instance)
        profile_obj.username = instance.email
        profile_obj.save()
#ユーザーが新規のとき、createdはtrue、更新のときはfalse
#sender=Userどのインスタンスが実行されたときにsignalを発動するか
post_save.connect(post_user_created, sender=User)