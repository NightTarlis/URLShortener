from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.template.context_processors import csrf


def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        args['username'] = request.POST.get('username', None)
        args['password'] = request.POST.get('password', None)
        user = auth.authenticate(username=args['username'], password=args['password'])
        if user is not None:
            auth.login(request, user=user)
            return redirect('/')
        else:
            args['login_error'] = "User doesn't exist"
            return render_to_response('login/authorization.html', args)
    else:
        return render_to_response('login/authorization.html', args)


def logout(request):
    auth.logout(request)
    return redirect('/auth/login/')
