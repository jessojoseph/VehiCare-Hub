from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('service/', views.listService, name='service'),
    path('add-service/', views.addservice, name='add-service'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('viewprofile/', views.viewprofile, name='viewprofile'),
    path('service/delete/<int:service_id>/', views.delete_service, name='delete_service'),
    path('update_service/<int:service_id>/', views.update_service, name='update_service'),
    path('base/', views.base, name='base'),
    path('book_appointment/', views.book_appointment, name='book_appointment'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('search/', views.search_view, name='search_results'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
    path('change_password/', views.change_password_client, name='change_password'),
    path('service/<int:service_id>/', views.service_view, name='service_view'),

    path('addworker/', views.addWorker, name='addworker'),
    path('workerdashboard/', views.workerdashboard, name='workerdashboard'),
    path('viewworker/', views.viewworker, name='viewworker'),
    path('worker_details/', views.worker_details, name='worker_details'),
    path('editworker/', views.editworker, name='editworker'), 
 


 
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
