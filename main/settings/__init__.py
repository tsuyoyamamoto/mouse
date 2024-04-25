# 9-1 setting.pyからsettingフォルダへ変更 local環境と本番環境を分ける


try:
    from .base import *
    
except:
    from .locals import *