from django.db import models
from django.contrib.auth.models import User  # ✅ Required to link resumes to users

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ✅ NEW: Link resume to user
    file = models.FileField(upload_to='resumes/')
    skills = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name.split('/')[-1]


class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    required_skills = models.TextField(help_text="Comma-separated list of required skills")
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class MatchResult(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return f"{self.resume} -> {self.job} ({self.score:.2f}%)"
