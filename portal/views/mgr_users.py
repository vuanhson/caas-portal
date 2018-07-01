from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import logout, login

import json, requests
import os

from .authentication import *
#these code handle the template mgr_user_details and mgr_user (.html)

def mgr_users(request):
    if check_auth(request) == False:
        return render(request,'portal/login.html',{'login_status': "401: Session Expired or you are not logged in",})
    if check_admin(request) == False:
        logout(request)
        return render(request,'portal/login.html',{
        'login_status': "403: You are not authorized to access this resources",
        })

    user_list_url = 'http://'+ IP[0] + ':5000/v3/users'
    user_list_res = requests.get(user_list_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
    system_role_list_url = 'http://'+ IP[0] + ':5000/v3/roles'
    system_role_list_res = requests.get(system_role_list_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
    system_project_list_url = 'http://'+ IP[0] + ':5000/v3/projects'
    system_project_list_res = requests.get(system_project_list_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )

    if user_list_res.status_code == 200:
        context = {
            'user_name' : request.session.get('user_name','Not logged in'),
            'data': user_list_res.json(),
            'system_role_list': system_role_list_res.json(),
            'system_project_list': system_project_list_res.json(),
            'domain_name' : request.session.get('domain_name','Not logged in'),
            'domain_id' : request.session.get('domain_id','Not logged in'),
        }
        return render(request, 'portal/mgr_users.html',context)
    return render(request, 'portal/mgr_users.html')


def mgr_user_create(request):
    if check_auth(request) == False:
        return render(request,'portal/login.html',{'login_status': "401: Session Expired or you are not logged in",})
    if check_admin(request) == False:
        logout(request)
        return render(request,'portal/login.html',{
        'login_status': "403: You are not authorized to access this resources",
        })

    enable = False
    if request.POST.get('enable', 'false') == 'true':
        enable = True
    else:
        enable = False
    payload = {
        "user": {
            "default_project_id": request.POST.get('primary_project',False),
            "domain_id": request.POST.get('domain_id',False),
            "enabled": enable,
            "name": request.POST.get('user_name',False),
            "password": request.POST.get('password', False),
            "description": request.POST.get('description', False),
            "email": request.POST.get('email',False)
        }
    }
    user_add_url = 'http://'+ IP[0] + ':5000/v3/users'
    user_add_exec = requests.post(user_add_url, data=json.dumps(payload), headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )

    #get new user ID
    user_list_url = 'http://'+ IP[0] + ':5000/v3/users'
    user_list_res = requests.get(user_list_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
    for user in user_list_res.json().get('users',{}):
        if user.get('name',{}) == request.POST.get('user_name',False):
            new_user_id = user.get('id',{})
    #get new user role ID
    system_role_list_url = 'http://'+ IP[0] + ':5000/v3/roles'
    system_role_list_res = requests.get(system_role_list_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
    for role in system_role_list_res.json().get('roles',{}):
        if role.get('name',{}) == request.POST.get('role',False):
            new_role_id = role.get('id',{})
    #assign role to user on project
    assign_url = 'http://'+ IP[0] + ':5000/v3/projects/' + request.POST.get('primary_project',False) + '/users/' + new_user_id + '/roles/' + new_role_id
    assign_exec = requests.put(assign_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
    return HttpResponseRedirect(reverse('portal:mgr_users'))

def mgr_user_action(request, action, user_id):
    if check_auth(request) == False:
        return render(request,'portal/login.html',{'login_status': "401: Session Expired or you are not logged in",})
    if check_admin(request) == False:
        logout(request)
        return render(request,'portal/login.html',{
        'login_status': "403: You are not authorized to access this resources",
        })


    if action =='viewdetails':
        user_detail_url = 'http://'+ IP[0] + ':5000/v3/users/' + user_id
        user_detail_res = requests.get(user_detail_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
        #List projects for user
        project_user_belong_to_url = 'http://'+ IP[0] + ':5000/v3/users/' + user_id + '/projects'
        project_user_belong_to_res = requests.get(project_user_belong_to_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )

        return render(request, 'portal/mgr_user_details.html', {
            'user_detail' : user_detail_res.json(),
            'project_user_belong_to' : project_user_belong_to_res.json(),
            })


    if action == 'delete':
        action_url = 'http://'+ IP[0] + ':5000/v3/users/' + user_id
        action_exec = requests.delete(action_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
    if action == 'disable' or action == 'enable':
        action_url = 'http://'+ IP[0] + ':5000/v3/users/' + user_id
        if action == 'disable':
            action_exec = requests.patch(
                action_url,
                data = json.dumps(
                    {
                        "user": {
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
                        "user": {
                            "enabled": True
                        }
                    }
                ),
                headers={
                    "X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in'),
                    "Content-Type" : "application/json",
                }
            )
    return HttpResponseRedirect(reverse('portal:mgr_users'))
