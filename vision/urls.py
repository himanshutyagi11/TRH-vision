from . import views
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    #path('dashboard', views.dashboard, name='dashboard'),
    path('internship/', views.internship, name='internship'),
    path('career/', views.career, name='career'),
    path('services/', views.services, name='services'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('refund-policy/', views.refund_policy, name='refund_policy'),
    path('sigin/', views.sigin, name='sigin'),
    path('signup/', views.signup, name='signup'),
    path('enroll/', views.enroll, name='enroll'),
    path('enroll/success/', views.enroll_success, name='enroll_success'),
    path('payment/create-order/', views.create_razorpay_order, name='create_razorpay_order'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # This captures the ID and sends it to the task_detail function
    path('task/<int:task_id>/', views.task_details, name='task_details'),
    path('submit-project/<int:project_id>/', views.submit_project, name='submit_project'),
    path('download-certificate/', views.generate_certificate, name='generate_certificate'),
    path('download-offer-letter/', views.download_offer_letter, name='download_offer_letter'),
    path('download-offer-letter/<int:enrollment_id>/', views.download_offer_letter, name='download_offer_letter_by_id'),
    path('verify/<str:student_id>/', views.verify_certificate, name='verify_certificate'),
    path('complete-daily-challenge/', views.complete_daily_challenge, name='complete_daily_challenge'),
    path('track-checkin/<int:track_id>/', views.track_checkin, name='track_checkin'),
    path('my-challenges/', views.manage_challenges, name='manage_challenges'),
    
    # ── Client Dashboard URLs ──────────────────────────────────
    path('client/login/', views.client_login, name='client_login'),
    path('client/dashboard/', views.client_dashboard, name='client_dashboard'),
    path('client/project/<int:project_id>/', views.client_project_detail, name='client_project_detail'),

    # ── Custom Admin Panel URLs ────────────────────────────────
    path('trhadmin/', views.trh_admin_dashboard, name='trh_admin_dashboard'),
    path('trhadmin/login/', views.trh_admin_login, name='trh_admin_login'),
    path('trhadmin/students/', views.trh_admin_students, name='trh_admin_students'),
    path('trhadmin/students/<int:user_id>/', views.trh_admin_student_detail, name='trh_admin_student_detail'),
    path('trhadmin/students/<int:user_id>/edit-id/', views.trh_admin_edit_student_id, name='trh_admin_edit_student_id'),
    path('trhadmin/clients/', views.trh_admin_clients, name='trh_admin_clients'),
    path('trhadmin/clients/create/', views.trh_admin_create_client, name='trh_admin_create_client'),
    path('trhadmin/clients/project/create/', views.trh_admin_create_project, name='trh_admin_create_project'),
    path('trhadmin/projects/<int:project_id>/', views.trh_admin_client_project, name='trh_admin_client_project'),
    path('trhadmin/enrollments/', views.trh_admin_enrollments, name='trh_admin_enrollments'),
    path('trhadmin/enrollments/<int:enrollment_id>/approve/', views.trh_admin_approve_enrollment, name='trh_admin_approve_enrollment'),
    path('trhadmin/enrollments/<int:enrollment_id>/send-offer/', views.trh_admin_send_offer_letter, name='trh_admin_send_offer_letter'),
    path('trhadmin/enrollments/<int:enrollment_id>/send-credentials/', views.trh_admin_send_credentials, name='trh_admin_send_credentials'),
    path('trhadmin/contacts/', views.trh_admin_contacts, name='trh_admin_contacts'),

    # Password Reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html',
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url='/reset/done/',
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html',
    ), name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


