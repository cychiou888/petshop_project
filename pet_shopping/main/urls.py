from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('picture/', views.picture_analyzer, name='picture_analyzer'),
    path('api/predict/', views.detect_pet, name='detect_pet'),
    path('log/', views.login, name='log'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path("about_us/",views.about_us,name="about_us"),
    path("pet_shop/",views.pet_shop,name="pet_shop"),
    path("header/",views.header,name="header"),
    path("footer/",views.footer,name="footer"),
    path("contact/",views.contact_us,name="contact"),   # 寵物辨識頁面
    path('pet-detection/', views.pet_detection, name='pet_detection'),
    path('api/predict/', views.detect_pet, name='detect_pet'),
    path('test-paths/', views.test_paths, name='test_paths')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)