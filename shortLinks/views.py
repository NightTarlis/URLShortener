from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template.context_processors import csrf
from shortLinks.models import Links
from django.contrib import auth
import hashlib
import re

ALPHABET = '23456789bcdfghjkmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ'
BASE = len(ALPHABET)

def redirect_to_basicUrl(request, short_url):
    link = get_object_or_404(Links, pk=short_url)
    if Session.objects.exists():
        return redirect(link.links_http)
    else:
        link.links_count += 1
        link.save()
        return redirect(link.links_http)


def service(request):
    args = {}
    args.update(csrf(request))
    args['user'] = auth.get_user(request)
    if args['user'].is_anonymous:
        return redirect('/auth/login/')
    else:
        if request.POST:
            args['url'] = request.POST.get('url', None)
            if re.match(r'(https:\/\/(\w+\.)?\w+\.\w{2,3}|http:\/\/(\w+\.)?\w+\.\w{2,3})', args['url']):
                args['short_url'] = (hashlib.md5(args['url'].encode())).hexdigest()
                args['short_url'] = int(args['short_url'], 16)
                args['short_url'] = encode(args['short_url'])[:6]
                args['username'] = str(args['user'])
                link = Links(links_http=args['url'], links_short=args['short_url'], links_login=args['username'])
                link.save()
                args['link'] = str(get_current_site(request)) + '/' + args['short_url']
                return render_to_response('shortLinks/service.html', args)
            else:
                args['error'] = "It's not HTTP or HTTPS"
                return render_to_response('shortLinks/service.html', args)
        else:
            return render_to_response('shortLinks/service.html', args)

def encode(number):
    string = ''
    while number > 0:
        string += ALPHABET[number % BASE]
        number //= BASE
    return string
