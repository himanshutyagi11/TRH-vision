from django.db import models
from django.contrib.auth.models import User

# models.py
class Task(models.Model):
    DOMAIN_CHOICES = [
        ('Data Analytics', 'Data Analytics'),
        ('Power BI developer', 'Power BI developer'),
        ('Web Development', 'Web Development'),
        ('Machine Learning', 'Machine Learning'),
        ('Data Science', 'Data Science'),
        ('Artificial Intelligence', 'Artificial Intelligence'),
    ]

    PERIOD_CHOICES = [
        (1, '1 Month'),
        (2, '2 Months'),
        (3, '3 Months'),
        (6, '6 Months'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=DOMAIN_CHOICES)
    description = models.TextField(null=True, blank=True)
    task_link = models.URLField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    required_period = models.IntegerField(
        choices=PERIOD_CHOICES, default=1,
        help_text="Which intern period this task belongs to"
    )
    users_completed = models.ManyToManyField(User, related_name='completed_tasks', blank=True)

    def __str__(self):
        return f"[{self.category}] {self.title}"

class Project(models.Model):
    DOMAIN_CHOICES = [
        ('Data Analytics', 'Data Analytics'),
        ('Power BI developer', 'Power BI developer'),
        ('Web Development', 'Web Development'),
        ('Machine Learning', 'Machine Learning'),
        ('Data Science', 'Data Science'),
        ('Artificial Intelligence', 'Artificial Intelligence'),
    ]

    PERIOD_CHOICES = [
        (1, '1 Month'),
        (2, '2 Months'),
        (3, '3 Months'),
        (6, '6 Months'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    problem_statement = models.FileField(upload_to='projects/', help_text="Upload PDF/Doc of the problem statement")
    category = models.CharField(max_length=50, choices=DOMAIN_CHOICES)
    required_period = models.IntegerField(
        choices=PERIOD_CHOICES, default=1,
        help_text="Which intern period this project belongs to"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.category} - {self.required_period} Month+)"

class ProjectSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_submissions')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='project_submissions/', null=True, blank=True, help_text="Upload PDF/Doc of the project")
    drive_link = models.URLField(null=True, blank=True, help_text="Link to Google Drive or GitHub")
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False, help_text="Check to approve this project submission for certificate generation")

    class Meta:
        unique_together = ('user', 'project')
        verbose_name = 'Project Submission'
        verbose_name_plural = 'Project Submissions'

    def __str__(self):
        return f"{self.user.username} - {self.project.title}"


class Profile(models.Model):
    # Options for Internship Domains
    DOMAIN_CHOICES = [
        ('Data Analytics', 'Data Analytics'),
        ('Power BI developer', 'Power BI developer'),
        ('Web development', 'Web development'),
        ('Machine Learning', 'Machine Learning'),
        ('Data Science', 'Data Science'),
        ('Artificial Intelligence', 'Artificial Intelligence'),
    ]

    # Options for Duration
    PERIOD_CHOICES = [
        ('1 Month', '1 Month'),
        ('2 Months', '2 Months'),
        ('3 Months', '3 Months'),
        ('6 Months', '6 Months')
    ]

    def get_period_integer(self):
        # Extracts the first digit from '1 Month', '2 Months', etc.
        try:
            return int(self.period.split()[0])
        except (ValueError, IndexError):
            return 1

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True, blank=True)

    # Use choices here for dropdowns
    Intren = models.CharField(max_length=50, choices=DOMAIN_CHOICES)
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES)

    def save(self, *args, **kwargs):
        if not self.student_id:
            # Generates: TRH20-26-001, TRH20-26-002, etc.
            self.student_id = f"TRH20-26-{self.user.id:03d}"
        super().save(*args, **kwargs)

    certificate = models.FileField(upload_to='certificates/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.student_id}"


class Question(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    correct_option = models.CharField(max_length=1, choices=[('a', 'A'), ('b', 'B'), ('c', 'C')])

    def __str__(self):
        return f"Q for {self.task.title}"


from ckeditor_uploader.fields import RichTextUploadingField

class LearningMaterial(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    content = RichTextUploadingField(blank=True, null=True)
    video_url = models.URLField(null=True, blank=True)
    file = models.FileField(upload_to='materials/', null=True, blank=True)
    week_number = models.IntegerField(default=1, help_text="Week number (1, 2, 3...)")
    order = models.IntegerField(default=1, help_text="Order within the week")

    class Meta:
        ordering = ['week_number', 'order']

    def __str__(self):
        return f"{self.task.title} - Week {self.week_number} - {self.title}"

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class ClientRequest(models.Model):
    SERVICE_CHOICES = [
        ('Web Development', 'Web Development'),
        ('Data Analytics', 'Data Analytics'),
        ('Power BI ', 'Power BI'),
        ('Predictive AI', 'Predictive AI'),
        ('Cloud Data', 'Cloud Data'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service_type = models.CharField(max_length=100, choices=SERVICE_CHOICES, default='Other')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name or self.name} - {self.service_type}"

class Enrollment(models.Model):
    DOMAIN_CHOICES = [
        ('Data Analytics', 'Data Analytics'),
        ('Power BI developer', 'Power BI developer'),
        ('Web Development', 'Web Development'),
        ('Machine Learning', 'Machine Learning'),
        ('Data Science', 'Data Science'),
        ('Artificial Intelligence', 'Artificial Intelligence'),
    ]
    DURATION_CHOICES = [
        ('1 Month', '1 Month'),
        ('2 Months', '2 Months'),
        ('3 Months', '3 Months'),
        ('6 Months', '6 Months'),
    ]

    name = models.CharField(max_length=200)
    college = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    domain = models.CharField(max_length=100, choices=DOMAIN_CHOICES)
    duration = models.CharField(max_length=50, choices=DURATION_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount in INR")
    transaction_id = models.CharField(max_length=100, blank=True, null=True, help_text="UPI/Razorpay Transaction ID")
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True, help_text="Razorpay Order ID")
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True, help_text="Razorpay Payment ID")
    payment_screenshot = models.ImageField(upload_to='payment_screenshots/', blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    generated_password = models.CharField(max_length=128, blank=True, null=True)
    credentials_sent = models.BooleanField(default=False)
    offer_letter_sent = models.BooleanField(default=False, help_text="Set to True after offer letter has been emailed to the student")
    start_date = models.DateField(null=True, blank=True, help_text="Admin-set internship start date (used on offer letter & certificate)")
    created_at = models.DateTimeField(auto_now_add=True)

    # Certificate payment — paid by the student AFTER completing internship
    certificate_paid = models.BooleanField(default=False, help_text="True when the student has paid for the completion certificate")
    certificate_payment_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Amount paid by the student to receive their completion certificate"
    )
    certificate_payment_id = models.CharField(
        max_length=200, blank=True, null=True,
        help_text="Razorpay/UPI payment ID for the certificate payment"
    )
    certificate_payment_date = models.DateTimeField(null=True, blank=True, help_text="When the student completed the certificate payment")

    def __str__(self):
        return f"{self.name} - {self.domain} ({self.duration})"


# -------------------------------------------------------------------
# Announcement model: period-specific notices shown on the dashboard
# -------------------------------------------------------------------
class Announcement(models.Model):
    PERIOD_CHOICES = [
        (1, '1 Month Interns (and above)'),
        (2, '2 Months Interns (and above)'),
        (3, '3 Months Interns (and above)'),
        (6, '6 Months Interns only'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    min_period = models.IntegerField(
        choices=PERIOD_CHOICES, default=1,
        help_text="Show this notice to interns whose period is >= this value"
    )
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide without deleting")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'

    def __str__(self):
        period_label = dict(self.PERIOD_CHOICES).get(self.min_period, str(self.min_period))
        return f"[{period_label}] {self.title}"

# -------------------------------------------------------------------
# Internship Pricing model: controls prices shown on the enroll page
# -------------------------------------------------------------------
class InternshipPricing(models.Model):
    DURATION_CHOICES = [
        ('1 Month', '1 Month'),
        ('2 Months', '2 Months'),
        ('3 Months', '3 Months'),
        ('6 Months', '6 Months'),
    ]

    duration = models.CharField(max_length=50, choices=DURATION_CHOICES, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text="Amount in INR (e.g. 199.00)")
    is_active = models.BooleanField(default=True, help_text="Show this duration option on the enrollment page")

    class Meta:
        ordering = ['duration']
        verbose_name = 'Internship Pricing'
        verbose_name_plural = 'Internship Pricing'

    def __str__(self):
        return f"{self.duration} - Rs.{self.price}"


# =================================================================
#  DAILY CHALLENGER SYSTEM  -  Multi-track, LeetCode-style
#  Up to 4 simultaneous challenge tracks per user
# =================================================================

class ChallengeTrack(models.Model):
    """
    A challenge category (e.g. Python, Gym, Freelancing, Self Project).
    System tracks are created by admin; users can also create custom ones.
    """
    name        = models.CharField(max_length=100)
    emoji       = models.CharField(max_length=10, default='⚡')
    description = models.CharField(max_length=255, blank=True)
    is_system   = models.BooleanField(
        default=False,
        help_text="System tracks are shown to all users as optional presets."
    )
    created_by  = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='custom_tracks'
    )

    class Meta:
        ordering = ['-is_system', 'name']
        verbose_name = 'Challenge Track'
        verbose_name_plural = 'Challenge Tracks'

    def __str__(self):
        tag = '[System]' if self.is_system else f'[{self.created_by}]'
        return f"{self.emoji} {self.name} {tag}"


class UserChallengeEnrollment(models.Model):
    """
    Links a user to a ChallengeTrack with a target milestone duration.
    Maximum 4 active enrollments per user.
    """
    TARGET_CHOICES = [
        (30,  '30 Days  - Starter'),
        (50,  '50 Days  - Committed'),
        (100, '100 Days - Dedicated'),
        (200, '200 Days - Elite'),
        (300, '300 Days - Master'),
        (500, '500 Days - Legend  Rs.500 Gift Card'),
    ]

    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenge_enrollments')
    track       = models.ForeignKey(ChallengeTrack, on_delete=models.CASCADE, related_name='enrollments')
    target_days = models.IntegerField(choices=TARGET_CHOICES, default=30)
    enrolled_at = models.DateField(auto_now_add=True)
    is_active   = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'track')
        verbose_name = 'User Challenge Enrollment'
        verbose_name_plural = 'User Challenge Enrollments'

    def __str__(self):
        return f"{self.user.username} -> {self.track.name} ({self.target_days}d)"


class DailyTrackCheckIn(models.Model):
    """One check-in per user per track per day."""
    user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='track_checkins')
    track   = models.ForeignKey(ChallengeTrack, on_delete=models.CASCADE, related_name='checkins')
    date    = models.DateField()
    notes   = models.CharField(max_length=300, blank=True, help_text="Optional: what did you do?")
    done_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'track', 'date')
        ordering = ['-date']
        verbose_name = 'Daily Track Check-In'
        verbose_name_plural = 'Daily Track Check-Ins'

    def __str__(self):
        return f"{self.user.username} - {self.track.name} on {self.date}"


class MilestoneAchievement(models.Model):
    """Awarded when a user hits a streak milestone on a track."""
    MILESTONE_CHOICES = [
        (30,  '30 Days'),
        (50,  '50 Days'),
        (100, '100 Days'),
        (200, '200 Days'),
        (300, '300 Days'),
        (500, '500 Days - Legend'),
    ]
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='milestones')
    track         = models.ForeignKey(ChallengeTrack, on_delete=models.CASCADE, related_name='milestones')
    milestone_days = models.IntegerField(choices=MILESTONE_CHOICES)
    achieved_at   = models.DateTimeField(auto_now_add=True)
    reward_sent   = models.BooleanField(default=False, help_text="Mark true when Rs.500 gift card is sent (500-day only)")

    class Meta:
        unique_together = ('user', 'track', 'milestone_days')
        verbose_name = 'Milestone Achievement'
        verbose_name_plural = 'Milestone Achievements'

    def __str__(self):
        return f"{self.user.username} - {self.track.name} - {self.milestone_days} Days"


class UserStreak(models.Model):
    """Overall daily streak: consecutive days with >=1 track checked in."""
    user                 = models.OneToOneField(User, on_delete=models.CASCADE, related_name='streak')
    current_streak       = models.IntegerField(default=0)
    longest_streak       = models.IntegerField(default=0)
    last_completion_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - Streak: {self.current_streak}"


# Keep old models (no longer used) for backwards-compat with migrations
class DailyChallengeTask(models.Model):
    DOMAIN_CHOICES = Task.DOMAIN_CHOICES
    date       = models.DateField()
    category   = models.CharField(max_length=50)
    title      = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=10, default='Easy')
    description = models.TextField()
    hint       = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Legacy Daily Challenge'

    def __str__(self):
        return f"[{self.date}] {self.title}"


class DailyCheckIn(models.Model):
    user           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_checkins')
    challenge      = models.ForeignKey(DailyChallengeTask, on_delete=models.CASCADE, null=True, blank=True)
    submitted_answer = models.TextField(blank=True, null=True)
    completed_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Legacy Daily Check-In'

    def __str__(self):
        return f"{self.user.username}"


# =================================================================
#  CLIENT DASHBOARD SYSTEM
#  Separate portal for business clients to track project progress
# =================================================================

class ClientProfile(models.Model):
    """Links a Django User to a client account (created by admin)."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    company_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    logo = models.ImageField(upload_to='client_logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} ({self.user.email})"


class ClientProject(models.Model):
    """A service project assigned to a client."""
    STATUS_CHOICES = [
        ('discovery', 'Discovery'),
        ('in_progress', 'In Progress'),
        ('review', 'Under Review'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ]
    SERVICE_CHOICES = [
        ('Web Development', 'Web Development'),
        ('Data Analytics', 'Data Analytics'),
        ('Power BI', 'Power BI'),
        ('Predictive AI', 'Predictive AI'),
        ('Cloud Data', 'Cloud Data'),
        ('Other', 'Other'),
    ]

    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    service_type = models.CharField(max_length=100, choices=SERVICE_CHOICES, default='Other')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='discovery')
    progress = models.IntegerField(default=0, help_text="Overall progress 0-100%")
    start_date = models.DateField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                 help_text="Total project budget in INR")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Client Project'
        verbose_name_plural = 'Client Projects'

    def __str__(self):
        return f"{self.title} - {self.client.company_name}"

    @property
    def completed_milestones(self):
        return self.milestones.filter(is_completed=True).count()

    @property
    def total_milestones(self):
        return self.milestones.count()


class ClientProjectMilestone(models.Model):
    """A milestone/phase within a client project."""
    project = models.ForeignKey(ClientProject, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Project Milestone'
        verbose_name_plural = 'Project Milestones'

    def __str__(self):
        status = 'Done' if self.is_completed else 'Pending'
        return f"{status} {self.title} - {self.project.title}"


class ClientProjectDeliverable(models.Model):
    """Files/documents delivered to the client."""
    project = models.ForeignKey(ClientProject, on_delete=models.CASCADE, related_name='deliverables')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='client_deliverables/')
    description = models.CharField(max_length=500, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Project Deliverable'
        verbose_name_plural = 'Project Deliverables'

    def __str__(self):
        return f"{self.title} - {self.project.title}"


class ClientProjectUpdate(models.Model):
    """Activity feed / status updates on a client project."""
    project = models.ForeignKey(ClientProject, on_delete=models.CASCADE, related_name='updates')
    message = models.TextField()
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Project Update'
        verbose_name_plural = 'Project Updates'

    def __str__(self):
        return f"Update on {self.project.title} - {self.created_at:%b %d}"


class ClientInvoice(models.Model):
    """Invoices/billing records for client projects."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    project = models.ForeignKey(ClientProject, on_delete=models.CASCADE, related_name='invoices')
    invoice_number = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    description = models.CharField(max_length=500, blank=True)
    issued_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    paid_date = models.DateField(null=True, blank=True)
    transaction_id = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-issued_date']
        verbose_name = 'Client Invoice'
        verbose_name_plural = 'Client Invoices'

    def __str__(self):
        return f"INV-{self.invoice_number} - Rs.{self.amount} ({self.status})"


# =================================================================
#  PUBLIC REVIEW / RATING MODEL
#  Anyone can submit; admin must approve before it shows on the
#  index page.
# =================================================================

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    name    = models.CharField(max_length=100, help_text="Reviewer full name")
    role    = models.CharField(max_length=150, blank=True,
                               help_text="Title / Company (e.g. Intern - Data Science)")
    message = models.TextField(help_text="Review / testimonial text")
    rating  = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    is_approved = models.BooleanField(
        default=False,
        help_text="Tick to show this review on the public homepage"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        status = 'approved' if self.is_approved else 'pending'
        return f"{self.name} - {self.rating}star ({status})"

    @property
    def initials(self):
        parts = self.name.strip().split()
        return ''.join(p[0].upper() for p in parts[:2])


# =================================================================
#  EMAIL TEMPLATE MODEL
#  Allows admin to configure email subject/body for:
#    - Offer Letter emails   (name='offer_letter')
#    - Credentials emails    (name='login_credentials')
#  Only editable via admin panel; records cannot be deleted.
# =================================================================

OFFER_LETTER_PLACEHOLDERS = """
Available placeholders for the offer letter email:
  {name}       - Student full name
  {domain}     - Internship domain (e.g. Data Science)
  {duration}   - Internship duration (e.g. 3 Months)
  {start_date} - Internship start date (e.g. July 01, 2026)
  {email}      - Student email address
"""

CREDENTIALS_PLACEHOLDERS = """
Available placeholders for the credentials email:
  {name}       - Student full name
  {domain}     - Internship domain (e.g. Data Science)
  {duration}   - Internship duration (e.g. 3 Months)
  {email}      - Student email address
  {student_id} - Student portal ID (e.g. TRH20-26-001)
  {password}   - Student login password
  {portal_url} - Portal login URL
"""


class EmailTemplate(models.Model):
    """
    Stores editable email templates for admin-triggered emails.
    Two records are pre-seeded via migration:
      - name='offer_letter'      - sent with the PDF offer letter
      - name='login_credentials' - sent with portal login details
    """
    TEMPLATE_CHOICES = [
        ('offer_letter', 'Offer Letter Email'),
        ('login_credentials', 'Login Credentials Email'),
    ]

    name = models.CharField(
        max_length=50,
        unique=True,
        choices=TEMPLATE_CHOICES,
        help_text="Internal identifier. Do not change.",
    )
    label = models.CharField(
        max_length=200,
        help_text="Friendly name shown in admin.",
    )
    subject = models.CharField(
        max_length=500,
        help_text="Email subject line. Use {name}, {domain}, {duration} as placeholders.",
    )
    body = models.TextField(
        help_text="Email body text. See the placeholder reference for available variables.",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Email Template'
        verbose_name_plural = 'Email Templates'

    def __str__(self):
        return self.label

    def get_rendered(self, context):
        """
        Returns (subject, body) with all {placeholder} variables replaced.
        Unrecognised keys are left as-is so a typo does not crash the send.
        """
        class SafeDict(dict):
            def __missing__(self, key):
                return '{' + key + '}'

        safe_ctx = SafeDict(context)
        rendered_subject = self.subject.format_map(safe_ctx)
        rendered_body = self.body.format_map(safe_ctx)
        return rendered_subject, rendered_body
