from pathlib import Path
#9-1デブロイ前にやること三選
from dotenv import load_dotenv
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent 
#　manage.pyのある場所
#9-1で階層が下がったので、parentを追加、合計３つ

#9-1でPARENT_DIRも追記
PARENT_DIR = Path(__file__).resolve().parent.parent.parent.parent

#9-1デブロイ前にやること三選
env_path = PARENT_DIR / "auth/.env"
load_dotenv(env_path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

#9-1デブロイ前にやること三選
SECRET_KEY = os.environ.get("secret_key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
# アプリを登録するためのもの
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',#7-4メッセージフレームワークの使い方であるのか確認
    'django.contrib.staticfiles',
    #django-allauth 6-3　追加
    'django.contrib.sites',    
    'allauth',     
    'allauth.account',     
    'allauth.socialaccount',#カンマを入れないと認識されないエラーが出た
    #apps
    'nippo',#作ったアプリを認識させる1-3
    'accounts',#6-1ユーザーモデルクラスの作成settings.pyへ追記
    #6-6 templateの変更 bootstrapを適用できるようにする下記の流れでcirspy_formというモジュールをインストールします。
    #crispy_formは、フォームに対して自動でBootstrapクラスを適用してくれるモジュールです。pip install django-crispy-forms
    ##pip install django-crispy-forms==1.14.0のバージョンでインストールしないとエラーになる
    "crispy_forms",#6-6追記
     'bootstrap4',#8-6カレンダーの表示
     'bootstrap_datepicker_plus',#8-6カレンダーの表示で追記
     'django_filters',#8-7 djangoフィルターの導入で追記（インストール後）
]

MIDDLEWARE = [
    "allauth.account.middleware.AccountMiddleware",#6-3 django-allauthの設定DjangoにおけるMiddleware（ミドルウェア）とは、Djangoのリクエスト／レスポンス処理の前後でフックを加える仕組みです。
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',#7-4メッセージフレームワークの使い方であるのか確認
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',#7-4メッセージフレームワークの使い方であるのか確認
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / "templates"], #1-3 srcの中にtemplatesを作る
        #テンプレートフォルダとは、HTMLファイルを保存していくフォルダになります
        #manage.pyのある場所に、templatesを作ると、htmlが自動的に認識される
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',#7-6requestが取得できるか確認default
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',#7-4メッセージフレームワークの使い方であるのか確認
            ],
            'builtins':[ 
                'bootstrap4.templatetags.bootstrap4',#8-6カレンダー表示
            ],
        },
    },
]

BOOTSTRAP4 = {#8-6カレンダー表記で追記
    'include_jquery': True,
}

WSGI_APPLICATION = 'main.wsgi.application'

AUTH_USER_MODEL = 'accounts.User'#このアプリを認証用として使うという宣言accountsはアプリ名、Userはモデルクラス名
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ja' #1-3設定

TIME_ZONE = 'Asia/Tokyo' #1-3設定



USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'  #スタティックファイルとは、.cssや、.jsファイルなどを入れておくフォルダ
STATICFILES_DIRS = [BASE_DIR / "static_local" ] #メディアファイルとは、画像などを入れておくフォルダ srcの下にフォルダを作成する
#manage.pyのところに、static_localフォルダを作るという意味
#static_local > cssとフォルダが続き、その中に「footer.css」を作成

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media_local"
#MEDIA_URL = '/media/'で画像を表示するためのpathを設定する
#MEDIA_URL：ブラウザからアクセスする際のアドレス 4-5画像を表示する方法
#MEDIA_ROOT：画像ファイルを読み込みにいく先のフォルダ 4-5画像を表示する方法
 
# JS ファイルとは何ですか? JS (JavaScript) は、Web ページで実行するための JavaScript コードを含むファイルです。 JavaScript ファイルは . js 拡張子で保存されます。
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [ 
  'django.contrib.auth.backends.ModelBackend', #デフォルト
  'allauth.account.auth_backends.AuthenticationBackend',#メールアドレスとパスワードの両方を使って認証する
] 

SITE_ID = 1#djangoの識別値

#ユーザーネームは使わない
ACCOUNT_USERNAME_REQUIRED = False 
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

#認証にはメールアドレスを使用する
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True

#ログイン後のリダイレクト先を指定
from django.urls import reverse_lazy
LOGIN_REDIRECT_URL = reverse_lazy('nippo-list')

#7-10 adapteで"accounts.adapter.MyNippoAdapter"を使うことを宣言
ACCOUNT_ADAPTER = "accounts.adapter.MyNippoAdapter"


"""
7-10 adapterを使う
django-allauth allauth>account>adapter.py に
   get_login_redirect_url(self, request):があり、
   　　　else:
            url = settings.LOGIN_REDIRECT_URL
        return resolve_url(url)
    これにより、ログイン後のリダイレクト先を指定している。
    だから、adapter.pyを同じように作り、ここを書き換えれば、aapterが使える
    setting.pyには上記の意味が備わっている
"""


#ログアウト後のリダイレクト先を指定allauthは全て"account_●●●"
ACCOUNT_LOGOUT_REDIRECT_URL = reverse_lazy("account_login")

#メールアドレスが確認済みである必要がある
ACCOUNT_EMAIL_VERIFICATION = "mandatory"

#即ログアウトとする
ACCOUNT_LOGOUT_ON_GET = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
#6-5　ConnectionRefusedエラーを回避し、Emailをターミナルに表示する

CRISPY_TEMPLATE_PACK = 'bootstrap4'#pip install django-crispy-forms==1.14.0のバージョンでインストールしないとエラーになる

"""
Djangoのログインの仕組み
djangoの認証は認証用のバックエンドによって行われます。このバックエンドはsettings.pyのAUTHENTICATION_BACKENDSに設定します。AUTHENTICATION_BACKENDSのデフォルト値は’django.contrib.auth.backends.ModelBackend’１つですが、バックエンドは配列として追加することが出来ます。

Djangoの認証はdjango.contrib.auth.authenticate関数で行われます。このauthenticate関数が呼ばれるとAUTHENTICATION_BACKENDSに記載されたバックエンドのauthenticate関数を順番に呼び出します。認証に失敗すれば次のバックエンドを呼び出します。もし認証に成功すれば、認証されたユーザーを返す仕組みです。

"""
"""
6-3でsetting.pyの設定が終わったら、mygrate　→　管理者ページでメールアドレスとサイトを登録する
新しくユーザーを登録した場合、自動的に登録されるが、既存のユーザーは、登録しなおさなければならない.
サイトは　localhost:8000に変更
loginのための認証方法をusernameからemailに変更するのが6-4
"""


"""1-3のフォルダの作成
src
├── main
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── media_local #作成しました
└── static_local #作成しました
1-3設定
テンプレートフォルダの設定
言語・タイムゾーンの設定
static, mediaフォルダの設定
"""
"""
DjangoにおけるMiddleware（ミドルウェア）とは、
Djangoのリクエスト／レスポンス処理の前後でフックを加える仕組みです。
"""