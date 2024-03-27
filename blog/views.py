"""urls.py에 들어갈 함수나 클래스 등은 views.py에서 정의함"""
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect

# from django.shortcuts import render
from .models import Post, Category, Tag, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from .forms import CommentForm

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
        context['comment_form'] = CommentForm
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

class PostCreate(LoginRequiredMixin,UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']  # Post 모델에서 사용할 필드명 리스트

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    # PostCreate에서 form_valid()함수를 재정의하면 CreateView에서 기본으로 제공하는 form_valid()함수의 기능을 확장할 수 있음
    def form_valid(self, form):
        current_user = self.request.user  # self.request.user 는 방문자를 의미
        # is_authenticated로 로그인 상태인지 확인
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            response = super(PostCreate, self).form_valid(form)

            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()

                tags_str = tags_str.replace(',', ';')
                while ';;' in tags_str:
                    tags_str = tags_str.replace(';;', ';')
                tags_list = tags_str.split(';')

                for t in tags_list:
                    t = t.strip()
                    if len(t) < 1: continue
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)

            return response
        else:
            return redirect('/blog/')

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    template_name = 'blog/post_update_form.html'

    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] = '; '.join(tags_str_list)

        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        # 방문자(request.user)는 로그인 한 상태여야 한다.
        # self.get_object().author에서 self.get_object()는 UpdateView의 메서드로 Post.objects.get(pk=pk)과 동일한 역할
        # 이렇게 가져온 Post 인스턴스의 author필드가 방문자와 동일한 경우에만 dispatch()메서드가 원래 역할을 함
        else:
            raise PermissionDenied
        # 그렇지 않은 경우 raise PermissionDenied를 실행


    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(',', ';')
            while ';;' in tags_str:
                tags_str = tags_str.replace(';;', ';')
            tags_list = tags_str.split(';')

            for t in tags_list:
                t = t.strip()
                if len(t) < 1: continue
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)

        return response


def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied