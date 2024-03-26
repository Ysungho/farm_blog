"""urls.py는 장고로 개발한 웹 사이트에 방문했을 때 어떤 페이지로 들어가야 하는지 알려줌"""

from django.urls import path
from . import views

"""urlpatterns는 URL과 URL이 들어올 때 어떻게 처리할지 명시해 줌"""
urlpatterns=[
    # '도메인 뒤에 /blog/가 붙었을 때는 blog/urls.py에서 처리한다'->blog/urls.py로 접근
    # /blog/ 뒤에 아무것도 없다면 blog/views.py에서 정의된 index()함수에서 처리
    #path('', views.index),
    #path('<int:pk>/',views.single_post_page),
    path('',views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),

    # catetory/뒤에 문자열이 붙는 URL을 입력하면 그 문자열을 views.py에 정의할 category_page()함수의 매개변수인 slug의 인자로 념겨줌
    # 127.0.0.1:8000/blog/category/programming/이라고 입력하면 programming/만 떼어 views.py의 category_page()로 보냄
    path('category/<str:slug>/', views.category_page),

]