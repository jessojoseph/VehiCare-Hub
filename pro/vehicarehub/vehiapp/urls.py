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
    path('create_slots/', views.create_daily_slots, name='create_slots'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('viewappointments/', views.viewappointment, name='viewappointments'),
    path('cancel_appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('admin_view_updates/', views.admin_view_updates, name='admin_view_updates'),



    path('search_services/', views.search_services, name='search_services'),
    path('change_password/', views.change_password_client, name='change_password'),
    path('service/<int:service_id>/', views.service_view, name='service_view'),

    path('addworker/', views.addWorker, name='addworker'),
    path('workerdashboard/', views.workerdashboard, name='workerdashboard'),
    path('viewworker/', views.viewworker, name='viewworker'),
    path('worker_details/', views.worker_details, name='worker_details'),
    path('editworker/', views.editworker, name='editworker'), 
    path('viewservice/<int:view_id>', views.view_service, name='viewservice'),
    path('admindash/', views.admindash, name='admindash'), 



    path('assign_task', views.assign_task, name='assign_task'), 
    path('workerdashboard/task/', views.worker_dashboard_tasks, name='worker_dashboard_tasks'),
    path('worker/update_work_status/<int:task_id>/', views.update_work_status, name='update_work_status'),
    path('view_updates/', views.view_updates, name='view_updates'),
    path('work_overview/', views.work_overview, name='work_overview'),
    path('leave_request/', views.leave_request, name='leave_request'),
    path('view_leavereq/', views.view_leavereq, name='view_leavereq'),
    path('view_leavestat/', views.view_leavestat, name='view_leavestat'),
    path('payment/<int:appointment_id>/', views.payment, name='payment'),
    path('paymenthandler/<int:appointment_id>/', views.paymenthandler, name='paymenthandler'),

    path('checkcondition/', views.prediction, name='checkcondition'),


 
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

