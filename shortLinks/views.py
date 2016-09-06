from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import HttpResponse, response
from django.shortcuts import render_to_response, redirect, get_object_or_404, render
from django.template import RequestContext
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from datetime import datetime

from shortLinks.models import Link
import hashlib


ALPHABET = '23456789bcdfghjkmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ'
BASE = len(ALPHABET)


def redirect_to_basic_url(request, short_url):
    link = get_object_or_404(Link, short=short_url)
    if str(short_url) in str(request.COOKIES.get('short_url')):
        return redirect(link.full)
    else:
        context = {'short_cookie': str(request.COOKIES.get('short_url'))}
        context['short_cookie'] += ' | ' + str(short_url)
        response = render(request, 'shortLinks/service.html', context)
        response.set_cookie('short_url', context['short_cookie'])
        link.count += 1
        link.save()
        return response


@login_required(login_url='/auth/login/')
def service(request):
    context_dict = {}
    context_dict.update(csrf(request))
    context_dict['user'] = auth.get_user(request)
    if request.POST:
        context_dict['url'] = request.POST.get('url', None)
        try:
            URLValidator(context_dict['url'])
            context_dict['short_url'] = str(datetime.now(tz=None)) + str(context_dict['user'])
            context_dict['short_url'] = (hashlib.md5(context_dict['short_url'].encode())).hexdigest()
            context_dict['short_url'] = int(context_dict['short_url'], 16)
            context_dict['short_url'] = encode(context_dict['short_url'])[:6]
            context_dict['username'] = str(context_dict['user'])
            if Link.objects.filter(short=context_dict['short_url']).count() > 0:
                context_dict['error'] = "Try again"
                return render_to_response('shortLinks/service.html', context_dict)
            else:
                link = Link(full=context_dict['url'],
                            short=context_dict['short_url'],
                            login_id=User.objects.get(username=context_dict['username']).id)

                link.save()
                context_dict['link'] = str(get_current_site(request)) + '/' + context_dict['short_url']
                return render_to_response('shortLinks/service.html', context_dict)
        except ValidationError:
            context_dict['error'] = "It's not URL"
            return render_to_response('shortLinks/service.html', context_dict)
    else:
        return render_to_response('shortLinks/service.html', context_dict)


def encode(number):
    string = ''
    while number > 0:
        string += ALPHABET[number % BASE]
        number //= BASE
    return string
