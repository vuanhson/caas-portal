from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import logout, login

import json, requests
import os

from .authentication import *

def mgr_roles(request):
	if check_auth(request) == False:
	    return render(request,'portal/login.html',{'login_status': "401: Session Expired or you are not logged in",})
	if check_admin(request) == False:
	    logout(request)
	    return render(request,'portal/login.html',{
	    'login_status': "403: You are not authorized to access this resources",
	    })
	system_role_list_url = 'http://'+ IP[0] + ':5000/v3/roles/'
	system_role_list_res = requests.get(system_role_list_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )

	if system_role_list_res.status_code == 200:
		context = {
		    'user_name' : request.session.get('user_name','Not logged in'),
		    'system_role_list': system_role_list_res.json(),
		    'domain_id' : request.session.get('domain_id','Not logged in'),
		}
		return render(request, 'portal/mgr_roles.html',context)
	return render(request, 'portal/mgr_roles.html')

def mgr_role_create(request):
	if request.POST.get('domain_specific_roles',False) == 'true':
		payload = {
    		"role": {
    			"domain_id": request.POST.get('domain_id',False),
    			"name": request.POST.get('role_name',False)
    		}
		}
	else:
		payload = {
    		"role": {
    			"name": request.POST.get('role_name',False)
    		}
		}
	role_add_url = 'http://'+ IP[0] + ':5000/v3/roles'
	role_add_exec = requests.post(role_add_url, data=json.dumps(payload), headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
	return HttpResponseRedirect(reverse('portal:mgr_roles'))

def mgr_role_action(request, action, role_id):
    if check_auth(request) == False:
        return render(request,'portal/login.html',{'login_status': "401: Session Expired or you are not logged in",})
    if check_admin(request) == False:
        logout(request)
        return render(request,'portal/login.html',{
        'login_status': "403: You are not authorized to access this resources",
        })

    if action == 'delete':
        action_url = 'http://'+ IP[0] + ':5000/v3/roles/' + role_id
        action_exec = requests.delete(action_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )

    return HttpResponseRedirect(reverse('portal:mgr_roles'))
