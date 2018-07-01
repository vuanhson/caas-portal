from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import logout, login

import json, requests
import os

from .authentication import *

def mgr_hypervisors(request):
    if check_auth(request) == False:
        return render(request,'portal/login.html',{'login_status': "401: Session Expired or you are not logged in",})
    if check_admin(request) == False:
        logout(request)
        return render(request,'portal/login.html',{
        'login_status': "403: You are not authorized to access this resources",
        })

    hypervisor_detail_url = 'http://'+ IP[0] + ':8774/v2.1/os-hypervisors/detail'
    hypervisor_detail_res = requests.get(hypervisor_detail_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
    if hypervisor_detail_res.status_code == 200:
        context = {
    		'user_name' : request.session.get('user_name','Not logged in'),
    		'data': hypervisor_detail_res.json()
    	}
        return render(request, 'portal/mgr_hypervisors.html',context)

    return render(request, 'portal/mgr_hypervisors.html')
