from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import logout, login

import json, requests
import os

from .authentication import *

def images(request):
    if check_auth(request) == False:
        return render(request,'portal/login.html',{'login_status': "401: Session Expired or you are not logged in",})
    image_detail_url = 'http://'+ IP[0] + ':9292/v2/images'
    image_detail_res = requests.get(image_detail_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )

    #Pass Project owner to context
    project_detail_url = 'http://' + IP[0] + ':5000/v3/projects'
    project_detail_res = requests.get(project_detail_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')})

    if image_detail_res.status_code == 200 and project_detail_res.status_code == 200:
        context = {
            'user_name' : request.session.get('user_name','Not logged in'),
            'data': image_detail_res.json(),
            'project_detail': project_detail_res.json()
        }
        return render(request, 'portal/images.html',context)
    elif image_detail_res.status_code == 200 and project_detail_res.status_code == 403:
        context = {
            'user_name' : request.session.get('user_name','Not logged in'),
            'data': image_detail_res.json(),
            'project_detail': '403'
        }
        return render(request, 'portal/images.html',context)

    return render(request, 'portal/images.html')

def image_action(request, action, image_id):
    if check_auth(request) == False:
        return render(request,'portal/login.html',{'login_status': "401: Session Expired or you are not logged in",})
    action_url = 'http://'+ IP[0] + ':9292/v2/images/' + image_id
    action_exec = requests.delete(action_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )

    return HttpResponseRedirect(reverse('portal:images'))
