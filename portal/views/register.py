from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import logout, login

import json, requests
import os

from .authentication import *

def register(request):
    # print(request.POST.get('domainname', False))
    # print(request.POST.get('projectname', False))
    # print(request.POST.get('email', False))
    # print(request.POST.get('password', False))
    payload = {
    "auth": {
        	"identity": {
            	"methods": [
	                "password"
            	],
            	"password": {
                	"user": {
                    	"name": "register_user",
                    	"domain": {
                        	"name": "default",
                    	},
                    	"password": '123456789',
                	}
            	}
        	},
        	"scope": {
            	"project": {
                	"name": 'demo',
					"domain": {
						"name": 'default',
					},
            	}
        	}
    	}
	}
    url = 'http://' + IP[0] + ':5000/v3/auth/tokens'
    api_res = requests.post(url, data=json.dumps(payload))
    register_token = api_res.headers.get('X-Subject-Token')


    payload = {
        "user": {
            "default_project_id": "1452e8ed2a754cc483b2f90689c53d7a" , #project demo
            "domain_id": "default",
            "enabled": True,
            "name": request.POST.get('username', False),
            "password": request.POST.get('password', False),
            "description": "registered from portal",
            "email": request.POST.get('email',False)
        }
    }
    user_add_url = 'http://'+ IP[0] + ':5000/v3/users'
    user_add_exec = requests.post(user_add_url, data=json.dumps(payload), headers={"X-Auth-Token":register_token} )

    #get new user ID
    user_list_url = 'http://'+ IP[0] + ':5000/v3/users'
    user_list_res = requests.get(user_list_url, headers={"X-Auth-Token":register_token} )
    new_user_id = ''
    for user in user_list_res.json().get('users',{}):
        if user.get('name',{}) == request.POST.get('username',False):
            new_user_id = user.get('id',{})
    #assign role user to newuser on project demo
    assign_url = 'http://'+ IP[0] + ':5000/v3/projects/1452e8ed2a754cc483b2f90689c53d7a/users/' + new_user_id + '/roles/6b3c529ea1a34709a4f627587f79833e'
    assign_exec = requests.put(assign_url, headers={"X-Auth-Token":register_token} )
    if user_add_exec.status_code == 201:
        return render(request,'portal/register.html',{'register_status' : 'Register successful.'})

    return render(request,'portal/register.html')
