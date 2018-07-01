from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

import json, requests

from .authentication import *

def home(request):
	if check_auth(request) == False:
		return render(request,'portal/login.html',{'login_status': "401: Session Expired or you are not logged in",})

	is_admin = False
	if check_admin(request) == True:
		is_admin = True
	compute_quotas_url = 'http://' + IP[0] + ':8774/v2.1/os-quota-sets/' + request.session.get('project_id','Not logged in') + '/detail'
	compute_quotas_res = requests.get(compute_quotas_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )

	volume_quotas_url = 'http://' + IP[0] + ':8776/v3/' + request.session.get('project_id','Not logged in') + '/os-quota-sets/' + request.session.get('project_id','Not logged in') + '?usage=True'
	volume_quotas_res = requests.get(volume_quotas_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )

	network_quotas_url = 'http://' + IP[0] + ':9696/v2.0/quotas/' + request.session.get('project_id','Not logged in') + '/details.json'
	network_quotas_res = requests.get(network_quotas_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )


	return render(request, 'portal/home.html',{
		'user_name' : request.session.get('user_name','Not logged in'),
		'user_id' : request.session.get('user_id','Not logged in'),
		'domain_name' : request.session.get('domain_name','Not logged in'),
		'domain_id' : request.session.get('domain_id','Not logged in'),
		'X_Auth_Token' : request.session.get('X_Auth_Token', 'Not logged in'),
		'roles': request.session.get('roles', 'Not logged in'),
		'project_name' : request.session.get('project_name','Not logged in'),
		'project_id' : request.session.get('project_id','Not logged in'),
		'token_issued' : request.session.get('token_issued','Not logged in'),
		'token_expires' : request.session.get('token_expires','Not logged in'),
		'compute_quotas' : compute_quotas_res.json(),
		'volume_quotas' : volume_quotas_res.json(),
		'network_quotas' : network_quotas_res.json(),
		'is_admin' : is_admin,
		})
