"""도메인 뒤에 아무것도 없으면 views.py에 있는 landing() 대문 페이지로
   도메인 뒤에 about_me/ 가 붙어 있으면 about_me() 함수를 실행해 자기 소개 페이지를 보여주도록 구성"""

from django.urls import path
from . import views

urlpatterns=[
    path('about_me/',views.about_me),
    path('',views.landing),
]