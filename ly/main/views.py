from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from main.forms import SignUpForm


# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_email_confirmed = False
            user.save()


            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode('utf-8')).decode('utf-8')


            current_site = get_current_site(request)
            mail_subject = 'подтвердите вашу почту'
            message = render_to_string('main/confirmation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            send_mail(mail_subject, message, 'something@example.com', [user.email])

            return redirect('main:email_confirmation_sent')
    else:
        form = SignUpForm()

    return render(request, 'main/signup.html', {'form': form})



def confirm_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_email_confirmed = True
        user.save()
        return redirect('main:login')

    else:
        raise Http404("Invalid confirmation link")


def email_confirmed_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_email_confirmed:
            return redirect('main:signup')
        return view_func(request, *args, **kwargs)

    return _wrapped_view
