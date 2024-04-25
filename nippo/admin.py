#admin.pyは管理画面の表示にかんする役割を担っている
from django.contrib import admin
from .models import NippoModel #追記1-5




#admin.site.register(NippoModel)#1-5　modelを管理サイトに登録する。

class NippoModelAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "public",
        "date",
        "slug",
        "timestamp"
    )
    list_filter = (
        "date",
        "user",
        "public"
    )
    ordering = ("date","timestamp","user")
    filter_horizontal = ()

    search_fields = ('title',"content","user")

admin.site.register(NippoModel, NippoModelAdmin)

