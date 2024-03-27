"""django 관리자 페이지 설정"""

from django.contrib import admin
from .models import Post, Category, Tag, Comment


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
# Category모델의 name필드 값이 입력됐을 때 자동으로 slug 값이 생성됨

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


"""관리자 페이지에 Post 모델 등록"""
admin.site.register(Post)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment)
