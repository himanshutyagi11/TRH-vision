"""
vision/serializers.py
Django REST Framework serializers for all TRH models.
Used by api_views.py to expose data as JSON REST endpoints.
"""

from rest_framework import serializers
from django.contrib.auth.models import User

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


# ---------------------------------------------------------------------------
#  AUTH / USER
# ---------------------------------------------------------------------------

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'is_active', 'date_joined', 'last_login']


# ---------------------------------------------------------------------------
#  INTERNSHIP — ENROLLMENTS
# ---------------------------------------------------------------------------

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = [
            'id', 'name', 'college', 'email', 'phone',
            'domain', 'duration', 'amount',
            'transaction_id', 'razorpay_order_id', 'razorpay_payment_id',
            'is_paid', 'is_approved', 'approved_at',
            'credentials_sent', 'offer_letter_sent',
            'start_date', 'created_at',
        ]


# ---------------------------------------------------------------------------
#  INTERN PROFILES
# ---------------------------------------------------------------------------

class ProfileSerializer(serializers.ModelSerializer):
    username    = serializers.CharField(source='user.username', read_only=True)
    email       = serializers.EmailField(source='user.email', read_only=True)
    first_name  = serializers.CharField(source='user.first_name', read_only=True)
    last_name   = serializers.CharField(source='user.last_name', read_only=True)
    date_joined = serializers.DateTimeField(source='user.date_joined', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id', 'student_id', 'username', 'email',
            'first_name', 'last_name', 'date_joined',
            'Intren', 'period', 'certificate',
        ]


# ---------------------------------------------------------------------------
#  TASKS
# ---------------------------------------------------------------------------

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'category', 'description',
            'task_link', 'due_date', 'required_period',
        ]


# ---------------------------------------------------------------------------
#  QUESTIONS (nested under tasks)
# ---------------------------------------------------------------------------

class QuestionSerializer(serializers.ModelSerializer):
    task_title = serializers.CharField(source='task.title', read_only=True)

    class Meta:
        model = Question
        fields = [
            'id', 'task', 'task_title',
            'question_text', 'option_a', 'option_b', 'option_c', 'correct_option',
        ]


# ---------------------------------------------------------------------------
#  LEARNING MATERIALS
# ---------------------------------------------------------------------------

class LearningMaterialSerializer(serializers.ModelSerializer):
    task_title = serializers.CharField(source='task.title', read_only=True)

    class Meta:
        model = LearningMaterial
        fields = [
            'id', 'task', 'task_title', 'title', 'content',
            'video_url', 'file', 'week_number', 'order',
        ]


# ---------------------------------------------------------------------------
#  PROJECTS (intern project bank)
# ---------------------------------------------------------------------------

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'problem_statement',
            'category', 'required_period', 'created_at',
        ]


# ---------------------------------------------------------------------------
#  PROJECT SUBMISSIONS
# ---------------------------------------------------------------------------

class ProjectSubmissionSerializer(serializers.ModelSerializer):
    username      = serializers.CharField(source='user.username', read_only=True)
    student_email = serializers.EmailField(source='user.email', read_only=True)
    project_title = serializers.CharField(source='project.title', read_only=True)

    class Meta:
        model = ProjectSubmission
        fields = [
            'id', 'user', 'username', 'student_email',
            'project', 'project_title',
            'file', 'drive_link', 'submitted_at', 'is_approved',
        ]


# ---------------------------------------------------------------------------
#  CONTACT FORM SUBMISSIONS
# ---------------------------------------------------------------------------

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            'id', 'name', 'email', 'phone', 'role',
            'subject', 'message', 'created_at',
        ]


# ---------------------------------------------------------------------------
#  CLIENT SERVICE REQUESTS
# ---------------------------------------------------------------------------

class ClientRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientRequest
        fields = [
            'id', 'name', 'company_name', 'email', 'phone',
            'service_type', 'message', 'created_at',
        ]


# ---------------------------------------------------------------------------
#  ANNOUNCEMENTS
# ---------------------------------------------------------------------------

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'content', 'min_period',
            'is_active', 'created_at',
        ]


# ---------------------------------------------------------------------------
#  INTERNSHIP PRICING
# ---------------------------------------------------------------------------

class InternshipPricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternshipPricing
        fields = ['id', 'duration', 'price', 'is_active']


# ---------------------------------------------------------------------------
#  REVIEWS / TESTIMONIALS
# ---------------------------------------------------------------------------

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id', 'name', 'role', 'message',
            'rating', 'is_approved', 'created_at',
        ]


# ---------------------------------------------------------------------------
#  DAILY CHALLENGE — TRACKS
# ---------------------------------------------------------------------------

class ChallengeTrackSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(
        source='created_by.username', read_only=True, default=None
    )

    class Meta:
        model = ChallengeTrack
        fields = [
            'id', 'name', 'emoji', 'description',
            'is_system', 'created_by', 'created_by_username',
        ]


# ---------------------------------------------------------------------------
#  CHALLENGE ENROLLMENTS
# ---------------------------------------------------------------------------

class UserChallengeEnrollmentSerializer(serializers.ModelSerializer):
    username    = serializers.CharField(source='user.username', read_only=True)
    track_name  = serializers.CharField(source='track.name', read_only=True)

    class Meta:
        model = UserChallengeEnrollment
        fields = [
            'id', 'user', 'username', 'track', 'track_name',
            'target_days', 'enrolled_at', 'is_active',
        ]


# ---------------------------------------------------------------------------
#  DAILY CHECK-INS
# ---------------------------------------------------------------------------

class DailyTrackCheckInSerializer(serializers.ModelSerializer):
    username   = serializers.CharField(source='user.username', read_only=True)
    track_name = serializers.CharField(source='track.name', read_only=True)

    class Meta:
        model = DailyTrackCheckIn
        fields = [
            'id', 'user', 'username', 'track', 'track_name',
            'date', 'notes', 'done_at',
        ]


# ---------------------------------------------------------------------------
#  MILESTONE ACHIEVEMENTS
# ---------------------------------------------------------------------------

class MilestoneAchievementSerializer(serializers.ModelSerializer):
    username   = serializers.CharField(source='user.username', read_only=True)
    track_name = serializers.CharField(source='track.name', read_only=True)

    class Meta:
        model = MilestoneAchievement
        fields = [
            'id', 'user', 'username', 'track', 'track_name',
            'milestone_days', 'achieved_at', 'reward_sent',
        ]


# ---------------------------------------------------------------------------
#  USER STREAKS
# ---------------------------------------------------------------------------

class UserStreakSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserStreak
        fields = [
            'id', 'user', 'username',
            'current_streak', 'longest_streak', 'last_completion_date',
        ]


# ---------------------------------------------------------------------------
#  CLIENT PORTAL — CLIENT PROFILES
# ---------------------------------------------------------------------------

class ClientProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email    = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = ClientProfile
        fields = [
            'id', 'user', 'username', 'email',
            'company_name', 'phone', 'industry', 'logo', 'created_at',
        ]


# ---------------------------------------------------------------------------
#  CLIENT PROJECTS
# ---------------------------------------------------------------------------

class ClientProjectMilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProjectMilestone
        fields = [
            'id', 'project', 'title', 'description',
            'is_completed', 'due_date', 'completed_at', 'order',
        ]


class ClientProjectDeliverableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProjectDeliverable
        fields = [
            'id', 'project', 'title', 'file',
            'description', 'uploaded_at',
        ]


class ClientProjectUpdateSerializer(serializers.ModelSerializer):
    posted_by_username = serializers.CharField(
        source='posted_by.username', read_only=True, default=None
    )

    class Meta:
        model = ClientProjectUpdate
        fields = [
            'id', 'project', 'message',
            'posted_by', 'posted_by_username', 'created_at',
        ]


class ClientProjectSerializer(serializers.ModelSerializer):
    client_company     = serializers.CharField(source='client.company_name', read_only=True)
    completed_milestones = serializers.IntegerField(read_only=True)
    total_milestones     = serializers.IntegerField(read_only=True)

    class Meta:
        model = ClientProject
        fields = [
            'id', 'client', 'client_company',
            'title', 'description', 'service_type', 'status', 'progress',
            'start_date', 'deadline', 'budget', 'created_at',
            'completed_milestones', 'total_milestones',
        ]


# ---------------------------------------------------------------------------
#  CLIENT INVOICES
# ---------------------------------------------------------------------------

class ClientInvoiceSerializer(serializers.ModelSerializer):
    project_title  = serializers.CharField(source='project.title', read_only=True)
    client_company = serializers.CharField(
        source='project.client.company_name', read_only=True
    )

    class Meta:
        model = ClientInvoice
        fields = [
            'id', 'project', 'project_title', 'client_company',
            'invoice_number', 'amount', 'status', 'description',
            'issued_date', 'due_date', 'paid_date', 'transaction_id',
        ]
