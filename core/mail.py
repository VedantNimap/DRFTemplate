from drf_template import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

def send_mail_func(to, subject, template, **kwargs):
    """
    Sends an email with the specified subject, template, and context.
    
    Args:
        to (list): List of recipient email addresses.
        subject (str): Subject of the email.
        template (str): Path to the HTML template to use.
        **kwargs: Context variables to populate the template.
    """
    # Render the HTML content with the provided context
    html_content = render_to_string(template, kwargs)

    # Create the email message with both plain text and HTML parts
    email = EmailMultiAlternatives(
        subject=subject,
        from_email=settings.EMAIL_HOST_USER,
        to=to,
    )
    
    # Attach the HTML content as an alternative
    email.attach_alternative(html_content, "text/html")
    
    # Send the email
    email.send(fail_silently=False)

