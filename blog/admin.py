"""django 관리자 페이지 설정"""

from django.contrib import admin
from .models import Post
# Register your models here.

"""관리자 페이지에 Post 모델 등록"""
admin.site.register(Post)
