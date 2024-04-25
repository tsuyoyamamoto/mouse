from django.shortcuts import render
#7-9空っぽのviewに新しく作る ユーザーが自分のプロフィールを変更したい。

from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

from .models import Profile
from .forms import ProfileUpdateForm

from utils.access_restrictions import OwnProfileOnly#8-2インポート


#アクセス制限を行う
class ProfileUpdateView(OwnProfileOnly, UpdateView):
    template_name = "accounts/profile-form.html"
    model = Profile
    form_class=ProfileUpdateForm
    success_url = reverse_lazy("nippo-list")
