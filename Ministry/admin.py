from django.contrib import admin
from .models import Comment

admin.site.register(Comment)  # Register the Comment model


from django.contrib import admin

# Customize admin site
admin.site.site_header = "Precious Beloved Ministry's Admin"
admin.site.site_title = "Precious Beloved Ministry"
admin.site.index_title = "Welcome to Precious Beloved Ministry's Admin Panel"


from .models import Event

admin.site.register(Event)

from django.contrib import admin
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from .models import ContactSubmission

class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'date_submitted', 'date_replied')
    search_fields = ('name', 'email')
    fields = ('name', 'email', 'phone', 'address', 'message', 'admin_reply')
    readonly_fields = ('name', 'email', 'phone', 'address', 'message')
    actions = ['send_reply_email']

    def send_reply_email(self, request, queryset):
        for contact in queryset:
            if contact.admin_reply:
                success = self.send_reply(contact)
                if success:
                    contact.date_replied = timezone.now()
                    contact.save()
        self.message_user(request, "Reply emails sent successfully.")
    
    def send_reply(self, contact):
        """ Send an email reply to the user """
        subject = "Response from Precious Beloved Children Ministries"
        recipient_email = contact.email

        # Render the email template with context
        message = render_to_string('email_template.html', {
            'contact': contact,
            'reply_message': contact.admin_reply,
            'year': timezone.now().year
        })

        try:
            send_mail(
                subject,
                '',  # Empty plain text content since we're using HTML
                settings.EMAIL_HOST_USER,
                [recipient_email],
                fail_silently=False,
                html_message=message
            )
            return True
        except BadHeaderError:
            return False

admin.site.register(ContactSubmission, ContactSubmissionAdmin)

from django.contrib import admin
from .models import Donation

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'amount', 'submitted_at', 'country', 'district', 'subcounty', 'parish', 'village', 'item_category']
    list_filter = ['country', 'district', 'subcounty', 'item_category']
    search_fields = ['name', 'phone', 'email']


from django.contrib import admin
from .models import UploadRequest, UploadedForm

@admin.register(UploadRequest)
class UploadRequestAdmin(admin.ModelAdmin):
    list_display = ('email', 'password', 'is_verified', 'created_at')
    search_fields = ('email',)

@admin.register(UploadedForm)
class UploadedFormAdmin(admin.ModelAdmin):
    list_display = ('upload_request', 'form_file', 'uploaded_at', 'is_replied', 'replied_at')
    search_fields = ('upload_request__email',)
    readonly_fields = ('uploaded_at', 'replied_at', 'is_replied')
    fields = ('upload_request', 'form_file', 'admin_reply', 'is_replied', 'replied_at')
    
    def save_model(self, request, obj, form, change):
        """Send an email when admin_reply is updated in the admin panel."""
        if change and 'admin_reply' in form.changed_data:
            obj.send_reply()
        super().save_model(request, obj, form, change)
