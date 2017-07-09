from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate

#from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from .forms import RegisterForm

site_name = 'Rokego'

def logout_view(request):
	"""Log the user out."""
	logout(request)
	return HttpResponseRedirect(reverse('distances:index'))

def register(request):
	"""Register a new user."""
	if request.method != 'POST':
		"""Display blank registration form."""
		form = RegisterForm()
	else:
		"""Process completed form."""
		form = RegisterForm(data=request.POST)
		
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			user.save()
			current_site = get_current_site(request)
			subject = 'Activate your {0} account.'.format(site_name)
			message = render_to_string('acc_active_email.html', {
                'user':user, 'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # user.email_user(subject, message)
			toemail = form.cleaned_data.get('email')
			email = EmailMessage(subject, message, to=[toemail])
			email.send()
			return HttpResponse('Please confirm your email address to complete the registration')
			# Log the user in and then redirect to home page.
			#authenticated_user = authenticate(username=new_user.username,
			#    password=request.POST['password1'])
			#login(request, authenticated_user)
			#return HttpResponseRedirect(reverse('distances:index'))
		
	context = {'form': form}
	return render(request, 'users/register.html', context)

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

#def password_reset_form(request):
	#form = 
	#return render(request, 'registration/password_reset_form.html', {'form': ))
	#return HttpResponseRedirect(reverse('registration:password_reset'))
#def password_reset(request):
#	return HttpResponseRedirect(reverse('users:password_reset_form'))
