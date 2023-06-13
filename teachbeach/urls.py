from django.conf.urls import url, include
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django.views.decorators.csrf import csrf_exempt

from main.views import (
    CompanyInstructorsView, TeacherViewSet, VenueViewSet, ClassView,
    CategoryViewSet, SubCategoryViewSet,
    InitView, ClassMediaViewSet, TeacherProfileView,
    CityView, SearchClassView, LearnerView,
    ClassDetailsView, ZipView,
    OrderView, PrivateEnrollView, GroupEnrollView,  
    LearnerClassesView, TeacherStudentsView,
    TeacherClassesView, SelectedTeacherClassesView,
    TeacherStripeAccountView, StripeAddCardView,
    PrivateEnrollConfirmView, PrivateEnrollRejectView,
    MessageViewSet, DraftClassViewSet, CloneClassView,
    StripeDeleteCardView, PaymentCardsView,
    StripeDefaultCardView, AddSubCategoryView,
    CompanyProfileView, UserViewSet, SelectedCompanyClassesView,
    EnrollNoPayClassView, CompanyVenueView, MostRecentClassesView,
    EnrFromSecretView, DeactivateClass, CsvExportView,
    LearnerClassPackageView, OrderRefundView,
    NewsletterView, TeacherClassMessageView,
    CsvStudentExportView, SearchView, ServiceFeeView,
    BuyMembershipView, BoostClassView, BuyEmailBoostView,
    RescheduleEnrollmentView, CancelMembershipView, EventViewSet,
    TeacherScheduleEnrollmentView, RequestClassView,
    CancelEnrollmentView, VideoFormView, SendOffersView,
    SendStudentEmailView, ICalView, TeacherMessageView,
    AutoCompleteView, SendAddStudent, TeacherStudentsEmail,
    TeacherBulkRescheduleView, TeacherSignInStudentView,
    UserSettingsView, HandShakeView, TeacherDashboardPreloadView,
    UserView, DeleteStudentView, AddManagedStudent, ExternalCalendarView,
    UploadStudents, MembershipView, ClassMembershipView, ClassTeacherView,
    StripeBuyMembershipView, MembershipByIdView, MembershipsListView, CompanyTeacherRequest, UpdateManagedStudent,
    StripeCancelMembershipView, CsvMembersExportView, TeacherCancelPrivateEnrollmentView,
    VueEditorUploadFileView, FacebookSignUp, GoogleSocialAuthView, StudentMembershipView,
    DiscussionSetupView, DiscussionDetailView, DiscussionCommentView,
    DiscussionAllListView
)
from . import views
from .sitemaps import (
    ClassSitemap, TeacherSitemap, StaticSitemap, CompanySitemap,
)

"""teachbeach URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

router = routers.DefaultRouter()
router.register(r'teachers', TeacherViewSet)
router.register(r'users', UserViewSet)
router.register(r'venues', VenueViewSet)
router.register(r'events', EventViewSet)
router.register(r'class_media', ClassMediaViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubCategoryViewSet, 'subcategories')
router.register(r'messages', MessageViewSet)
router.register(r'draft', DraftClassViewSet)

sitemaps = {
    'class': ClassSitemap,
    'teacher': TeacherSitemap,
    'static': StaticSitemap,
    'company': CompanySitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path("socket/", include("web_socket.urls")),
    # path('social-auth/', include('social_django.urls', namespace='social')),
    path('social/facebook/', csrf_exempt(FacebookSignUp.as_view()), name='facebook-auth'),
    path('social/google/', csrf_exempt(GoogleSocialAuthView.as_view()), name='google-auth'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    # Authentication
    url(r'^api/auth/login/', views.LoginView.as_view()),
    url(r'^api/auth/logout/', views.LogoutView.as_view()),
    url(r'^api/auth/change_password/', views.ChangePasswordView.as_view()),
    # forgot password
    url(r'^api/user/reset_password/$', views.StartPasswordResetView.as_view()),
    url(r'^api/user/reset_password/finish/$', views.FinishPasswordResetView.as_view()),
    url(r'^password_reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/', views.PasswordResetView.as_view(), name='password_reset_confirm'),

    # main api
    url(r'^api/init/', InitView.as_view()),
    url(r'^api/user/', UserView.as_view()),
    url(r'^api/handshake/', HandShakeView.as_view()),
    url(r'^api/clone_class/(\d*)/', CloneClassView.as_view()),
    url(r'^api/classes/(\d*)/', ClassDetailsView.as_view()),
    url(r'^api/classes/', ClassView.as_view()),
    url(r'^api/add_subcategory/', AddSubCategoryView.as_view()),
    url(r'^api/learner/classes/', LearnerClassesView.as_view()),
    url(r'^api/learners/', LearnerView.as_view()),
    url(r'^api/learner/class_packages/(\d*)/', LearnerClassPackageView.as_view()),
    url(r'^api/stripe/add_card', StripeAddCardView.as_view()),
    url(r'^api/enroll_class', EnrollNoPayClassView.as_view()),
    url(r'^api/stripe/delete_card/(.*)/', StripeDeleteCardView.as_view()),
    url(r'^api/stripe/set_default_card/(.*)/', StripeDefaultCardView.as_view()),
    url(r'^api/private_enroll/(\d*)/confirm/', PrivateEnrollConfirmView.as_view()),
    url(r'^api/private_enroll/(\d*)/reject/', PrivateEnrollRejectView.as_view()),
    url(r'^api/private_enroll/', PrivateEnrollView.as_view()),
    url(r'^api/group_enroll/', GroupEnrollView.as_view()),
    url(r'^api/orders/(\d*)/refund/', OrderRefundView.as_view()),
    url(r'^api/orders/(\d*)/', OrderView.as_view()),
    url(r'^api/newsletter', NewsletterView.as_view()),
    url(r'^api/deactivate_class/', DeactivateClass.as_view()),
    url(r'^api/filter_classes/', SearchClassView.as_view()),
    url(r'^api/cities/', CityView.as_view()),
    url(r'^api/zips/', ZipView.as_view()),
    url(r'^api/csv_export/', CsvExportView.as_view()),
    url(r'^api/csv_student_export/', CsvStudentExportView.as_view()),
    url(r'^api/csv_members_export/', CsvMembersExportView.as_view()),
    url(r'^api/teacher_profile/(\d*)/', TeacherProfileView.as_view()),
    url(r'^api/teacher_profile/', TeacherProfileView.as_view()),
    url(r'^api/company_profile/(.*)/', CompanyProfileView.as_view()),
    url(r'^api/company_profile/', CompanyProfileView.as_view()),
    url(r'^api/company_venues/', CompanyVenueView.as_view()),
    url(r'^api/teacher_students/', TeacherStudentsView.as_view()),
    url(r'^api/teacher/(\d*)/classes/', SelectedTeacherClassesView.as_view()),
    url(r'^api/company/(\d*)/classes/', SelectedCompanyClassesView.as_view()),
    url(r'^api/teacher_classes/', TeacherClassesView.as_view()),
    url(r'^api/payment_cards/', PaymentCardsView.as_view()),
    url(r'^api/teacher/create_stripe_account/', TeacherStripeAccountView.as_view()),
    url(r'^api/most_recent_classes/', MostRecentClassesView.as_view()),
    url(r'^api/enr_from_secret/(.*)/', EnrFromSecretView.as_view()),
    url(r'^api/teacher_class/(\d*)/message/', TeacherClassMessageView.as_view()),
    url(r'^api/search/(.*)', SearchView.as_view()),
    url(r'^api/service_fee/', ServiceFeeView.as_view()),
    url(r'^api/buy_membership', BuyMembershipView.as_view()),
    url(r'^api/cancel_membership', CancelMembershipView.as_view()),
    url(r'^api/buy_email_boost', BuyEmailBoostView.as_view()),
    url(r'^api/boost_class/(\d*)/', BoostClassView.as_view()),
    url(r'^api/teacher_reschedule', RescheduleEnrollmentView.as_view()),
    url(r'^api/teacherd_schedule_enrollment/', TeacherScheduleEnrollmentView.as_view()),
    url(r'^api/teacher_date_reschedule', TeacherBulkRescheduleView.as_view()),
    url(r'^api/teacher_cancel_private_erollment', TeacherCancelPrivateEnrollmentView.as_view()),
    url(r'^api/request_class', RequestClassView.as_view()),
    url(r'^api/student_cancel_enrollment/(\d*)', CancelEnrollmentView.as_view()),
    url(r'^api/video_form_request/', VideoFormView.as_view()),
    url(r'^api/send_offers/', SendOffersView.as_view()),
    url(r'^api/autocomplete/', AutoCompleteView.as_view()),
    url(r'^api/send_email_to_student/', SendStudentEmailView.as_view()),
    url(r'^api/ical', ICalView.as_view()),
    url(r'^api/message/', TeacherMessageView.as_view()),
    url(r'^api/send_add_student_request/', SendAddStudent.as_view()),
    url(r'^api/teacher_students_email/', TeacherStudentsEmail.as_view()),
    url(r'^api/teacher_sign_student', TeacherSignInStudentView.as_view()),
    url(r'^api/user_settings/', UserSettingsView.as_view()),
    url(r'^api/teacher_dashboard_preload/', TeacherDashboardPreloadView.as_view()),
    url(r'^api/add_managed_student/', AddManagedStudent.as_view()),
    url(r'^api/update_managed_student/', UpdateManagedStudent.as_view()),
    url(r'^api/delete_student/', DeleteStudentView.as_view()),
    url(r'^api/external_calendar/', ExternalCalendarView.as_view()),
    url(r'^api/upload_students/', UploadStudents.as_view()),
    url(r'^twilio/sms/', views.TwilioSMS.as_view()),
    url(r'^api/memberships/', MembershipsListView.as_view()),
    url(r'^api/teacher_membership/(\d*)/', MembershipByIdView.as_view()),
    url(r'^api/teacher_membership/', MembershipView.as_view()),
    url(r'^api/learner_memberships/', StudentMembershipView.as_view()),
    url(r'^api/class_teacher/(\d*)/', ClassTeacherView.as_view()),
    url(r'^api/class_membership/(\d*)/', ClassMembershipView.as_view()),
    url(r'^api/stripe/buy_membership', StripeBuyMembershipView.as_view()),
    url(r'^api/stripe/cancel_membership/', StripeCancelMembershipView.as_view()),
    url(r'^api/company_teacher_request/', CompanyTeacherRequest.as_view()),
    url(r'^api/company_instructors/', CompanyInstructorsView.as_view()),
    url(r'^api/vue_editor_upload_file/', csrf_exempt(VueEditorUploadFileView.as_view())),

    # DISCUSSION
    url(r'^api/discussion-setup/', DiscussionSetupView.as_view()), # SETUP DISc.
    url(r'^api/discussion/all/$', DiscussionAllListView.as_view()), # FETCH ALL DISc.
    url(r'^api/discussion/(\d*)/$', DiscussionDetailView.as_view()), # LATEST DISc.
    url(r'^api/discussion/$', DiscussionDetailView.as_view()), # SPECIFIC DISc.
    url(r'^api/comments/(\d*)/$', DiscussionCommentView.as_view()), # DISc. Comments

    url(r'^api/', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += url(r'', views.AppView.as_view()),