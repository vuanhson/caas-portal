from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import logout, login

import json, requests
import os
#----------------------------------------------------------------------------------------------------------------
# READ IP
module_dir = os.path.dirname(__file__)
with open(os.path.join(module_dir, 'apis_call_ip.txt')) as f:
	IP = f.read().split('\n')
#----------------------------------------------------------------------------------------------------------------
def login_system(request):
	response = render(request, 'portal/login.html')
	payload = {
    "auth": {
        	"identity": {
            	"methods": [
	                "password"
            	],
            	"password": {
                	"user": {
                    	"name": request.POST.get('username',False),
                    	"domain": {
                        	"name": request.POST.get('domainname',False),
                    	},
                    	"password": request.POST.get('password',False),
                	}
            	}
        	},
        	"scope": {
            	"project": {
                	"name": request.POST.get('projectname',False),
					"domain": {
						"name": request.POST.get('domainname',False),
					},
            	}
        	}
    	}
	}
	url = 'http://' + IP[0] + ':5000/v3/auth/tokens'
	api_res = requests.post(url, data=json.dumps(payload))

	if api_res.status_code == 401:
		return render(request,'portal/login.html',{'login_status': "401: Unauthorized - Credentials are not correct",})
	if api_res.status_code == 201:
		
		response = HttpResponseRedirect(reverse('portal:home'))
		request.session['user_name'] = api_res.json().get('token',{}).get('user',{}).get('name',{})
		request.session['user_id'] = api_res.json().get('token',{}).get('user',{}).get('id',{})
		request.session['domain_name'] = api_res.json().get('token',{}).get('user',{}).get('domain',{}).get('name',{})
		request.session['domain_id'] = api_res.json().get('token',{}).get('user',{}).get('domain',{}).get('id',{})
		request.session['X_Auth_Token'] = api_res.headers.get('X-Subject-Token')
		request.session['project_name'] = api_res.json().get('token',{}).get('project',{}).get('name',{})
		request.session['project_id'] = api_res.json().get('token',{}).get('project',{}).get('id',{})
		request.session['token_issued'] = api_res.json().get('token',{}).get('issued_at',{})
		request.session['token_expires'] = api_res.json().get('token',{}).get('expires_at',{})
		request.session['roles'] = api_res.json().get('token',{}).get('roles',{})
		#request.session['ip'] = IP check admin trong home template se goi va lay ip[1] <- username cua admin he thong
		return response

	return response

def logout_system(request):
	logout(request)
	return render(request, 'portal/landing.html')

def check_auth(request):
	url = 'http://' + IP[0] + ':8774/v2.1/servers'
	api_res = requests.get(url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
	if api_res.status_code == 200:
		return True
	else:
		return False

def check_admin(request):
	# neu ton tai role la admin thi se vao dc trang admin
	roles = request.session.get('roles','Not logged in')
	for role in roles:
		for key, value in role.items():
			if key == 'name' and value =='admin':
				return True
	else:
		return False
