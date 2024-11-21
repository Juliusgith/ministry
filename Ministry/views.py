from django.shortcuts import render

def home(request):
    return render(request, 'home.html')



from django.shortcuts import render, redirect
from .forms import CommentForm  # Import the form

def blog_home(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)  # Handle form submission
        if form.is_valid():
            form.save()  # Save the form data
            return redirect('blog_home')  # Redirect to the same page to avoid resubmission
    else:
        form = CommentForm()  # Display an empty form for GET requests

    return render(request, 'blog_home.html', {'form': form})  # Render the template with the form

def about_us(request):
    return render(request, 'about_us.html')



from .models import Event

def home(request):
    # Get all upcoming events
    events = Event.objects.all()
    return render(request, 'home.html', {'events': events})


from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from .forms import ContactForm

def contact_view(request):
    success_message = None
    error_message = None

    # Check if user has sent a message within the last 10 minutes
    last_message_time = request.session.get('last_message_time')
    if last_message_time:
        last_message_time = timezone.datetime.fromisoformat(last_message_time)
        time_diff = timezone.now() - last_message_time
        if time_diff < timedelta(minutes=10):
            wait_time = 10 - int(time_diff.total_seconds() // 60)
            error_message = f"Please wait {wait_time} more minute(s) before sending another message. You can reach us out on from our contact information or contact the manager from his contact details."
            return render(request, 'contact_us.html', {'form': ContactForm(), 'error_message': error_message})

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save form data
            success_message = "Your message has been sent successfully!"
            # Store the current time in session after successful form submission
            request.session['last_message_time'] = timezone.now().isoformat()
            return redirect('success')
    else:
        form = ContactForm()

    return render(request, 'contact_us.html', {'form': form, 'success_message': success_message, 'error_message': error_message})


def success_view(request):
    # Render a success message and allow the user to proceed to the home page
    return render(request, 'success.html')



import os
from io import BytesIO
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Donation
from .forms import DonationForm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# Dictionary to hold descriptions for each category
category_descriptions = {
    'child_sponsorship': 'Support the education, healthcare, and basic needs of a specific child.',
    'education_fund': 'Contribute to school fees, supplies, and educational programs for children.',
    'feeding_program': 'Help provide nutritious meals to children in need.',
    'healthcare_support': 'Aid in medical care, immunizations, and health check-ups for children.',
    'housing_shelter': 'Support building safe homes and shelters for vulnerable children.',
    'community_outreach': 'Fund projects that support families and the broader community.',
    'spiritual_growth': 'Assist in providing resources for spiritual education and church programs.',
    'emergency_relief': 'Provide urgent support during times of crisis, such as food, medicine,& shelter.',
    'general_support': 'Unrestricted donations to be used where most needed within the ministry.'
}

def register_donation(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save()
            return redirect('preview_donation', pk=donation.id)
    else:
        form = DonationForm()
    return render(request, 'register.html', {'form': form})

def preview_donation(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    category_description = category_descriptions.get(donation.item_category, 'No description available')
    return render(request, 'preview.html', {
        'donation': donation,
        'category_description': category_description
    })

def download_pdf(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    category_description = category_descriptions.get(donation.item_category, 'No description available')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{donation.name}_donation.pdf"'

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    title_style = styles['Title']
    subtitle_style = styles['Heading2']
    normal_style = styles['Normal']

    # Header section
    # Header Section with blue font color
    header = Paragraph(
    '<font color="#2E86C1"><b>Precious Beloved Children Ministries Contribution Sheet</b></font>', 
    title_style
)
    header_table = Table([[header]], colWidths=[500])
    header_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 14),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ('TOPPADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 12))
    

    # Side-by-side tables for Payment Details and Contact Information
    
    payment_details = [
        ['Account Number: 1234567890'],
        ['MTN Mobile Money: +256700123456'],
        ['Airtel Money: +256750987654']
    ]
    contact_info = [
        ['Kwio Akuru Village, Lobodegi Parish'],
        ['Pokwero Subcounty, Pakwach District'],
        ['Along Pakwach-Wadelai Road, Uganda'],
        ['WhatsApp: +256700987654 | Contact: 0770927154']
    ]

    payment_table = Table(payment_details, colWidths=[250])
    contact_table = Table(contact_info, colWidths=[250])

    payment_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold')
    ]))
    contact_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold')
    ]))

    side_by_side_table = Table([[payment_table, contact_table]], colWidths=[280, 280])
    elements.append(side_by_side_table)
    elements.append(Spacer(1, 12))

    # Donation Information Table
    # Donation Information Table with bold labels and regular inputs
    donation_info = [
    [Paragraph('<b>Name:</b>', normal_style), donation.name],
    [Paragraph('<b>Phone:</b>', normal_style), donation.phone],
    [Paragraph('<b>Email:</b>', normal_style), donation.email],
    [Paragraph('<b>Amount:</b>', normal_style), str(donation.amount)],
    [Paragraph('<b>Country:</b>', normal_style), donation.country],
    [Paragraph('<b>District:</b>', normal_style), donation.district],
    [Paragraph('<b>Subcounty:</b>', normal_style), donation.subcounty],
    [Paragraph('<b>Parish:</b>', normal_style), donation.parish],
    [Paragraph('<b>Village:</b>', normal_style), donation.village],
    [Paragraph('<b>Category:</b>', normal_style), donation.item_category],
    [Paragraph('<b>Description:</b>', normal_style), category_description]
]

    donation_table = Table(donation_info, colWidths=[150, 350])
    donation_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(donation_table)
    elements.append(Spacer(1, 12))


    # Cheque Details
    elements.append(Paragraph("Cheque Details", subtitle_style))
    cheque_details_data = [
        ['Bank Name:', '', 'Cheque No:', ''],
        ['Amount:', '', 'Amount in Words:', '']
    ]
    cheque_details_table = Table(cheque_details_data, colWidths=[120, 120, 120, 120])
    cheque_details_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(cheque_details_table)
    elements.append(Spacer(1, 12))

    # Ledger Section
    ledger_data = [
    ['Amount', 'Category'],
    ['50000', ''],
    ['20000', ''],
    ['10000', ''],
    ['5000', ''],
    ['1000', '']
]

# Create the ledger table
    ledger_table = Table(ledger_data, colWidths=[150, 350])
    ledger_table.setStyle(TableStyle([
    # Background color for headers (Rich Blue)
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86C1')),  # Rich blue color
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # White text for better contrast
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('ALIGN', (0, 1), (-1, -1), 'CENTER')  # Center align the content below headers
    ]))
    elements.append(ledger_table)
    elements.append(Spacer(1, 12))


    # Additional Information Section
    additional_info_data = [
        ['Amount in Words:', '______________________________________________________________'],
        ['Paid in By:', '______________________________________________________________'],
        ['Signature:', '______________________________________________________________']
    ]
    additional_info_table = Table(additional_info_data, colWidths=[150, 350])
    elements.append(additional_info_table)
    elements.append(Spacer(1, 12))

    # Footer
    current_year = datetime.now().year

# Updated footer content with additional information
    footer_info = [
    ['Thank you for your support! For inquiries, contact us on +256 770927154 or WhatsApp: +256770927154' ],
    [f'Precious Beloved Children Ministries | © {current_year} All Rights Reserved']
]

# Create the footer table
    footer_table = Table(footer_info, colWidths=500)
    footer_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
    ('TEXTCOLOR', (0, 0), (-1, -1), colors.darkblue),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4)
]))

# Add the footer to the PDF elements
    elements.append(footer_table)
    elements.append(Spacer(1, 6))  # Reduced the spacer to save space

    doc.build(elements)
    response.write(buffer.getvalue())
    buffer.close()
    return response






import random
import string
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from .models import UploadRequest, UploadedForm
from .forms import EmailForm, PasswordForm, UploadForm

def generate_random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

def upload_request_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = generate_random_password()
            upload_request = UploadRequest.objects.create(email=email, password=password)

            # Send password to the user's email
            send_mail(
                'Your Upload Password',
                f'Your password is: {password}',
                'noreply@yourwebsite.com',
                [email],
                fail_silently=False,
            )
            return redirect('verify_password', pk=upload_request.id)
    else:
        form = EmailForm()
    return render(request, 'upload_request.html', {'form': form})

def verify_password_view(request, pk):
    upload_request = get_object_or_404(UploadRequest, pk=pk)
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == upload_request.password:
                upload_request.is_verified = True
                upload_request.save()
                return redirect('upload_form', pk=upload_request.id)
            else:
                form.add_error('password', 'Incorrect Password. Please check your Email and enter the correct Password.')
    else:
        form = PasswordForm()
    return render(request, 'verify_password.html', {'form': form})

def upload_form_view(request, pk):
    upload_request = get_object_or_404(UploadRequest, pk=pk, is_verified=True)
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form_file = form.cleaned_data['form_file']
            UploadedForm.objects.create(upload_request=upload_request, form_file=form_file)
            return redirect('thank_you')
    else:
        form = UploadForm()
    return render(request, 'upload_form.html', {'form': form})

def thank_you_view(request):
    return render(request, 'thank_you.html')