from django.shortcuts import render
from blog.models import Post
# Create your views here.

from django.shortcuts import render
from blog.models import Post


def landing(request):
    recent_posts = Post.objects.order_by('-pk')[:3]
    return render(
        request,
        'single_pages/landing.html',
        {
            'recent_posts': recent_posts,
        }
    )


"""Django에서 render 함수는 템플릿을 렌더링하여 클라이언트에게 전달할 HTTP 응답을 생성합니다. 
render 함수는 첫 번째 인수로 요청 객체(request)를, 두 번째 인수로 템플릿 파일의 경로를 받습니다. 
필요에 따라 세 번째 인수로 템플릿 컨텍스트(context)를 추가로 전달할 수도 있습니다."""


def about_me(request):
    return render(
        request,
        'single_pages/about_me.html'
    )
