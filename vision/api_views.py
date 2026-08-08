"""
vision/api_views.py
Django REST Framework ViewSets for all TRH models.
All endpoints require Token Authentication (admin token).

Power BI usage:
  GET /api/v1/<endpoint>/   → returns JSON array of all records
  GET /api/v1/<endpoint>/<id>/  → returns single record

Authentication header required:
  Authorization: Token <your-admin-token>
"""

from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import (
    Task, Project, ProjectSubmission,
    Profile, Question, LearningMaterial,
    Contact, ClientRequest, Enrollment,
    Announcement, InternshipPricing,
    ChallengeTrack, UserChallengeEnrollment,
    DailyTrackCheckIn, MilestoneAchievement, UserStreak,
    ClientProfile, ClientProject, ClientProjectMilestone,
    ClientProjectDeliverable, ClientProjectUpdate, ClientInvoice,
    Review,
)

from .serializers import (
    UserSerializer, EnrollmentSerializer, ProfileSerializer,
    TaskSerializer, QuestionSerializer, LearningMaterialSerializer,
    ProjectSerializer, ProjectSubmissionSerializer,
    ContactSerializer, ClientRequestSerializer,
    AnnouncementSerializer, InternshipPricingSerializer, ReviewSerializer,
    ChallengeTrackSerializer, UserChallengeEnrollmentSerializer,
    DailyTrackCheckInSerializer, MilestoneAchievementSerializer, UserStreakSerializer,
    ClientProfileSerializer, ClientProjectSerializer,
    ClientProjectMilestoneSerializer, ClientProjectDeliverableSerializer,
    ClientProjectUpdateSerializer, ClientInvoiceSerializer,
)


# ---------------------------------------------------------------------------
#  API ROOT  — lists all available endpoints
# ---------------------------------------------------------------------------

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def api_root(request, format=None):
    """
    TRH Vision REST API — all available endpoints.
    Include header:  Authorization: Token <your-admin-token>
    """
    return Response({
        # Auth
        'obtain-token':         reverse('api-token-auth', request=request, format=format),

        # Internship / Students
        'enrollments':          reverse('enrollment-list', request=request, format=format),
        'students':             reverse('profile-list', request=request, format=format),
        'users':                reverse('user-list', request=request, format=format),

        # Curriculum
        'tasks':                reverse('task-list', request=request, format=format),
        'questions':            reverse('question-list', request=request, format=format),
        'learning-materials':   reverse('learningmaterial-list', request=request, format=format),

        # Projects
        'projects':             reverse('project-list', request=request, format=format),
        'project-submissions':  reverse('projectsubmission-list', request=request, format=format),

        # Contacts
        'contacts':             reverse('contact-list', request=request, format=format),
        'client-requests':      reverse('clientrequest-list', request=request, format=format),

        # CMS
        'announcements':        reverse('announcement-list', request=request, format=format),
        'pricing':              reverse('internshippricing-list', request=request, format=format),
        'reviews':              reverse('review-list', request=request, format=format),

        # Daily Challenges
        'challenge-tracks':         reverse('challengetrack-list', request=request, format=format),
        'challenge-enrollments':    reverse('userchallengeenrollment-list', request=request, format=format),
        'daily-checkins':           reverse('dailytrackcheckin-list', request=request, format=format),
        'milestone-achievements':   reverse('milestoneachievement-list', request=request, format=format),
        'user-streaks':             reverse('userstreak-list', request=request, format=format),

        # Client Portal
        'client-profiles':      reverse('clientprofile-list', request=request, format=format),
        'client-projects':      reverse('clientproject-list', request=request, format=format),
        'client-milestones':    reverse('clientprojectmilestone-list', request=request, format=format),
        'client-deliverables':  reverse('clientprojectdeliverable-list', request=request, format=format),
        'client-updates':       reverse('clientprojectupdate-list', request=request, format=format),
        'client-invoices':      reverse('clientinvoice-list', request=request, format=format),
    })


# ---------------------------------------------------------------------------
#  SHARED PERMISSION CLASS — admin only
# ---------------------------------------------------------------------------

class IsAdminUser(permissions.BasePermission):
    """Only Django staff / superusers can access the API."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


# ---------------------------------------------------------------------------
#  AUTH / USER
# ---------------------------------------------------------------------------

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List all Django users (interns + admins).
    GET /api/v1/users/
    GET /api/v1/users/<id>/
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'username']


# ---------------------------------------------------------------------------
#  ENROLLMENTS
# ---------------------------------------------------------------------------

class EnrollmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    All internship enrollment records with payment & approval status.
    GET /api/v1/enrollments/
    GET /api/v1/enrollments/<id>/

    Filter examples:
      ?is_paid=true
      ?is_approved=true
      ?domain=Data+Science
    """
    queryset = Enrollment.objects.all().order_by('-created_at')
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email', 'domain', 'duration', 'college']
    ordering_fields = ['created_at', 'name', 'domain', 'duration', 'amount']


# ---------------------------------------------------------------------------
#  STUDENT PROFILES
# ---------------------------------------------------------------------------

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Intern portal profiles (one per approved student).
    GET /api/v1/students/
    GET /api/v1/students/<id>/
    """
    queryset = Profile.objects.select_related('user').all().order_by('student_id')
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['student_id', 'user__username', 'user__email', 'Intren', 'period']
    ordering_fields = ['student_id', 'Intren', 'period']


# ---------------------------------------------------------------------------
#  TASKS & CURRICULUM
# ---------------------------------------------------------------------------

class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    """Internship task bank."""
    queryset = Task.objects.all().order_by('category', 'required_period')
    serializer_class = TaskSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'category']
    ordering_fields = ['category', 'required_period']


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    """MCQ questions attached to tasks."""
    queryset = Question.objects.select_related('task').all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['task__title', 'question_text']


class LearningMaterialViewSet(viewsets.ReadOnlyModelViewSet):
    """Learning materials (videos, files, notes) grouped by task and week."""
    queryset = LearningMaterial.objects.select_related('task').all()
    serializer_class = LearningMaterialSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'task__title']
    ordering_fields = ['week_number', 'order']


# ---------------------------------------------------------------------------
#  PROJECTS
# ---------------------------------------------------------------------------

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """Project bank assigned to interns."""
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'category']
    ordering_fields = ['created_at', 'category', 'required_period']


class ProjectSubmissionViewSet(viewsets.ReadOnlyModelViewSet):
    """Intern project submissions with approval status."""
    queryset = ProjectSubmission.objects.select_related('user', 'project').all()
    serializer_class = ProjectSubmissionSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'user__email', 'project__title']
    ordering_fields = ['submitted_at', 'is_approved']


# ---------------------------------------------------------------------------
#  CONTACTS
# ---------------------------------------------------------------------------

class ContactViewSet(viewsets.ReadOnlyModelViewSet):
    """Public contact form submissions."""
    queryset = Contact.objects.all().order_by('-created_at')
    serializer_class = ContactSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email', 'subject']
    ordering_fields = ['created_at']


class ClientRequestViewSet(viewsets.ReadOnlyModelViewSet):
    """Business client service enquiries."""
    queryset = ClientRequest.objects.all().order_by('-created_at')
    serializer_class = ClientRequestSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'company_name', 'email', 'service_type']
    ordering_fields = ['created_at', 'service_type']


# ---------------------------------------------------------------------------
#  CMS
# ---------------------------------------------------------------------------

class AnnouncementViewSet(viewsets.ReadOnlyModelViewSet):
    """Dashboard announcements."""
    queryset = Announcement.objects.all().order_by('-created_at')
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAdminUser]


class InternshipPricingViewSet(viewsets.ReadOnlyModelViewSet):
    """Internship pricing plans."""
    queryset = InternshipPricing.objects.all()
    serializer_class = InternshipPricingSerializer
    permission_classes = [IsAdminUser]


class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    """Public reviews & testimonials."""
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'role', 'message']
    ordering_fields = ['created_at', 'rating']


# ---------------------------------------------------------------------------
#  DAILY CHALLENGES
# ---------------------------------------------------------------------------

class ChallengeTrackViewSet(viewsets.ReadOnlyModelViewSet):
    """Challenge track definitions."""
    queryset = ChallengeTrack.objects.select_related('created_by').all()
    serializer_class = ChallengeTrackSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class UserChallengeEnrollmentViewSet(viewsets.ReadOnlyModelViewSet):
    """Which users enrolled in which challenge tracks."""
    queryset = UserChallengeEnrollment.objects.select_related('user', 'track').all()
    serializer_class = UserChallengeEnrollmentSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'track__name']
    ordering_fields = ['enrolled_at', 'target_days']


class DailyTrackCheckInViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Daily check-in records — one per user per track per day.
    Great for Power BI calendar heatmaps.
    """
    queryset = DailyTrackCheckIn.objects.select_related('user', 'track').all()
    serializer_class = DailyTrackCheckInSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'track__name', 'notes']
    ordering_fields = ['date', 'done_at']


class MilestoneAchievementViewSet(viewsets.ReadOnlyModelViewSet):
    """Awarded milestones (30/50/100/200/300/500 day badges)."""
    queryset = MilestoneAchievement.objects.select_related('user', 'track').all()
    serializer_class = MilestoneAchievementSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'track__name']
    ordering_fields = ['achieved_at', 'milestone_days']


class UserStreakViewSet(viewsets.ReadOnlyModelViewSet):
    """Current and longest streak per user."""
    queryset = UserStreak.objects.select_related('user').all()
    serializer_class = UserStreakSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username']
    ordering_fields = ['current_streak', 'longest_streak']


# ---------------------------------------------------------------------------
#  CLIENT PORTAL
# ---------------------------------------------------------------------------

class ClientProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """Business client profiles."""
    queryset = ClientProfile.objects.select_related('user').all()
    serializer_class = ClientProfileSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['company_name', 'user__email', 'industry']
    ordering_fields = ['created_at', 'company_name']


class ClientProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """Client service projects with status and progress."""
    queryset = ClientProject.objects.select_related('client').all()
    serializer_class = ClientProjectSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'client__company_name', 'status', 'service_type']
    ordering_fields = ['created_at', 'status', 'progress', 'deadline']


class ClientProjectMilestoneViewSet(viewsets.ReadOnlyModelViewSet):
    """Milestones/phases within client projects."""
    queryset = ClientProjectMilestone.objects.select_related('project').all()
    serializer_class = ClientProjectMilestoneSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'project__title']
    ordering_fields = ['order', 'due_date']


class ClientProjectDeliverableViewSet(viewsets.ReadOnlyModelViewSet):
    """Files delivered to clients."""
    queryset = ClientProjectDeliverable.objects.select_related('project').all()
    serializer_class = ClientProjectDeliverableSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'project__title']
    ordering_fields = ['uploaded_at']


class ClientProjectUpdateViewSet(viewsets.ReadOnlyModelViewSet):
    """Activity / status update feed on client projects."""
    queryset = ClientProjectUpdate.objects.select_related('project', 'posted_by').all()
    serializer_class = ClientProjectUpdateSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['project__title', 'message']
    ordering_fields = ['created_at']


class ClientInvoiceViewSet(viewsets.ReadOnlyModelViewSet):
    """Client invoices with payment status."""
    queryset = ClientInvoice.objects.select_related('project', 'project__client').all()
    serializer_class = ClientInvoiceSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'invoice_number', 'status',
        'project__title', 'project__client__company_name',
    ]
    ordering_fields = ['issued_date', 'due_date', 'amount', 'status']
