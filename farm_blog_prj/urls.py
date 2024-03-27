"""farm_blog_prj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

"""사용자가 어떤 URL 형식으로 접근했을 때 어떻게 웹 사이트를 작동시킬지 정리해 놓은 파일"""
"""urls.py는 장고로 개발한 웹 사이트에 방문했을 때 어떤 페이지로 들어가야 하는지 알려줌"""
"""과정: 방문자가 서버 ip/admin/으로 접속하면 admin.site.urls에 정의된 내용을 찾아 처리함"""

from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('blog/',include('blog.urls')), #blog/로 접속할 때는 blog앱의 urls.py를 참고하도록 설정
    path('admin/', admin.site.urls),
    path('',include('single_pages.urls')), #도메인 뒤에 아무것도 붙어 있지 않은 경우 single_pages로 이동하도록 설정
    path('markdownx/', include('markdownx.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)