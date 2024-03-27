"""블로그의 핵심인 포스트의 형태를 정의하는 Post 모델을 만듬"""
"""제목(title), 내용(content), 작성일(created_at), 작성자 정보(author)가 필요"""

from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
import os


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    # unique=True는 동일한 이름의 카테고리를 만들 수 없음
    # SlugField 는 사람이 읽을 수 있는 텍스트로 고유 URL를 만들고 싶을 때 사용

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'

    # class Meta:
    #     verbose_name_plural = 'categories'


# Create your models here.
class Post(models.Model):
    """CharField는 문자(char)를 담는 필드를 만듬
    content필드는 문자열의 길이 제한을 TextField를 사용해서 만듬
    created_at 필드는 DateTimeField로 만듬
    DateTimeField는 월,일,시,분,초까지 기록할 수 있게 필드를 만듬"""
    title = models.CharField(max_length=20)  # 제목: 최대 20글자
    hook_text = models.CharField(max_length=100, blank=True)
    content = MarkdownxField()  # 글 내용

    # blank=True는 해당 옵션이 필수는 아니라는 뜻
    # blog/files/년/월/일/ 경로가 생기고, 그 아래 파일이 저장됨
    head_image = models.ImageField(upload_to='blog/images/%y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%y/%m/%d/', blank=True)

    # 포스트 작성
    created_at = models.DateTimeField(auto_now_add=True)  # 작성시간 : 현재 시간 자동 입력
    # auto_now_add=True 처음 레코드가 설정될 때 현재 시각이 자동으로 저장

    # 포스트 수정
    updated_at = models.DateTimeField(auto_now=True)

    # 작성자
    # on_delete=models.SET_NULL은 작성자가 데이터베이스에서 삭제되었을 때 작성자 명을 빈칸으로 만듬
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # null=True는 미분류 카테고리 존재, ForeignKey로 연결된 카테고리가 삭제되면 catetory필드만 null이 되도록 설정
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    tags = models.ManyToManyField(Tag, blank=True)

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://doitdjango.com/avatar/id/1439/f72fd099673af77a/svg/{self.author.email}.png'

    def __str__(self):
        return f'[{self.pk}]{self.title}::{self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]

    def get_content_markdown(self):
        return markdown(self.content)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    # content 필드는 TestField로 구성하고 줄바꿈 만 구현
    # created_at 필드와 modified_at 필드는 DateTimeField로 만듬
    # created_at 필드에는 처음 생성될 때 시간을 저장하도록 auto_now=True로 설정
    # modified_at 필드는 저장될 때 시간을 저장하도록 auto_now=True로 설정

    # 작성자 명 출력
    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'	https://doitdjango.com/avatar/id/1439/d7bd69a23722d433/svg/{self.author.username}'
