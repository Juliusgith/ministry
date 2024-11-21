from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.blog_home, name='blog_home'),
    path('about/', views.about_us, name='about_us'),
    path('contact/', views.contact_view, name='contact_us'),
    path('success/', views.success_view, name='success'),
    path('register/', views.register_donation, name='register_donation'),
    path('preview/<int:pk>/', views.preview_donation, name='preview_donation'),
    path('download/<int:pk>/', views.download_pdf, name='download_pdf'),
    path('upload/', views.upload_request_view, name='upload_request'),
    path('verify/<int:pk>/', views.verify_password_view, name='verify_password'),
    path('upload-form/<int:pk>/', views.upload_form_view, name='upload_form'),
    path('thank-you/', views.thank_you_view, name='thank_you'),
] 

# Static and media file configurations
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


