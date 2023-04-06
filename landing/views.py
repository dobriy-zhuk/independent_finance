from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.forms.models import inlineformset_factory
from django.views.decorators.http import require_POST
from .tasks import send_email_message
from django.contrib.auth.models import User, Group
from backoffice.models import Staff, Subscription, Manager, Course, Company
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.conf import settings as conf_settings
import requests
import json


def send_email_with_template(to, name):
    htmly = get_template('emails/welcome_email.html')

    content = {'name': name}

    html_content = htmly.render(content)
    msg = EmailMultiAlternatives("Welcome to 'GuaranteeHR operation system'", html_content, "info@guaranteehr.com", [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def index(request):

    response_data = {}
    if request.POST.get('action') == 'post':
        email = request.POST.get('email')
        body = "Lead from Guarantee HR\nEmail: " + email + "\n"

        if email:
            try:
                send_mail("New Lead from Guarantee Finance", body, 'info@guaranteehr.com', ['info@guaranteehr.com'])

                send_email_with_template(email, name="")

            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            response_data['result'] = "Thank you for getting in touch! " \
                                      "One of our colleagues will get back in touch with you soon! " \
                                      "Have a great day!"
        else:
            # In reality we'd use a form class
            # to get proper validation errors.
            response_data['result'] = "Check your form, please"

        return JsonResponse(response_data)

    return render(request, 'landing/index.html', {})


def price(request):

    return render(request, 'landing/price.html', {})


def teacher_hire(request):

    response_data = {}
    if request.POST.get('action') == 'post':
        email = request.POST.get('email')
        body = "Lead from Guarantee HR\nEmail: " + email + "\n"

        if email:
            try:
                send_mail("New Lead from Guarantee HR", body, 'info@garantylearning.com', ['info@garantylearning.com'])

                send_email_with_template(email, name="")

            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            response_data['result'] = "Thank you for getting in touch! " \
                                      "One of our colleagues will get back in touch with you soon! " \
                                      "Have a great day!"
        else:
            # In reality we'd use a form class
            # to get proper validation errors.
            response_data['result'] = "Check your form, please"

        return JsonResponse(response_data)

    return render(request, 'landing/teacher_staff.html', {})

def teacher_join(request):

    response_data = {}
    if request.POST.get('action') == 'post':
        email = request.POST.get('email')
        body = "Lead from Guarantee HR\nEmail: " + email + "\n"

        if email:
            try:
                send_mail("New Lead from Guarantee HR", body, 'info@guaranteehr.com', ['info@guaranteehr.com'])

                send_email_with_template(email, name="")

            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            response_data['result'] = "Thank you for getting in touch! " \
                                      "One of our colleagues will get back in touch with you soon! " \
                                      "Have a great day!"
        else:
            # In reality we'd use a form class
            # to get proper validation errors.
            response_data['result'] = "Check your form, please"

        return JsonResponse(response_data)

    return render(request, 'landing/teacher_join.html', {})

def test_form(request):
    return render(request, 'landing/test_form.html', {})


def contacts(request):
    return render(request, 'landing/contacts.html', {})

@require_POST
def full_contact(request):

    response_data = {}
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    city = request.POST.get('city')
    comment = request.POST.get('comment')

    body = "Новая заявка от клиента\nИмя: " + str(name) + "\nEmail: " + str(email) + "\nТелефон: " + str(phone) + \
           " \nКомментарий: " + str(comment)

    from django.core.mail import send_mail
    a = send_mail('Subject here', 'Here is the message.', 'info@guaranteehr.com', ['kvasovao@yandex.ru'],
                  fail_silently=False)

    try:
        #send_mail("Заявка с вашего сайта от клиента", body, 'info@garantylearning.com', ['kvsaovao@yandex.ru'])

        if email:

            a = send_mail('Subject here', 'Here is the message.', 'info@guaranteehr.com', ['kvasovao@yandex.ru'],
                          fail_silently=False)
            print(a)


            user, created = User.objects.get_or_create(username=email,
                                                       email=email)
            user.first_name = "Guest"
            if created:
                user.is_active = False
                user.save()
                user.refresh_from_db()

                #send approve email to new user
                associated_users = User.objects.filter(Q(email=email))
                if associated_users.exists():
                    for user in associated_users:
                        email_content = {
                            'domain': '127.0.0.1:8000',
                            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                        }
                        send_email_message.delay('emails/welcome_email.html',
                                                 [email],
                                                 "Welcome to GuaranteeHR",
                                                 email_content
                                                 )
                        messages.success(request, 'We sent you email. Approve it and create password!')




            response_data['result'] = "Ваша заявка отправлена. Мы свяжемся с вами в ближайшее время! " \
                                      "А пока можете зайти в свой <a href='https://guaranteehr.com/box/accounts/login/'>" \
                                      "личный кабинет</a> (логин и пароль отправлены на вашу почту)"

        if name and phone and email:

            user, created = User.objects.get_or_create(username=email,
                                                       email=email)
            user.first_name = name
            if created:
                user.set_password("787876")
                user.save()
                user.refresh_from_db()

            manager, created = Manager.objects.get_or_create(user=user)
            if created:
                manager.phone = phone
            manager.save()

            send_email_message.delay('emails/new_client_email.html',
                                     [email],
                                     "Welcome to GuaranteeHR",
                                     email_content
                                     )
            response_data['result'] = "Ваша заявка отправлена. Мы свяжемся с вами в ближайшее время! " \
                                      "А пока можете зайти в свой <a href='https://guaranteehr.com/box/accounts/login/'>" \
                                      "личный кабинет</a> (логин и пароль отправлены на вашу почту)"

    except BadHeaderError:
        return HttpResponse('Invalid header found.')

    return JsonResponse(response_data)


def payment(request):
    return render(request, 'landing/payment.html', {})


#Webhook after payment using Paddle acquiring
def payment_paddle(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')
        subject = request.POST.get('subject')
        email = request.POST.get('receipt_email')
        comment = request.POST.get('comment')

        url = "https://vendors.paddle.com/api/2.0/product/generate_pay_link"
        payload = "vendor_id=147950&vendor_auth_code=6aca414866fcec1dcab7d357e5663cd982135e63c21096b8f9&product_id={}&".format(
            subject)

        if amount != '':
            payload = {
                'vendor_id': conf_settings.PADDLE_VENDOR_ID,
                'vendor_auth_code': conf_settings.PADDLE_AUTH_CODE,
                'title': "Lessons",
                'webhook_url': 'https://guaranteelearning.com/en/payment/',
                'prices[0]': "USD:{}".format(amount)
            }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.request("POST", url, data=payload, headers=headers)
        result = json.loads(response.text)

        return JsonResponse({'formUrl': result["response"]["url"]})



@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /box/",
        "Disallow: /cgi-bin/",
        "Host: https://guaranteehr.com",
        "Sitemap: https://guaranteehr.com/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
