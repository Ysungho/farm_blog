"""urls.py에 들어갈 함수나 클래스 등은 views.py에서 정의함"""
from django.shortcuts import render

# from django.shortcuts import render
from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView

"""PostList를래스를 ListView클래스를 상속해서 만듬"""


class PostList(ListView):
    model = Post
    ordering = '-pk'

    # template_name = 'blog/index.html'
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

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context


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


def category_page(request, slug):
    # URL에서 추출하여 category_page()함수의 인자로 받은 slug와 동일한 slug를 갖는 카테고리를 불러오는 쿼리셋을 만들어 catetory 변수에 저장
    if slug == 'no_category':  # slug인자가 no_catetory로 넘어오면 카테고리가 없는 포스트만 보여줌
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,  # 필터링한 카테고리만 가지고 올것
            'categories': Category.objects.all(),  # 페이지 오른쪽에 위치한 카테고리 카드를 채워줌
            'no_category_post_count': Post.objects.filter(category=None).count(),  # 카테고리 카드 맨 아래에 미분류 포스트와 그 개수를 알려줌
            'category': category,  # 페이지 타이틀 옆에 카테고리 이름을 알려줌
        }
    )


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()
    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'tag': tag,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
        }
    )
# URL에서 인자로 넘오온 slug와 동일안 slug를 가진 태그를 퀘리셋으로 가져와 tag에 저장
# 태그에 연결된 포스트 전체를 post_list에 저장 후 쿼리 셋으로 가져온 인자를 render()함수 안에 딕셔너리로 담음
# 참고로 categories, tag는 형제 함수로 내용과 만드는 과정이 비슷함
