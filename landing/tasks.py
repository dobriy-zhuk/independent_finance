from celery import Celery
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.template import Template, Context
from django.template.loader import get_template
from smtplib import SMTPException


app = Celery('hr_system', broker='redis://localhost:6379')

@app.task
def send_email_message(template, to, title, email_content):

    try:
        if template == 'emails/new_client_email_en.html':
            company = "GuaranteeHR <info@guaranteehr.com>"
        else:
            company = "GuaranteeHR<info@guaranteehr.com>"

        htmly = get_template(template)

        html_content = htmly.render(email_content)
        msg = EmailMultiAlternatives(title, html_content,
                                     company, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except BadHeaderError:  # If mail's Subject is not properly formatted.
        print('Invalid header found.')
    except SMTPException as e:  # It will catch other errors related to SMTP.
        print('There was an error sending an email.' + str(e))
    except:  # It will catch All other possible errors.
        print("Mail Sending Failed!")

