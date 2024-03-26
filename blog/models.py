"""블로그의 핵심인 포스트의 형태를 정의하는 Post 모델을 만듬"""
"""제목(title), 내용(content), 작성일(created_at), 작성자 정보(author)가 필요"""

from django.db import models


# Create your models here.
class Post(models.Model):
    """CharField는 문자(char)를 담는 필드를 만듬
    content필드는 문자열의 길이 제한을 TextField를 사용해서 만듬
    created_at 필드는 DateTimeField로 만듬
    DateTimeField는 월,일,시,분,초까지 기록할 수 있게 필드를 만듬"""
    title = models.CharField(max_length=20)  # 제목: 최대 20글자
    content = models.TextField()  # 글 내용

    #blank=True는 해당 옵션이 필수는 아니라는 뜻
    head_image = models.ImageField(upload_to='blog/images/%y/%m/%d/', blank=True)
    # 포스트 작성
    created_at = models.DateTimeField(auto_now_add=True)  # 작성시간 : 현재 시간 자동 입력
    # auto_now_add=True 처음 레코드가 설정될 때 현재 시각이 자동으로 저장

    # 포스트 수정
    updated_at = models.DateTimeField(auto_now=True)

    # 작성자는 추후 작성 예정

    def __str__(self):
        return f'[{self.pk}]{self.title}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'
