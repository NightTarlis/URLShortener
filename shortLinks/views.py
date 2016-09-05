from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from datetime import datetime

from shortLinks.models import Link
import hashlib


ALPHABET = '23456789bcdfghjkmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ'
BASE = len(ALPHABET)


def redirect_to_basicUrl(request, short_url):
    link = get_object_or_404(Link, short=short_url)
    if request.COOKIES:
        return redirect(link.full)
    else:
        link.count += 1
        link.save()
        return redirect(link.full)


@login_required(login_url='/auth/login/')
def service(request):
    context = {}
    context.update(csrf(request))
    context['user'] = auth.get_user(request)
    if request.POST:
        context['url'] = request.POST.get('url', None)
        validate = URLValidator()
        try:
            validate(context['url'])
            context['short_url'] = str(datetime.now(tz=None)) + str(context['user'])
            context['short_url'] = (hashlib.md5(context['short_url'].encode())).hexdigest()
            context['short_url'] = int(context['short_url'], 16)
            context['short_url'] = encode(context['short_url'])[:6]
            context['username'] = str(context['user'])
            if Link.objects.filter(short=context['short_url']).count() > 0:
                context['error'] = "Try again"
                return render_to_response('shortLinks/service.html', context)
            else:
                link = Link(full=context['url'], short=context['short_url'], login=context['username'])
                link.save()
                context['link'] = str(get_current_site(request)) + '/' + context['short_url']
                return render_to_response('shortLinks/service.html', context)
        except ValidationError:
            context['error'] = "It's not URL"
            return render_to_response('shortLinks/service.html', context)
    else:
        return render_to_response('shortLinks/service.html', context)


def encode(number):
    string = ''
    while number > 0:
        string += ALPHABET[number % BASE]
        number //= BASE
    return string
