from django.shortcuts import render, redirect
from django.contrib import messages
import models



def index(request):
    users = models.User.objects.all()
    context = {
        'users':users
    }
    try:
        if request.session['userID']:
            request.session.pop('userID')
    except KeyError:
        pass
    return render(request, 'belt/index.html', context)

def login(request):
    login = models.User.objects.login( request.POST )
    if not login[0]:
        errors = login[1]
        if 'no_entry' in errors:
            messages.error(request, 'Fill EVERYTHING out, you dunce.', extra_tags = 'login')
        if 'invalid_em' in errors:
            messages.error(request, 'Your email is broken, guy.', extra_tags = 'login')
        if 'short_pw' in errors:
            messages.error(request, 'Password is too short, dude.', extra_tags = 'login')
        if 'invalid_pw' in errors:
            messages.error(request, 'Weak password, brah.', extra_tags = 'login')
        if 'abs_em' in errors:
            messages.error(request, 'YOU DON\'T EXIST', extra_tags = 'login')
        if 'abs_pw' in errors:
            messages.error(request, 'Nice try, slick... wrong password!', extra_tags = 'login')
        return redirect('/')
    else:
        loggedUsr = models.User.objects.filter( email = request.POST['email'].lower() )
        request.session['userID'] = loggedUsr[0].id
        print request.session['userID']
        messages.success(request, "WOOHOO!... Now what...?")
        return redirect('/home')

def register(request):
    register = models.User.objects.register( request.POST )
    try:
        if not register[0]:
            errors = register[1]
            if 'no_entry' in errors:
                messages.error(request, 'Fill EVERYTHING out, you dunce.', extra_tags = 'register')
            if 'short_fn' in errors:
                messages.error(request, 'Don\'t be a hipster. You know your first name isn\t that short.', extra_tags = 'register')
            if 'short_ln' in errors:
                messages.error(request, 'Your last name isn\'t THAT short, dude...', extra_tags = 'register')
            if 'invalid_em' in errors:
                messages.error(request, 'Your email is broken, guy.', extra_tags = 'register')
            if 'short_pw' in errors:
                messages.error(request, 'Password is too short, dude.', extra_tags = 'register')
            if 'invalid_pw' in errors:
                messages.error(request, 'Weak password, brah.', extra_tags = 'register')
            if 'invalid_fn' in errors:
                messages.error(request, "Nuh-uh, for real? That's your name?! Letters only!", extra_tags = 'register')
            if 'invalid_ln' in errors:
                messages.error(request, "What kind of last name is that?! What\'re you a robot or something? Leters only!", extra_tags = 'register')
            if 'pwcnf_unmatch' in errors:
                messages.error(request, "You LITERALLY JUST TYPED your password. How could you get it wrong right after?!", extra_tags = 'register')
            if 'invalid_bd' in errors:
                messages.error(request, "Birthdate like this right here: YYYY-MM-DD", extra_tags = 'register')
            if 'future_baby' in errors:
                messages.error(request, "No future babies allowed, time traveler.", extra_tags = 'register')
            return redirect('/')
    except:
        loggedUsr = models.User.objects.filter( email = request.POST['email'].lower() )
        request.session['userID'] = loggedUsr[0].id
        messages.success(request, 'Yay, you wasted your time and signed up.')
        print request.session['userID']
        return redirect('/home')

def home(request):
    userInfo = models.User.objects.filter( id = request.session['userID'] )
    toys = models.Toy.objects.filter(user=userInfo)
    makers = models.Maker.objects.all()
    print toys
    context = {
        'user':userInfo[0],
        'toys':toys,
        'makers':makers
    }

    return render(request, 'belt/home.html', context)


def add_toy(request):
    toys = models.Toy.objects.all()
    context = {
        'toys': toys,
    }
    return render(request, 'belt/add_toy.html', context)

def add_toy_process(request):
    add_toy = models.User.objects.add_toy( request.POST, request.session['userID'] )
    if not add_toy[0]:
        errors = add_toy[1]
        if 'no_entry' in errors:
            messages.error(request, 'Fill EVERYTHING out, you dunce.', extra_tags = 'login')
            return redirect ('/add_toy')
    messages.success(request, 'You added '+'\"'+str(add_toy[1]).title()+'\"')
    return redirect('/add_toy')

def delete_toy(request, toy_id):
    models.Toy.objects.filter(id=toy_id).delete()
    return redirect('/home')

def remove_toy(request, toy_id):
    user = models.User.objects.filter( id = request.session['userID'] )
    userremove = user[0]
    models.Toy.objects.remove(userid, toy_id)
    return redirect('/home')




def logout(request):
    request.session.flush()
    return redirect('/')
