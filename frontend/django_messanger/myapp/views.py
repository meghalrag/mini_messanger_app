import json
from django.shortcuts import render,HttpResponse,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection,IntegrityError
from django.contrib import messages
from .forms import RegForm,LoginForm
from .api_service import sigup_api, login_api, user_profile_api, add_post_api, get_post_api, delete_post_api
# from util.db import to_dict
# Create your views here.
def home(request):
    return render(request,'reg.html')


def login(request):
    if request.method=='POST':
        forms=LoginForm(request.POST)
        if forms.is_valid():
            email=forms.cleaned_data['email']
            passw=forms.cleaned_data['password']
            res = login_api({
                    "email": email,
                    "password": passw
                })
            if "error" in res:
                messages.add_message(
                    request,
                    messages.ERROR,
                    res["error"]
                )
                return redirect('user:login')
            else:
                access_token = res["access_token"]
                request.session['access_token'] = access_token
                return redirect('user:userhome')
    else:
        forms=LoginForm() 
        return render(request,'create.html',{'f':'login','form':forms})


def userhome(request):
    try:
        token = request.session['access_token']
    except KeyError:
        return redirect("user:login")
    res_user = user_profile_api(token)
    if "status_code" in res_user and res_user["status_code"] == 403:
        return redirect("user:logout")
    elif "error" in res_user:
        messages.add_message(
            request,
            messages.ERROR,
            res_user["error"]
        )
        redirect("user:login")
    else:
        res_post = get_post_api(token)
        if "status_code" in res_post and res_post["status_code"] == 403:
            messages.add_message(
                request,
                messages.ERROR,
                res_post["error"]
            )
            return redirect("user:logout")
        elif "error" in res_post:
            messages.add_message(
                request,
                messages.ERROR,
                res_post["error"]
            )
            redirect("user:userhome")
        else:
            posts = sorted(res_post["data"], key=lambda k: k['id'], reverse=True) 
            return render(request,'home.html',{'user':res_user, "post":posts})


def signup(request):
    if request.method=="POST":
        forms=RegForm(request.POST)
        if forms.is_valid():
            email=forms.cleaned_data['email']
            passw=forms.cleaned_data['passwordreg']
            cpassw=forms.cleaned_data['cpasswordreg']
            if passw != cpassw:
                messages.add_message(
                request,
                messages.ERROR,
                'password not match'
                )
                return redirect('user:signup')
            else:
                res = sigup_api({
                        "email": email,
                        "password": passw
                    })
                if "error" in res:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        res["error"]
                    )
                    return redirect('user:signup')
                else:
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        'user registered successfully'
                    )
                    return redirect('user:login')
        else:
             for error_field in forms.errors:
                if error_field in forms.fields:
                    forms.fields[error_field].widget.attrs['class'] += ' is-invalid'
            # return HttpResponse(forms.errors)
    else:
        forms=RegForm()
    return render(request,'create.html',{'form':forms})


def addpost(request):
    try:
        token = request.session["access_token"]
        if request.method=="POST":
            title = request.POST.get("title")
            content = request.POST.get("content")
            params = {
                "title": title,
                "content": content
            }
            res = add_post_api(token, params)
            if "status_code" in res and res["status_code"] == 403:
                messages.add_message(
                    request,
                    messages.ERROR,
                    res["error"]
                )
                return redirect("user:logout")
            elif "error" in res:
                messages.add_message(
                    request,
                    messages.ERROR,
                    res["error"]
                )
                redirect("user:userhome")
            else:
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    res["data"]
                )
                return redirect("user:userhome")
            
    except Exception as err:
        messages.add_message(
            request,
            messages.ERROR,
            str(err)
        )
        return redirect("user:userhome")
    

def deletepost(request):
    try:
        token = request.session["access_token"]
        if request.method=="POST":
            post_id = request.POST.get("post_id")
            res = delete_post_api(token, post_id)
            if "status_code" in res and res["status_code"] == 403:
                messages.add_message(
                    request,
                    messages.ERROR,
                    res["error"]
                )
                return redirect("user:logout")
            elif "error" in res:
                messages.add_message(
                    request,
                    messages.ERROR,
                    res["error"]
                )
                redirect("user:userhome")
            else:
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    res["data"]
                )
                return redirect("user:userhome")
            
    except Exception as err:
        messages.add_message(
            request,
            messages.ERROR,
            str(err)
        )
        return redirect("user:userhome")
    
def ajax_get_post(request):
    token = request.session["access_token"]
    res_post = get_post_api(token)
    if "status_code" in res_post and res_post["status_code"] == 403:
        messages.add_message(
            request,
            messages.ERROR,
            res_post["error"]
        )
        return redirect("user:logout")
    elif "error" in res_post:
        messages.add_message(
            request,
            messages.ERROR,
            res_post["error"]
        )
        redirect("user:userhome")
    else:
        posts = sorted(res_post["data"], key=lambda k: k['id'], reverse=True) 
        obj=json.dumps(posts)
        return HttpResponse(obj)


def logout(request):
    del request.session['access_token']
    return redirect('user:login')
