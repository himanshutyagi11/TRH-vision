from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Task, Profile # Import Profile from models
import base64

def index(request):
    from .models import Review
    reviews = Review.objects.filter(is_approved=True).order_by('-created_at')
    return render(request, "vision/index.html", {'reviews': reviews})


def submit_review(request):
    """Public endpoint: anyone can submit a review; it awaits admin approval."""
    from .models import Review
    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        role    = request.POST.get('role', '').strip()
        message = request.POST.get('message', '').strip()
        rating  = request.POST.get('rating', '5').strip()

        errors = []
        if not name:
            errors.append('Name is required.')
        if not message:
            errors.append('Review message is required.')
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValueError
        except ValueError:
            errors.append('Rating must be between 1 and 5.')
            rating = 5

        if not errors:
            Review.objects.create(
                name=name,
                role=role,
                message=message,
                rating=rating,
                is_approved=False,
            )
            messages.success(
                request,
                "Thank you for your review! It will appear on the homepage after approval."
            )
        else:
            for e in errors:
                messages.error(request, e)

    return redirect('index')


def about(request):
    return render(request,"vision/about.html")

def terms(request):
    return render(request, "vision/terms.html")

def privacy(request):
    return render(request, "vision/privacy.html")

def refund_policy(request):
    return render(request, "vision/refund.html")

from django.core.mail import send_mail
from .models import Contact, ClientRequest

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        try:
            # Logic: If Role is 'Business', save to ClientRequest (2nd Database)
            if role == 'Business':
                ClientRequest.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    # We can use subject as 'company_name' or 'service_type' if needed, 
                    # but for now we'll just map subject -> company_name implies it's a business enquiry
                    company_name=subject, 
                    message=message,
                    service_type='Other' # Default or parse from message
                )
                db_name = "Client Database"
            else:
                # Else save to Contact (General)
                Contact.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    role=role,
                    subject=subject,
                    message=message
                )
                db_name = "Contact Database"
            
            # 2. Save to CSV File (Append mode) - KEEPING AS BACKUP
            import csv
            import os
            from django.conf import settings
            
            csv_file_path = os.path.join(settings.BASE_DIR, 'contacts.csv')
            file_exists = os.path.isfile(csv_file_path)
            
            with open(csv_file_path, 'a', newline='') as csvfile:
                fieldnames = ['Name', 'Email', 'Phone', 'Role', 'Subject', 'Message', 'Timestamp']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow({
                    'Name': name,
                    'Email': email,
                    'Phone': phone,
                    'Role': role,
                    'Subject': subject,
                    'Message': message,
                    'Timestamp': timezone.now().strftime("%Y-%m-%d %H:%M:%S")
                })

            # 3. Send Email Notification (to Admin)
            email_subject = f"New {role} Inquiry: {subject}"
            email_body = f"""
            New inquiry received from TRHvision Website.
            Saved to: {db_name}
            
            Name: {name}
            Email: {email}
            Phone: {phone}
            Role: {role}
            Subject: {subject}
            
            Message:
            {message}
            """
            send_mail(
                email_subject,
                email_body,
                'noreply@trhvision.in', # From Email (Dummy for console)
                ['support@trhvision.com'], # To Email (Admin)
                fail_silently=False,
            )
            
            messages.success(request, "Message sent successfully! We'll be in touch.")
            return redirect('contact')
            
        except Exception as e:
            messages.error(request, f"Error sending message: {e}")
            
    return render(request, 'vision/contact.html')

from .models import Enrollment, InternshipPricing
import razorpay
import json
import hmac
import hashlib
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def enroll(request):
    """Renders the enrollment form (GET), and handles free enrollment submissions (POST)."""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        college = request.POST.get('college', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        domain = request.POST.get('domain', '').strip()
        duration = request.POST.get('duration', '').strip()

        if not (name and college and email and phone and domain and duration):
            messages.error(request, "Please fill in all fields.")
            return redirect('enroll')

        try:
            pricing = InternshipPricing.objects.get(duration=duration, is_active=True)
            price = int(pricing.price)
        except InternshipPricing.DoesNotExist:
            price = -1

        if price != 0:
            messages.error(request, "Invalid payment or pricing configuration.")
            return redirect('enroll')

        try:
            # Save enrollment for free internship
            enrollment = Enrollment.objects.create(
                name=name,
                college=college,
                email=email,
                phone=phone,
                domain=domain,
                duration=duration,
                amount=0,
                transaction_id='FREE_ENROLL',
                razorpay_order_id='FREE_ENROLL',
                razorpay_payment_id='FREE_ENROLL',
                is_paid=True,
            )

            # Save in session for success page download link
            request.session['enrolled_id'] = enrollment.id

            # Offer letter will be sent by the background processor after admin approval and 4 hours have passed

            # --- Notify admin ---
            try:
                send_mail(
                    f"✅ New Free Enrollment: {name} — {domain}",
                    f"""
New Free Enrollment!

Name:       {name}
College:    {college}
Email:      {email}
Phone:      {phone}
Domain:     {domain}
Duration:   {duration}
Amount:     ₹0
""",
                    'noreply@trhvision.in',
                    ['support@trhvision.in'],
                    fail_silently=True,
                )
            except Exception:
                pass

            return redirect('enroll_success')
        except Exception as e:
            messages.error(request, f"Enrollment error: {e}")
            return redirect('enroll')

    # GET request behavior
    active_pricings = InternshipPricing.objects.filter(is_active=True).order_by('duration')
    pricing_map = {p.duration: int(p.price) for p in active_pricings}
    context = {
        'active_pricings': active_pricings,
        'pricing_map_json': json.dumps(pricing_map)
    }
    return render(request, 'vision/enroll.html', context)


@csrf_exempt
def create_razorpay_order(request):
    """AJAX endpoint: creates a Razorpay order and returns the details as JSON."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        duration = data.get('duration', '')
        
        try:
            pricing = InternshipPricing.objects.get(duration=duration, is_active=True)
            amount_inr = int(pricing.price)
        except InternshipPricing.DoesNotExist:
            amount_inr = 0
            
        if amount_inr == 0:
            return JsonResponse({'error': 'Invalid duration selected or price not set'}, status=400)

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )
        order = client.order.create({
            'amount': amount_inr * 100,  # Razorpay expects paise
            'currency': 'INR',
            'payment_capture': 1,
        })
        return JsonResponse({
            'order_id': order['id'],
            'amount':   order['amount'],
            'currency': order['currency'],
            'key':      settings.RAZORPAY_KEY_ID,
        })
    except Exception as e:
        error_msg = str(e)
        if "Authentication failed" in error_msg:
            error_msg = "Razorpay Authentication Failed: Your RAZORPAY_KEY_ID or RAZORPAY_KEY_SECRET in .env is invalid or expired. Please update them with active keys from dashboard.razorpay.com."
        return JsonResponse({'error': error_msg}, status=500)


@csrf_exempt
def payment_success(request):
    """Called by the frontend after payment. Verifies signature, saves enrollment."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        razorpay_order_id   = request.POST.get('razorpay_order_id', '')
        razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_signature  = request.POST.get('razorpay_signature', '')

        # --- Verify signature ---
        key_secret = settings.RAZORPAY_KEY_SECRET.encode()
        message = f"{razorpay_order_id}|{razorpay_payment_id}".encode()
        generated_sig = hmac.new(key_secret, message, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(generated_sig, razorpay_signature):
            messages.error(request, "Payment verification failed. Please contact support.")
            return redirect('enroll')

        # --- Collect form data ---
        name     = request.POST.get('name', '')
        college  = request.POST.get('college', '')
        email    = request.POST.get('email', '')
        phone    = request.POST.get('phone', '')
        domain   = request.POST.get('domain', '')
        duration = request.POST.get('duration', '')
        
        try:
            pricing = InternshipPricing.objects.get(duration=duration)
            amount   = pricing.price
        except InternshipPricing.DoesNotExist:
            amount   = 0

        # --- Save or update enrollment ---
        enrollment = Enrollment.objects.filter(email=email).first()
        if enrollment:
            enrollment.is_paid = True
            enrollment.transaction_id = razorpay_payment_id
            enrollment.razorpay_order_id = razorpay_order_id
            enrollment.razorpay_payment_id = razorpay_payment_id
            if amount > 0:
                enrollment.amount = amount
            if name:
                enrollment.name = name
            enrollment.save()
        else:
            enrollment = Enrollment.objects.create(
                name=name,
                college=college,
                email=email,
                phone=phone,
                domain=domain,
                duration=duration,
                amount=amount,
                transaction_id=razorpay_payment_id,
                razorpay_order_id=razorpay_order_id,
                razorpay_payment_id=razorpay_payment_id,
                is_paid=True,
            )

        # Save in session for success page download link
        request.session['enrolled_id'] = enrollment.id

        # --- Notify admin ---
        try:
            send_mail(
                f"✅ New Enrollment (Razorpay): {name} — {domain}",
                f"""
New Paid Enrollment via Razorpay!

Name:       {name}
College:    {college}
Email:      {email}
Phone:      {phone}
Domain:     {domain}
Duration:   {duration}
Amount:     ₹{amount}
Order ID:   {razorpay_order_id}
Payment ID: {razorpay_payment_id}
""",
                'noreply@trhvision.in',
                ['support@trhvision.in'],
                fail_silently=True,
            )
        except Exception:
            pass  # Don't break enrollment flow if email fails

        if request.user.is_authenticated:
            messages.success(request, "Payment verified successfully! Your certificate is now unlocked for download.")
            return redirect('dashboard')

        return redirect('enroll_success')

    except Exception as e:
        messages.error(request, f"Enrollment error: {e}")
        if request.user.is_authenticated:
            return redirect('dashboard')
        return redirect('enroll')


def enroll_success(request):
    enrolled_id = request.session.get('enrolled_id')
    enrollment = None
    if enrolled_id:
        try:
            enrollment = Enrollment.objects.get(id=enrolled_id)
        except Enrollment.DoesNotExist:
            pass
    return render(request, 'vision/enroll_success.html', {'enrollment': enrollment})

def services(request):
    return render(request, 'vision/services.html')

def internship(request):
    # Kept for backward compatibility — redirects to the career page
    return redirect('career')

def career(request):
    return render(request, "vision/career.html")

# You mentioned you want to be the only one creating users. 
# You can keep this view but I recommend using the Django Admin instead.
@user_passes_test(lambda u: u.is_superuser)
def signup(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match!")
            return render(request, "vision/signup.html")

        # Check if user already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, "vision/signup.html")

        # 1. Create the user only ONCE
        myuser = User.objects.create_user(username=email, email=email, password=pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        
        # 2. Create the profile only ONCE
        # The sequential ID (TRH20-26-001) will be generated by the model's save method
        Profile.objects.create(
            user=myuser, 
            Intren="Python",  # Provide a default so the NOT NULL constraint passes
            period="6 Months" # Provide a default
        )

        messages.success(request, "Registration successful!")
        return redirect('sigin')

    return render(request, "vision/signin.html")

def sigin(request):
    if request.method == "POST":
        uname = request.POST.get('username') 
        passw = request.POST.get('password')
        user = authenticate(request, username=uname, password=passw)
        
        if user is not None:
            login(request, user)
            # Smart redirect based on user type
            if user.is_staff or user.is_superuser:
                return redirect('trh_admin_dashboard')
            if hasattr(user, 'client_profile'):
                return redirect('client_dashboard')
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password")
    return render(request, "vision/sigin.html")

# views.py
@login_required(login_url='sigin')
def dashboard(request):
    try:
        profile = request.user.profile
        student_id = profile.student_id
        internship_name = profile.Intren 
        period_text = profile.period # This is "1 Month", "2 Months", etc.
    except Profile.DoesNotExist:
        return redirect('index') # Or handle as needed

    # Mapping your PERIOD_CHOICES to integers for filtering
    duration_map = {
        '1 Month': 1,
        '2 Months': 2,
        '3 Months': 3,
        '6 Months': 6,
    }
    student_limit = duration_map.get(period_text, 1)

    # Filter tasks: 
    # 1. Matches the category (e.g. 'Python')
    # 2. required_period is LESS THAN OR EQUAL TO the student's internship period
    all_tasks = list(Task.objects.filter(
        category=internship_name,
        required_period__lte=student_limit
    ).order_by('id'))

    # Sequential unlock: each task is locked until the previous one is completed
    for i, task in enumerate(all_tasks):
        if i == 0:
            task.is_locked = False  # First task always accessible
        else:
            prev_task = all_tasks[i - 1]
            task.is_locked = request.user not in prev_task.users_completed.all()
    
    # Progress calculation
    total_tasks = len(all_tasks)
    completed_tasks_count = sum(1 for t in all_tasks if request.user in t.users_completed.all())
    
    progress_percent = 0
    if total_tasks > 0:
        progress_percent = int((completed_tasks_count / total_tasks) * 100)

    # Calculate days remaining
    from django.utils import timezone
    from datetime import timedelta
    
    date_joined = request.user.date_joined
    days_since_joined = (timezone.now() - date_joined).days
    
    # Calculate total days based on period_text
    period_days_map = {
        '1 Month': 30,
        '2 Months': 60,
        '3 Months': 90,
        '6 Months': 180,
    }
    total_days = period_days_map.get(period_text, 30) # Default to 30 if not found
    days_remaining = max(0, total_days - days_since_joined)
    
    # Calculate current week
    current_week = (days_since_joined // 7) + 1

    # Filter Projects
    from .models import Project, Announcement, ProjectSubmission
    projects = list(Project.objects.filter(
        category=internship_name,
        required_period__lte=student_limit
    ))

    all_projects_submitted = True
    all_projects_cleared = True
    
    if len(projects) == 0:
        all_projects_submitted = True
        all_projects_cleared = True
    else:
        for p in projects:
            sub = ProjectSubmission.objects.filter(user=request.user, project=p).first()
            p.submission = sub
            if not sub:
                all_projects_submitted = False
                all_projects_cleared = False
            else:
                diff = timezone.now() - sub.submitted_at
                if not sub.is_approved and diff.days < 3:
                    all_projects_cleared = False

    # Filter Announcements: visible to interns whose period >= min_period
    announcements = Announcement.objects.filter(
        is_active=True,
        min_period__lte=student_limit
    )

    # Certificate eligibility: all tasks must be completed
    all_tasks_complete = (total_tasks > 0 and completed_tasks_count == total_tasks)
    
    certificate_unlocked = False
    validation_pending = False
    days_left_for_cert = 0

    if all_tasks_complete and all_projects_submitted and len(projects) > 0:
        latest_sub_date = max(p.submission.submitted_at for p in projects)
        diff = timezone.now() - latest_sub_date
        
        if all_projects_cleared:
            certificate_unlocked = True
        else:
            validation_pending = True
            days_left_for_cert = max(0, 3 - diff.days)
    elif all_tasks_complete and len(projects) == 0:
        certificate_unlocked = True
        
    has_certificate = bool(profile.certificate)

    # ══════════════════════════════════════════════════════════
    # DAILY CHALLENGER — multi-track system
    # ══════════════════════════════════════════════════════════
    from .models import (
        UserStreak, ChallengeTrack, UserChallengeEnrollment,
        DailyTrackCheckIn, MilestoneAchievement
    )
    from datetime import date, timedelta

    today = date.today()
    MILESTONES = [30, 50, 100, 200, 300, 500]

    # Overall streak (any check-in today counts)
    streak, _ = UserStreak.objects.get_or_create(user=request.user)
    if streak.last_completion_date and streak.last_completion_date < today - timedelta(days=1):
        streak.current_streak = 0
        streak.save()

    # User's active enrollments (max 4)
    enrollments = list(
        UserChallengeEnrollment.objects.filter(user=request.user, is_active=True)
        .select_related('track')[:4]
    )

    # Enrich each enrollment with today's status + per-track streak + milestone data
    today_done_count = 0
    for enr in enrollments:
        checked_today = DailyTrackCheckIn.objects.filter(
            user=request.user, track=enr.track, date=today
        ).exists()
        enr.checked_today = checked_today
        if checked_today:
            today_done_count += 1

        # Per-track consecutive streak (walk backwards)
        track_streak = 0
        check_day = today if checked_today else today - timedelta(days=1)
        while DailyTrackCheckIn.objects.filter(
            user=request.user, track=enr.track, date=check_day
        ).exists():
            track_streak += 1
            check_day -= timedelta(days=1)
        enr.track_streak = track_streak

        # Total check-ins for this track (for milestone progress)
        enr.total_checkins = DailyTrackCheckIn.objects.filter(
            user=request.user, track=enr.track
        ).count()

        # Next milestone
        earned = [m for m in MILESTONES if enr.track_streak >= m]
        pending = [m for m in MILESTONES if enr.track_streak < m]
        enr.next_milestone = pending[0] if pending else None
        enr.last_milestone = earned[-1] if earned else None
        enr.milestone_pct = (
            round((enr.track_streak / enr.next_milestone) * 100)
            if enr.next_milestone else 100
        )

        # Check and award milestones
        for m in MILESTONES:
            if enr.track_streak >= m:
                MilestoneAchievement.objects.get_or_create(
                    user=request.user, track=enr.track, milestone_days=m
                )

    # Color theme based on how many tracks checked in today
    color_themes = {
        0: 'theme-0',  # slate/neutral
        1: 'theme-1',  # emerald green
        2: 'theme-2',  # rose pink
        3: 'theme-3',  # midnight dark
        4: 'theme-4',  # amber gold
    }
    dc_theme = color_themes.get(today_done_count, 'theme-0')

    # 30-day overall heatmap
    calendar_days = []
    for i in range(29, -1, -1):
        day = today - timedelta(days=i)
        count = DailyTrackCheckIn.objects.filter(user=request.user, date=day).count()
        calendar_days.append({'date': day, 'count': count, 'is_today': day == today})
    # System tracks user hasn't enrolled in yet (for 'Add Track' suggestions)
    enrolled_track_ids = [enr.track_id for enr in enrollments]
    available_tracks = ChallengeTrack.objects.filter(is_system=True).exclude(
        id__in=enrolled_track_ids
    )

    # Milestone achievements
    user_milestones = MilestoneAchievement.objects.filter(user=request.user).select_related('track')

    # Fetch student enrollment for offer letter download (only if admin-approved)
    from .models import Enrollment
    enrollment = Enrollment.objects.filter(email=request.user.email, is_paid=True, is_approved=True).first()
    paid_enrollment = Enrollment.objects.filter(email=request.user.email, is_paid=True).first()
    is_paid = bool(paid_enrollment)

    context = {
        'tasks': all_tasks,
        'projects': projects,
        'announcements': announcements,
        'completed_count': completed_tasks_count,
        'total_count': total_tasks,
        'progress_percent': progress_percent,
        'student_id': student_id,
        'internship_name': internship_name,
        'period_text': period_text,
        'student_limit': student_limit,
        'days_remaining': days_remaining,
        'current_week': current_week,
        'total_days': total_days,
        'days_passed': days_since_joined,
        'all_tasks_complete': all_tasks_complete,
        'certificate_unlocked': certificate_unlocked,
        'validation_pending': validation_pending,
        'days_left_for_cert': days_left_for_cert,
        'all_projects_cleared': all_projects_cleared,
        'has_certificate': has_certificate,
        'is_paid': is_paid,
        # Daily Challenger
        'streak': streak,
        'enrollments': enrollments,
        'today_done_count': today_done_count,
        'dc_theme': dc_theme,
        'calendar_days': calendar_days,
        'available_tracks': available_tracks,
        'user_milestones': user_milestones,
        'enrollment': enrollment,
    }
    return render(request, 'vision/dashboard.html', context)


@login_required(login_url='sigin')
def task_details(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    try:
        profile = request.user.profile
    except Exception:
        messages.error(request, "Your student profile is not set up yet. Please contact admin.")
        return redirect('dashboard')
    
    # Mapping for security check
    duration_map = {'1 Month': 1, '2 Months': 2, '3 Months': 3, '6 Months': 6}
    student_limit = duration_map.get(profile.period, 1)

    # Check if student is allowed to see this task
    if task.category != profile.Intren or task.required_period > student_limit:
        messages.error(request, "This task is not included in your internship duration.")
        return redirect('dashboard')

    # Sequential unlock check: task N is only accessible if task N-1 is completed
    all_tasks_ordered = list(Task.objects.filter(
        category=profile.Intren,
        required_period__lte=student_limit
    ).order_by('id'))
    task_index = next((i for i, t in enumerate(all_tasks_ordered) if t.id == task.id), None)
    if task_index is not None and task_index > 0:
        prev_task = all_tasks_ordered[task_index - 1]
        if request.user not in prev_task.users_completed.all():
            messages.error(request, "Complete the previous task first to unlock this one.")
            return redirect('dashboard')

    # --- New Logic for Drip Feed ---
    from django.utils import timezone
    from .models import LearningMaterial
    
    # Calculate days since joined
    days_since_joined = (timezone.now() - request.user.date_joined).days
    # Week 1 starts at day 0. Week 2 starts at day 7, etc.
    # So: 0-6 days = Week 1, 7-13 days = Week 2
    current_week = (days_since_joined // 7) + 1
    
    materials = list(LearningMaterial.objects.filter(task=task).order_by('week_number', 'order').distinct())
    
    for material in materials:
        material.locked = material.week_number > current_week

    # Assessment unlocks only when ALL materials are accessible (none locked)
    has_locked_materials = any(material.locked for material in materials)

    # Handle assessment submission (POST)
    if request.method == 'POST' and not has_locked_materials:
        # Mark task as completed only when the assessment is submitted
        # and all learning materials are already unlocked
        task.users_completed.add(request.user)
        messages.success(request, "Assessment submitted! Task marked as completed.")
        return redirect('dashboard')

    # Fallback: if task has no questions and all materials are unlocked,
    # mark as completed on page visit so the student isn't stuck
    if not has_locked_materials and not task.questions.exists():
        task.users_completed.add(request.user)

    context = {
        'task': task,
        'materials': materials,
        'current_week': current_week,
        'has_locked_materials': has_locked_materials,
    }
    return render(request, 'vision/task_details.html', context)

# ── Certificate generation imports ──────────────────────────────────────────
try:
    import os, io
    from django.conf import settings
    from django.http import HttpResponse
    from django.core.files.base import ContentFile
    from PIL import Image, ImageDraw, ImageFont
    import qrcode as qrcode_lib
except ImportError:
    Image = None
    qrcode_lib = None


def _generate_unid(enrollment):
    """Generate a strictly sequential Unique ID from an Enrollment record.
    Format: TRH-{domain_prefix}-{YYMM}-{sequential_number}
    Sequence resets per domain per month.
    Example: TRH-DA-2607-001, TRH-DA-2607-002, TRH-AI-2607-001
    """
    from django.utils import timezone as tz
    from .models import Profile
    import re

    DOMAIN_PREFIX_MAP = {
        'Artificial Intelligence': 'AI',
        'Machine Learning': 'ML',
        'Data Science': 'DS',
        'Data Analytics': 'DA',
        'Web Development': 'WD',
        'Web development': 'WD',
        'Power BI developer': 'PB',
    }
    domain_prefix = DOMAIN_PREFIX_MAP.get(enrollment.domain, enrollment.domain[:2].upper())
    date_part = (
        enrollment.created_at.strftime('%y%m')
        if hasattr(enrollment, 'created_at') and enrollment.created_at
        else tz.now().strftime('%y%m')
    )
    prefix_pattern = f"TRH-{domain_prefix}-{date_part}-"

    # Find the highest existing sequential number for this domain+month
    existing_ids = Profile.objects.filter(
        student_id__startswith=prefix_pattern
    ).values_list('student_id', flat=True)

    max_seq = 0
    for sid in existing_ids:
        try:
            seq_part = sid.replace(prefix_pattern, '')
            num = int(seq_part)
            if num > max_seq:
                max_seq = num
        except (ValueError, AttributeError):
            pass

    next_seq = max_seq + 1
    return f"TRH-{domain_prefix}-{date_part}-{next_seq:03d}"


def _load_font(path, size):
    """Try to load a TrueType font, fall back to PIL default."""
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def _draw_centered_text(draw, y, text, font, color, img_width):
    """Draw text horizontally centered at vertical position y."""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    x = (img_width - text_w) // 2
    draw.text((x, y), text, font=font, fill=color)


def _build_certificate_pdf(user, profile, enrollment=None):
    """
    Draws student details directly onto TRJcertificate.png using Pillow,
    then saves the result as a single-page PDF.
    Returns PDF bytes, or None on failure.
    """
    if not Image or not qrcode_lib:
        return None

    # ── 1. Open the certificate background ───────────────────────────────
    cert_img_path = os.path.join(
        settings.BASE_DIR, 'vision', 'static', 'vision', 'image', 'TRjcertificate.png'
    )
    if not os.path.exists(cert_img_path):
        return None

    cert = Image.open(cert_img_path).convert('RGBA')
    W, H = cert.size          # 2000 × 1414 for TRJcertificate.png
    draw = ImageDraw.Draw(cert)

    # ── 2. Load fonts ─────────────────────────────────────────────────────
    FONTS_DIR = os.path.join(settings.BASE_DIR, 'vision', 'static', 'vision', 'fonts') + os.sep
    font_name_bold  = _load_font(FONTS_DIR + 'arialbd.ttf',  90)   # student name
    font_heading    = _load_font(FONTS_DIR + 'arial.ttf',     50)   # domain line
    font_body       = _load_font(FONTS_DIR + 'arial.ttf',     38)   # description
    font_body_bold  = _load_font(FONTS_DIR + 'arialbd.ttf',   38)   # description bold
    font_small      = _load_font(FONTS_DIR + 'arial.ttf',     28)   # cert id / date

    NAVY   = '#1a3c6e'
    DARK   = '#222222'
    GRAY   = '#555555'

    full_name    = f"{user.first_name} {user.last_name}"
    domain_line  = f"{profile.period}  ·  {profile.Intren}  Internship"
    from django.utils import timezone
    issue_date   = timezone.now().strftime("%B %d, %Y")

    # Use profile.student_id as the single source of truth for UNID
    cert_id = profile.student_id

    # ── 3. Draw text on the certificate ──────────────────────────────────
    # Cert ID — pushed right and slightly down (sweet spot)
    draw.text((220, 40), f"Cert No: {cert_id}", font=font_small, fill=GRAY)

    # Issue Date — top right corner, pushed left
    date_text = f"Issue Date: {issue_date}"
    bbox = draw.textbbox((0, 0), date_text, font=font_small)
    tw = bbox[2] - bbox[0]
    draw.text((W - tw - 180, 40), date_text, font=font_small, fill=GRAY)

    # Student name — sits ON the underline (underline is at y≈760; name top at y≈665)
    _draw_centered_text(draw, 665, full_name, font_name_bold, NAVY, W)

    # ── Calculate internship dates ────────────────────────────────────────
    from dateutil.relativedelta import relativedelta
    period_months_map = {'1-Month': 1, '2-Months': 2, '3-Months': 3, '6-Months': 6,
                         '1 Month': 1, '2 Months': 2, '3 Months': 3, '6 Months': 6}
    duration_months   = period_months_map.get(profile.period, 1)
    # Use admin-set start_date from enrollment, fall back to user.date_joined
    if enrollment and enrollment.start_date:
        start_date = enrollment.start_date
    else:
        start_date = user.date_joined.date()
    end_date        = start_date + relativedelta(months=duration_months)
    start_str       = start_date.strftime("%d %b %Y")
    end_str         = end_date.strftime("%d %b %Y")

    # Professional description — 3 wide lines, centered vertically in the area (y=840–1080)
    def draw_mixed_line(y, segments, default_color):
        """Draws a line of text composed of multiple (text, font) segments, centered."""
        # 1. Calculate total width of the line to center it
        total_width = 0
        for text, fnt in segments:
            bbox = draw.textbbox((0, 0), text, font=fnt)
            total_width += (bbox[2] - bbox[0])
        
        # 2. Draw each segment starting from the centered X coordinate
        current_x = (W - total_width) // 2
        for text, fnt in segments:
            draw.text((current_x, y), text, font=fnt, fill=default_color)
            bbox = draw.textbbox((0, 0), text, font=fnt)
            current_x += (bbox[2] - bbox[0])

    # Line 1: "for successfully completing a {period} {domain} Internship"
    line1_segments = [
        (f"for successfully completing a {profile.period} ", font_body),
        (f"{profile.Intren}", font_body_bold),  # BOLD DOMAIN
        (" Internship", font_body)
    ]

    # Line 2: "at TRH Vision from {start} to {end},"
    line2_segments = [
        ("at ", font_body),
        ("TRHvision", font_body_bold),  # BOLD COMPANY
        (f" from {start_str} to {end_str},", font_body)
    ]

    domain = profile.Intren
    if domain == 'Data Analytics':
        l3_text = "demonstrating strong analytical skills, data interpretation, and"
        l4_text = "proficiency in delivering actionable insights through data-driven problem solving."
    elif domain == 'Power BI developer':
        l3_text = "showcasing expertise in interactive dashboard design, data modeling, and"
        l4_text = "producing impactful business intelligence solutions and visualizations."
    elif domain in ['Web development', 'Web Development']:
        l3_text = "demonstrating technical proficiency in robust coding and architecture, and"
        l4_text = "building scalable responsive web applications using modern frameworks."
    elif domain == 'Machine Learning':
        l3_text = "showcasing advanced skills in model training, predictive analytics, and"
        l4_text = "deploying machine learning algorithms to solve complex real-world problems."
    elif domain == 'Data Science':
        l3_text = "demonstrating excellence in statistical analysis, predictive modeling, and"
        l4_text = "extracting meaningful patterns from complex datasets to drive innovation."
    elif domain == 'Artificial Intelligence':
        l3_text = "showcasing innovation in developing intelligent systems, algorithms, and"
        l4_text = "applying advanced AI concepts to build forward-thinking technological solutions."
    else:
        l3_text = "demonstrating exceptional dedication, technical proficiency, and"
        l4_text = "professional commitment throughout all assigned responsibilities."

    line3_segments = [(l3_text, font_body)]
    line4_segments = [(l4_text, font_body)]

    # 4 lines evenly spaced between y=840 and y=1065 (fits above signatures at y=1220)
    draw_mixed_line(840,  line1_segments, GRAY)
    draw_mixed_line(915,  line2_segments, GRAY)
    draw_mixed_line(990,  line3_segments, GRAY)
    draw_mixed_line(1065, line4_segments, GRAY)

    # ── Signature section — bottom left & middle ──
    # CEO Signature (Left)
    sig1_x1       = int(W * 0.12)
    sig1_x2       = int(W * 0.30)
    sig_y_line    = 1220  # Pushed lower
    sig1_center_x = (sig1_x1 + sig1_x2) // 2

    draw.line([(sig1_x1, sig_y_line), (sig1_x2, sig_y_line)], fill=NAVY, width=3)

    def draw_sig_text(text, center_x, y, fnt, color):
        bb = draw.textbbox((0, 0), text, font=fnt)
        tw = bb[2] - bb[0]
        draw.text((center_x - tw // 2, y), text, font=fnt, fill=color)

    def paste_sign_image(img_name, center_x, line_y, target_w=150):
        sig_path = os.path.join(settings.BASE_DIR, 'vision', 'static', 'vision', 'image', img_name)
        if os.path.exists(sig_path):
            try:
                sig_img = Image.open(sig_path).convert("RGBA")
                
                # Auto-crop transparent borders
                alpha = sig_img.split()[-1]
                bbox = alpha.getbbox()
                if bbox:
                    sig_img = sig_img.crop(bbox)

                # Resize to fit above the signature line nicely
                sig_w, sig_h = sig_img.size
                new_w = target_w  # Custom width per signature to maintain visual balance
                new_h = int(sig_h * (new_w / sig_w))
                sig_img = sig_img.resize((new_w, new_h), Image.LANCZOS)
                
                paste_x = center_x - (new_w // 2)
                paste_y = line_y - new_h - 10
                cert.paste(sig_img, (paste_x, paste_y), sig_img)
            except Exception:
                pass

    draw_sig_text("CEO & Founder", sig1_center_x, 1250, font_small, DARK)
    draw_sig_text("TRHvision",     sig1_center_x, 1285, font_small, GRAY)
    paste_sign_image("ceo_signature.png", sig1_center_x, sig_y_line)

    # Co-Founder Signature (Right)
    sig2_x1       = int(W * 0.70)  # Moved right
    sig2_x2       = int(W * 0.88)  # Moved right
    sig2_center_x = (sig2_x1 + sig2_x2) // 2

    draw.line([(sig2_x1, sig_y_line), (sig2_x2, sig_y_line)], fill=NAVY, width=3)
    
    draw_sig_text("Harshit Dubey", sig2_center_x, 1250, font_small, DARK)
    draw_sig_text("Human Resource",  sig2_center_x, 1285, font_small, GRAY)
    paste_sign_image("HR signature.png", sig2_center_x, sig_y_line, target_w=90)

    # ── 4. Generate & paste QR code — bottom right, above footer ─────────
    qr = qrcode_lib.QRCode(version=1, box_size=8, border=3)
    qr.add_data(f"https://trhvision.in/verify/{cert_id}")
    qr.make(fit=True)
    qr_img  = qr.make_image(fill_color="black", back_color="white").convert('RGBA')
    qr_size = 160
    qr_img  = qr_img.resize((qr_size, qr_size), Image.LANCZOS)
    # Place QR down and to the right corner
    qr_x = W - qr_size - 40
    qr_y = 1250
    cert.paste(qr_img, (qr_x, qr_y))

    # Draw "Verify at" above the QR code
    verify_text = "Verify at"
    bbox = draw.textbbox((0, 0), verify_text, font=font_small)
    tw = bbox[2] - bbox[0]
    text_x = qr_x + (qr_size - tw) // 2
    text_y = qr_y - 35
    draw.text((text_x, text_y), verify_text, font=font_small, fill=GRAY)

    # ── 5. Convert to RGB and save as single-page PDF ─────────────────────
    cert_rgb = cert.convert('RGB')
    pdf_buffer = io.BytesIO()
    cert_rgb.save(pdf_buffer, format='PDF', resolution=150)
    pdf_bytes = pdf_buffer.getvalue()

    # ── 6. Save to profile ────────────────────────────────────────────────
    file_name = f"Certificate_{cert_id}.pdf"
    profile.certificate.save(file_name, ContentFile(pdf_bytes), save=True)

    return pdf_bytes


@login_required(login_url='sigin')
def submit_project(request, project_id):
    from .models import Project, ProjectSubmission
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        
        # Check if already submitted
        submission, created = ProjectSubmission.objects.get_or_create(user=request.user, project=project)
        
        file = request.FILES.get('project_file')
        link = request.POST.get('drive_link')
        
        if file:
            submission.file = file
        if link:
            submission.drive_link = link
            
        submission.save()
        messages.success(request, f"Project '{project.title}' submitted successfully!")
    return redirect('dashboard')


@login_required(login_url='sigin')
def generate_certificate(request):
    """Download the student's certificate as a single-page PDF."""
    if not Image:
        return HttpResponse("Pillow (PIL) is not installed.", status=500)

    profile = request.user.profile
    
    # ── Security Check for Certificate Unlock ──
    duration_map = {'1 Month': 1, '2 Months': 2, '3 Months': 3, '6 Months': 6}
    student_limit = duration_map.get(profile.period, 1)
    
    # Check tasks
    all_tasks = Task.objects.filter(category=profile.Intren, required_period__lte=student_limit)
    total_tasks = all_tasks.count()
    completed_tasks = sum(1 for t in all_tasks if request.user in t.users_completed.all())
    
    if total_tasks > 0 and completed_tasks != total_tasks:
        messages.error(request, "You must complete all tasks before downloading your certificate.")
        return redirect('dashboard')
        
    # Check projects
    from .models import Project, ProjectSubmission
    from django.utils import timezone
    projects = Project.objects.filter(category=profile.Intren, required_period__lte=student_limit)
    
    for p in projects:
        sub = ProjectSubmission.objects.filter(user=request.user, project=p).first()
        if not sub:
            messages.error(request, f"You must submit project '{p.title}' before downloading your certificate.")
            return redirect('dashboard')
            
        diff = timezone.now() - sub.submitted_at
        if not sub.is_approved and diff.days < 3:
            messages.error(request, f"Please wait {3 - diff.days} more day(s) for verification before downloading your certificate.")
            return redirect('dashboard')

    # Look up the student's enrollment to use the same UNID as the offer letter
    from .models import Enrollment
    enrollment = Enrollment.objects.filter(email=request.user.email, is_paid=True).first()
    if not enrollment:
        messages.error(request, "Payment required! Please complete your payment before downloading your certificate.")
        return redirect('dashboard')

    pdf_bytes = _build_certificate_pdf(request.user, profile, enrollment=enrollment)

    # Use profile.student_id as the single source of truth
    cert_id = profile.student_id

    if pdf_bytes:
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        if request.GET.get('download') == 'true':
            response['Content-Disposition'] = f'attachment; filename="Certificate_{cert_id}.pdf"'
        else:
            response['Content-Disposition'] = f'inline; filename="Certificate_{cert_id}.pdf"'
        return response
    return HttpResponse("Error generating certificate PDF.", status=500)


def verify_certificate(request, student_id):
    from .models import Profile
    profile = get_object_or_404(Profile, student_id=student_id)
    
    # Check if certificate exists for this profile
    has_cert = bool(profile.certificate)
    
    context = {
        'profile': profile,
        'has_cert': has_cert,
    }
    return render(request, 'vision/verify_certificate.html', context)


def _build_offer_letter_pdf(enrollment):
    """
    Draws student details directly onto TRHvision_offer_letter-1.png using Pillow,
    then saves the result as a single-page PDF.
    Returns PDF bytes, or None on failure.
    """
    if not Image:
        return None

    # Open the template image
    template_path = os.path.join(
        settings.BASE_DIR, 'vision', 'static', 'vision', 'image', 'TRHo-1.png'
    )
    if not os.path.exists(template_path):
        return None

    img = Image.open(template_path).convert('RGBA')
    W, H = img.size # 1700 x 2200
    draw = ImageDraw.Draw(img)

    # Load fonts (bundled with project for cross-platform deployment)
    FONTS_DIR = os.path.join(settings.BASE_DIR, 'vision', 'static', 'vision', 'fonts') + os.sep
    try:
        font_bold    = ImageFont.truetype(FONTS_DIR + 'arialbd.ttf', 29)
        font_regular = ImageFont.truetype(FONTS_DIR + 'arial.ttf',   26)
        font_small   = ImageFont.truetype(FONTS_DIR + 'arial.ttf',   23)
    except Exception:
        font_bold = ImageFont.load_default()
        font_regular = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Format Date — use admin-set start_date, fall back to created_at
    if enrollment.start_date:
        issue_date = enrollment.start_date.strftime("%B %d, %Y")
    elif hasattr(enrollment, 'created_at') and enrollment.created_at:
        issue_date = enrollment.created_at.strftime("%B %d, %Y")
    else:
        issue_date = timezone.now().strftime("%B %d, %Y")
    
    # UNID — use profile.student_id as the single source of truth
    # Look up the student's profile (if it exists) to get the authoritative ID
    from .models import Profile as _Profile
    try:
        _student_profile = _Profile.objects.get(user__email=enrollment.email)
        unid = _student_profile.student_id
    except _Profile.DoesNotExist:
        # Profile not yet created (first-time generation during auto-approval)
        unid = _generate_unid(enrollment)

    # 1. Fill in Date and UNID — aligned to exact label positions in TRHo-1.png
    # Template labels detected at: DATE y=482, UNID y=526, both ending at x≈1180
    VALUE_X = 1195   # 15px gap after label right edge (~1180)
    draw.text((VALUE_X, 482), issue_date, font=font_regular, fill="#222222", anchor="lm")
    draw.text((VALUE_X, 526), unid,       font=font_regular, fill="#222222", anchor="lm")

    # 2. Draw Recipient info
    draw.text((200, 600), "To,", font=font_bold, fill="#222222")
    draw.text((200, 645), enrollment.name, font=font_bold, fill="#1a3c6e")

    # Normalize domain to full display name
    DOMAIN_DISPLAY = {
        'aI': 'Artificial Intelligence',
        'ai': 'Artificial Intelligence',
        'AI': 'Artificial Intelligence',
        'Artificial Intelligence': 'Artificial Intelligence',
        'ML': 'Machine Learning',
        'ml': 'Machine Learning',
        'Machine Learning': 'Machine Learning',
        'DS': 'Data Science',
        'Data Science': 'Data Science',
        'DA': 'Data Analytics',
        'Data Analytics': 'Data Analytics',
        'WD': 'Web Development',
        'Web Development': 'Web Development',
        'Web development': 'Web Development',
        'Webdevlopment': 'Web Development',
        'Power BI developer': 'Power BI Development',
        'Power BI': 'Power BI Development',
    }
    display_domain = DOMAIN_DISPLAY.get(enrollment.domain, enrollment.domain)

    # 3. Subject
    draw.text((200, 780), f"Subject: Offer of Virtual Internship in {display_domain}", font=font_bold, fill="#1a3c6e")

    # 4. Salutation
    draw.text((200, 850), f"Dear {enrollment.name},", font=font_bold, fill="#222222")

    # 5. Body paragraphs — JUSTIFIED text helper
    def draw_wrapped_text(draw, text, x, y, max_width, font, line_spacing=10, fill="#444444"):
        # Split text into wrapped lines
        words = text.split(' ')
        lines = []
        current_line = []
        for word in words:
            test = current_line + [word]
            bbox = draw.textbbox((0, 0), ' '.join(test), font=font)
            if bbox[2] - bbox[0] > max_width and current_line:
                lines.append(current_line)
                current_line = [word]
            else:
                current_line = test
        if current_line:
            lines.append(current_line)

        current_y = y
        for i, line_words in enumerate(lines):
            is_last = (i == len(lines) - 1)

            if is_last or len(line_words) == 1:
                # Last line or single word → left-aligned
                draw.text((x, current_y), ' '.join(line_words), font=font, fill=fill)
            else:
                # Full line → justified: spread words across max_width
                words_w = [
                    draw.textbbox((0, 0), w, font=font)[2] - draw.textbbox((0, 0), w, font=font)[0]
                    for w in line_words
                ]
                total_words_w = sum(words_w)
                gaps = len(line_words) - 1
                gap_size = (max_width - total_words_w) / gaps
                for j, word in enumerate(line_words):
                    word_x = x + sum(words_w[:j]) + j * gap_size
                    draw.text((int(word_x), current_y), word, font=font, fill=fill)

            # Line height from first word
            h = draw.textbbox((0, 0), line_words[0], font=font)[3] - \
                draw.textbbox((0, 0), line_words[0], font=font)[1]
            current_y += h + line_spacing
        return current_y

    # Calculate internship dates
    from dateutil.relativedelta import relativedelta
    period_months_map = {'1-Month': 1, '2-Months': 2, '3-Months': 3, '6-Months': 6,
                         '1 Month': 1, '2 Months': 2, '3 Months': 3, '6 Months': 6}
    duration_months = period_months_map.get(enrollment.duration, 1)
    # Use admin-set start_date, fall back to created_at
    if enrollment.start_date:
        start_date = enrollment.start_date
    elif hasattr(enrollment, 'created_at') and enrollment.created_at:
        start_date = enrollment.created_at.date()
    else:
        start_date = timezone.now().date()
    end_date = start_date + relativedelta(months=duration_months)
    start_str = start_date.strftime("%B %Y")
    end_str = end_date.strftime("%B %Y")

    body_p1 = (
        f"We are pleased to inform you that you have been selected for the Virtual Internship Programme at TRHvision "
        f"in the {display_domain} domain. This offer is issued following your successful enrollment and "
        f"verification process."
    )

    body_p2 = (
        f"The internship is scheduled for a duration of {enrollment.duration}, commencing in {start_str} and "
        f"concluding in {end_str}. During this period, you will collaborate on curated projects, technical tasks, "
        f"core modules, and skill-based assessments designed to build practical expertise in the domain."
    )

    body_p3 = (
        f"We are confident that through your dedication and successful completion of these milestone tasks, you will "
        f"develop the foundational technical skills, analytical mindset, and professional discipline required for a "
        f"successful career in {display_domain}."
    )

    body_p4 = (
        "Upon satisfactory completion of all program requirements and project submissions, you will be awarded a "
        "verified Internship Completion Certificate from TRHvision."
    )

    body_p5 = (
        "Should you have any further questions or require assistance, please feel free to reach out to our support "
        "team at hr@trhvision.com."
    )

    body_p6 = (
        "Congratulations on your selection. We look forward to a productive learning journey with you."
    )

    y_cursor = 910
    y_cursor = draw_wrapped_text(draw, body_p1, 200, y_cursor, 1300, font_regular) + 22
    y_cursor = draw_wrapped_text(draw, body_p2, 200, y_cursor, 1300, font_regular) + 22
    y_cursor = draw_wrapped_text(draw, body_p3, 200, y_cursor, 1300, font_regular) + 22
    y_cursor = draw_wrapped_text(draw, body_p4, 200, y_cursor, 1300, font_regular) + 22
    y_cursor = draw_wrapped_text(draw, body_p5, 200, y_cursor, 1300, font_regular) + 22
    y_cursor = draw_wrapped_text(draw, body_p6, 200, y_cursor, 1300, font_regular) + 15

    # 6. Warm regards + CEO & HR signatures side by side (flows with content via y_cursor)
    y_cursor += 125
    draw.text((200, y_cursor), "Warm regards,", font=font_regular, fill="#222222")
    y_cursor += 70

    sig_y = y_cursor  # Track the signature row y position

    # ── Fixed signature box size (same for both CEO and HR) ──
    SIG_BOX_W = 200
    SIG_BOX_H = 80

    def paste_signature(img, path, x, y, box_w, box_h):
        """Paste a signature image fitted into a fixed bounding box."""
        if not os.path.exists(path):
            return
        try:
            sig_img = Image.open(path).convert("RGBA")
            alpha = sig_img.split()[-1]
            bbox = alpha.getbbox()
            if bbox:
                sig_img = sig_img.crop(bbox)
            sig_w, sig_h = sig_img.size
            # Scale to fit within the box while preserving aspect ratio
            scale = min(box_w / sig_w, box_h / sig_h)
            new_w = int(sig_w * scale)
            new_h = int(sig_h * scale)
            sig_img = sig_img.resize((new_w, new_h), Image.LANCZOS)
            # Center vertically within the box
            offset_y = (box_h - new_h) // 2
            img.paste(sig_img, (x, y + offset_y), sig_img)
        except Exception:
            pass

    # ── CEO Signature (Left side) ──
    ceo_sig_path = os.path.join(settings.BASE_DIR, 'vision', 'static', 'vision', 'image', 'ceo_signature.png')
    paste_signature(img, ceo_sig_path, 200, sig_y, SIG_BOX_W, SIG_BOX_H)

    # ── HR Signature (Right side) ──
    hr_sig_x = int(W * 0.45)  # Shifted left
    hr_sig_path = os.path.join(settings.BASE_DIR, 'vision', 'static', 'vision', 'image', 'HR signature.png')
    paste_signature(img, hr_sig_path, hr_sig_x, sig_y, SIG_BOX_W, SIG_BOX_H)

    # Convert to RGB and save as single-page PDF
    img_rgb = img.convert('RGB')
    pdf_buffer = io.BytesIO()
    img_rgb.save(pdf_buffer, format='PDF', resolution=150)
    pdf_bytes = pdf_buffer.getvalue()
    pdf_buffer.close()

    return pdf_bytes


def download_offer_letter(request, enrollment_id=None):
    """Download the student's Internship Offer Letter as a PDF."""
    if not Image:
        return HttpResponse("Pillow (PIL) is not installed.", status=500)

    from .models import Enrollment
    from django.utils import timezone
    import io

    enrollment = None
    if enrollment_id is not None:
        # Check session to authorize non-logged-in users (newly registered)
        session_enrolled_id = request.session.get('enrolled_id')
        if session_enrolled_id == enrollment_id or (request.user.is_authenticated and request.user.is_staff):
            try:
                enrollment = Enrollment.objects.get(id=enrollment_id, is_paid=True)
            except Enrollment.DoesNotExist:
                pass
        
        # Alternatively, if user is logged in, they can access their own enrollment by ID
        if not enrollment and request.user.is_authenticated:
            try:
                enrollment = Enrollment.objects.get(id=enrollment_id, email=request.user.email, is_paid=True)
            except Enrollment.DoesNotExist:
                pass
    else:
        # Requires login and fetches by user's email
        if not request.user.is_authenticated:
            return redirect('sigin')
        try:
            enrollment = Enrollment.objects.filter(email=request.user.email, is_paid=True).first()
        except Enrollment.DoesNotExist:
            pass

    if not enrollment:
        messages.error(request, "Enrollment record not found or unauthorized.")
        return redirect('dashboard' if request.user.is_authenticated else 'index')

    # Block offer letter download until admin has approved the enrollment
    if not enrollment.is_approved:
        messages.error(request, "Your offer letter is pending admin approval. Please check back later.")
        return redirect('dashboard' if request.user.is_authenticated else 'enroll_success')

    pdf_bytes = _build_offer_letter_pdf(enrollment)

    if pdf_bytes:
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        filename = f"Offer_Letter_{enrollment.name.replace(' ', '_')}.pdf"
        if request.GET.get('download') == 'true':
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
        else:
            response['Content-Disposition'] = f'inline; filename="{filename}"'
        return response
    return HttpResponse("Error generating offer letter PDF.", status=500)

@login_required(login_url='sigin')
def track_checkin(request, track_id):
    """POST: Check in for a specific challenge track today."""
    if request.method != 'POST':
        return redirect('dashboard')

    from .models import (
        ChallengeTrack, DailyTrackCheckIn, UserStreak,
        MilestoneAchievement, UserChallengeEnrollment
    )
    from datetime import date, timedelta

    today = date.today()
    track = get_object_or_404(ChallengeTrack, id=track_id)
    notes = request.POST.get('notes', '').strip()

    # Ensure user is enrolled in this track
    enrolled = UserChallengeEnrollment.objects.filter(
        user=request.user, track=track, is_active=True
    ).exists()
    if not enrolled:
        messages.error(request, "You're not enrolled in this track.")
        return redirect('dashboard')

    _, created = DailyTrackCheckIn.objects.get_or_create(
        user=request.user, track=track, date=today,
        defaults={'notes': notes}
    )

    if created:
        # Update overall streak
        streak, _ = UserStreak.objects.get_or_create(user=request.user)
        if streak.last_completion_date == today - timedelta(days=1):
            streak.current_streak += 1
        elif streak.last_completion_date != today:
            streak.current_streak = 1
        streak.last_completion_date = today
        if streak.current_streak > streak.longest_streak:
            streak.longest_streak = streak.current_streak
        streak.save()

        messages.success(request, f"{track.emoji} {track.name} — checked in! Keep going! 🔥")
    else:
        messages.info(request, f"You already checked in for {track.name} today.")

    return redirect('dashboard')


@login_required(login_url='sigin')
def manage_challenges(request):
    """GET/POST: Let user manage their challenge enrollments."""
    from .models import ChallengeTrack, UserChallengeEnrollment

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'enroll':
            track_id   = request.POST.get('track_id')
            target     = int(request.POST.get('target_days', 30))
            track      = get_object_or_404(ChallengeTrack, id=track_id)
            active_count = UserChallengeEnrollment.objects.filter(
                user=request.user, is_active=True
            ).count()
            if active_count >= 4:
                messages.error(request, "You can have at most 4 active challenges at once.")
            else:
                enr, created = UserChallengeEnrollment.objects.get_or_create(
                    user=request.user, track=track,
                    defaults={'target_days': target, 'is_active': True}
                )
                if not created:
                    enr.is_active = True
                    enr.target_days = target
                    enr.save()
                messages.success(request, f"{track.emoji} {track.name} added to your challenges!")

        elif action == 'remove':
            enr_id = request.POST.get('enrollment_id')
            UserChallengeEnrollment.objects.filter(
                id=enr_id, user=request.user
            ).update(is_active=False)
            messages.info(request, "Challenge removed.")

        elif action == 'add_custom':
            name  = request.POST.get('name', '').strip()
            emoji = request.POST.get('emoji', '⚡').strip() or '⚡'
            desc  = request.POST.get('description', '').strip()
            target = int(request.POST.get('target_days', 30))
            if not name:
                messages.error(request, "Please enter a track name.")
            else:
                active_count = UserChallengeEnrollment.objects.filter(
                    user=request.user, is_active=True
                ).count()
                if active_count >= 4:
                    messages.error(request, "You can have at most 4 active challenges at once.")
                else:
                    track = ChallengeTrack.objects.create(
                        name=name, emoji=emoji, description=desc,
                        is_system=False, created_by=request.user
                    )
                    UserChallengeEnrollment.objects.create(
                        user=request.user, track=track, target_days=target
                    )
                    messages.success(request, f"{emoji} Custom challenge '{name}' created!")

        return redirect('manage_challenges')

    # ── GET ─────────────────────────────────────────────────────
    from .models import (
        ChallengeTrack, UserChallengeEnrollment,
        DailyTrackCheckIn, UserStreak, MilestoneAchievement
    )
    from datetime import date, timedelta
    import json

    today = date.today()
    MILESTONES = [30, 50, 100, 200, 300, 500]
    TRACK_PALETTE = [
        '#10b981', '#f472b6', '#60a5fa', '#fbbf24',
        '#a78bfa', '#f87171', '#34d399', '#fb923c'
    ]

    # All enrollments (active + inactive)
    enrollments = list(
        UserChallengeEnrollment.objects.filter(user=request.user)
        .select_related('track').order_by('-is_active', 'enrolled_at')
    )
    active_enrollments = [e for e in enrollments if e.is_active]

    # Overall streak
    streak, _ = UserStreak.objects.get_or_create(user=request.user)
    if streak.last_completion_date and streak.last_completion_date < today - timedelta(days=1):
        streak.current_streak = 0
        streak.save()

    # ── Per-track enrichment ──────────────────────────────────────
    for i, enr in enumerate(active_enrollments):
        enr.color = TRACK_PALETTE[i % len(TRACK_PALETTE)]

        # Today check-in
        enr.checked_today = DailyTrackCheckIn.objects.filter(
            user=request.user, track=enr.track, date=today
        ).exists()

        # Total check-ins ever
        enr.total_checkins = DailyTrackCheckIn.objects.filter(
            user=request.user, track=enr.track
        ).count()

        # Current track streak
        track_streak = 0
        check_day = today if enr.checked_today else today - timedelta(days=1)
        while DailyTrackCheckIn.objects.filter(
            user=request.user, track=enr.track, date=check_day
        ).exists():
            track_streak += 1
            check_day -= timedelta(days=1)
        enr.track_streak = track_streak

        # Last check-in date
        last_ci = DailyTrackCheckIn.objects.filter(
            user=request.user, track=enr.track
        ).order_by('-date').first()
        enr.last_checkin_date = last_ci.date if last_ci else None

        # 30-day per-track heatmap
        enr.cal30 = []
        for j in range(29, -1, -1):
            day = today - timedelta(days=j)
            done = DailyTrackCheckIn.objects.filter(
                user=request.user, track=enr.track, date=day
            ).exists()
            enr.cal30.append({'date': day, 'done': done, 'is_today': day == today})

        # Next milestone
        earned  = [m for m in MILESTONES if enr.track_streak >= m]
        pending = [m for m in MILESTONES if enr.track_streak < m]
        enr.next_milestone  = pending[0] if pending else None
        enr.last_milestone  = earned[-1] if earned else None
        enr.milestone_pct   = (
            round((enr.track_streak / enr.next_milestone) * 100)
            if enr.next_milestone else 100
        )

    # ── Chart data ───────────────────────────────────────────────
    # Bar chart: last 14 days, stacked bars per track
    last_14    = [today - timedelta(days=i) for i in range(13, -1, -1)]
    bar_labels = json.dumps([d.strftime('%d %b') for d in last_14])
    bar_datasets = []
    for i, enr in enumerate(active_enrollments):
        data = []
        for day in last_14:
            done = DailyTrackCheckIn.objects.filter(
                user=request.user, track=enr.track, date=day
            ).exists()
            data.append(1 if done else 0)
        bar_datasets.append({
            'label':           f"{enr.track.emoji} {enr.track.name}",
            'data':            data,
            'backgroundColor': enr.color,
            'borderRadius':    4,
        })
    bar_datasets_json = json.dumps(bar_datasets)

    # Pie chart: total check-ins per track
    pie_labels = json.dumps([f"{e.track.emoji} {e.track.name}" for e in active_enrollments])
    pie_data   = json.dumps([e.total_checkins for e in active_enrollments])
    pie_colors = json.dumps([e.color for e in active_enrollments])

    # ── Recent activity log (last 14 days, all tracks) ───────────
    recent_log = DailyTrackCheckIn.objects.filter(
        user=request.user,
        date__gte=today - timedelta(days=13)
    ).select_related('track').order_by('-date', 'track__name')

    # ── Summary stats ─────────────────────────────────────────────
    total_overall   = DailyTrackCheckIn.objects.filter(user=request.user).count()
    perfect_days    = 0  # days where ALL active tracks were done
    if active_enrollments:
        active_track_ids = [e.track_id for e in active_enrollments]
        for j in range(29, -1, -1):
            day = today - timedelta(days=j)
            done_count = DailyTrackCheckIn.objects.filter(
                user=request.user, track_id__in=active_track_ids, date=day
            ).count()
            if done_count >= len(active_enrollments):
                perfect_days += 1

    system_tracks = ChallengeTrack.objects.filter(is_system=True).exclude(
        enrollments__user=request.user, enrollments__is_active=True
    )
    target_choices = UserChallengeEnrollment.TARGET_CHOICES

    return render(request, 'vision/manage_challenges.html', {
        'enrollments':       enrollments,
        'active_enrollments': active_enrollments,
        'system_tracks':     system_tracks,
        'target_choices':    target_choices,
        'streak':            streak,
        'total_overall':     total_overall,
        'perfect_days':      perfect_days,
        'recent_log':        recent_log,
        'bar_labels':        bar_labels,
        'bar_datasets':      bar_datasets_json,
        'pie_labels':        pie_labels,
        'pie_data':          pie_data,
        'pie_colors':        pie_colors,
        'today':             today,
    })



@login_required(login_url='sigin')
def complete_daily_challenge(request):
    """Legacy - redirect to dashboard."""
    return redirect('dashboard')


# ═══════════════════════════════════════════════════════════════
#  CLIENT DASHBOARD VIEWS
# ═══════════════════════════════════════════════════════════════
from .models import (
    ClientProfile, ClientProject, ClientProjectMilestone,
    ClientProjectDeliverable, ClientProjectUpdate, ClientInvoice
)


def client_login(request):
    """Login page for clients."""
    if request.method == 'POST':
        uname = request.POST.get('username')
        passw = request.POST.get('password')
        user = authenticate(request, username=uname, password=passw)
        if user is not None:
            login(request, user)
            # Check if user has a client profile
            if hasattr(user, 'client_profile'):
                return redirect('client_dashboard')
            else:
                messages.error(request, "No client account found for this user.")
                return redirect('client_login')
        else:
            messages.error(request, "Invalid email or password")
    return render(request, 'vision/client_login.html')


@login_required(login_url='client_login')
def client_dashboard(request):
    """Main client dashboard showing all projects."""
    try:
        client_profile = request.user.client_profile
    except ClientProfile.DoesNotExist:
        messages.error(request, "No client profile found.")
        return redirect('index')

    projects = ClientProject.objects.filter(client=client_profile)
    active_projects = projects.exclude(status='completed')
    completed_projects = projects.filter(status='completed')

    # Overall stats
    total_projects = projects.count()
    active_count = active_projects.count()

    # Average progress across active projects
    if active_count > 0:
        avg_progress = sum(p.progress for p in active_projects) / active_count
    else:
        avg_progress = 0

    # Total invoices
    total_paid = ClientInvoice.objects.filter(
        project__client=client_profile, status='paid'
    ).aggregate(total=models.Sum('amount'))['total'] or 0
    pending_amount = ClientInvoice.objects.filter(
        project__client=client_profile, status='pending'
    ).aggregate(total=models.Sum('amount'))['total'] or 0

    # Recent updates across all projects
    recent_updates = ClientProjectUpdate.objects.filter(
        project__client=client_profile
    ).select_related('project', 'posted_by')[:10]

    context = {
        'client': client_profile,
        'projects': projects,
        'active_projects': active_projects,
        'completed_projects': completed_projects,
        'total_projects': total_projects,
        'active_count': active_count,
        'avg_progress': int(avg_progress),
        'total_paid': total_paid,
        'pending_amount': pending_amount,
        'recent_updates': recent_updates,
    }
    return render(request, 'vision/client_dashboard.html', context)


@login_required(login_url='client_login')
def client_project_detail(request, project_id):
    """Detailed view of a single client project."""
    try:
        client_profile = request.user.client_profile
    except ClientProfile.DoesNotExist:
        return redirect('index')

    project = get_object_or_404(ClientProject, id=project_id, client=client_profile)
    milestones = project.milestones.all()
    deliverables = project.deliverables.all()
    updates = project.updates.select_related('posted_by').all()
    invoices = project.invoices.all()

    # Calculate days remaining
    days_remaining = None
    if project.deadline:
        from django.utils import timezone
        from datetime import date
        delta = project.deadline - date.today()
        days_remaining = max(0, delta.days)

    context = {
        'client': client_profile,
        'project': project,
        'milestones': milestones,
        'deliverables': deliverables,
        'updates': updates,
        'invoices': invoices,
        'days_remaining': days_remaining,
    }
    return render(request, 'vision/client_project_detail.html', context)


# ═══════════════════════════════════════════════════════════════
#  CUSTOM ADMIN PANEL VIEWS
#  Accessible only to superusers / staff
# ═══════════════════════════════════════════════════════════════

def staff_required(view_func):
    """Decorator: allow only staff/superuser."""
    from functools import wraps
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('trh_admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper


def trh_admin_login(request):
    """Admin panel login."""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('trh_admin_dashboard')
    if request.method == 'POST':
        uname = request.POST.get('username')
        passw = request.POST.get('password')
        user = authenticate(request, username=uname, password=passw)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('trh_admin_dashboard')
        else:
            messages.error(request, "Invalid credentials or not authorized.")
    return render(request, 'vision/trh_admin_login.html')


@staff_required
def trh_admin_dashboard(request):
    """Admin panel overview with KPIs."""
    from django.db.models import Sum, Count
    from .models import Enrollment, Contact, ClientRequest

    # Student stats
    total_students = Profile.objects.count()
    active_domains = Profile.objects.values('Intren').annotate(c=Count('id'))

    # Client stats
    total_clients = ClientProfile.objects.count()
    active_client_projects = ClientProject.objects.exclude(status='completed').count()
    total_client_projects = ClientProject.objects.count()

    # Revenue
    total_enrollment_revenue = Enrollment.objects.filter(is_paid=True).aggregate(
        total=Sum('amount'))['total'] or 0
    total_client_revenue = ClientInvoice.objects.filter(status='paid').aggregate(
        total=Sum('amount'))['total'] or 0

    # Recent entries
    recent_enrollments = Enrollment.objects.order_by('-created_at')[:5]
    recent_contacts = Contact.objects.order_by('-created_at')[:5]
    recent_client_requests = ClientRequest.objects.order_by('-created_at')[:5]
    recent_projects = ClientProject.objects.order_by('-created_at')[:5]

    context = {
        'total_students': total_students,
        'active_domains': active_domains,
        'total_clients': total_clients,
        'active_client_projects': active_client_projects,
        'total_client_projects': total_client_projects,
        'total_enrollment_revenue': total_enrollment_revenue,
        'total_client_revenue': total_client_revenue,
        'recent_enrollments': recent_enrollments,
        'recent_contacts': recent_contacts,
        'recent_client_requests': recent_client_requests,
        'recent_projects': recent_projects,
    }
    return render(request, 'vision/trh_admin_dashboard.html', context)


@staff_required
def trh_admin_students(request):
    """Student management page."""
    students = Profile.objects.select_related('user').all().order_by('-user__date_joined')

    # Apply filters
    domain_filter = request.GET.get('domain', '')
    period_filter = request.GET.get('period', '')
    search = request.GET.get('q', '')

    if domain_filter:
        students = students.filter(Intren=domain_filter)
    if period_filter:
        students = students.filter(period=period_filter)
    if search:
        students = students.filter(
            models.Q(user__first_name__icontains=search) |
            models.Q(user__last_name__icontains=search) |
            models.Q(user__email__icontains=search) |
            models.Q(student_id__icontains=search)
        )

    # Enrich with progress data
    for student in students:
        duration_map = {'1 Month': 1, '2 Months': 2, '3 Months': 3, '6 Months': 6}
        limit = duration_map.get(student.period, 1)
        tasks = Task.objects.filter(category=student.Intren, required_period__lte=limit)
        total = tasks.count()
        completed = sum(1 for t in tasks if student.user in t.users_completed.all())
        student.progress = int((completed / total * 100)) if total > 0 else 0
        student.completed_tasks = completed
        student.total_tasks = total

    context = {
        'students': students,
        'domain_filter': domain_filter,
        'period_filter': period_filter,
        'search': search,
        'domain_choices': Profile.DOMAIN_CHOICES,
        'period_choices': Profile.PERIOD_CHOICES,
    }
    return render(request, 'vision/trh_admin_students.html', context)


@staff_required
def trh_admin_student_detail(request, user_id):
    """Individual student detail."""
    student_user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=student_user)

    duration_map = {'1 Month': 1, '2 Months': 2, '3 Months': 3, '6 Months': 6}
    limit = duration_map.get(profile.period, 1)
    tasks = list(Task.objects.filter(category=profile.Intren, required_period__lte=limit).order_by('id'))
    total = len(tasks)
    completed = sum(1 for t in tasks if student_user in t.users_completed.all())
    progress = int((completed / total * 100)) if total > 0 else 0

    # Projects
    from .models import Project, ProjectSubmission
    projects = Project.objects.filter(category=profile.Intren, required_period__lte=limit)
    for p in projects:
        p.submission = ProjectSubmission.objects.filter(user=student_user, project=p).first()

    # Find matching enrollment for offer letter
    from .models import Enrollment
    enrollment = Enrollment.objects.filter(email=student_user.email, is_paid=True).first()
    enrollment_id = enrollment.id if enrollment else None

    # Compute the UNID that matches the offer letter
    enrollment_unid = _generate_unid(enrollment) if enrollment else None

    context = {
        'student_user': student_user,
        'profile': profile,
        'tasks': tasks,
        'total_tasks': total,
        'completed_tasks': completed,
        'progress': progress,
        'projects': projects,
        'enrollment_id': enrollment_id,
        'enrollment_unid': enrollment_unid,
    }
    return render(request, 'vision/trh_admin_student_detail.html', context)


@staff_required
def trh_admin_edit_student_id(request, user_id):
    """Allow admin to edit a student's ID (UNID)."""
    if request.method != 'POST':
        return redirect('trh_admin_student_detail', user_id=user_id)

    profile = get_object_or_404(Profile, user_id=user_id)
    new_id = request.POST.get('student_id', '').strip()

    if not new_id:
        messages.error(request, "Student ID cannot be empty.")
        return redirect('trh_admin_student_detail', user_id=user_id)

    # Validate uniqueness (exclude current profile)
    if Profile.objects.filter(student_id=new_id).exclude(pk=profile.pk).exists():
        messages.error(request, f"Student ID '{new_id}' is already in use by another student.")
        return redirect('trh_admin_student_detail', user_id=user_id)

    profile.student_id = new_id
    profile.save()
    messages.success(request, f"Student ID updated to '{new_id}' successfully.")
    return redirect('trh_admin_student_detail', user_id=user_id)

@staff_required
def trh_admin_clients(request):
    """Client management page."""
    clients = ClientProfile.objects.select_related('user').all().order_by('-created_at')
    search = request.GET.get('q', '')
    if search:
        clients = clients.filter(
            models.Q(company_name__icontains=search) |
            models.Q(user__email__icontains=search) |
            models.Q(phone__icontains=search)
        )

    # Enrich with stats
    for client in clients:
        client.active_projects = client.projects.exclude(status='completed').count()
        client.total_projects = client.projects.count()
        paid = ClientInvoice.objects.filter(
            project__client=client, status='paid'
        ).aggregate(total=models.Sum('amount'))['total'] or 0
        client.total_paid = paid

    context = {
        'clients': clients,
        'search': search,
    }
    return render(request, 'vision/trh_admin_clients.html', context)


@staff_required
def trh_admin_create_client(request):
    """Create a new client account (admin only)."""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        company_name = request.POST.get('company_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        industry = request.POST.get('industry', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        if not email or not password or not company_name:
            messages.error(request, "Email, password, and company name are required.")
            return redirect('trh_admin_clients')

        if User.objects.filter(username=email).exists():
            messages.error(request, f"A user with email {email} already exists.")
            return redirect('trh_admin_clients')

        # Create user
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Create client profile
        ClientProfile.objects.create(
            user=user,
            company_name=company_name,
            phone=phone,
            industry=industry,
        )

        # Send welcome email
        try:
            from django.core.mail import send_mail
            send_mail(
                f"Welcome to TRHvision — Client Portal Access",
                f"""Dear {first_name or company_name},

Your client portal account has been created at TRHvision.

Login URL: https://trhvision.in/client/login/
Email: {email}
Password: {password}

You can track your project progress, view deliverables, and check invoices through your dashboard.

Best regards,
TRHvision Team
""",
                'noreply@trhvision.in',
                [email],
                fail_silently=True,
            )
        except Exception:
            pass

        messages.success(request, f"Client account created for {company_name}!")
        return redirect('trh_admin_clients')

    return redirect('trh_admin_clients')


@staff_required
def trh_admin_client_project(request, project_id):
    """Manage a specific client project (view + edit)."""
    project = get_object_or_404(ClientProject, id=project_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_project':
            project.title = request.POST.get('title', project.title)
            project.status = request.POST.get('status', project.status)
            project.progress = int(request.POST.get('progress', project.progress))
            project.description = request.POST.get('description', project.description)
            deadline = request.POST.get('deadline')
            if deadline:
                project.deadline = deadline
            project.save()
            messages.success(request, "Project updated!")

        elif action == 'add_milestone':
            ClientProjectMilestone.objects.create(
                project=project,
                title=request.POST.get('milestone_title', ''),
                description=request.POST.get('milestone_description', ''),
                due_date=request.POST.get('milestone_due_date') or None,
                order=project.milestones.count() + 1,
            )
            messages.success(request, "Milestone added!")

        elif action == 'toggle_milestone':
            mid = request.POST.get('milestone_id')
            milestone = get_object_or_404(ClientProjectMilestone, id=mid, project=project)
            milestone.is_completed = not milestone.is_completed
            if milestone.is_completed:
                from django.utils import timezone
                milestone.completed_at = timezone.now()
            else:
                milestone.completed_at = None
            milestone.save()

            # Auto-recalculate progress
            total_m = project.milestones.count()
            done_m = project.milestones.filter(is_completed=True).count()
            if total_m > 0:
                project.progress = int((done_m / total_m) * 100)
                project.save()

        elif action == 'add_deliverable':
            f = request.FILES.get('deliverable_file')
            if f:
                ClientProjectDeliverable.objects.create(
                    project=project,
                    title=request.POST.get('deliverable_title', f.name),
                    file=f,
                    description=request.POST.get('deliverable_description', ''),
                )
                messages.success(request, "Deliverable uploaded!")

                # Send email notification to client
                try:
                    from django.core.mail import send_mail
                    send_mail(
                        f"📦 New Deliverable — {project.title}",
                        f"""Hi {project.client.user.first_name or project.client.company_name},

A new deliverable has been uploaded for your project "{project.title}".

Login to your dashboard to download it:
https://trhvision.in/client/project/{project.id}/

— TRHvision Team
""",
                        'noreply@trhvision.in',
                        [project.client.user.email],
                        fail_silently=True,
                    )
                except Exception:
                    pass

        elif action == 'post_update':
            msg = request.POST.get('update_message', '').strip()
            if msg:
                ClientProjectUpdate.objects.create(
                    project=project,
                    message=msg,
                    posted_by=request.user,
                )
                messages.success(request, "Update posted!")

                # Send email notification
                try:
                    from django.core.mail import send_mail
                    send_mail(
                        f"📋 Project Update — {project.title}",
                        f"""Hi {project.client.user.first_name or project.client.company_name},

There's a new update on your project "{project.title}":

{msg}

View full details on your dashboard:
https://trhvision.in/client/project/{project.id}/

— TRHvision Team
""",
                        'noreply@trhvision.in',
                        [project.client.user.email],
                        fail_silently=True,
                    )
                except Exception:
                    pass

        elif action == 'add_invoice':
            inv_number = request.POST.get('invoice_number', '').strip()
            inv_amount = request.POST.get('invoice_amount', '0')
            inv_desc = request.POST.get('invoice_description', '')
            inv_due = request.POST.get('invoice_due_date') or None
            if inv_number and float(inv_amount) > 0:
                ClientInvoice.objects.create(
                    project=project,
                    invoice_number=inv_number,
                    amount=inv_amount,
                    description=inv_desc,
                    due_date=inv_due,
                )
                messages.success(request, "Invoice added!")

        elif action == 'mark_invoice_paid':
            inv_id = request.POST.get('invoice_id')
            invoice = get_object_or_404(ClientInvoice, id=inv_id, project=project)
            invoice.status = 'paid'
            from datetime import date
            invoice.paid_date = date.today()
            invoice.transaction_id = request.POST.get('transaction_id', '')
            invoice.save()
            messages.success(request, f"Invoice {invoice.invoice_number} marked as paid!")

        elif action == 'create_project':
            ClientProject.objects.create(
                client=project.client if hasattr(project, 'client') else None,
                title=request.POST.get('title', ''),
                description=request.POST.get('description', ''),
                service_type=request.POST.get('service_type', 'Other'),
                start_date=request.POST.get('start_date') or None,
                deadline=request.POST.get('deadline') or None,
                budget=request.POST.get('budget') or None,
            )
            messages.success(request, "New project created!")

        return redirect('trh_admin_client_project', project_id=project.id)

    milestones = project.milestones.all()
    deliverables = project.deliverables.all()
    updates = project.updates.select_related('posted_by').all()
    invoices = project.invoices.all()

    context = {
        'project': project,
        'milestones': milestones,
        'deliverables': deliverables,
        'updates': updates,
        'invoices': invoices,
        'status_choices': ClientProject.STATUS_CHOICES,
        'service_choices': ClientProject.SERVICE_CHOICES,
    }
    return render(request, 'vision/trh_admin_client_project.html', context)


@staff_required
def trh_admin_create_project(request):
    """Create a new project for a client."""
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        client = get_object_or_404(ClientProfile, id=client_id)
        project = ClientProject.objects.create(
            client=client,
            title=request.POST.get('title', ''),
            description=request.POST.get('description', ''),
            service_type=request.POST.get('service_type', 'Other'),
            start_date=request.POST.get('start_date') or None,
            deadline=request.POST.get('deadline') or None,
            budget=request.POST.get('budget') or None,
        )
        messages.success(request, f"Project '{project.title}' created for {client.company_name}!")
        return redirect('trh_admin_client_project', project_id=project.id)
    return redirect('trh_admin_clients')


@staff_required
def trh_admin_enrollments(request):
    """Enrollment management page."""
    from .models import Enrollment
    enrollments = Enrollment.objects.order_by('-created_at')

    # Filters
    domain_filter = request.GET.get('domain', '')
    payment_filter = request.GET.get('payment', '')
    search = request.GET.get('q', '')

    if domain_filter:
        enrollments = enrollments.filter(domain=domain_filter)
    if payment_filter == 'paid':
        enrollments = enrollments.filter(is_paid=True)
    elif payment_filter == 'unpaid':
        enrollments = enrollments.filter(is_paid=False)
    if search:
        enrollments = enrollments.filter(
            models.Q(name__icontains=search) |
            models.Q(email__icontains=search) |
            models.Q(phone__icontains=search) |
            models.Q(college__icontains=search)
        )

    context = {
        'enrollments': enrollments,
        'domain_filter': domain_filter,
        'payment_filter': payment_filter,
        'search': search,
    }
    return render(request, 'vision/trh_admin_enrollments.html', context)


@staff_required
def trh_admin_contacts(request):
    """Contact and client request viewer."""
    from .models import Contact, ClientRequest
    contacts = Contact.objects.order_by('-created_at')
    client_requests = ClientRequest.objects.order_by('-created_at')

    tab = request.GET.get('tab', 'contacts')

    context = {
        'contacts': contacts,
        'client_requests': client_requests,
        'tab': tab,
    }
    return render(request, 'vision/trh_admin_contacts.html', context)


@staff_required
def trh_admin_approve_enrollment(request, enrollment_id):
    """Admin view to approve a student's enrollment and generate their credentials."""
    from .models import Enrollment, Profile
    import random
    from django.utils import timezone
    from datetime import datetime

    if request.method != 'POST':
        messages.error(request, "Invalid request method.")
        return redirect('trh_admin_enrollments')

    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    if not enrollment.is_paid:
        messages.error(request, "Cannot approve an unpaid enrollment.")
        return redirect('trh_admin_enrollments')

    if enrollment.is_approved:
        messages.warning(request, "Enrollment is already approved.")
        return redirect('trh_admin_enrollments')

    # Parse the admin-set start date
    start_date_str = request.POST.get('start_date', '').strip()
    if start_date_str:
        try:
            enrollment.start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid start date format. Please use the date picker.")
            return redirect('trh_admin_enrollments')
    else:
        enrollment.start_date = timezone.now().date()

    # Generate a user-friendly, secure password based on student's name
    first_name = enrollment.name.strip().split()[0] if enrollment.name.strip() else "Student"
    cleaned_name = ''.join(c for c in first_name if c.isalnum())
    rand_num = random.randint(100, 999)
    temp_password = f"TRH@{cleaned_name.capitalize()}{rand_num}"

    enrollment.is_approved = True
    enrollment.approved_at = timezone.now()
    enrollment.generated_password = temp_password
    enrollment.save()

    # --- Immediately create User + Profile with sequential student ID ---
    username = enrollment.email.strip()
    user = User.objects.filter(username=username).first()
    if not user:
        name_parts = enrollment.name.strip().split()
        user = User.objects.create_user(
            username=username,
            email=username,
            password=temp_password,
            first_name=name_parts[0] if name_parts else "",
            last_name=" ".join(name_parts[1:]) if len(name_parts) > 1 else ""
        )

        # Map domains to match Profile model choices
        domain_mapping = {
            'Web Development': 'Web development',
            'Webdevlopment': 'Web development',
            'ML': 'Machine Learning',
            'Artificial Intelligence': 'Artificial Intelligence',
            'data science': 'Data Science',
        }
        normalized_domain = domain_mapping.get(enrollment.domain, enrollment.domain)

        # Generate sequential student ID
        unid = _generate_unid(enrollment)

        Profile.objects.create(
            user=user,
            Intren=normalized_domain,
            period=enrollment.duration,
            student_id=unid
        )

    messages.success(
        request,
        f"✅ Enrollment for {enrollment.name} approved! "
        f"Student ID generated. "
        f"Now you can send the Offer Letter, and then dispatch Login Credentials."
    )
    return redirect('trh_admin_enrollments')


# ──────────────────────────────────────────────────────────────────
#  STEP 1: Admin sends Offer Letter email (one-click)
# ──────────────────────────────────────────────────────────────────
@staff_required
def trh_admin_send_offer_letter(request, enrollment_id):
    """Admin one-click view: generate and email the offer letter to the student."""
    from .models import Enrollment, EmailTemplate
    from django.core.mail import EmailMessage
    from django.conf import settings as django_settings

    if request.method != 'POST':
        messages.error(request, "Invalid request method.")
        return redirect('trh_admin_enrollments')

    enrollment = get_object_or_404(Enrollment, id=enrollment_id)

    if not enrollment.is_approved:
        messages.error(request, "Cannot send offer letter for an unapproved enrollment.")
        return redirect('trh_admin_enrollments')

    if enrollment.offer_letter_sent:
        messages.warning(request, f"Offer letter was already sent to {enrollment.name}.")
        return redirect('trh_admin_enrollments')

    # Generate the offer letter PDF
    pdf_bytes = _build_offer_letter_pdf(enrollment)

    try:
        from_email = getattr(django_settings, 'EMAIL_HOST_USER', None) or \
                     getattr(django_settings, 'DEFAULT_FROM_EMAIL', 'noreply@trhvision.in')

        # Build template context
        start_date_str = (
            enrollment.start_date.strftime('%B %d, %Y')
            if enrollment.start_date else 'your confirmed start date'
        )
        template_ctx = {
            'name':       enrollment.name,
            'domain':     enrollment.domain,
            'duration':   enrollment.duration,
            'start_date': start_date_str,
            'email':      enrollment.email,
        }

        # Load subject/body from DB (with safe fallback)
        tpl = EmailTemplate.objects.filter(name='offer_letter').first()
        if tpl:
            email_subject, email_body = tpl.get_rendered(template_ctx)
        else:
            # Hardcoded fallback in case migration has not run yet
            email_subject = (
                f"\U0001f389 Internship Offer Letter \u2013 {enrollment.domain} | TRHvision Academy"
            )
            email_body = (
                f"Dear {enrollment.name},\n\n"
                "Greetings from TRHvision Academy! \U0001f389\n\n"
                f"We are delighted to officially welcome you to our internship programme. "
                f"Your enrollment in the {enrollment.domain} internship programme for a duration of "
                f"{enrollment.duration} has been reviewed and approved by our academic team.\n\n"
                "Please find your official Internship Offer Letter attached to this email.\n\n"
                f"Your internship journey begins on {start_date_str}. "
                "We will soon send you your portal login credentials.\n\n"
                "With warm regards,\nTRHvision Academy Team\n"
                "\U0001f4e7 info@trhvision.in | \U0001f310 www.trhvision.in"
            )

        email_message = EmailMessage(
            subject=email_subject,
            body=email_body,
            from_email=from_email,
            to=[enrollment.email],
            cc=['rachit.tyagi@trhvision.in'],
        )

        if pdf_bytes:
            email_message.attach(
                f"Offer_Letter_{enrollment.name.replace(' ', '_')}.pdf",
                pdf_bytes,
                "application/pdf"
            )

        email_message.send(fail_silently=False)

        enrollment.offer_letter_sent = True
        enrollment.save()

        messages.success(
            request,
            f"\U0001f4e9 Offer letter successfully sent to {enrollment.name} ({enrollment.email}). "
            f"You may now send the login credentials."
        )

    except Exception as e:
        messages.error(request, f"Failed to send offer letter: {e}")

    return redirect('trh_admin_enrollments')



# ──────────────────────────────────────────────────────────────────
#  STEP 2: Admin sends Login Credentials email (one-click)
#  Only available after offer letter has been sent.
# ──────────────────────────────────────────────────────────────────
@staff_required
def trh_admin_send_credentials(request, enrollment_id):
    """Admin one-click view: email login credentials to the student.
    Only allowed after the offer letter has been sent."""
    from .models import Enrollment, EmailTemplate
    from django.core.mail import EmailMessage
    from django.conf import settings as django_settings

    if request.method != 'POST':
        messages.error(request, "Invalid request method.")
        return redirect('trh_admin_enrollments')

    enrollment = get_object_or_404(Enrollment, id=enrollment_id)

    if not enrollment.is_approved:
        messages.error(request, "Cannot send credentials for an unapproved enrollment.")
        return redirect('trh_admin_enrollments')

    if not enrollment.offer_letter_sent:
        messages.error(
            request,
            "\u26a0\ufe0f Please send the Offer Letter first before dispatching credentials."
        )
        return redirect('trh_admin_enrollments')

    if enrollment.credentials_sent:
        messages.warning(request, f"Credentials were already sent to {enrollment.name}.")
        return redirect('trh_admin_enrollments')

    # Ensure generated_password exists on enrollment
    if not enrollment.generated_password:
        first_name = enrollment.name.strip().split()[0] if enrollment.name.strip() else "Student"
        cleaned_name = ''.join(c for c in first_name if c.isalnum())
        import random
        rand_num = random.randint(100, 999)
        enrollment.generated_password = f"TRH@{cleaned_name.capitalize()}{rand_num}"
        enrollment.save()

    # Ensure Django User exists and has correct password
    username = enrollment.email.strip()
    user = User.objects.filter(username=username).first()
    if user:
        # Sync password to match the one sent in the email
        user.set_password(enrollment.generated_password)
        user.save()
        
        # Ensure Profile exists and has a valid, corrected student_id
        try:
            profile = user.profile
            if not profile.student_id or profile.student_id == enrollment.name or ' ' in profile.student_id or not profile.student_id.startswith('TRH'):
                profile.student_id = _generate_unid(enrollment)
                profile.save()
            student_id = profile.student_id
        except Exception:
            from .models import Profile
            domain_mapping = {
                'Web Development': 'Web development',
                'Webdevlopment': 'Web development',
                'ML': 'Machine Learning',
                'Artificial Intelligence': 'Artificial Intelligence',
                'data science': 'Data Science',
            }
            normalized_domain = domain_mapping.get(enrollment.domain, enrollment.domain)
            student_id = _generate_unid(enrollment)
            profile = Profile.objects.create(
                user=user,
                Intren=normalized_domain,
                period=enrollment.duration,
                student_id=student_id
            )
    else:
        # Create user
        name_parts = enrollment.name.strip().split()
        user = User.objects.create_user(
            username=username,
            email=username,
            password=enrollment.generated_password,
            first_name=name_parts[0] if name_parts else "",
            last_name=" ".join(name_parts[1:]) if len(name_parts) > 1 else ""
        )
        from .models import Profile
        domain_mapping = {
            'Web Development': 'Web development',
            'Webdevlopment': 'Web development',
            'ML': 'Machine Learning',
            'Artificial Intelligence': 'Artificial Intelligence',
            'data science': 'Data Science',
        }
        normalized_domain = domain_mapping.get(enrollment.domain, enrollment.domain)
        student_id = _generate_unid(enrollment)
        profile = Profile.objects.create(
            user=user,
            Intren=normalized_domain,
            period=enrollment.duration,
            student_id=student_id
        )

    try:
        from_email = getattr(django_settings, 'EMAIL_HOST_USER', None) or \
                     getattr(django_settings, 'DEFAULT_FROM_EMAIL', 'noreply@trhvision.in')

        # Build template context
        template_ctx = {
            'name':       enrollment.name,
            'domain':     enrollment.domain,
            'duration':   enrollment.duration,
            'email':      enrollment.email,
            'student_id': student_id,
            'password':   enrollment.generated_password,
            'portal_url': 'http://trhvision.com/sigin/',
        }

        # Load subject/body from DB (with safe fallback)
        tpl = EmailTemplate.objects.filter(name='login_credentials').first()
        if tpl:
            email_subject, email_body = tpl.get_rendered(template_ctx)
        else:
            # Hardcoded fallback in case migration has not run yet
            email_subject = (
                f"\U0001f511 Your TRHvision Academy Login Credentials"
                f" \u2013 {enrollment.domain} Internship"
            )
            email_body = (
                f"Dear {enrollment.name},\n\n"
                "We hope you have received your Offer Letter and are excited to begin "
                "your internship at TRHvision Academy!\n\n"
                "Your student account on the TRHvision Academy Portal is now active.\n\n"
                "\u2501" * 28 + "\n"
                "\U0001f393 Your Login Credentials\n"
                "\u2501" * 28 + "\n"
                f"  Portal URL : http://trhvision.com/sigin/\n"
                f"  Student ID : {student_id}\n"
                f"  Username   : {enrollment.email}\n"
                f"  Password   : {enrollment.generated_password}\n"
                "\u2501" * 28 + "\n\n"
                "\U0001f4cc Important Notes:\n"
                "  \u2022 Please log in immediately and change your password for security.\n"
                "  \u2022 Complete your profile setup once you log in.\n"
                "  \u2022 Follow the module guidelines sequentially for best results.\n\n"
                "Warm regards,\nTRHvision Academy Team\n"
                "\U0001f4e7 info@trhvision.in | \U0001f310 www.trhvision.in"
            )

        email_message = EmailMessage(
            subject=email_subject,
            body=email_body,
            from_email=from_email,
            to=[enrollment.email],
            cc=['rachit.tyagi@trhvision.in'],
        )
        email_message.send(fail_silently=False)

        enrollment.credentials_sent = True
        enrollment.save()

        messages.success(
            request,
            f"\U0001f511 Login credentials successfully sent to {enrollment.name} ({enrollment.email}). "
            f"Onboarding complete!"
        )

    except Exception as e:
        messages.error(request, f"Failed to send credentials: {e}")

    return redirect('trh_admin_enrollments')




def process_approved_enrollments():
    """
    Background worker: Finds approved enrollments older than 4 hours,
    creates their Django User/Profile, emails credentials + offer letter,
    and marks them as sent.
    """
    from datetime import timedelta
    from django.utils import timezone
    from django.contrib.auth.models import User
    from .models import Enrollment, Profile
    from django.core.mail import EmailMessage

    now = timezone.now()
    four_hours_ago = now - timedelta(hours=4)

    # Query approved, paid enrollments that are at least 4 hours old and haven't had credentials sent
    pending = Enrollment.objects.filter(
        is_paid=True,
        is_approved=True,
        credentials_sent=False,
        created_at__lte=four_hours_ago
    )

    for enrollment in pending:
        try:
            username = enrollment.email.strip()
            # Try to fetch existing user, otherwise create a new one
            user = User.objects.filter(username=username).first()
            if not user:
                name_parts = enrollment.name.strip().split()
                first_name = name_parts[0] if name_parts else ""
                last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

                user = User.objects.create_user(
                    username=username,
                    email=username,
                    password=enrollment.generated_password
                )
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                # Map domains if needed to match Profile constraints
                domain_mapping = {
                    'Web Development': 'Web development',
                    'Webdevlopment': 'Web development',
                    'ML': 'Machine Learning',
                    'Artificial Intelligence': 'Artificial Intelligence',
                    'data science': 'Data Science',
                }
                normalized_domain = domain_mapping.get(enrollment.domain, enrollment.domain)

                # Compute UNID from enrollment (same format as offer letter)
                unid = _generate_unid(enrollment)

                # Create profile with the enrollment UNID as student_id
                Profile.objects.create(
                    user=user,
                    Intren=normalized_domain,
                    period=enrollment.duration,
                    student_id=unid
                )

            # Generate PDF offer letter
            pdf_bytes = _build_offer_letter_pdf(enrollment)

            email_body = f"""Dear {enrollment.name},

Congratulations! We are pleased to inform you that your virtual internship enrollment in the {enrollment.domain} domain for a duration of {enrollment.duration} has been approved by our academic team!

Your official Internship Offer Letter is attached to this email.

To help you get started, we have created your student account on the TRHvision Academy Portal. You can log in to your personalized student dashboard to view learning materials, track milestones, and submit your tasks/projects.

Here are your dashboard login credentials:
------------------------------------------
Portal URL: http://trhvision.com/sigin/
Username:   {enrollment.email}
Password:   {enrollment.generated_password}
------------------------------------------

Important details:
- Please log in using the credentials above and complete your profile setup.
- You can download your offer letter at any time from your dashboard.
- Follow the guidelines and complete the modules sequentially.

We wish you a productive and enriching internship experience with us!

Best regards,
TRHvision Academy Team
"""

            from django.conf import settings
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@trhvision.in')
            smtp_user = getattr(settings, 'EMAIL_HOST_USER', '')
            if smtp_user:
                from_email = smtp_user

            email_message = EmailMessage(
                subject="Internship Approved: Login Credentials & Offer Letter - TRHvision",
                body=email_body,
                from_email=from_email,
                to=[enrollment.email],
            )

            if pdf_bytes:
                email_message.attach(
                    f"Offer_Letter_{enrollment.name.replace(' ', '_')}.pdf",
                    pdf_bytes,
                    "application/pdf"
                )

            email_message.send(fail_silently=False)

            # Mark as sent
            enrollment.credentials_sent = True
            enrollment.save()
            print(f"Successfully sent credentials and offer letter to {enrollment.email}")

        except Exception as e:
            print(f"Error processing credentials for enrollment {enrollment.id}: {e}")


def start_approved_enrollments_dispatcher():
    """Starts the background thread checking for approved enrollments to process."""
    import threading
    import time

    def run_dispatcher():
        print("Starting Approved Enrollments Dispatcher background thread...")
        time.sleep(10)  # Wait for Django server startup to complete
        while True:
            try:
                process_approved_enrollments()
            except Exception as e:
                print(f"Error in Approved Enrollments Dispatcher: {e}")
            time.sleep(60)  # Run checks every 60 seconds

    t = threading.Thread(target=run_dispatcher, daemon=True)
    t.start()
