from celery import Celery
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.template import Template, Context
from smtplib import SMTPException

app = Celery('hr_system', broker='redis://localhost:6379')

@app.task
def send_email_with_delay(title, to, body):
    try:
        htmly = Template(body)

        content = {'name': "Artem",
                   'position': "position",
                   'time': "time"}

        html_content = htmly.render(Context(content))
        msg = EmailMultiAlternatives(title, html_content,
                                     "GuaranteeHR <info@garantylearning.com>", to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except BadHeaderError:  # If mail's Subject is not properly formatted.
        print('Invalid header found.')
    except SMTPException as e:  # It will catch other errors related to SMTP.
        print('There was an error sending an email.' + str(e))
    except:  # It will catch All other possible errors.
        print("Mail Sending Failed!")

