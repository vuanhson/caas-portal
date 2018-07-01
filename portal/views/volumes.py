from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

import json, requests
import os

from .authentication import *

def volumes(request):
    if check_auth(request) == False:
        return render(request,'portal/login.html',{'login_status': "401: Session Expired or you are not logged in",})
    volume_detail_url = 'http://'+ IP[0] + ':8776/v3/' + request.session.get('project_id','Not logged in') + '/volumes/detail'
    volume_detail_res = requests.get(volume_detail_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
    compute_detail_url = 'http://' + IP[0] + ':8774/v2.1/servers/detail'
    compute_detail_res = requests.get(compute_detail_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )

    if volume_detail_res.status_code == 200:
        context = {
            'user_name' : request.session.get('user_name','Not logged in'),
            'data': volume_detail_res.json(),
            'compute_detail' : compute_detail_res.json()
        }
        return render(request, 'portal/volumes.html',context)
    return render(request, 'portal/volumes.html')

def volume_action(request, action, volume_id):
    if check_auth(request) == False:
        return render(request,'portal/login.html',{'login_status': "401: Session Expired or you are not logged in",})
    #only delete so not need if
    action_url = 'http://'+ IP[0] + ':8776/v3/' + request.session.get('project_id','Not logged in') + '/volumes/' + volume_id
    action_exec = requests.delete(action_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
    return HttpResponseRedirect(reverse('portal:volumes'))
