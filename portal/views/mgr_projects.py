from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import logout, login

import json, requests
import os

from .authentication import *

def mgr_projects(request):
	if check_auth(request) == False:
	    return render(request,'portal/login.html',{'login_status': "401: Session Expired or you are not logged in",})
	if check_admin(request) == False:
	    logout(request)
	    return render(request,'portal/login.html',{
	    'login_status': "403: You are not authorized to access this resources",
	    })
	system_project_list_url = 'http://'+ IP[0] + ':5000/v3/projects'
	system_project_list_res = requests.get(system_project_list_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
	system_domain_list_url = 'http://'+ IP[0] + ':5000/v3/domains'
	system_domain_list_res = requests.get(system_domain_list_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
	if system_project_list_res.status_code == 200:
		context = {
		    'user_name' : request.session.get('user_name','Not logged in'),
		    'system_project_list': system_project_list_res.json(),
		    'system_domain_list': system_domain_list_res.json(),
		    'domain_id' : request.session.get('domain_id','Not logged in'),
		}
		return render(request, 'portal/mgr_projects.html',context)
	return render(request, 'portal/mgr_projects.html')

def mgr_project_create(request):
    enable = False
    if request.POST.get('enable', 'false') == 'true': 
        enable = True
    else:
        enable = False

    is_domain = False
    if request.POST.get('is_domain', 'false') == 'true': 
        is_domain = True
    else:
        is_domain = False
    payload = {
    	"project": {
    	        "description": request.POST.get('description', False),
    	        "domain_id": request.POST.get('domain_id',False),
    	        "enabled": enable,
    	        "is_domain": is_domain,
    	        "name": request.POST.get('project_name',False)
    	    }
    }
    project_add_url = 'http://'+ IP[0] + ':5000/v3/projects'
    project_add_exec = requests.post(project_add_url, data=json.dumps(payload), headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
    return HttpResponseRedirect(reverse('portal:mgr_projects'))

def mgr_project_action(request, action, project_id):
    if check_auth(request) == False:
        return render(request,'portal/login.html',{'login_status': "401: Session Expired or you are not logged in",})
    if check_admin(request) == False:
        logout(request)
        return render(request,'portal/login.html',{
        'login_status': "403: You are not authorized to access this resources",
        })

    if action == 'delete':
        action_url = 'http://'+ IP[0] + ':5000/v3/projects/' + project_id
        action_exec = requests.delete(action_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
    if action == 'disable' or action == 'enable':
        action_url = 'http://'+ IP[0] + ':5000/v3/projects/' + project_id
        if action == 'disable':
            action_exec = requests.patch(
                action_url, 
                data = json.dumps(
                    {
                        "project": {
                            "enabled": False
                        }
                    }
                ), 
                headers={
                    "X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in'),
                    "Content-Type" : "application/json",
                } 
            )
        if action == 'enable':
            action_exec = requests.patch(
                action_url, 
                data = json.dumps(
                    {
                        "project": {
                            "enabled": True
                        }
                    }
                ), 
                headers={
                    "X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in'),
                    "Content-Type" : "application/json",
                } 
            )
    return HttpResponseRedirect(reverse('portal:mgr_projects'))
