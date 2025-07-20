from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import ResumeUploadForm, RegisterForm, LoginForm, JobCreateForm
from .models import Resume, Job, MatchResult

import docx2txt
from PyPDF2 import PdfReader


def home(request):
    return render(request, 'home.html')


# ---------------------- AUTHENTICATION ----------------------

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid credentials.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


# ---------------------- UPLOAD & MATCHING ----------------------

@login_required
def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user  # Add this field in your model if missing
            uploaded_file = request.FILES['file']

            # Extract text from resume
            text = ''
            if uploaded_file.name.endswith('.pdf'):
                reader = PdfReader(uploaded_file)
                for page in reader.pages:
                    text += page.extract_text() or ''
            elif uploaded_file.name.endswith('.docx'):
                text = docx2txt.process(uploaded_file)

            resume.skills = text
            resume.save()

            # Match with jobs
            for job in Job.objects.all():
                match_score = calculate_match_score(text, job.description)
                MatchResult.objects.create(resume=resume, job=job, score=match_score)

            messages.success(request, "Resume uploaded and matched with jobs!")
            return redirect('matched_results')
    else:
        form = ResumeUploadForm()
    return render(request, 'upload_resume.html', {'form': form})


@login_required
def matched_results(request):
    resumes = Resume.objects.filter(user=request.user).order_by('-uploaded_at')
    matched_results = []
    for resume in resumes:
        results = MatchResult.objects.filter(resume=resume).order_by('-score')
        job_scores = [(result.job, round(result.score, 2)) for result in results]
        matched_results.append({'resume': resume, 'matches': job_scores})
    return render(request, 'matched_results.html', {'matched_results': matched_results})


# ---------------------- Matching Logic ----------------------

def calculate_match_score(resume_text, job_desc):
    resume_words = set(resume_text.lower().split())
    job_words = set(job_desc.lower().split())

    if not job_words:
        return 0.0

    common = resume_words.intersection(job_words)
    score = (len(common) / len(job_words)) * 100
    return score


# ---------------------- JOB LIST & JOB CREATION ----------------------

@login_required
def job_list(request):
    jobs = Job.objects.all().order_by('-posted_at')
    return render(request, 'job_list.html', {'jobs': jobs})




@login_required
def create_job(request):
    if request.method == 'POST':
        form = JobCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Job created successfully.")
            return redirect('job_list')
    else:
        form = JobCreateForm()
    return render(request, 'create_job.html', {'form': form})
