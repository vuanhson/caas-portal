from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import logout, login

import json, requests
import os

from .authentication import *

def flavors(request):
    if check_auth(request) == False:
        return render(request,'portal/login.html',{'login_status': "401: Session Expired or you are not logged in",})
    flavor_detail_url = 'http://'+ IP[0] + ':8774/v2.1/flavors/detail'
    flavor_detail_res = requests.get(flavor_detail_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
    if flavor_detail_res.status_code == 200:
        context = {
            'user_name' : request.session.get('user_name','Not logged in'),
            'data': flavor_detail_res.json()
        }
        return render(request, 'portal/flavors.html',context)
    return render(request, 'portal/flavors.html')

def flavor_action(request, action, flavor_id):
    if check_auth(request) == False:
        return render(request,'portal/login.html',{'login_status': "401: Session Expired or you are not logged in",})
    action_url = 'http://'+ IP[0] + ':8774/v2.1/flavors/'+ flavor_id
    action_exec = requests.delete(action_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )

    return HttpResponseRedirect(reverse('portal:flavors'))
