from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('login2/', views.login2, name='login2'),
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




    path('insureadmindash/', views.insureadmindash, name='insureadmindash'),
    path('addadvisor/', views.addadvisor, name='addadvisor'),
    path('admin_category', views.admin_category_view,name='admin_category'),
    path('admin_view_category', views.admin_view_category_view,name='admin_view_category'),
    path('admin_update_category', views.admin_update_category_view,name='admin_update_category'),
    path('update_category/<int:pk>', views.update_category_view,name='update_category'),
    path('admin_add_category', views.admin_add_category_view,name='admin_add_category'),
    path('admin_delete_category', views.admin_delete_category_view,name='admin_delete_category'),
    path('delete_category/<int:pk>', views.delete_category_view,name='delete_category'),


    path('admin_policy', views.admin_policy_view,name='admin_policy'),
    path('admin_add_policy', views.admin_add_policy_view,name='admin_add_policy'),
    path('admin_view_policy', views.admin_view_policy_view,name='admin_view_policy'),
    path('admin_update_policy', views.admin_update_policy_view,name='admin_update_policy'),
    path('update_policy/<int:pk>', views.update_policy_view,name='update_policy'),
    path('admin_delete_policy', views.admin_delete_policy_view,name='admin_delete_policy'),
    path('delete_policy/<int:pk>', views.delete_policy_view,name='delete_policy'),

    path('admin_view_policy_holder', views.admin_view_policy_holder_view,name='admin_view_policy_holder'),
    path('admin_view_approved_policy_holder', views.admin_view_approved_policy_holder_view,name='admin_view_approved_policy_holder'),
    path('admin_view_disapproved_policy_holder', views.admin_view_disapproved_policy_holder_view,name='admin_view_disapproved_policy_holder'),
    path('admin_view_waiting_policy_holder', views.admin_view_waiting_policy_holder_view,name='admin_view_waiting_policy_holder'),
    path('approve_request/<int:pk>', views.approve_request_view,name='approve_request'),
    path('reject_request/<int:pk>', views.disapprove_request_view,name='reject_request'),

    path('admin_question/', views.admin_question_view,name='admin_question'),
    path('update_question/<int:pk>', views.update_question_view,name='update_question'),

    path('admin_view_customer/', views.admin_view_customer_view,name='admin_view_customer'),
    path('update_customer/<int:pk>', views.update_customer_view,name='update_customer'),
    path('delete_customer/<int:pk>', views.delete_customer_view,name='delete_customer'),
    # path('insure1/', views.insure1, name='insure1'),
    
    # path('customerclick', views.customerclick_view,name='customerclick'),
    # path('customersignup', views.customer_signup_view,name='customersignup'),
    path('customer_dashboard', views.customer_dashboard_view,name='customer_dashboard'),

    path('apply_policy', views.apply_policy_view,name='apply_policy'),
    # path('apply/<int:pk>/', views.apply_insurance_view, name='apply'),
    path('apply/<int:pk>/', views.apply_insurance_view, name='apply_insurance'),
    path('history', views.history_view,name='history'),

    path('apply_insurance/<int:pk>/', views.apply_insurance_view, name='apply_insurance'),
    path('history_claim/', views.history_claim_view, name='history_claim'),
    path('admin_history_claim/', views.admin_history_claim_view, name='admin_history_claim'),
    path('approve_claim/<int:claim_id>/', views.approve_claim, name='approve_claim'),
    path('reject_claim/<int:claim_id>/', views.reject_claim, name='reject_claim'),

    path('admin_add_surveyor/', views.register_surveyor, name='admin_add_surveyor'),

    path('survayordashboard/', views.survayor_dashboard, name='survayordashboard'),
    path('survayorbase/', views.survayor_base_dashboard, name='survayorbase'),
    path('update_survayor/<int:pk>/', views.update_survayor_view, name='update_survayor'),
    path('admin_view_survayor/', views.admin_view_survayor_view, name='admin_view_survayor'),
    path('admin_assign_claim/', views.assign_claim_view, name='admin_assign_claim'),
    path('surveyor_assigned_claims/', views.surveyor_assigned_claims, name='surveyor_assigned_claims'),
    path('view_claim_details/<int:claim_id>/', views.view_claim_details, name='view_claim_details'),


    path('ask_question', views.ask_question_view,name='ask_question'),
    path('question_history', views.question_history_view,name='question_history'),
    path('submit_claim/', views.submit_claim_view, name='submit_claim'),

    path('request_assistance/', views.request_assistance, name='assistance'),
    path('breakdown-requests/', views.breakdown_requests, name='assistance_requests'),

    path('assign-breakdown/', views.assign_breakdown, name='assign-breakdown'),
    path('worker_breakdown/', views.worker_breakdown, name='worker_breakdown'),

    path('send-otp-to-customer/<int:request_id>/', views.send_otp_to_customer, name='send_otp_to_customer'),
    path('verify-order-otp/', views.verify_order_otp, name='verify_order_otp'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

