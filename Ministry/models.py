from django.db import models

class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=255, null=True, blank=True)
    comment_text = models.TextField()  # Correctly defined
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name  # Returns the name of the commenter



class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    image = models.ImageField(upload_to='event_images/')
    
    def __str__(self):
        return self.title
    

from django.db import models
from django.utils import timezone

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField()
    admin_reply = models.TextField(null=True, blank=True)  # Admin reply
    date_submitted = models.DateTimeField(auto_now_add=True)
    date_replied = models.DateTimeField(null=True, blank=True)  # Date of admin reply

    def __str__(self):
        return self.name
    


from django.db import models

class Donation(models.Model):
    # Country will be a free text input
    country = models.CharField(max_length=100)

    # Donation categories and their descriptions
    ITEM_CATEGORY_CHOICES = [
        ('child_sponsorship', 'Child Sponsorship'),
        ('education_fund', 'Education Fund'),
        ('feeding_program', 'Feeding Program'),
        ('healthcare_support', 'Healthcare Support'),
        ('housing_shelter', 'Housing and Shelter'),
        ('community_outreach', 'Community Outreach'),
        ('spiritual_growth', 'Spiritual Growth'),
        ('emergency_relief', 'Emergency Relief'),
        ('general_support', 'General Support'),
    ]
    item_category = models.CharField(max_length=50, choices=ITEM_CATEGORY_CHOICES)

    # Other fields
    district = models.CharField(max_length=100)
    subcounty = models.CharField(max_length=100)
    parish = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.amount}"
    




from django.db import models
from django.core.mail import send_mail
from django.utils import timezone


class UploadRequest(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class UploadedForm(models.Model):
    upload_request = models.ForeignKey(UploadRequest, on_delete=models.CASCADE)
    form_file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Fields for admin reply
    admin_reply = models.TextField(blank=True, null=True, help_text='Write your reply here')
    is_replied = models.BooleanField(default=False)
    replied_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Form uploaded by {self.upload_request.email}"

    def send_reply(self):
        """Send an email reply to the user if the admin has entered a reply."""
        if self.admin_reply and not self.is_replied:
            send_mail(
                subject='Response to Your Form Submission',
                message=self.admin_reply,
                from_email='rwothongeojulius052@gmail.com',
                recipient_list=[self.upload_request.email],
                fail_silently=False,
            )
            self.is_replied = True
            self.replied_at = timezone.now()
            self.save()

