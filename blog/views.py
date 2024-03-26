"""urls.py에 들어갈 함수나 클래스 등은 views.py에서 정의함"""

#from django.shortcuts import render
from .models import Post, Category
from django.views.generic import ListView, DetailView

"""PostList를래스를 ListView클래스를 상속해서 만듬"""
class PostList(ListView):
    model = Post
    ordering = '-pk'
    #template_name = 'blog/index.html'
    # html파일명을 _list.html로 변경하거나 template_name='blog/index.html'로 설정하면 됨

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()

        # Category.objects.all()로 모든 카테고리를가져와  'categories'라는 이름의 키에 연결함
        context['categories'] = Category.objects.all()

        # Post.objects.filter(category=None).count()로 쿼리셋을 만들어 'no_category_post_count'에 연결
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

class PostDetail(DetailView):
    model = Post


# def index(request):
#     # Post.objects.all()로 모든 Post 레코드를 가져와 posts에 저장
#     # .order_by('.pk')는 pk값의 역순으로 정렬=> 가장 최근에 만든 포스트 부터 조회됨
#     posts = Post.objects.all().order_by('-pk')
#
#     # render() 함수 안에 posts를 딕셔너리 형태로 추가
#     return render(
#         # index.html에서 posts를 이용가능하게 만들어줌
#         request,
#         'blog/index.html',
#         {
#             # index.html에서 {%for p in posts%} 형식으로 사용하면 {{p.title}} 이렇게 사용가능
#             # {{}}은 단순 변수임
#             # 반드시 {%endfor%}로 마무리 해야함
#
#             'posts': posts,
#         }
#     )


def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)

    return render(
        request,
        'blog/single_post_page.html',
        {
            'post': post,
        }
    )
