from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.http import HttpResponse
from django.views.decorators.http import require_GET


def send_email_with_template(to, name):
    htmly = get_template('emails/welcome_email.html')

    content = {'name': name}

    html_content = htmly.render(content)
    msg = EmailMultiAlternatives("Welcome to 'GuaranteeHR operation system'", html_content, "info@garantylearning.com", [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def index(request):

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

    return render(request, 'landing/index.html', {})


@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /box/",
        "Disallow: /cgi-bin/",
        "Host: https://guaranteehr.com"
        "Sitemap: https://guaranteehr.com/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
